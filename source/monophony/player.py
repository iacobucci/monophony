import copy
import random
import time

from monophony import DISPLAY_NAME, ID, downloads, logging, recents, settings, yt
from monophony.asynchronous import Task
from monophony.data import Group, PlaybackMode, PlaybackState, Song
from monophony.mpris import EventHandler, EventSender, Server

from gi.repository import GObject, Gst


class ReportProgressTask(Task):
	def _function(self):
		logging.info(__name__, 'Progress reporting started')
		while not self.is_canceled():
			self._update_progress()
			time.sleep(1)

		logging.info(__name__, 'Progress reporting stopped')


class FindRadioSongsTask(Task):
	def _function(self, from_song: Song, ignore_songs: Group) -> Group | None:
		return yt.get_similar_songs(from_song, ignore_songs)


class FindURITask(Task):
	def _function(self, song: Song, known_uris: dict) -> str | None:
		logging.info(
			__name__, f'Looking for "{song.yt_id}" song URI locally and online...'
		)
		if uri := known_uris.get(song.yt_id):
			logging.info(__name__, 'Found already known song URI')
			return uri

		if downloads.is_downloaded(song):
			song_path = downloads.get_file(song)
			if song_path:
				logging.info(__name__, 'Found local song URI')
				return 'file://' + song_path

		if self.is_canceled():
			logging.info(__name__, 'Canceled URI lookup')
			return None

		if uri := yt.get_song_uri(song):
			logging.info(__name__, 'Found online song URI')
			return uri

		logging.error(__name__, 'Failed to find song URI')
		return None


