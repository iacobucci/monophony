'''Wrappers for YT.'''

import contextlib
import json
import os
import re
import subprocess
import time
import traceback

from monophony import NAME, get_user_config_dir, settings
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


def get_oauth_path() -> str:
	'''Get path to oauth.json file.'''
	return os.path.join(get_user_config_dir(), 'oauth.json')



def get_yt_client() -> ytmusicapi.YTMusic:
	'''Get a YTMusic client instance, using OAuth credentials if available.

	:return: YTMusic instance.
	'''
	oauth_path = get_oauth_path()
	client_id = settings.load('oauth_client_id', '')
	client_secret = settings.load('oauth_client_secret', '')

	if os.path.exists(oauth_path):
		try:
			with contextlib.suppress(Exception):
				with open(oauth_path, encoding='utf-8') as f:
					token_data = json.load(f)
				if isinstance(token_data, dict):
					if not client_id and token_data.get('client_id'):
						client_id = token_data['client_id']
						settings.save({'oauth_client_id': client_id})
					if not client_secret and token_data.get('client_secret'):
						client_secret = token_data['client_secret']
						settings.save({'oauth_client_secret': client_secret})

			if client_id and client_secret:
				creds = ytmusicapi.OAuthCredentials(client_id, client_secret)
				return ytmusicapi.YTMusic(oauth_path, oauth_credentials=creds)
			return ytmusicapi.YTMusic(oauth_path)
		except Exception as e:
			logboth.error(__name__, f'Failed to load OAuth client: {e}')

	return ytmusicapi.YTMusic()



def is_authenticated() -> bool:
	'''Check if YouTube account is authenticated via OAuth.

	:return: True if authenticated.
	'''
	oauth_path = get_oauth_path()
	return os.path.exists(oauth_path)


def import_oauth_file(filepath: str) -> bool:
	'''Import an existing oauth.json file into Monophony configuration.

	:param filepath: Path to oauth.json file.
	:return: True if successfully imported.
	'''
	try:
		with open(filepath, encoding='utf-8') as f:
			data = json.load(f)
		if not isinstance(data, dict) or ('access_token' not in data and 'refresh_token' not in data):
			logboth.error(__name__, 'Invalid oauth.json file structure')
			return False

		dest_path = get_oauth_path()
		os.makedirs(os.path.dirname(dest_path), exist_ok=True)
		with open(dest_path, 'w', encoding='utf-8') as f:
			json.dump(data, f, indent=True)

		if 'client_id' in data and 'client_secret' in data:
			settings.save({'oauth_client_id': data['client_id'], 'oauth_client_secret': data['client_secret']})

		logboth.info(__name__, f'Successfully imported OAuth file from {filepath}')
		return True
	except Exception as e:
		logboth.error(__name__, f'Failed to import OAuth file: {e}')
		return False



def start_oauth_flow(client_id: str, client_secret: str) -> dict | None:
	'''Start OAuth device code flow.

	:param client_id: OAuth client ID.
	:param client_secret: OAuth client secret.
	:return: Dict with user_code, device_code, verification_url, expires_in, or None if error.
	'''
	try:
		creds = ytmusicapi.OAuthCredentials(client_id, client_secret)
		return creds.get_code()
	except Exception as e:
		logboth.error(__name__, f'Failed to start OAuth flow: {e}')
		return None


