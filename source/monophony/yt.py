'''Wrappers for YT.'''

import contextlib
import re
import subprocess
import time
import traceback

from monophony.asynchronous import Task
from monophony.data import Artist, Group, Song, TimeString, YTItem

import logboth
import requests
import ytmusicapi


# Exceptions raised by some (but not all) ytmusicapi functions in case of a data
# parsing error. They can be safely interpreted as a "not found" response from YTM. In
# the case of an internet connection error, requests.exceptions.RequestException is
# raised instead
_YTMUSICAPI_PARSING_EXCEPTIONS = (AttributeError, KeyError, TypeError)


class SearchResult:
	'''Wrapper for supported search result type.'''

	def __init__(self, type_: str, top: bool, item: YTItem | None=None):
		'''Initialize result for type.

		:param type_: Result type.
		:param top: Whether this is a top result.
		:param item: Optional item data.
		:raise KeyError: On unsupported type.
		'''
		if type_ == 'single':
			type_ = 'album'

		self.item = item or {
			'album': Group,
			'artist': Artist,
			'playlist': Group,
			'song': Song,
			'video': Song
		}[type_]()
		self.top = top
		self.type = type_


def _get_artist_name(name_data: list[dict] | str) -> str:
	if isinstance(name_data, str):
		return name_data
	if not isinstance(name_data, list):
		logboth.warning(__name__, 'Got unusual artist name data', name_data or None)
		return ''

	return ', '.join(
		[artist.get('name', '') for artist in name_data if 'id' in artist]
	)


def _get_artist_id(artists: list[dict] | str) -> str:
	if isinstance(artists, str):
		return ''
	if not isinstance(artists, list):
		logboth.warning(__name__, 'Got unusual artist data', artists or None)
		return ''

	a_id = ''
	for artist in artists:
		a_id = artist.get('id', '')
		if a_id:
			break

	return a_id


def _parse_single_result(yt: ytmusicapi.YTMusic, data: dict) -> SearchResult | None:
	category = data.get('category', '')
	type_ = data.get('resultType', '')

	if type_ in ('podcast', 'episode'):
		logboth.info(__name__, 'Discarded podcast result')
		return None

	try:
		result = SearchResult(type_, category == 'Top result')
	except KeyError:
		logboth.error(
			__name__, f'Failed to parse result of unexpected type "{type_}"', data
		)
		return None

	if result.type == 'artist':
		result.item.name = (
			_get_artist_name(data.get('artists', '')) or
			data.get('artist', '')
		)
		result.item.yt_id = (
			_get_artist_id(data.get('artists', '')) or
			data.get('browseId', '')
		)
	else:
		result.item.yt_id = (
			data.get('videoId', '') or
			data.get('browseId', '') or
			data.get('playlistId', '')
		)
		result.item.title = data.get('title', '')
		result.item.author.yt_id = (
			_get_artist_id(data.get('artists', '')) or
			_get_artist_id(data.get('author', '')) or
			data.get('channelId', '')
		)
		result.item.author.name = (
			_get_artist_name(data.get('artists', '')) or
			_get_artist_name(data.get('author', '')) or
			data.get('artist', '')
		)
		result.item.length = (
			data.get('duration', '') or
			TimeString(seconds=int(data.get('lengthSeconds', 0))).as_string()
		)
		thumbnail_container = data.get('thumbnails') or data.get('thumbnail')
		result.item.thumbnail = (
			thumbnail_container[0].get('url', '')
				if isinstance(thumbnail_container, list)
					else (
						thumbnail_container.get('thumbnails') or [{}]
					)[0].get('url', '')
		) if thumbnail_container else ''

	if not result.item.yt_id:
		result_name = (
			result.item.name if isinstance(result.item, Artist) else result.item.title
		)
		logboth.warning(
			__name__,
			f'Discarded id-less result "{result_name}" of type "{result.type}"'
		)
		return None

	if result.type in ('album', 'playlist'):
		try:
			try:
				playlist = yt.get_playlist(result.item.yt_id, limit=None)
			except _YTMUSICAPI_PARSING_EXCEPTIONS:
				playlist = yt.get_album(result.item.yt_id)
		except (
			*_YTMUSICAPI_PARSING_EXCEPTIONS,
			ytmusicapi.exceptions.YTMusicUserError, # Invalid ID
			requests.exceptions.RequestException
		):
			logboth.error(
				__name__, 'Failed to parse a result', traceback.format_exc()
			)
			return None

		result.item.title = playlist.get('title', result.item.title)
		for song_data in playlist.get('tracks', []):
			song_data['resultType'] = 'song'
			parsed_song_data = _parse_single_result(yt, song_data)
			if parsed_song_data:
				if result.item.thumbnail and not parsed_song_data.item.thumbnail:
					parsed_song_data.item.thumbnail = result.item.thumbnail
				result.item.songs.append(parsed_song_data.item)

	return result