class Player(GObject.Object):
	def __init__(self):
		super().__init__()

		Gst.init([])

		self._find_uri_task = Task()
		self._progress_task = Task()
		self._radio_task = Task()
		self._last_known_position = 0
		self._start_position = 0
		self._song_uris = {}
		self._queue = Group()
		self._queue_index = 0
		self.mode = PlaybackMode.NORMAL
		self.state = PlaybackState.NONE
		self.paused = False
		self.buffering = False

		pulse_sink = Gst.ElementFactory.make('pulsesink', None)
		pulse_sink.props.client_name = DISPLAY_NAME
		pulse_sink.props.stream_properties = Gst.Structure.new_from_string(
			'props,'
			f'application.name={DISPLAY_NAME},'
			f'application.id={ID},'
			f'application.icon_name={ID},'
			'media.role=music,'
		)

		self._playbin = Gst.ElementFactory.make('playbin3', None)
		self._playbin.props.audio_sink = pulse_sink
		self._playbin.props.video_sink = Gst.ElementFactory.make('fakevideosink', None)
		self._playbin.set_state(Gst.State.READY)
		self._playbin.get_bus().add_signal_watch()
		self._playbin.get_bus().connect('message::error', self._on_bus_error)
		self._playbin.get_bus().connect('message::latency', self._on_latency)
		self._playbin.get_bus().connect('message::state-changed', self._on_state_change)
		self._playbin.get_bus().connect('message::stream-start', self._on_stream_start)
		self._playbin.get_bus().connect('message::buffering', self._on_buffering)
		self._playbin.get_bus().connect('message::eos', self._on_stream_end)

		# Last part of ID and not DISPLAY_NAME as that can differ
		self._mpris_server = Server(ID.split('.')[-1], EventHandler(self))
		self._mpris_event_sender = EventSender(self._mpris_server)
		self._mpris_server.publish()

		self.set_mode(int(settings.load('mode', PlaybackMode.NORMAL)))
		self.set_volume(float(settings.load('volume', 1.0)))

	@GObject.Signal(name='queue-changed')
	def _queue_changed(self, _queue: object, _index: int):
		return

	@GObject.Signal(name='recents-changed')
	def _recents_changed(self):
		return

	@GObject.Signal(name='progress-changed')
	def _progress_changed(self, _progress: float):
		return

	@GObject.Signal(name='buffering-changed')
	def _buffering_changed(self, _progress: float):
		return

	@GObject.Signal(name='state-changed')
	def _state_changed(self, _state: int):
		return

	@GObject.Signal(name='volume-changed')
	def _volume_changed(self, _volume: float):
		return

	@GObject.Signal(name='mode-changed')
	def _mode_changed(self, _mode: int):
		return

	@GObject.Signal(name='pause-changed')
	def _pause_changed(self, _pause: bool):
		return

	@GObject.Signal(name='raise')
	def _raise(self):
		return

	def _on_background_uri_search_done(self, task: FindURITask):
		if task.result:
			self._save_uri(task.extra_data.yt_id, task.result)

		if self._find_uri_task.is_running():
			return

		for song in self._queue.songs:
			if song.yt_id not in self._song_uris:
				self._find_uri_task = FindURITask(
					callback=self._on_background_uri_search_done,
					args=(song, self._song_uris)
				)
				self._find_uri_task.extra_data = song
				self._find_uri_task.start()
				return

		logging.info(__name__, 'Found all song URIs for current queue')

	def _on_buffering(self, _bus: Gst.Bus, message: Gst.Message):
		percentage = message.parse_buffering()
		self.emit('buffering-changed', percentage / 100.0)
		if percentage < 100: # noqa: PLR2004 - 100%
			if not self.buffering:
				logging.info(__name__, 'Buffering...')
				self._playbin.set_state(Gst.State.PAUSED)
				self.buffering = True

			return

		logging.info(__name__, 'Done buffering')
		self.buffering = False
		if self.state != PlaybackState.NONE:
			self._playbin.set_state(Gst.State.PLAYING)
			self.state = PlaybackState.PLAYING
			self.emit('state-changed', self.state)
			if self._start_position > 0:
				logging.info(__name__, f'Seeking to {self._start_position}ns')
				self._playbin.seek_simple(
					Gst.Format.TIME,
					Gst.SeekFlags.FLUSH | Gst.SeekFlags.ACCURATE,
					self._start_position
				)
				self._start_position = 0
			return

		logging.info(
			__name__, 'Ignoring end of buffering as state is already NONE'
		)

	def _on_bus_error(self, _bus: Gst.Bus, message: Gst.Message):
		logging.error(__name__, 'Bus error', message.parse_error().gerror.message)
		self.pop_uri(self._queue.songs[self._queue_index].yt_id)
		self.play(
			self._queue.songs[self._queue_index],
			self._queue,
			self._last_known_position
		)

	def _on_latency(self, _bus: Gst.Bus, _message: Gst.Message):
		if self._playbin.recalculate_latency():
			logging.info(__name__, 'Recalculated latency')
		else:
			logging.error(__name__, 'Failed to recalculate latency')

	def _on_radio_songs_found(self, task: FindRadioSongsTask):
		if task.is_canceled() or self._radio_task is not task:
			return

		if not task.result:
			logging.warning(__name__, 'No radio songs found')
			self.play(self._queue.songs[self._queue_index], self._queue)
			return

		self.play(task.result.songs[0], task.result)

	def _on_state_change(self, _bus: Gst.Bus, _message: Gst.Message):
		success, state, _d = self._playbin.get_state(1)
		if success != Gst.StateChangeReturn.SUCCESS:
			return
		if state == Gst.State.PLAYING and self.paused:
			logging.info(__name__, 'Adjusted state to paused after change')
			self._playbin.set_state(Gst.State.PAUSED)

	def _on_stream_start(self, _bus: Gst.Bus, _message: Gst.Message):
		if self.state == PlaybackState.LOADING and not self.buffering:
			logging.info(__name__, 'Stream started')
			self._playbin.set_state(Gst.State.PLAYING)
			self.state = PlaybackState.PLAYING
			self.emit('state-changed', self.state)
			if self._start_position:
				logging.info(__name__, f'Seeking to {self._start_position}ns')
				self._playbin.seek_simple(
					Gst.Format.TIME,
					Gst.SeekFlags.FLUSH | Gst.SeekFlags.ACCURATE,
					self._start_position
				)
				self._start_position = 0

	def _on_stream_end(self, _bus: Gst.Bus, _message):
		logging.info(__name__, 'Stream has ended')
		self.next()

	def _report_progress(self, _task: ReportProgressTask):
		duration = self.get_duration_ns()
		position = self.get_position_ns()
		if duration > 0 and not self.buffering:
			self.emit('progress-changed', position / duration)
			if position > 0:
				self._last_known_position = position

	def _save_uri(self, yt_id: str, uri: str):
		while len(self._song_uris) > len(self._queue.songs):
			self._song_uris.pop(next(iter(self._song_uris.keys())))

		self._song_uris[yt_id] = uri
		logging.info(__name__, f'Added URI for song "{yt_id}" to known')

	def _start_playback(self, task: FindURITask, position: int=0):
		if task.is_canceled() or self._find_uri_task is not task:
			logging.info(__name__, 'Ignoring callback from canceled URI lookup task')
			return

		song = self._queue.songs[self._queue_index]
		uri = task.result
		if not uri:
			logging.error(__name__, f'Failed to find URI for song "{song.yt_id}"')
			self.play(song, self._queue, position)
			return

		self._save_uri(song.yt_id, uri)
		self._find_uri_task = FindURITask(
			callback=self._on_background_uri_search_done,
			args=(song, self._song_uris)
		)
		self._find_uri_task.extra_data = song
		self._find_uri_task.start()

		self._progress_task = ReportProgressTask(
			progress_callback=self._report_progress
		)
		self._progress_task.start()

		# Don't actually start yet - wait for messages on the bus
		self._playbin.props.uri = uri
		self._playbin.set_state(Gst.State.PAUSED)
		logging.info(__name__, 'Started playback')

	def add_to_queue(self, group: Group):
		if self._queue.songs:
			self._queue.songs += group.songs
			self.emit('queue-changed', self._queue, self._queue_index)
			return

		self.play(group.songs[0], group)

	def get_current_song(self) -> Song | None:
		if self._queue.songs:
			return self._queue.songs[self._queue_index]

		return None

	def get_duration_ns(self) -> float:
		return self._playbin.query_duration(Gst.Format.TIME)[1]

	def get_position_ns(self) -> float:
		return self._playbin.query_position(Gst.Format.TIME)[1]

	def get_queue(self) -> Group:
		return self._queue

	def get_volume(self) -> float:
		return self._playbin.props.volume

	def move_song(self, song: Song, target: Song):
		logging.info(
			__name__, f'Moving song "{song.yt_id}" to "{target.yt_id}" in queue...'
		)
		current_song = self._queue.songs[self._queue_index]
		from_index = self._queue.songs.index(song)
		to_index = self._queue.songs.index(target)
		if abs(from_index - to_index) > 1:
			self._queue.songs.pop(from_index)
			self._queue.songs.insert(self._queue.songs.index(target), song)
		else:
			self._queue.songs[from_index], self._queue.songs[to_index] = (
				self._queue.songs[to_index], self._queue.songs[from_index]
			)

		self._queue_index = self._queue.songs.index(current_song)
		self.emit('queue-changed', self._queue, self._queue_index)
		logging.info(__name__, 'Moved song in queue')

	def next(self, from_user: bool=False):
		if self.mode == PlaybackMode.RADIO:
			if len(self._queue.songs) > self._queue_index + 1:
				self.play(self._queue.songs[self._queue_index + 1], self._queue)
				return

			self.state = PlaybackState.LOADING
			self.emit('state-changed', self.state)
			self._radio_task = FindRadioSongsTask(
				callback=self._on_radio_songs_found,
				args=(self._queue.songs[self._queue_index], self._queue)
			)
			self._radio_task.start()
			return

		if self.mode == PlaybackMode.LOOP_QUEUE:
			if len(self._queue.songs) > self._queue_index + 1:
				self.play(self._queue.songs[self._queue_index + 1], self._queue)
				return

			self.play(self._queue.songs[0], self._queue)
			return

		if self.mode == PlaybackMode.LOOP_SONG:
			if from_user:
				if len(self._queue.songs) > self._queue_index + 1:
					self.play(self._queue.songs[self._queue_index + 1], self._queue)
					return

				self.stop()
				return

			self.play(self._queue.songs[self._queue_index], self._queue)
			return

		if len(self._queue.songs) > self._queue_index + 1:
			self.play(self._queue.songs[self._queue_index + 1], self._queue)
			return

		self.stop()

	def play(self, song: Song, group: Group, position: int=0):
		logging.info(
			__name__, f'Playback of song "{song.yt_id}" at {position}ns requested'
		)

		recents.add(song)
		self.emit('recents-changed')
		self.state = PlaybackState.LOADING
		self.emit('state-changed', self.state)
		self._queue = copy.deepcopy(group)
		self._queue_index = self._queue.songs.index(song)
		self.emit('queue-changed', self._queue, self._queue_index)
		self._playbin.set_state(Gst.State.NULL)
		self._playbin.props.uri = ''
		self.buffering = False
		self.paused = False
		if position <= 0:
			self._start_position = 0
			self.emit('progress-changed', 0)
		else:
			self._start_position = position
		self._last_known_position = self._start_position
		self.emit('buffering-changed', 0)

		self._mpris_event_sender.emit_all()

		self._find_uri_task.cancel()
		self._progress_task.cancel()
		self._radio_task.cancel()
		self._find_uri_task = FindURITask(
			callback=self._start_playback,
			callback_args=(position,),
			args=(song, self._song_uris)
		)
		self._find_uri_task.extra_data = song
		self._find_uri_task.start()

	def pop_uri(self, yt_id: str) -> str | None:
		if yt_id in self._song_uris:
			logging.info(__name__, f'Popped known URI for song "{yt_id}"')
			return self._song_uris.pop(yt_id)

		return None

	def previous(self):
		if self._queue_index > 0:
			self.play(self._queue.songs[self._queue_index - 1], self._queue)
			return

		self.seek(0)

	def remove_from_queue(self, song: Song):
		if len(self._queue.songs) > 1:
			current_song = self._queue.songs[self._queue_index]
			self._queue.songs.remove(song)
			self._queue_index = self._queue.songs.index(current_song)
			self.emit('queue-changed', self._queue, self._queue_index)
			return

		self.stop()

	def seek(self, value: float):
		seek_position = round(self.get_duration_ns() * value)
		self._playbin.seek_simple(
			Gst.Format.TIME, Gst.SeekFlags.FLUSH, max(seek_position, 0)
		)
		self._mpris_event_sender.on_seek(value)

	def set_pause(self, pause: bool):
		logging.info(__name__, f'Setting pause to "{pause}"...')
		self.paused = pause

		if not self.buffering and self.state != PlaybackState.LOADING:
			self._playbin.set_state(
				Gst.State.PAUSED if self.paused else Gst.State.PLAYING
			)

		self.emit('pause-changed', pause)
		self._mpris_event_sender.on_playpause()
		logging.info(__name__, f'Set pause to "{pause}"')

	def set_volume(
		self, volume: float, notify_frontend: bool=True, notify_mpris: bool=True
	):
		settings.save({'volume': volume})
		self._playbin.props.volume = volume
		if notify_mpris:
			self._mpris_event_sender.on_volume()
		if notify_frontend:
			self.emit('volume-changed', volume)

	def set_mode(self, mode: int):
		self.mode = mode
		settings.save({'mode': mode})
		self.emit('mode-changed', self.mode)

	def shuffle(self):
		logging.info(__name__, 'Shuffling songs...')
		back_part = self._queue.songs[:self._queue_index]
		front_part = self._queue.songs[self._queue_index + 1:]

		shuffled = []
		if len(back_part) > 1 or len(front_part) > 1:
			while True:
				shuffled = [
					*random.sample(back_part, k=len(back_part)),
					self._queue.songs[self._queue_index],
					*random.sample(front_part, k=len(front_part)),
				]
				if shuffled != self._queue.songs:
					self._queue.songs = shuffled
					self.emit('queue-changed', self._queue, self._queue_index)
					break

		logging.info(__name__, 'Shuffled songs')

	def stop(self):
		logging.info(__name__, 'Stopping playback...')
		self._find_uri_task.cancel()
		self._progress_task.cancel()
		self._radio_task.cancel()
		self._playbin.set_state(Gst.State.NULL)
		self._playbin.props.uri = ''
		self.state = PlaybackState.NONE
		self.emit('state-changed', self.state)
		self.paused = False
		self.buffering = False
		self._queue = Group()
		self._queue_index = 0
		self.emit('queue-changed', self._queue, self._queue_index)
		self._mpris_event_sender.emit_all()
		logging.info(__name__, 'Stopped playback')