def finish_oauth_flow(client_id: str, client_secret: str, device_code: str) -> tuple[bool, str]:
	'''Finish OAuth flow with device code and save credentials.

	:param client_id: OAuth client ID.
	:param client_secret: OAuth client secret.
	:param device_code: Device code obtained from start_oauth_flow.
	:return: Tuple of (success, error_message).
	'''
	try:
		creds = ytmusicapi.OAuthCredentials(client_id, client_secret)
		token_dict = creds.token_from_code(device_code)
		if isinstance(token_dict, dict):
			token_dict['client_id'] = client_id
			token_dict['client_secret'] = client_secret
		elif hasattr(token_dict, 'as_dict'):
			token_dict = token_dict.as_dict()
			token_dict['client_id'] = client_id
			token_dict['client_secret'] = client_secret

		oauth_path = get_oauth_path()
		os.makedirs(os.path.dirname(oauth_path), exist_ok=True)
		with open(oauth_path, 'w', encoding='utf-8') as f:
			json.dump(token_dict, f, indent=True)

		settings.save({'oauth_client_id': client_id, 'oauth_client_secret': client_secret})
		logboth.info(__name__, 'Successfully authenticated YouTube account')
		return True, ''
	except ytmusicapi.auth.oauth.exceptions.BadOAuthClient as e:
		msg = f'BadOAuthClient: {e}. Check if "YouTube Data API v3" is enabled in Google Cloud Console.'
		logboth.error(__name__, f'Failed to complete OAuth flow: {msg}\n{traceback.format_exc()}')
		return False, msg
	except Exception as e:
		msg = f'{type(e).__name__}: {e}'
		logboth.error(__name__, f'Failed to complete OAuth flow: {msg}\n{traceback.format_exc()}')
		return False, msg


def logout_account():
	'''Remove YouTube account authentication token while preserving client credentials.'''
	oauth_path = get_oauth_path()
	if os.path.exists(oauth_path):
		with contextlib.suppress(OSError):
			os.remove(oauth_path)
	logboth.info(__name__, 'Logged out YouTube account token')



def _get_user_playlists_tv(yt: ytmusicapi.YTMusic) -> list[dict]:
	try:
		body = {'browseId': 'FEmusic_liked_playlists'}
		ctx = {
			'context': {
				'client': {
					'clientName': 'TVHTML5',
					'clientVersion': '7.20260828.00.00',
					'hl': 'en'
				},
				'user': {}
			}
		}
		body.update(ctx)
		res = yt._session.post('https://music.youtube.com/youtubei/v1/browse', json=body, headers=yt.headers).json()

		def extract_text(obj):
			if not obj:
				return ''
			if isinstance(obj, str):
				return obj
			if isinstance(obj, dict):
				if 'simpleText' in obj:
					return obj['simpleText']
				if 'runs' in obj and isinstance(obj['runs'], list):
					return ''.join(r.get('text', '') for r in obj['runs'] if isinstance(r, dict))
			return ''

		def find_tiles(obj):
			tiles = []
			if isinstance(obj, dict):
				if 'tileRenderer' in obj:
					tr = obj['tileRenderer']
					meta = tr.get('metadata', {}).get('tileMetadataRenderer', {})
					title = extract_text(meta.get('title'))
					pid = ''
					cmd = tr.get('onSelectCommand', {})
					if 'watchEndpoint' in cmd:
						pid = cmd['watchEndpoint'].get('playlistId', '')
					elif 'browseEndpoint' in cmd:
						pid = cmd['browseEndpoint'].get('browseId', '').removeprefix('VL')

					if pid:
						tiles.append({'playlistId': pid, 'title': title})
				for v in obj.values():
					tiles.extend(find_tiles(v))
			elif isinstance(obj, list):
				for item in obj:
					tiles.extend(find_tiles(item))
			return tiles

		parsed = find_tiles(res)
		seen = set()
		unique = []
		for p in parsed:
			if p['playlistId'] not in seen:
				seen.add(p['playlistId'])
				unique.append(p)
		return unique
	except Exception as e:
		logboth.error(__name__, f'Failed to get TV library playlists: {e}')
		return []


def get_user_playlists() -> list[dict]:
	'''Get list of playlists from the authenticated user's library.

	:return: List of playlist dicts.
	'''
	if not is_authenticated():
		return []
	try:
		yt = get_yt_client()
		try:
			return yt.get_library_playlists(limit=None)
		except Exception as e:
			logboth.warning(__name__, f'get_library_playlists standard call failed ({e}), using TVHTML5 fallback')
			return _get_user_playlists_tv(yt)
	except Exception as e:
		logboth.error(__name__, f'Failed to get library playlists: {e}')
		return []