def get_song_uri(song: Song) -> str | None:
	'''Get YT playback URI from song ID.

	:param song: Song to get URI for.
	:return: Playback URI, if found.
	'''
	logboth.info(__name__, f'Getting URI for song "{song.yt_id}"...')
	try:
		response = requests.get(
			f'https://music.youtube.com/watch?v={song.yt_id}', timeout=5
		)
	except requests.exceptions.RequestException:
		logboth.error(__name__, 'Failed to get song URI', traceback.format_exc())
		return None

	response_match = re.search('/watch\\?v=...........', response.text)
	if response_match:
		new_id = response_match[0].split('=')[-1]
		if len(new_id) != 11: # noqa: PLR2004 - YT ID length
			logboth.warning(
				__name__,
				f'Got invalid id "{new_id}" for redirect from song "{song.yt_id}"'
			)
		elif new_id != song.yt_id:
			logboth.info(__name__, f'Redirected song "{song.yt_id}" to "{new_id}"')
			song.yt_id = new_id
	else:
		logboth.warning(
			__name__,
			f'No redirect information returned for song "{song.yt_id}"',
			response.text
		)

	out, err = subprocess.Popen(
		[
			'yt-dlp',
			'--get-url',
			'--extract-audio',
			'--quiet',
			'--no-warnings',
			f'https://music.youtube.com/watch?v={song.yt_id}'
		],
		text=True,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE,
	).communicate()
	if err:
		logboth.error(__name__, 'Failed to get song URI', err)
		return None

	logboth.info(__name__, 'Got song URI')
	return out.split('\n')[0]


def get_similar_songs(song: Song, ignore: Group | None=None) -> Group | None:
	'''Get group of songs similar to a song.

	:param song: Song.
	:param ignore: Group of songs to ignore while searching.
	:return: Group of similar songs, if found.
	'''
	logboth.info(
		__name__,
		f'Getting similar song to "{song.yt_id}" ignoring '
		f'{len(ignore.songs) if ignore else 0} songs...'
	)
	yt = ytmusicapi.YTMusic()
	ignore = ignore or Group()

	try:
		data = yt.get_watch_playlist(song.yt_id, radio=True)['tracks']
	except (*_YTMUSICAPI_PARSING_EXCEPTIONS, requests.exceptions.RequestException):
		logboth.error(
			__name__, 'Failed to get similar song', traceback.format_exc()
		)
		return None

	available_songs = []
	for item in data:
		item['resultType'] = 'song'
		parsed = _parse_single_result(yt, item)
		if not parsed:
			continue

		song = parsed.item
		for ignore_song in ignore.songs:
			if ignore_song.yt_id == song.yt_id:
				break
		else:
			available_songs.append(song)

	if available_songs:
		logboth.info(__name__, f'Got {len(available_songs)} similar songs')
		return Group(songs=available_songs)

	logboth.error(__name__, 'Failed to get similar song - no songs available')
	return Group()


def get_song(id_: str) -> Song | None:
	'''Get song from YT ID.

	:param id_: YT ID of song.
	:return: Song, if found.
	'''
	logboth.info(__name__, f'Getting song "{id_}"...')
	yt = ytmusicapi.YTMusic()

	try:
		result = yt.get_song(id_)['videoDetails']
	except (*_YTMUSICAPI_PARSING_EXCEPTIONS, requests.exceptions.RequestException):
		logboth.error(
			__name__, 'Failed to get song', traceback.format_exc()
		)
		return None

	result['resultType'] = 'song'
	if parsed := _parse_single_result(yt, result):
		logboth.info(__name__, 'Got song')
		return parsed.item

	logboth.error(__name__, 'Failed to get song')
	return None


def get_album_or_playlist(yt_id: str) -> Group | None:
	'''Get group from YT ID.

	:param yt_id: YT ID of album or playlist.
	:return: Group, if found.
	'''
	logboth.info(__name__, f'Getting album/playlist "{yt_id}"...')

	if result := _parse_single_result(
		ytmusicapi.YTMusic(),
		{
			'resultType': 'playlist',
			'playlistId': yt_id
		}
	):
		logboth.info(__name__, 'Got album/playlist')
		return result.item

	logboth.error(__name__, 'Failed to get album/playlist')
	return None


