'''MPRIS integration.'''

import decimal

from monophony import ID
from monophony.data import PlaybackMode, PlaybackState

import logboth
from mprisify.adapters import MprisAdapter
from mprisify.adapters import PlayState as MprisPlayState
from mprisify.events import PlayerEventAdapter as MprisPlayerEventAdapter
from mprisify.server import Server as MprisServer


class EventHandler(MprisAdapter):
	'''Handler for events received via MPRIS.

	Controls the player based on events.
	'''

	def __init__(self, player: object):
		'''Initialize with player.

		:param player: Player object to control.
		'''
		super().__init__()
		self._player = player

	def get_desktop_entry(self) -> str:
		'''Get the desktop entry name.

		This is just the app ID.

		:return: Desktop entry name.
		'''
		return ID

	def can_quit(self) -> bool:
		'''Check if quitting via MPRIS is enabled.

		:return: False.
		'''
		return False

	def get_current_position(self) -> float:
		'''Get the current playback position in ns.

		:return: Playback position.
		'''
		return self._player.get_position_ns() / 1000

	def next(self):
		'''Skip to next song.'''
		self._player.next(from_user=True)

	def previous(self):
		'''Skip to previous song.'''
		self._player.previous()

	def pause(self):
		'''Pause playback.'''
		self._player.set_pause(True)

	def resume(self):
		'''Resume playback.'''
		self._player.set_pause(False)

	def stop(self):
		'''Stop playback.'''
		self._player.stop()

	def get_playstate(self) -> MprisPlayState:
		'''Get the playback state.

		The state is either stopped, playing or paused.

		:return: Playback state.
		'''
		playstate = MprisPlayState.PLAYING
		if self._player.paused:
			playstate = MprisPlayState.PAUSED
		elif self._player.state == PlaybackState.NONE:
			playstate = MprisPlayState.STOPPED

		logboth.info(__name__, f'Reported playstate as "{playstate}"')
		return playstate

	def is_repeating(self) -> bool:
		'''Check if current song is set to repeat.

		:return: Current song repeat state.
		'''
		return self._player.mode == PlaybackMode.LOOP_SONG

	def get_shuffle(self) -> bool:
		'''Check if playback in random order is enabled.

		There is no such mode in the app.

		:return: False.
		'''
		return False

	def get_volume(self) -> float:
		'''Get the player volume.

		:return: Player volume.
		'''
		return self._player.get_volume()

	def set_volume(self, volume: decimal.Decimal):
		'''Set the player volume.

		:param volume: Volume.
		'''
		self._player.set_volume(float(volume), notify_mpris=False)

	def is_mute(self) -> bool:
		'''Check if the player is muted.

		There is no distinct "muted" state in the app. The volume can still be set to 0.

		:return: False.
		'''
		return False

	def can_go_next(self) -> bool:
		'''Check if skipping to the next song is enabled.

		This is always the case. If nothing is playing, it just has no effect.

		:return: True.
		'''
		return True

	def can_go_previous(self) -> bool:
		'''Check if skipping to the previous song is enabled.

		This is always the case. If nothing is playing, it just has no effect.

		:return: True.
		'''
		return True

	def can_play(self) -> bool:
		'''Check if resuming playback is enabled.

		This is true as long as the player has a song selected, regardless of state.

		:return: Whether resuming playback is enabled.
		'''
		return bool(self._player.get_current_song())

	def can_pause(self) -> bool:
		'''Check if pausing playback is enabled.

		This is true as long as the player has a song selected, regardless of state.

		:return: Whether pausing playback is enabled.
		'''
		return bool(self._player.get_current_song())

	def can_seek(self) -> bool:
		'''Check if seeking is enabled.

		Seeking via MPRIS is not supported.

		:return: False.
		'''
		return False

	def can_control(self) -> bool:
		'''Check if controling the player is enabled.

		This has to be true for other events to fire.

		:return: True.
		'''
		return True

	def can_raise(self) -> bool:
		'''Check if raising the window is enabled.

		:return: True.
		'''
		return True

	def set_raise(self, value: bool):
		'''Raise or lower the window.

		Only raising is supported. Falsey values ignored.

		:param value: Whether to raise.
		'''
		if value:
			self._player.emit('raise')

	def metadata(self) -> dict:
		'''Get current track metadata.

		:return: Current track metadata.
		'''
		metadata = {'mpris:trackid': '/org/mpris/MediaPlayer2/TrackList/NoTrack'}
		if song := self._player.get_current_song():
			duration_ns = self._player.get_duration_ns()
			metadata = {
				'mpris:trackid': '/track/1',
				'mpris:artUrl': song.thumbnail,
				'mpris:length': duration_ns / 1000,
				'xesam:title': song.title,
				'xesam:artist': [song.author.name]
			}

		logboth.info(__name__, 'Reported metadata for current song', metadata)
		return metadata


class Server(MprisServer):
	'''MPRIS server.'''

	def __init__(self, id_: str, event_handler: EventHandler):
		'''Initialize with id and handler.

		:param id_: ``org.mpris.MediaPlayer2.{id_}``
		:param event_handler: Event handler object.
		'''
		super().__init__(id_, adapter=event_handler)


class EventSender(MprisPlayerEventAdapter):
	'''MPRIS event sender.'''

	def __init__(self, server: Server):
		'''Initialize with MPRIS server.

		:param server: MPRIS server.
		'''
		super().__init__(root=server.root, player=server.player)