def create_user_playlist(title: str, description: str='', video_ids: list[str] | None=None) -> str | None:
	'''Create a playlist in the user's YouTube account library.

	:param title: Playlist title.
	:param description: Optional description.
	:param video_ids: List of song YT IDs to add.
	:return: Created YouTube playlist ID or None.
	'''
	if not is_authenticated():
		return None
	try:
		yt = get_yt_client()
		playlist_id = yt.create_playlist(title, description, video_ids=video_ids or [])
		logboth.info(__name__, f'Created remote playlist "{title}" ({playlist_id})')
		return playlist_id
	except Exception as e:
		logboth.error(__name__, f'Failed to create user playlist "{title}": {e}')
		return None


def add_songs_to_user_playlist(playlist_id: str, song_ids: list[str]) -> bool:
	'''Add songs to a user's YouTube playlist.

	:param playlist_id: YT playlist ID.
	:param song_ids: List of song YT IDs to add.
	:return: True if successful.
	'''
	if not is_authenticated() or not playlist_id or not song_ids:
		return False
	try:
		yt = get_yt_client()
		yt.add_playlist_items(playlist_id, song_ids)
		logboth.info(__name__, f'Added {len(song_ids)} songs to remote playlist "{playlist_id}"')
		return True
	except Exception as e:
		logboth.error(__name__, f'Failed to add songs to remote playlist "{playlist_id}": {e}')
		return False


def remove_songs_from_user_playlist(playlist_id: str, song_ids: list[str]) -> bool:
	'''Remove songs from a user's YouTube playlist.

	:param playlist_id: YT playlist ID.
	:param song_ids: List of song YT IDs to remove.
	:return: True if successful.
	'''
	if not is_authenticated() or not playlist_id or not song_ids:
		return False
	try:
		yt = get_yt_client()
		playlist_data = yt.get_playlist(playlist_id, limit=None)
		tracks = playlist_data.get('tracks', [])
		items_to_remove = []
		for track in tracks:
			if track.get('videoId') in song_ids and 'setVideoId' in track:
				items_to_remove.append({
					'videoId': track['videoId'],
					'setVideoId': track['setVideoId']
				})
		if items_to_remove:
			yt.remove_playlist_items(playlist_id, items_to_remove)
			logboth.info(__name__, f'Removed {len(items_to_remove)} songs from remote playlist "{playlist_id}"')
			return True
		return False
	except Exception as e:
		logboth.error(__name__, f'Failed to remove songs from remote playlist "{playlist_id}": {e}')
		return False


def delete_user_playlist(playlist_id: str) -> bool:
	'''Delete a user's YouTube playlist.

	:param playlist_id: YT playlist ID to delete.
	:return: True if successful.
	'''
	if not is_authenticated() or not playlist_id:
		return False
	try:
		yt = get_yt_client()
		yt.delete_playlist(playlist_id)
		logboth.info(__name__, f'Deleted remote playlist "{playlist_id}"')
		return True
	except Exception as e:
		logboth.error(__name__, f'Failed to delete remote playlist "{playlist_id}": {e}')
		return False



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


