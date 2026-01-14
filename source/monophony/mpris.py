import decimal

from monophony import ID
from monophony.data import PlaybackMode, PlaybackState

import logboth
from mprisify.adapters import MprisAdapter
from mprisify.adapters import PlayState as MprisPlayState
from mprisify.events import PlayerEventAdapter as MprisPlayerEventAdapter
from mprisify.server import Server as MprisServer


class EventHandler(MprisAdapter):
	def __init__(self, player: object):
		super().__init__()
		self._player = player

	def get_desktop_entry(self) -> str:
		return ID

	def can_quit(self) -> bool:
		return False

	def get_current_position(self) -> float:
		return self._player.get_position_ns() / 1000

	def next(self):
		self._player.next(from_user=True)

	def previous(self):
		self._player.previous()

	def pause(self):
		self._player.set_pause(True)

	def resume(self):
		self._player.set_pause(False)

	def stop(self):
		self._player.stop()

	def get_playstate(self) -> MprisPlayState:
		playstate = MprisPlayState.PLAYING
		if self._player.paused:
			playstate = MprisPlayState.PAUSED
		elif self._player.state == PlaybackState.NONE:
			playstate = MprisPlayState.STOPPED

		logboth.info(__name__, f'Reported playstate as "{playstate}"')
		return playstate

	def is_repeating(self) -> bool:
		return self._player.mode == PlaybackMode.LOOP_SONG

	def get_shuffle(self) -> bool:
		return False

	def get_volume(self):
		return self._player.get_volume()

	def set_volume(self, volume: decimal.Decimal):
		self._player.set_volume(float(volume), notify_mpris=False)

	def is_mute(self) -> bool:
		return False

	def can_go_next(self) -> bool:
		return True

	def can_go_previous(self) -> bool:
		return True

	def can_play(self) -> bool:
		return bool(self._player.get_current_song())

	def can_pause(self) -> bool:
		return bool(self._player.get_current_song())

	def can_seek(self) -> bool:
		return False

	def can_control(self) -> bool:
		return True

	def can_raise(self) -> bool:
		return True

	def set_raise(self, value: bool):
		if value:
			self._player.emit('raise')

	def metadata(self) -> dict:
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
	def __init__(self, id_: str, event_handler: EventHandler):
		super().__init__(id_, adapter=event_handler)


class EventSender(MprisPlayerEventAdapter):
	def __init__(self, server: Server):
		super().__init__(root=server.root, player=server.player)
