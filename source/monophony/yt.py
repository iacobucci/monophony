import contextlib
import subprocess
import time
import traceback

from monophony import logging
from monophony.asynchronous import Task
from monophony.data import Artist, Group, Song, TimeString, YTItem

import requests
import ytmusicapi


# Exceptions raised by some (but not all) ytmusicapi functions in case of a data
# parsing error. They can be safely interpreted as a "not found" response from YTM. In
# the case of an internet connection error, requests.exceptions.ConnectionError is
# raised instead
YTMUSICAPI_PARSING_EXCEPTIONS = (AttributeError, KeyError, TypeError)


class SearchResult:
	# Raises KeyError on unknown type
	def __init__(self, type_: str, top: bool, item: YTItem | None=None):
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
		logging.warning(__name__, 'Got unusual artist name data', name_data or None)
		return ''

	return ', '.join(
		[artist.get('name', '') for artist in name_data if 'id' in artist]
	)


def _get_artist_id(artists: list[dict] | str) -> str:
	if isinstance(artists, str):
		return ''
	if not isinstance(artists, list):
		logging.warning(__name__, 'Got unusual artist data', artists or None)
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
		logging.info(__name__, 'Discarded podcast result')
		return None

	try:
		result = SearchResult(type_, category == 'Top result')
	except KeyError:
		logging.error(
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
		logging.warning(
			__name__,
			f'Discarded id-less result "{result_name}" of type "{result.type}"'
		)
		return None

	if result.type in ('album', 'playlist'):
		try:
			try:
				playlist = yt.get_playlist(result.item.yt_id, limit=None)
			except YTMUSICAPI_PARSING_EXCEPTIONS:
				playlist = yt.get_album(result.item.yt_id)
		except (
			*YTMUSICAPI_PARSING_EXCEPTIONS,
			ytmusicapi.exceptions.YTMusicUserError, # Invalid ID
			requests.exceptions.ConnectionError
		):
			logging.error(
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
	logging.info(__name__, f'Getting URI for song "{song.yt_id}"...')
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
		logging.error(__name__, 'Failed to get song URI', err)
		return None

	logging.info(__name__, 'Got song URI')
	return out.split('\n')[0]


def get_similar_songs(song: Song, ignore: Group | None=None) -> Group | None:
	logging.info(
		__name__,
		f'Getting similar song to "{song.yt_id}" ignoring '
		f'{len(ignore.songs) if ignore else 0} songs...'
	)
	yt = ytmusicapi.YTMusic()
	ignore = ignore if ignore else Group()

	try:
		data = yt.get_watch_playlist(song.yt_id, radio=True)['tracks']
	except (*YTMUSICAPI_PARSING_EXCEPTIONS, requests.exceptions.ConnectionError):
		logging.error(
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
		logging.info(__name__, f'Got {len(available_songs)} similar songs')
		return Group(songs=available_songs)

	logging.error(__name__, 'Failed to get similar song - no songs available')
	return Group()


def get_song(id_: str) -> Song | None:
	logging.info(__name__, f'Getting song "{id_}"...')
	yt = ytmusicapi.YTMusic()

	try:
		result = yt.get_song(id_)['videoDetails']
	except (*YTMUSICAPI_PARSING_EXCEPTIONS, requests.exceptions.ConnectionError):
		logging.error(
			__name__, 'Failed to get song', traceback.format_exc()
		)
		return None

	result['resultType'] = 'song'
	if parsed := _parse_single_result(yt, result):
		logging.info(__name__, 'Got song')
		return parsed.item

	logging.error(__name__, 'Failed to get song')
	return None


def get_album_or_playlist(yt_id: str) -> Group | None:
	logging.info(__name__, f'Getting album/playlist "{yt_id}"...')

	if result := _parse_single_result(
		ytmusicapi.YTMusic(),
		{
			'resultType': 'playlist',
			'playlistId': yt_id
		}
	):
		logging.info(__name__, 'Got album/playlist')
		return result.item

	logging.error(__name__, 'Failed to get album/playlist')
	return None


class ParseResultsTask(Task):
	def _function(
		self, yt: ytmusicapi.YTMusic, data: list[dict], limit: int | None=None,
	) -> list[SearchResult] | None:
		count_per_type = {}

		logging.info(
			__name__, f'Parsing {len(data)} results with limit of {limit} per type...'
		)
		results = []
		got_top_result = False
		for i, item in enumerate(data):
			if self.is_canceled():
				logging.info(__name__, 'Parsing canceled')
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
						logging.warning(__name__, 'Multiple top results')
						parsed.top = False
					else:
						logging.info(__name__, f'Top result type is "{parsed.type}"')
						got_top_result = True

				count_per_type[parsed.type] = count_per_type.get(parsed.type, 0) + 1
				results.append(parsed)

		# Internal results (in albums, playlists) not counted
		logging.info(__name__, f'Done parsing results, kept {len(results)}/{len(data)}')
		return results


class GetArtistTask(Task):
	def _on_parse_progress_update(self, task: ParseResultsTask, progress: float):
		if not task.is_canceled():
			self._update_progress(0.5 + progress / 2)

	def _function(
		self, browse_id: str, filter_: str, limit: int | None=None
	) -> list[SearchResult] | None:
		logging.info(
			__name__,
			f'Getting artist "{browse_id}" with filter "{filter_}" and limit of '
			f'{limit} per type...'
		)
		yt = ytmusicapi.YTMusic()

		logging.info(__name__, 'Fetching artist...')
		try:
			try:
				data = yt.get_artist(browse_id)
				logging.info(__name__, 'Fetched artist')
			except YTMUSICAPI_PARSING_EXCEPTIONS:
				logging.info(__name__, 'No such artist, fetching as user instead...')
				data = yt.get_user(browse_id)
				logging.info(__name__, 'Fetched artist as user')
		except (*YTMUSICAPI_PARSING_EXCEPTIONS, requests.exceptions.ConnectionError):
			logging.error(
				__name__,
				'Failed to get artist - could not fetch',
				traceback.format_exc()
			)
			return None

		if self.is_canceled():
			logging.info(__name__, 'Canceled getting artist')
			return None

		self._update_progress(0.1)

		to_parse = []
		for type_ in ('songs', 'videos'):
			if filter_ and type_ != filter_:
				continue

			if not (group := data.get(type_)):
				logging.info(__name__, f'Artist has no {type_} list')
				continue

			tracks = []
			logging.info(
				__name__, f'Trying to get {type_} from artist with get_playlist...'
			)
			try:
				try:
					tracks = yt.get_playlist(group.get('browseId', ''))['tracks']
				except YTMUSICAPI_PARSING_EXCEPTIONS:
					logging.info(
						__name__,
						f'Got no {type_}, trying with get_user_videos instead...'
					)
					# Does not raise YTMUSICAPI_PARSING_EXCEPTIONS, ever
					tracks = yt.get_user_videos(browse_id, group.get('params', ''))
			except requests.exceptions.ConnectionError:
				logging.error(__name__, 'Failed to get artist', traceback.format_exc())
				return None

			if not tracks:
				logging.info(
					__name__, f'Got no {type_}, trying from "results" list instead...'
				)
				if not (tracks := group.get('results')):
					logging.info(__name__, f'Got no {type_} from artist')
					continue

			logging.info(__name__, f'Got {len(tracks)} {type_} from artist')
			for track in tracks:
				track['resultType'] = type_[:-1]
				to_parse.append(track)

			if self.is_canceled():
				logging.info(__name__, 'Canceled getting artist')
				return None

		self._update_progress(0.2)
		for type_ in ('albums', 'singles', 'playlists'):
			if filter_ and ('albums' if type_ == 'singles' else type_) != filter_:
				continue

			if not (group := data.get(type_)):
				logging.info(__name__, f'Artist has no {type_} list')
				continue

			lists = []
			logging.info(
				__name__, f'Trying to get {type_} from artist with get_artist_albums...'
			)
			try:
				try:
					lists = yt.get_artist_albums(
						group.get('browseId', ''), group.get('params', '')
					)
				except YTMUSICAPI_PARSING_EXCEPTIONS:
					logging.info(
						__name__,
						f'Got no {type_}, trying with get_user_playlists instead...'
					)
					# Does not raise YTMUSICAPI_PARSING_EXCEPTIONS, ever
					lists = yt.get_user_playlists(browse_id, group.get('params', ''))
			except requests.exceptions.ConnectionError:
				logging.error(__name__, 'Failed to get artist', traceback.format_exc())
				return None

			if not lists:
				logging.info(
					__name__, f'Got no {type_}, trying from "results" list instead...'
				)
				if not (lists := group.get('results')):
					logging.info(__name__, f'Got no {type_} from artist')
					continue

			logging.info(__name__, f'Got {len(lists)} {type_} from artist')
			for list_ in lists:
				list_['resultType'] = type_[:-1]
				to_parse.append(list_)

			if self.is_canceled():
				logging.info(__name__, 'Canceled getting artist')
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
				logging.info(__name__, 'Canceled getting artist')
				return None

		if results := parse_task.result:
			for result in results:
				if not result.item.author.name:
					result.item.author.name = data.get('name', '')

			time.sleep(0.1)
			logging.info(__name__, 'Got artist')
			return results

		logging.error(__name__, 'Failed to get artist')
		return None


class GetRecommendationsTask(Task):
	def _function(self) -> list[Group] | None:
		logging.info(__name__, 'Getting recommendations...')
		yt = ytmusicapi.YTMusic()

		try:
			data = yt.get_home()
		except (*YTMUSICAPI_PARSING_EXCEPTIONS, requests.exceptions.ConnectionError):
			logging.error(
				__name__, 'Failed to get recommendations', traceback.format_exc()
			)
			return None

		recommendations = []
		for i, grouping in enumerate(data):
			playlist = Group(title=grouping.get('title', ''))
			for item in grouping.get('contents', []):
				if not isinstance(item, dict):
					logging.warning(__name__, 'Unexpected recommendation item', item)
					continue

				if 'videoId' not in item:
					continue

				item['resultType'] = 'song'
				if parsed := _parse_single_result(yt, item):
					playlist.songs.append(parsed.item)

			if playlist.songs:
				recommendations.append(playlist)
			self._update_progress(i / len(data))

		logging.info(__name__, f'Got {len(recommendations)} groups of recommendations')
		return recommendations


class SearchTask(Task):
	def _on_parse_progress_update(self, task: ParseResultsTask, progress: float):
		if not task.is_canceled():
			self._update_progress(0.5 + progress / 2)

	def _function(
		self, query: str, filter_: str='', limit: int | None=None
	) -> list[SearchResult] | None:
		logging.info(__name__, f'Searching for "{query}" with filter "{filter_}"...')
		yt = ytmusicapi.YTMusic()

		self._update_progress(0.1)
		try:
			if '?v=' in query and '/' in query:
				song = get_song(query.split('?v=')[-1].split('&')[0])
				if song:
					logging.info(__name__, 'Done searching - got song from URL')
					return [SearchResult('song', True, song)]
				logging.error(
					__name__, 'Failed to search - failed to get song from URL'
				)
				return None
			if 'youtu.be/' in query:
				song = get_song(query.split('youtu.be/')[-1].split('?')[0])
				if song:
					logging.info(__name__, 'Done searching - got song from URL')
					return [SearchResult('song', True, song)]
				logging.error(
					__name__, 'Failed to search - failed to get song from URL'
				)
				return None

			self._update_progress(0.2)
			data = (
				yt.search(query, filter=filter_, limit=100) if filter_
					else yt.search(query)
			)
		except (*YTMUSICAPI_PARSING_EXCEPTIONS, requests.exceptions.ConnectionError):
			logging.error(__name__, 'Failed to search', traceback.format_exc())
			return None

		if self.is_canceled():
			logging.info(__name__, 'Canceled search')
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
				logging.info(__name__, 'Canceled search')
				return None

		if parse_task.result is not None:
			time.sleep(0.1)
			logging.info(__name__, 'Done searching')
			return parse_task.result

		logging.error(__name__, 'Failed to search')
		return None