def get_updated_song(song: Song) -> Song | None:
	'''Get song with new ID from song with possibly retired ID.

	This is needed because YT song IDs can change at any time for any reason.
	This will fail if there is no connection.

	:param song: Song to get updated version of.
	:return: Song with updated ID, if YT connection succeded.
	'''
	logboth.info(__name__, f'Getting updated version of song {song.yt_id}...')
	try:
		response = requests.get(
			f'https://music.youtube.com/watch?v={song.yt_id}', timeout=5
		)
	except requests.exceptions.RequestException:
		logboth.error(
			__name__,
			f'Failed to get updated version of song {song.yt_id}',
			traceback.format_exc()
		)
		return None

	response_match = re.search('/watch\\?v=...........', response.text)
	if response_match:
		new_id = response_match[0].split('=')[-1]
		if new_id != song.yt_id:
			logboth.info(__name__, f'Got updated ID "{new_id}" for song "{song.yt_id}"')
			song.yt_id = new_id
		else:
			logboth.info(__name__, f'Song "{song.yt_id}" is up to date')
		return song

	logboth.warning(
		__name__,
		f'No ID in song update response for song "{song.yt_id}"',
		response.text
	)
	return song


def get_song_uri(song: Song) -> str | None:
	'''Get YT playback URI from song ID.

	:param song: Song to get URI for.
	:return: Playback URI, if found.
	'''
	logboth.info(__name__, f'Getting URI for song "{song.yt_id}"...')

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
	yt = get_yt_client()
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
	yt = get_yt_client()

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


def _get_playlist_tv(yt_id: str) -> Group | None:
	if not is_authenticated() or not yt_id:
		return None
	try:
		yt = get_yt_client()
		browse_id = 'FEmusic_liked_videos' if yt_id == 'LM' else ('VL' + yt_id if not yt_id.startswith('VL') else yt_id)
		body = {'browseId': browse_id}
		ctx = {
			'context': {
				'client': {
					'clientName': 'TVHTML5',
					'clientVersion': '7.20260828.00.00',
					'hl': 'en'
				},
				'user': {}
			}
		}
		body.update(ctx)
		res = yt._session.post('https://music.youtube.com/youtubei/v1/browse', json=body, headers=yt.headers).json()

		def extract_text(obj):
			if not obj:
				return ''
			if isinstance(obj, str):
				return obj
			if isinstance(obj, dict):
				if 'simpleText' in obj:
					return obj['simpleText']
				if 'runs' in obj and isinstance(obj['runs'], list):
					return ''.join(r.get('text', '') for r in obj['runs'] if isinstance(r, dict))
			return ''

		def find_tiles(obj):
			tiles = []
			if isinstance(obj, dict):
				if 'tileRenderer' in obj:
					tr = obj['tileRenderer']
					cmd = tr.get('onSelectCommand', {})
					vid = ''
					if 'watchEndpoint' in cmd:
						vid = cmd['watchEndpoint'].get('videoId', '')
					elif 'videoId' in tr:
						vid = tr['videoId']

					if vid:
						meta = tr.get('metadata', {}).get('tileMetadataRenderer', {})
						title = extract_text(meta.get('title'))

						artist = ''
						lines = meta.get('lines', [])
						if lines and isinstance(lines, list):
							items = lines[0].get('lineRenderer', {}).get('items', [])
							if items and isinstance(items, list):
								artist = extract_text(items[0].get('lineItemRenderer', {}).get('text'))

						thumb = f'https://i.ytimg.com/vi/{vid}/hqdefault.jpg'
						thumbnails = tr.get('header', {}).get('tileHeaderRenderer', {}).get('thumbnail', {}).get('thumbnails', [])
						if thumbnails and isinstance(thumbnails, list):
							thumb = thumbnails[-1].get('url', thumb)

						length = ''
						overlays = tr.get('header', {}).get('tileHeaderRenderer', {}).get('thumbnailOverlays', [])
						for o in overlays:
							if 'thumbnailOverlayTimeStatusRenderer' in o:
								length = extract_text(o['thumbnailOverlayTimeStatusRenderer'].get('text'))

						tiles.append({
							'yt_id': vid,
							'title': title or vid,
							'artist': artist,
							'thumbnail': thumb,
							'length': length
						})
				for v in obj.values():
					tiles.extend(find_tiles(v))
			elif isinstance(obj, list):
				for item in obj:
					tiles.extend(find_tiles(item))
			return tiles

		raw_songs = find_tiles(res)
		seen = set()
		unique = []
		for s in raw_songs:
			if s['yt_id'] not in seen:
				seen.add(s['yt_id'])
				song_obj = Song(
					title=s['title'] or s['yt_id'],
					author=Artist(name=s['artist']),
					length=s['length'] or '',
					thumbnail=s['thumbnail'],
					yt_id=s['yt_id']
				)

				unique.append(song_obj)

		if unique:
			title = 'Liked Music' if yt_id == 'LM' else yt_id
			return Group(title=title, yt_id=yt_id, songs=unique)
		return None
	except Exception as e:
		logboth.warning(__name__, f'TVHTML5 playlist fetch failed for "{yt_id}": {e}')
		return None