class ParseResultsTask(Task):
	'''Task for parsing raw ytmusicapi data and constructing a list of search results.

	.. code-block::

		ParseResultsTask(
			args=(ytmusicapi.YTMusic(), raw_data, limit)
		)

	'''

	def _function(
		self, yt: ytmusicapi.YTMusic, data: list[dict], limit: int | None=None,
	) -> list[SearchResult] | None:
		count_per_type = {}

		logboth.info(
			__name__, f'Parsing {len(data)} results with limit of {limit} per type...'
		)
		results = []
		got_top_result = False
		for i, item in enumerate(data):
			if self.is_canceled():
				logboth.info(__name__, 'Parsing canceled')
				return None

			with contextlib.suppress(KeyError):
				temp_result = SearchResult(item.get('resultType'), False)
				if limit and count_per_type.get(temp_result.type, 0) >= limit:
					continue

			parsed = _parse_single_result(yt, item)
			self._update_progress(i / len(data))
			if parsed:
				if parsed.top:
					if got_top_result:
						logboth.warning(__name__, 'Multiple top results')
						parsed.top = False
					else:
						logboth.info(__name__, f'Top result type is "{parsed.type}"')
						got_top_result = True

				count_per_type[parsed.type] = count_per_type.get(parsed.type, 0) + 1
				results.append(parsed)

		# Internal results (in albums, playlists) not counted
		logboth.info(__name__, f'Done parsing results, kept {len(results)}/{len(data)}')
		return results


class GetArtistTask(Task):
	'''Task for getting list of search results from artist ID.

	.. code-block::

		GetArtistTask(
			args=(artist_id, type_filter, limit)
		)

	'''

	def _on_parse_progress_update(self, task: ParseResultsTask, progress: float):
		if not task.is_canceled():
			self._update_progress(0.5 + progress / 2)

	def _function(
		self, browse_id: str, filter_: str, limit: int | None=None
	) -> list[SearchResult] | None:
		logboth.info(
			__name__,
			f'Getting artist "{browse_id}" with filter "{filter_}" and limit of '
			f'{limit} per type...'
		)
		yt = ytmusicapi.YTMusic()

		logboth.info(__name__, 'Fetching artist...')
		try:
			try:
				data = yt.get_artist(browse_id)
				logboth.info(__name__, 'Fetched artist')
			except _YTMUSICAPI_PARSING_EXCEPTIONS:
				logboth.info(__name__, 'No such artist, fetching as user instead...')
				data = yt.get_user(browse_id)
				logboth.info(__name__, 'Fetched artist as user')
		except (*_YTMUSICAPI_PARSING_EXCEPTIONS, requests.exceptions.RequestException):
			logboth.error(
				__name__,
				'Failed to get artist - could not fetch',
				traceback.format_exc()
			)
			return None

		if self.is_canceled():
			logboth.info(__name__, 'Canceled getting artist')
			return None

		self._update_progress(0.1)

		to_parse = []
		for type_ in ('songs', 'videos'):
			if filter_ and type_ != filter_:
				continue

			if not (group := data.get(type_)):
				logboth.info(__name__, f'Artist has no {type_} list')
				continue

			tracks = []
			logboth.info(
				__name__, f'Trying to get {type_} from artist with get_playlist...'
			)
			try:
				try:
					tracks = yt.get_playlist(group.get('browseId', ''))['tracks']
				except _YTMUSICAPI_PARSING_EXCEPTIONS:
					logboth.info(
						__name__,
						f'Got no {type_}, trying with get_user_videos instead...'
					)
					# Does not raise _YTMUSICAPI_PARSING_EXCEPTIONS, ever
					tracks = yt.get_user_videos(browse_id, group.get('params', ''))
			except requests.exceptions.RequestException:
				logboth.error(__name__, 'Failed to get artist', traceback.format_exc())
				return None

			if not tracks:
				logboth.info(
					__name__, f'Got no {type_}, trying from "results" list instead...'
				)
				if not (tracks := group.get('results')):
					logboth.info(__name__, f'Got no {type_} from artist')
					continue

			logboth.info(__name__, f'Got {len(tracks)} {type_} from artist')
			for track in tracks:
				track['resultType'] = type_[:-1]
				to_parse.append(track)

			if self.is_canceled():
				logboth.info(__name__, 'Canceled getting artist')
				return None

		self._update_progress(0.2)
		for type_ in ('albums', 'singles', 'playlists'):
			if filter_ and ('albums' if type_ == 'singles' else type_) != filter_:
				continue

			if not (group := data.get(type_)):
				logboth.info(__name__, f'Artist has no {type_} list')
				continue

			lists = []
			logboth.info(
				__name__, f'Trying to get {type_} from artist with get_artist_albums...'
			)
			try:
				try:
					lists = yt.get_artist_albums(
						group.get('browseId', ''), group.get('params', '')
					)
				except _YTMUSICAPI_PARSING_EXCEPTIONS:
					logboth.info(
						__name__,
						f'Got no {type_}, trying with get_user_playlists instead...'
					)
					# Does not raise _YTMUSICAPI_PARSING_EXCEPTIONS, ever
					lists = yt.get_user_playlists(browse_id, group.get('params', ''))
			except requests.exceptions.RequestException:
				logboth.error(__name__, 'Failed to get artist', traceback.format_exc())
				return None

			if not lists:
				logboth.info(
					__name__, f'Got no {type_}, trying from "results" list instead...'
				)
				if not (lists := group.get('results')):
					logboth.info(__name__, f'Got no {type_} from artist')
					continue

			logboth.info(__name__, f'Got {len(lists)} {type_} from artist')
			for list_ in lists:
				list_['resultType'] = type_[:-1]
				to_parse.append(list_)

			if self.is_canceled():
				logboth.info(__name__, 'Canceled getting artist')
				return None

		self._update_progress(0.5)
		parse_task = ParseResultsTask(
			progress_callback=self._on_parse_progress_update,
			args=(yt, to_parse, limit)
		)
		parse_task.start()
		while parse_task.is_running():
			time.sleep(0.1)
			if self.is_canceled():
				parse_task.cancel()
				logboth.info(__name__, 'Canceled getting artist')
				return None

		if results := parse_task.result:
			for result in results:
				if not result.item.author.name:
					result.item.author.name = data.get('name', '')

			time.sleep(0.1)
			logboth.info(__name__, 'Got artist')
			return results

		logboth.error(__name__, 'Failed to get artist')
		return None


