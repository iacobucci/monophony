import contextlib
import datetime
from typing import Any

import logboth


class YTItem:
	def __eq__(self, other: Any):
		if isinstance(other, YTItem):
			return self.yt_id == other.yt_id

		return False

	def __hash__(self):
		return hash(self.yt_id)

	def __init__(self, yt_id: str=''):
		self.yt_id = yt_id or ''

	def serialize(self) -> dict:
		return {'id': self.yt_id}


class Artist(YTItem):
	def __init__(self, name: str='', yt_id: str=''):
		super().__init__(yt_id)
		self.name = name or ''

	def serialize(self) -> dict:
		return {'name': self.name, 'id': self.yt_id}


class Song(YTItem):
	def __init__(
		self,
		title: str='',
		author: Artist | None=None,
		length: str='',
		thumbnail: str='',
		yt_id: str=''
	):
		super().__init__(yt_id)
		self.title = title or ''
		self.author = author or Artist()
		self.length = length or ''
		self.thumbnail = thumbnail or ''

	def serialize(self) -> dict:
		return {
			'title': self.title,
			'author': self.author.name,
			'author_id': self.author.yt_id,
			'length': self.length,
			'thumbnail': self.thumbnail,
			'id': self.yt_id
		}


class Group(YTItem):
	def __init__(
		self,
		title: str='',
		author: Artist | None=None,
		songs: list[Song] | None=None,
		yt_id: str=''
	):
		super().__init__(yt_id)

		self._songs = []
		self.title = title or ''
		self.author = author or Artist()
		self.songs = songs or []

	@property
	def songs(self) -> list:
		return self._songs

	@songs.setter
	def songs(self, song_list: list[Song]):
		ids = []
		unique_songs = []
		for song in song_list:
			if not song.yt_id or song.yt_id in ids:
				continue

			unique_songs.append(song)
			ids.append(song.yt_id)

		self._songs = unique_songs

	def serialize(self) -> dict:
		return {
			'title': self.title,
			'author': self.author.name,
			'author_id': self.author.yt_id,
			'contents': [s.serialize() for s in self.songs],
			'id': self.yt_id
		}


class TimeString:
	SECONDS_POS = 0
	MINUTES_POS = 1
	HOURS_POS = 2

	def __init__(self, string: str='', seconds: int=0):
		if string:
			self._string = string
		else:
			self._string = str(datetime.timedelta(seconds=abs(seconds)))

	def as_seconds(self) -> int:
		seconds = 0
		parts = self._string.split(':')
		if len(parts) > TimeString.SECONDS_POS:
			with contextlib.suppress(ValueError):
				seconds += int(parts[-1])
		if len(parts) > TimeString.MINUTES_POS:
			with contextlib.suppress(ValueError):
				seconds += int(parts[-2]) * 60
		if len(parts) > TimeString.HOURS_POS:
			with contextlib.suppress(ValueError):
				seconds += int(parts[-3]) * 60 * 60
		if len(parts) > TimeString.HOURS_POS + 1:
			logboth.warning(
				__name__, f'TimeString "{self._string}" has too many parts'
			)

		return abs(seconds)

	def as_string(self) -> str:
		return self._string


class PlaybackMode:
	NORMAL = 0
	LOOP_SONG = 1
	LOOP_QUEUE = 2
	RADIO = 3


class PlaybackState:
	NONE = 0
	PLAYING = 1
	LOADING = 2