def get_album_or_playlist(yt_id: str) -> Group | None:
	'''Get group from YT ID.

	:param yt_id: YT ID of album or playlist.
	:return: Group, if found.
	'''
	logboth.info(__name__, f'Getting album/playlist "{yt_id}"...')

	if is_authenticated():
		if tv_group := _get_playlist_tv(yt_id):
			logboth.info(__name__, f'Got album/playlist "{yt_id}" via TVHTML5 ({len(tv_group.songs)} songs)')
			return tv_group

	if result := _parse_single_result(
		get_yt_client(),
		{
			'resultType': 'playlist',
			'playlistId': yt_id
		}
	):
		logboth.info(__name__, 'Got album/playlist')
		return result.item

	logboth.error(__name__, 'Failed to get album/playlist')
	return None



def song_exists(song: Song) -> bool | None:
	'''Check if song is available on YT.

	This is impossible to determine if there is no connection.

	:param song: Song to check.
	:return: Whether the song is available, if can be determined.
	'''
	logboth.info(__name__, f'Checking if song "{song.yt_id}" exists...')
	yt = get_yt_client()
	try:
		song_data = yt.get_song(song.yt_id)
	except (*_YTMUSICAPI_PARSING_EXCEPTIONS, requests.exceptions.RequestException):
		logboth.error(
			__name__, 'Failed to check if song exists', traceback.format_exc()
		)
		return None

	exists = song_data.get('playabilityStatus', {}).get('status') not in (
		'ERROR', 'UNPLAYABLE'
	)
	if exists:
		logboth.info(__name__, f'Song "{song.yt_id}" exists')
	else:
		logboth.warning(__name__, f'Song "{song.yt_id}" does not exist')

	return exists


class ParseResultsTask(Task):
	'''Task for parsing raw ytmusicapi data and constructing a list of search results.

	.. code-block::

		ParseResultsTask(
			args=(get_yt_client(), raw_data, limit)
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
		yt = get_yt_client()

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
		# Unauthenticated YTMusic instance to prevent HTTP 400 Bad Request on FEmusic_home with TV OAuth tokens
		yt = ytmusicapi.YTMusic()

		try:
			data = yt.get_home()
		except Exception:
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
		yt = get_yt_client()

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
			max_retries = 3
			one_result_retries = 0
			while True:
				try:
					data = (
						yt.search(query, filter=filter_, limit=100) if filter_
							else yt.search(query)
					)
				except Exception as e:
					logboth.warning(__name__, f'Search call failed ({e}), using unauthenticated fallback')
					unauth_yt = ytmusicapi.YTMusic()
					data = (
						unauth_yt.search(query, filter=filter_, limit=100) if filter_
							else unauth_yt.search(query)
					)

				# Work around weird single-result response that happens sometimes
				if len(data) > 1 or one_result_retries == max_retries:
					break
				logboth.warning(
					__name__,
					f'Got fewer than 2 results - retrying... ({one_result_retries + 1})'
				)
				yt = get_yt_client() # New session usually fixes the issue
				one_result_retries += 1
		except Exception as e:
			logboth.error(__name__, f'Failed to search: {e}', traceback.format_exc())
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