class GetRecommendationsTask(Task):
	'''Task for fetching list of recommended playlists.'''

	def _function(self) -> list[Group] | None:
		logboth.info(__name__, 'Getting recommendations...')
		yt = ytmusicapi.YTMusic()

		try:
			data = yt.get_home()
		except (*_YTMUSICAPI_PARSING_EXCEPTIONS, requests.exceptions.RequestException):
			logboth.error(
				__name__, 'Failed to get recommendations', traceback.format_exc()
			)
			return None

		recommendations = []
		for i, grouping in enumerate(data):
			playlist = Group(title=grouping.get('title', ''))
			for item in grouping.get('contents', []):
				if not isinstance(item, dict):
					logboth.warning(__name__, 'Unexpected recommendation item', item)
					continue

				if 'videoId' not in item:
					continue

				item['resultType'] = 'song'
				if parsed := _parse_single_result(yt, item):
					playlist.songs.append(parsed.item)

			if playlist.songs:
				recommendations.append(playlist)
			self._update_progress(i / len(data))

		logboth.info(__name__, f'Got {len(recommendations)} groups of recommendations')
		return recommendations


class SearchTask(Task):
	'''Task for searching YT.

	.. code-block::

		SearchTask(
			args=(query, type_filter, limit)
		)

	'''

	def _on_parse_progress_update(self, task: ParseResultsTask, progress: float):
		if not task.is_canceled():
			self._update_progress(0.5 + progress / 2)

	def _function(
		self, query: str, filter_: str='', limit: int | None=None
	) -> list[SearchResult] | None:
		logboth.info(__name__, f'Searching for "{query}" with filter "{filter_}"...')
		yt = ytmusicapi.YTMusic()

		self._update_progress(0.1)
		try:
			if '?v=' in query and '/' in query:
				song = get_song(
					query.rsplit('?v=', maxsplit=1)[-1].split('&', maxsplit=1)[0]
				)
				if song:
					logboth.info(__name__, 'Done searching - got song from URL')
					return [SearchResult('song', True, song)]
				logboth.error(
					__name__, 'Failed to search - failed to get song from URL'
				)
				return None
			if 'youtu.be/' in query:
				song = get_song(
					query.rsplit('youtu.be/', maxsplit=1)[-1].split('?', maxsplit=1)[0]
				)
				if song:
					logboth.info(__name__, 'Done searching - got song from URL')
					return [SearchResult('song', True, song)]
				logboth.error(
					__name__, 'Failed to search - failed to get song from URL'
				)
				return None

			self._update_progress(0.2)
			data = (
				yt.search(query, filter=filter_, limit=100) if filter_
					else yt.search(query)
			)
		except (*_YTMUSICAPI_PARSING_EXCEPTIONS, requests.exceptions.RequestException):
			logboth.error(__name__, 'Failed to search', traceback.format_exc())
			return None

		if self.is_canceled():
			logboth.info(__name__, 'Canceled search')
			return None

		self._update_progress(0.5)
		parse_task = ParseResultsTask(
			progress_callback=self._on_parse_progress_update,
			args=(yt, data, limit)
		)
		parse_task.start()
		while parse_task.is_running():
			time.sleep(0.1)
			if self.is_canceled():
				parse_task.cancel()
				logboth.info(__name__, 'Canceled search')
				return None

		if parse_task.result is not None:
			time.sleep(0.1)
			logboth.info(__name__, 'Done searching')
			return parse_task.result

		logboth.error(__name__, 'Failed to search')
		return None
