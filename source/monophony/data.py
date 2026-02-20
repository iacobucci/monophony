'''Containers for representing different types of data.'''

import contextlib
import datetime
from typing import Any

import logboth


class YTItem:
	'''Any kind of YT item that may have an ID.

	Not to be used directly. Inherit from this in a new class instead.
	'''

	def __eq__(self, other: Any):
		'''Override for ``==``.

		If the other object is not a ``YTItem``, the objects are not equal. Otherwise,
		the objects' YT IDs are compared.

		Note that items with empty IDs are considered equal.

		:param other: Object to compare to.
		:return: Comparison result.
		'''
		if isinstance(other, YTItem):
			return self.yt_id == other.yt_id

		return False

	def __hash__(self) -> int:
		'''Override for ``hash()``.

		The hash produced is a hash of the item's YT ID. This is to ensure that
		items with the same ID will be considered equal.

		:return: Item hash.
		'''
		return hash(self.yt_id)

	def __init__(self, yt_id: str=''):
		'''Initialize with optional YT ID.

		An ID should be provided if one is available. It must be an actual ID from
		YT - do not make one up. If YT does not provide an ID, it may be better to
		discard such a result rather than attempt to work with an item with no ID.

		:param yt_id: Item ID.
		'''
		self.yt_id = yt_id or ''
		'''Item's YT ID.

		Always 11 characters or empty.
		'''

	def serialize(self) -> dict:
		'''Generate a dictionary representation of the item.

		.. code-block::

			{
				'id': ...
			}

		:return: Serialized item.
		'''
		return {'id': self.yt_id}


class Artist(YTItem):
	'''An artist from YT.

	Only a reference - does not actually hold the artist's work.

	This class should be used to represent both users and artists (YT makes a
	distinction).
	'''

	def __init__(self, name: str='', yt_id: str=''):
		'''Initialize with optional name and YT ID.

		An ID should be provided if one is available. It must be an actual ID from
		YT - do not make one up. If YT does not provide an ID, it may be better to
		discard such a result rather than attempt to work with an item with no ID.

		:param name: Artist name.
		:param yt_id: Artist ID.
		'''
		super().__init__(yt_id)

		self.name = name or ''
		'''Artist's name.'''

	def serialize(self) -> dict:
		'''Generate a dictionary representation of the artist.

		.. code-block::

			{
				'id': ...,
				'name': ...
			}

		:return: Serialized artist.
		'''
		return {'name': self.name, 'id': self.yt_id}


class Song(YTItem):
	'''A song from YT.

	This class should be used to represent both videos and songs (YT makes a
	distinction).
	'''

	def __init__(
		self,
		title: str='',
		author: Artist | None=None,
		length: str='',
		thumbnail: str='',
		yt_id: str=''
	):
		'''Initialize with optional data.

		An ID should be provided if one is available. It must be an actual ID from
		YT - do not make one up. If YT does not provide an ID, it may be better to
		discard such a result rather than attempt to work with an item with no ID.

		:param title: Song title.
		:param author: First artist listed for the song.
		:param length: Song duration in XX:XX:XX format. See ``TimeString``.
		:param thumbnail: Song thumbnail URL.
		:param yt_id: Song ID.
		'''
		super().__init__(yt_id)

		self.title = title or ''
		'''Song title.'''

		self.author = author or Artist()
		'''First artist listed for the song.'''

		self.length = length or ''
		'''Song duration in XX:XX:XX format. See ``TimeString``.'''

		self.thumbnail = thumbnail or ''
		'''Song thumbnail URL.'''

	def serialize(self) -> dict:
		'''Generate a dictionary representation of the song.

		.. code-block::

			{
				'title': ...,
				'author': ...,
				'author_id': ...,
				'length': ...,
				'thumbnail': ...,
				'id': ...
			}

		:return: Serialized song.
		'''
		return {
			'title': self.title,
			'author': self.author.name,
			'author_id': self.author.yt_id,
			'length': self.length,
			'thumbnail': self.thumbnail,
			'id': self.yt_id
		}


class Group(YTItem):
	'''A group of songs from YT.

	This class should be used to represent both albums and playlists (YT makes a
	distinction).

	Groups should not be compared via ``==``, as user-created local groups do not
	have IDs. Compare their lists of songs instead.
	'''

	def __init__(
		self,
		title: str='',
		author: Artist | None=None,
		songs: list[Song] | None=None,
		yt_id: str=''
	):
		'''Initialize with optional data.

		An ID should be provided if one is available. It must be an actual ID from
		YT - do not make one up. If YT does not provide an ID, it may be better to
		discard such a result rather than attempt to work with an item with no ID.

		Local user-created playlists do not have IDs.

		:param title: Group title.
		:param author: First artist listed for the group.
		:param songs: Songs in the group.
		:param yt_id: Group ID.
		'''
		super().__init__(yt_id)

		self._songs = []

		self.title = title or ''
		'''Group title.'''

		self.author = author or Artist()
		'''First artist listed for the group.'''

		self.songs = songs or []
		'''Songs in the group.'''

	@property
	def songs(self) -> list[Song]:
		'''List of songs.

		:getter: Returns the group's list of songs.
		:setter: Sets the group's list of songs while removing duplicates.
		:type: list[Song]
		'''
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
		'''Generate a dictionary representation of the group.

		The "contents" entry is a list of serialized songs.

		.. code-block::

			{
				'title': ...,
				'author': ...,
				'author_id': ...,
				'contents': ...,
				'id': ...
			}

		:return: Serialized group.
		'''
		return {
			'title': self.title,
			'author': self.author.name,
			'author_id': self.author.yt_id,
			'contents': [s.serialize() for s in self.songs],
			'id': self.yt_id
		}


class TimeString:
	'''Converts between seconds and string representations of time.'''

	_SECONDS_POS = 0
	_MINUTES_POS = 1
	_HOURS_POS = 2

	def __init__(self, string: str='', seconds: int=0):
		'''Initialize from either a string or seconds.'''
		if string:
			self._string = string
		else:
			self._string = str(datetime.timedelta(seconds=abs(seconds)))

	def as_seconds(self) -> int:
		'''Get the time value as seconds.

		:return: Seconds.
		'''
		seconds = 0
		parts = self._string.split(':')
		if len(parts) > TimeString._SECONDS_POS:
			with contextlib.suppress(ValueError):
				seconds += int(parts[-1])
		if len(parts) > TimeString._MINUTES_POS:
			with contextlib.suppress(ValueError):
				seconds += int(parts[-2]) * 60
		if len(parts) > TimeString._HOURS_POS:
			with contextlib.suppress(ValueError):
				seconds += int(parts[-3]) * 60 * 60
		if len(parts) > TimeString._HOURS_POS + 1:
			logboth.warning(
				__name__, f'TimeString "{self._string}" has too many parts'
			)

		return abs(seconds)

	def as_string(self) -> str:
		'''Get the time value as a string.

		:return: Time in XX:XX:XX format.
		'''
		return self._string


class PlaybackMode:
	'''Playback modes for the player.'''

	NORMAL = 0
	'''Play songs in order, stop after the last one.'''

	LOOP_SONG = 1
	'''Play the current song on repeat.'''

	LOOP_QUEUE = 2
	'''Play songs in order, start over after the last one.'''

	RADIO = 3
	'''Play songs in order, automatically add more similar songs after the last one.'''


class PlaybackState:
	'''States the player can be in.'''

	NONE = 0
	'''No song, player inactive.'''

	PLAYING = 1
	'''Playing a song. Does not indicate pause state.'''

	LOADING = 2
	'''Loading a song. Refers to both fetching the URL and buffering.'''
