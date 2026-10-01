'''Wrappers for YT.'''

import contextlib
import json
import os
import re
import subprocess
import threading
import time
import traceback

from monophony import NAME, cache, get_user_config_dir, settings

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



_cached_unauth_client = None
_cached_auth_client = None
_oauth_token_failed = False


def _reset_cached_clients():
	global _cached_unauth_client, _cached_auth_client, _oauth_token_failed
	_cached_unauth_client = None
	_cached_auth_client = None
	_oauth_token_failed = False


@contextlib.contextmanager
def _tv_context(yt_client):
	'''Temporarily set YTMusic client to TVHTML5 to allow OAuth mutations.'''
	client_dict = yt_client.context.get('context', {}).get('client', {})
	orig_name = client_dict.get('clientName')
	orig_ver = client_dict.get('clientVersion')
	client_dict['clientName'] = 'TVHTML5'
	client_dict['clientVersion'] = '7.20260828.00.00'
	try:
		yield yt_client
	finally:
		if orig_name is not None:
			client_dict['clientName'] = orig_name
		if orig_ver is not None:
			client_dict['clientVersion'] = orig_ver


def _get_oauth_headers() -> dict[str, str] | None:
	'''Get Authorization headers for YouTube Data API v3 calls.'''
	if not is_authenticated():
		return None
	try:
		yt = get_yt_client()
		token = yt.headers.get('Authorization')
		if token:
			return {'Authorization': token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
	except Exception:
		pass
	return None


def get_yt_client(unauth: bool = False) -> ytmusicapi.YTMusic:
	'''Get a YTMusic client instance, using OAuth credentials if available.

	:param unauth: Whether to force an unauthenticated client.
	:return: YTMusic instance.
	'''
	global _cached_unauth_client, _cached_auth_client, _oauth_token_failed

	if unauth or _oauth_token_failed:
		if _cached_unauth_client is None:
			_cached_unauth_client = ytmusicapi.YTMusic()
		return _cached_unauth_client

	if _cached_auth_client is not None:
		return _cached_auth_client

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
				client = ytmusicapi.YTMusic(oauth_path, oauth_credentials=creds)
			else:
				client = ytmusicapi.YTMusic(oauth_path)

			# Verify token validity; fall back to unauthenticated if token refresh fails
			try:
				_ = client.headers
				_cached_auth_client = client
				return client
			except Exception as e:
				_oauth_token_failed = True
				logboth.warning(__name__, f'OAuth token invalid or expired ({e}), falling back to unauthenticated client')
				if _cached_unauth_client is None:
					_cached_unauth_client = ytmusicapi.YTMusic()
				return _cached_unauth_client
		except Exception as e:
			logboth.error(__name__, f'Failed to load OAuth client: {e}')

	if _cached_unauth_client is None:
		_cached_unauth_client = ytmusicapi.YTMusic()
	return _cached_unauth_client



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

		_reset_cached_clients()
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
		_reset_cached_clients()
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
	_reset_cached_clients()
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


def _get_tv_playlist_tracks(yt_client: ytmusicapi.YTMusic, playlist_id: str) -> list[dict]:
	'''Extract videoId and setVideoId from TVHTML5 playlist response.'''
	try:
		ctx = {'context': {'client': {'clientName': 'TVHTML5', 'clientVersion': '7.20260828.00.00', 'hl': 'en'}, 'user': {}}}
		browse_id = playlist_id if playlist_id.startswith('VL') else f'VL{playlist_id}'
		body = {'browseId': browse_id}
		body.update(ctx)
		res = yt_client._session.post('https://music.youtube.com/youtubei/v1/browse', json=body, headers=yt_client.headers).json()

		tracks = []
		def find_tiles(obj):
			if isinstance(obj, dict):
				if 'tileRenderer' in obj:
					tr = obj['tileRenderer']
					video_id = tr.get('contentId') or tr.get('onSelectCommand', {}).get('watchEndpoint', {}).get('videoId', '')
					set_video_id = ''
					for item in tr.get('onLongPressCommand', {}).get('showMenuCommand', {}).get('menu', {}).get('menuRenderer', {}).get('items', []):
						actions = item.get('menuServiceItemRenderer', {}).get('serviceEndpoint', {}).get('playlistEditEndpoint', {}).get('actions', [])
						for act in actions:
							if act.get('action') == 'ACTION_REMOVE_VIDEO' and act.get('setVideoId'):
								set_video_id = act['setVideoId']
								break
						if set_video_id:
							break
					if video_id:
						tracks.append({'videoId': video_id, 'setVideoId': set_video_id})
				for v in obj.values():
					find_tiles(v)
			elif isinstance(obj, list):
				for item in obj:
					find_tiles(item)
		find_tiles(res)
		return tracks
	except Exception as e:
		logboth.warning(__name__, f'Failed to get TV playlist tracks for "{playlist_id}": {e}')
		return []


def get_user_playlists() -> list[dict]:
	'''Get list of playlists from the authenticated user's library and account.

	:return: List of playlist dicts.
	'''
	if not is_authenticated():
		return []

	playlists = []
	seen_ids = set()

	# 1. Try YouTube Data API v3 (returns all user-created channel playlists)
	headers = _get_oauth_headers()
	if headers:
		try:
			res = requests.get(
				'https://www.googleapis.com/youtube/v3/playlists?part=snippet&mine=true&maxResults=50',
				headers=headers,
				timeout=10
			)
			if res.status_code == 200:
				for item in res.json().get('items', []):
					pid = item.get('id', '')
					title = item.get('snippet', {}).get('title', '')
					if pid and pid not in seen_ids:
						seen_ids.add(pid)
						playlists.append({'playlistId': pid, 'title': title})
		except Exception as e:
			logboth.warning(__name__, f'Failed to get playlists via YouTube Data API v3: {e}')

	# 2. Try TVHTML5 for YouTube Music library playlists
	try:
		yt = get_yt_client()
		tv_lists = _get_user_playlists_tv(yt)
		for p in tv_lists:
			pid = p.get('playlistId') or p.get('browseId', '').removeprefix('VL')
			if pid and pid not in seen_ids:
				seen_ids.add(pid)
				playlists.append(p)
	except Exception as e:
		logboth.warning(__name__, f'Failed to get playlists via TVHTML5: {e}')

	return playlists


def create_user_playlist(title: str, description: str='', video_ids: list[str] | None=None) -> str | None:
	'''Create a playlist in the user's YouTube account library.

	:param title: Playlist title.
	:param description: Optional description.
	:param video_ids: List of song YT IDs to add.
	:return: Created YouTube playlist ID or None.
	'''
	if not is_authenticated():
		return None

	# 1. Try YouTube Data API v3
	headers = _get_oauth_headers()
	if headers:
		try:
			body = {
				'snippet': {
					'title': title,
					'description': description
				},
				'status': {
					'privacyStatus': 'private'
				}
			}
			res = requests.post(
				'https://www.googleapis.com/youtube/v3/playlists?part=snippet,status',
				headers=headers,
				json=body,
				timeout=15
			)
			if res.status_code in (200, 201):
				pid = res.json().get('id')
				logboth.info(__name__, f'Created remote playlist "{title}" ({pid}) via YouTube Data API v3')
				if video_ids and pid:
					add_songs_to_user_playlist(pid, video_ids)
				return pid
			else:
				logboth.warning(__name__, f'YouTube Data API v3 create playlist returned {res.status_code}: {res.text[:200]}')
		except Exception as e:
			logboth.warning(__name__, f'Failed to create playlist via Data API v3: {e}')

	# 2. Fallback to YTMusic client
	try:
		yt = get_yt_client()
		with _tv_context(yt):
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

	clean_pid = playlist_id.removeprefix('VL')

	# Handle Liked Music virtual playlist: adding means rating as LIKE
	if clean_pid in ('LM', 'FEmusic_liked_videos'):
		success = True
		for sid in song_ids:
			if not rate_song(sid, 'LIKE'):
				success = False
		if success:
			logboth.info(__name__, f'Rated {len(song_ids)} songs as LIKE for "{clean_pid}"')
		return success

	# 1. Try TVHTML5 via ytmusicapi (0 API quota cost, bulk add)
	try:
		yt = get_yt_client()
		with _tv_context(yt):
			res = yt.add_playlist_items(clean_pid, song_ids)
			if isinstance(res, dict) and ('SUCCEEDED' in str(res.get('status', '')) or 'playlistEditResults' in res):
				logboth.info(__name__, f'Added {len(song_ids)} songs to remote playlist "{clean_pid}" via TVHTML5')
				return True
	except Exception as e:
		logboth.warning(__name__, f'TVHTML5 add_playlist_items failed ({e}), falling back to Data API v3')

	# 2. Fallback: YouTube Data API v3
	headers = _get_oauth_headers()
	if headers:
		try:
			success = True
			for sid in song_ids:
				body = {
					'snippet': {
						'playlistId': clean_pid,
						'resourceId': {
							'kind': 'youtube#video',
							'videoId': sid
						}
					}
				}
				r = requests.post(
					'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet',
					headers=headers,
					json=body,
					timeout=15
				)
				if r.status_code not in (200, 201):
					success = False
					logboth.warning(__name__, f'Data API v3 failed to add song "{sid}" to playlist "{clean_pid}": {r.text[:200]}')
			if success:
				logboth.info(__name__, f'Added {len(song_ids)} songs to remote playlist "{clean_pid}" via Data API v3')
				return True
		except Exception as e:
			logboth.error(__name__, f'Failed to add songs to remote playlist "{clean_pid}" via Data API v3: {e}')

	return False


def remove_songs_from_user_playlist(playlist_id: str, song_ids: list[str]) -> bool:
	'''Remove songs from a user's YouTube playlist.

	:param playlist_id: YT playlist ID.
	:param song_ids: List of song YT IDs to remove.
	:return: True if successful.
	'''
	if not is_authenticated() or not playlist_id or not song_ids:
		return False

	clean_pid = playlist_id.removeprefix('VL')

	# Handle Liked Music virtual playlist: removing means rating as INDIFFERENT
	if clean_pid in ('LM', 'FEmusic_liked_videos'):
		success = True
		for sid in song_ids:
			if not rate_song(sid, 'INDIFFERENT'):
				success = False
		if success:
			logboth.info(__name__, f'Unliked {len(song_ids)} songs for "{clean_pid}"')
		return success

	# 1. Try YouTube Data API v3 (lists exact item IDs and deletes them)
	headers = _get_oauth_headers()
	if headers:
		try:
			res = requests.get(
				f'https://www.googleapis.com/youtube/v3/playlistItems?part=id,snippet&playlistId={clean_pid}&maxResults=50',
				headers=headers,
				timeout=15
			)
			if res.status_code == 200:
				removed_count = 0
				for item in res.json().get('items', []):
					vid = item.get('snippet', {}).get('resourceId', {}).get('videoId')
					if vid in song_ids:
						del_res = requests.delete(
							f'https://www.googleapis.com/youtube/v3/playlistItems?id={item["id"]}',
							headers=headers,
							timeout=15
						)
						if del_res.status_code in (200, 204):
							removed_count += 1
				if removed_count > 0:
					logboth.info(__name__, f'Removed {removed_count} songs from remote playlist "{clean_pid}" via Data API v3')
					return True
		except Exception as e:
			logboth.warning(__name__, f'Failed to remove songs via Data API v3: {e}')

	# 2. Fallback: TVHTML5 / ytmusicapi
	try:
		yt = get_yt_client()
		tracks = _get_tv_playlist_tracks(yt, clean_pid)
		items_to_remove = []
		for track in tracks:
			if track.get('videoId') in song_ids and track.get('setVideoId'):
				items_to_remove.append({
					'videoId': track['videoId'],
					'setVideoId': track['setVideoId']
				})
		if items_to_remove:
			with _tv_context(yt):
				yt.remove_playlist_items(clean_pid, items_to_remove)
			logboth.info(__name__, f'Removed {len(items_to_remove)} songs from remote playlist "{clean_pid}" via TVHTML5')
			return True
		return False
	except Exception as e:
		logboth.error(__name__, f'Failed to remove songs from remote playlist "{clean_pid}": {e}')
		return False


def delete_user_playlist(playlist_id: str) -> bool:
	'''Delete a user's YouTube playlist.

	:param playlist_id: YT playlist ID to delete.
	:return: True if successful.
	'''
	if not is_authenticated() or not playlist_id:
		return False

	clean_pid = playlist_id.removeprefix('VL')

	# 1. Try YouTube Data API v3
	headers = _get_oauth_headers()
	if headers:
		try:
			res = requests.delete(
				f'https://www.googleapis.com/youtube/v3/playlists?id={clean_pid}',
				headers=headers,
				timeout=15
			)
			if res.status_code in (200, 204):
				logboth.info(__name__, f'Deleted remote playlist "{clean_pid}" via YouTube Data API v3')
				return True
			else:
				logboth.warning(__name__, f'Data API v3 delete returned {res.status_code}: {res.text[:200]}')
		except Exception as e:
			logboth.warning(__name__, f'Failed to delete playlist via Data API v3: {e}')

	# 2. Fallback: YTMusic client
	try:
		yt = get_yt_client()
		with _tv_context(yt):
			yt.delete_playlist(clean_pid)
		logboth.info(__name__, f'Deleted remote playlist "{clean_pid}"')
		return True
	except Exception as e:
		logboth.error(__name__, f'Failed to delete remote playlist "{clean_pid}": {e}')
		return False


def rate_song(video_id: str, rating: str = 'LIKE') -> bool:
	'''Rate a song on YouTube Music (LIKE, DISLIKE, INDIFFERENT).

	:param video_id: YouTube video ID.
	:param rating: One of 'LIKE', 'DISLIKE', 'INDIFFERENT'.
	:return: True if successful.
	'''
	if not is_authenticated():
		return False

	# 1. Try TVHTML5 via ytmusicapi
	try:
		yt = get_yt_client()
		with _tv_context(yt):
			yt.rate_song(video_id, rating)
		logboth.info(__name__, f'Rated song "{video_id}" as "{rating}" on YouTube Music')
		return True
	except Exception as e:
		logboth.warning(__name__, f'TVHTML5 rate_song failed ({e}), trying Data API v3')

	# 2. Fallback: YouTube Data API v3
	headers = _get_oauth_headers()
	if headers:
		try:
			v3_rating = rating.lower()
			if v3_rating == 'indifferent':
				v3_rating = 'none'
			res = requests.post(
				f'https://www.googleapis.com/youtube/v3/videos/rate?id={video_id}&rating={v3_rating}',
				headers=headers,
				timeout=10
			)
			if res.status_code in (200, 204):
				logboth.info(__name__, f'Rated song "{video_id}" as "{rating}" via Data API v3')
				return True
			else:
				logboth.warning(__name__, f'Data API v3 rate returned {res.status_code}: {res.text[:200]}')
		except Exception as err:
			logboth.error(__name__, f'Failed to rate song "{video_id}" via Data API v3: {err}')

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


def _parse_single_result(
	yt: ytmusicapi.YTMusic, data: dict, load_tracks: bool = True
) -> SearchResult | None:
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
			data.get('playlistId', '') or
			data.get('browseId', '')
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
		if not load_tracks:
			return result

		playlist = None
		try:
			unauth = get_yt_client(unauth=True)
			if result.item.yt_id.startswith('MPREb'):
				playlist = unauth.get_album(result.item.yt_id)
			else:
				try:
					playlist = unauth.get_playlist(result.item.yt_id, limit=None)
				except Exception:
					playlist = unauth.get_album(result.item.yt_id)
		except Exception:
			try:
				if result.item.yt_id.startswith('MPREb'):
					playlist = yt.get_album(result.item.yt_id)
				else:
					try:
						playlist = yt.get_playlist(result.item.yt_id, limit=None)
					except Exception:
						playlist = yt.get_album(result.item.yt_id)
			except Exception:
				logboth.warning(__name__, f'Failed to parse album/playlist "{result.item.yt_id}"')
				return None

		if not playlist or not isinstance(playlist, dict):
			return None

		result.item.title = playlist.get('title', result.item.title)
		for song_data in playlist.get('tracks', []):
			if not isinstance(song_data, dict):
				continue
			song_data['resultType'] = 'song'
			parsed_song_data = _parse_single_result(yt, song_data, load_tracks=False)
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


_ydl_client = None
_ydl_lock = threading.Lock()


def _get_ydl():
	global _ydl_client
	if _ydl_client is None:
		try:
			import sys, os
			if os.path.exists('/app/bin/yt-dlp') and '/app/bin/yt-dlp' not in sys.path:
				sys.path.insert(0, '/app/bin/yt-dlp')
			import yt_dlp
			opts = {
				'format': 'bestaudio/best',
				'quiet': True,
				'no_warnings': True,
				'extract_flat': False,
				'skip_download': True,
				'extractor_args': {'youtube': {'player_client': ['ios', 'android', 'web']}}
			}
			_ydl_client = yt_dlp.YoutubeDL(opts)
		except Exception as e:
			logboth.warning(__name__, f'Failed to initialize in-process yt_dlp: {e}')
			_ydl_client = False
	return _ydl_client if _ydl_client is not False else None


def get_song_uri(song: Song) -> str | None:
	'''Get YT playback URI from song ID.

	:param song: Song to get URI for.
	:return: Playback URI, if found.
	'''
	logboth.info(__name__, f'Getting URI for song "{song.yt_id}"...')

	ydl = _get_ydl()
	if ydl is not None:
		try:
			with _ydl_lock:
				info = ydl.extract_info(
					f'https://music.youtube.com/watch?v={song.yt_id}',
					download=False
				)
			url = info.get('url') if info else None
			if url:
				logboth.info(__name__, f'Got fast streaming URI for song "{song.yt_id}"')
				return url
		except Exception as e:
			logboth.warning(
				__name__, f'In-process URI extraction failed for "{song.yt_id}" ({e}), falling back to CLI...'
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


def _parse_watch_track(renderer: dict) -> Song | None:
	'''Parse a playlistPanelVideoRenderer dictionary into a Song.'''
	video_id = renderer.get('videoId')
	if not video_id:
		return None

	title_runs = renderer.get('title', {}).get('runs', [])
	title = title_runs[0].get('text', '') if title_runs else ''

	length_runs = renderer.get('lengthText', {}).get('runs', [])
	length = length_runs[0].get('text', '') if length_runs else ''

	thumbs = renderer.get('thumbnail', {}).get('thumbnails', [])
	thumbnail = thumbs[-1].get('url', '') if thumbs else ''

	byline_runs = renderer.get('longBylineText', {}).get('runs', [])
	artist_name = ''
	artist_id = ''
	for r in byline_runs:
		if 'browseEndpoint' in r.get('navigationEndpoint', {}):
			artist_name = r.get('text', '')
			artist_id = r['navigationEndpoint']['browseEndpoint'].get('browseId', '')
			break
	if not artist_name and byline_runs:
		artist_name = byline_runs[0].get('text', '')

	return Song(
		title=title,
		author=Artist(name=artist_name, yt_id=artist_id),
		length=length,
		thumbnail=thumbnail,
		yt_id=video_id
	)


def get_watch_next(
	video_id: str | None = None,
	playlist_id: str | None = None,
	radio: bool = False,
	shuffle: bool = False,
	params: str | None = None,
	continuation: str | None = None
) -> dict:
	'''Robust wrapper for YouTube's "next" endpoint (watch panel / radio).

	Extracts tracks, radio chips, continuations, and related tab browseId without
	crashing on missing endpoints or unexpected tab structures.

	:return: dict with keys: 'tracks', 'chips', 'continuation', 'title', 'related_browse_id', 'lyrics_browse_id'.
	'''
	yt = get_yt_client(unauth=True)

	body = {
		'enablePersistentPlaylistPanel': True,
		'isAudioOnly': True,
		'tunerSettingValue': 'AUTOMIX_SETTING_NORMAL',
	}
	if video_id:
		body['videoId'] = video_id
		if not playlist_id:
			playlist_id = f'RDAMVM{video_id}'
	if playlist_id:
		body['playlistId'] = playlist_id
	if shuffle and playlist_id is not None:
		body['params'] = 'wAEB8gECKAE%3D'
	elif radio and not params:
		body['params'] = 'wAEB'
	elif params:
		body['params'] = params

	additional_params = f'&continuation={continuation}&ctoken={continuation}' if continuation else ''
	try:
		res = yt._send_request('next', body, additionalParams=additional_params)
	except Exception as e:
		logboth.error(__name__, f'Failed to call next endpoint: {e}')
		return {
			'tracks': [],
			'chips': [],
			'continuation': None,
			'title': '',
			'related_browse_id': None,
			'lyrics_browse_id': None
		}

	tracks = []
	chips = []
	next_continuation = None
	queue_title = ''
	related_browse_id = None
	lyrics_browse_id = None

	if continuation:
		panel = res.get('continuationContents', {}).get('playlistPanelContinuation', {})
		for item in panel.get('contents', []):
			if 'playlistPanelVideoRenderer' in item:
				if song := _parse_watch_track(item['playlistPanelVideoRenderer']):
					tracks.append(song)
		conts = panel.get('continuations', [])
		if conts:
			next_continuation = conts[0].get('nextRadioContinuationData', {}).get('continuation') or \
								conts[0].get('nextContinuationData', {}).get('continuation')
		return {
			'tracks': tracks,
			'chips': [],
			'continuation': next_continuation,
			'title': '',
			'related_browse_id': None,
			'lyrics_browse_id': None
		}

	single_col = res.get('contents', {}).get('singleColumnMusicWatchNextResultsRenderer', {})
	tabs = single_col.get('tabbedRenderer', {}).get('watchNextTabbedResultsRenderer', {}).get('tabs', [])
	if not tabs:
		return {
			'tracks': [],
			'chips': [],
			'continuation': None,
			'title': '',
			'related_browse_id': None,
			'lyrics_browse_id': None
		}

	queue_content = None
	for tab in tabs:
		tab_renderer = tab.get('tabRenderer', {})
		if 'content' in tab_renderer and 'musicQueueRenderer' in tab_renderer['content']:
			queue_content = tab_renderer['content']['musicQueueRenderer']
		endpoint = tab_renderer.get('endpoint', {}).get('browseEndpoint', {})
		music_config = endpoint.get('browseEndpointContextSupportedConfigs', {}).get('browseEndpointContextMusicConfig', {})
		page_type = music_config.get('pageType', '')
		if page_type == 'MUSIC_PAGE_TYPE_TRACK_RELATED' or tab_renderer.get('title') == 'Related':
			related_browse_id = endpoint.get('browseId')
		elif page_type == 'MUSIC_PAGE_TYPE_TRACK_LYRICS' or tab_renderer.get('title') == 'Lyrics':
			lyrics_browse_id = endpoint.get('browseId')

	if queue_content:
		queue_header = queue_content.get('header', {}).get('musicQueueHeaderRenderer', {})
		subtitle_runs = queue_header.get('subtitle', {}).get('runs', [])
		if subtitle_runs:
			queue_title = subtitle_runs[0].get('text', '')

		raw_chips = queue_content.get('subHeaderChipCloud', {}).get('chipCloudRenderer', {}).get('chips', [])
		for c in raw_chips:
			rc = c.get('chipCloudChipRenderer', {})
			text_runs = rc.get('text', {}).get('runs', [])
			text = text_runs[0].get('text', '') if text_runs else ''
			is_selected = rc.get('isSelected', False)
			nav_endpoint = rc.get('navigationEndpoint', {})
			watch_ep = nav_endpoint.get('watchEndpoint') or nav_endpoint.get('queueUpdateCommand', {}).get('fetchContentsCommand', {}).get('watchEndpoint', {})
			chip_params = watch_ep.get('params', '')
			chip_playlist_id = watch_ep.get('playlistId', '')
			if text:
				chips.append({
					'title': text,
					'params': chip_params,
					'playlist_id': chip_playlist_id,
					'is_selected': is_selected
				})

		panel = queue_content.get('content', {}).get('playlistPanelRenderer', {})
		for item in panel.get('contents', []):
			if 'playlistPanelVideoRenderer' in item:
				if song := _parse_watch_track(item['playlistPanelVideoRenderer']):
					tracks.append(song)

		conts = panel.get('continuations', [])
		if conts:
			next_continuation = conts[0].get('nextRadioContinuationData', {}).get('continuation') or \
								conts[0].get('nextContinuationData', {}).get('continuation')

	return {
		'tracks': tracks,
		'chips': chips,
		'continuation': next_continuation,
		'title': queue_title,
		'related_browse_id': related_browse_id,
		'lyrics_browse_id': lyrics_browse_id
	}


def get_radio(
	seed_song: Song | None = None,
	seed_group: Group | None = None,
	seed_artist: Artist | None = None,
	params: str | None = None,
	continuation: str | None = None,
	playlist_id: str | None = None
) -> dict:
	'''Start or continue a radio station based on a song, artist, playlist, or chip filter.

	Inspired by Vivi Music's YouTubeQueue radio implementation.

	:param seed_song: Seed song.
	:param seed_group: Seed playlist or album group.
	:param seed_artist: Seed artist.
	:param params: Optional radio chip filter parameter (e.g. Discover, Popular).
	:param continuation: Optional continuation token for infinite loading.
	:param playlist_id: Explicit radio playlist ID if known.
	:return: dict with 'tracks', 'chips', 'continuation', 'title'.
	'''
	video_id = None
	resolved_playlist_id = playlist_id
	title = 'Radio'

	if continuation:
		return get_watch_next(continuation=continuation)

	if seed_song and seed_song.yt_id:
		video_id = seed_song.yt_id
		if not resolved_playlist_id:
			resolved_playlist_id = f'RDAMVM{seed_song.yt_id}'
		title = f'Radio - {seed_song.title}'
	elif seed_artist and seed_artist.yt_id:
		title = f'Radio - {seed_artist.name}'
		if not resolved_playlist_id:
			if getattr(seed_artist, 'radio_id', None):
				resolved_playlist_id = seed_artist.radio_id
			else:
				try:
					yt = get_yt_client(unauth=True)
					data = yt.get_artist(seed_artist.yt_id)
					resolved_playlist_id = data.get('radioId')
				except Exception:
					pass
				if not resolved_playlist_id:
					resolved_playlist_id = f'RDEM{seed_artist.yt_id[2:] if seed_artist.yt_id.startswith("UC") else seed_artist.yt_id}'
	elif seed_group and seed_group.yt_id:
		title = f'Radio - {seed_group.title}'
		if not resolved_playlist_id:
			pl = seed_group.yt_id
			if pl.startswith('VL'):
				pl = pl[2:]
			if not pl.startswith('RD'):
				resolved_playlist_id = f'RDAMPL{pl}'
			else:
				resolved_playlist_id = pl

	res = get_watch_next(
		video_id=video_id,
		playlist_id=resolved_playlist_id,
		radio=True,
		params=params
	)
	if not res.get('title') and title:
		res['title'] = title
	return res


def get_search_suggestions(query: str) -> dict:
	'''Get search suggestions from YouTube Music.

	Returns both text query completions and direct matching items (artists, songs, playlists, albums).

	:param query: Query string typed by the user.
	:return: dict with 'queries' (list[str]) and 'items' (list[dict]).
	'''
	if not query or not query.strip():
		return {'queries': [], 'items': []}

	yt = get_yt_client(unauth=True)
	try:
		res = yt._send_request('music/get_search_suggestions', {'input': query.strip()})
	except Exception as e:
		logboth.warning(__name__, f'Failed to get search suggestions: {e}')
		return {'queries': [], 'items': []}

	contents = res.get('contents', [])
	queries = []
	items = []

	if len(contents) > 0:
		for c in contents[0].get('searchSuggestionsSectionRenderer', {}).get('contents', []):
			runs = c.get('searchSuggestionRenderer', {}).get('suggestion', {}).get('runs', [])
			q = ''.join(r.get('text', '') for r in runs)
			if q and q not in queries:
				queries.append(q)

	if len(contents) > 1:
		for c in contents[1].get('searchSuggestionsSectionRenderer', {}).get('contents', []):
			mr = c.get('musicResponsiveListItemRenderer', {})
			if not mr:
				continue
			col0_runs = mr.get('flexColumns', [{}])[0].get('musicResponsiveListItemFlexColumnRenderer', {}).get('text', {}).get('runs', [])
			title = col0_runs[0].get('text', '') if col0_runs else ''
			col1_runs = mr.get('flexColumns', [{}, {}])[1].get('musicResponsiveListItemFlexColumnRenderer', {}).get('text', {}).get('runs', [])
			subtitle = ''.join(r.get('text', '') for r in col1_runs)

			thumbs = mr.get('thumbnail', {}).get('musicThumbnailRenderer', {}).get('thumbnail', {}).get('thumbnails', [])
			thumbnail = thumbs[-1].get('url', '') if thumbs else ''

			nav = mr.get('navigationEndpoint', {})
			page_type = nav.get('browseEndpoint', {}).get('browseEndpointContextSupportedConfigs', {}).get('browseEndpointContextMusicConfig', {}).get('pageType', '')
			browse_id = nav.get('browseEndpoint', {}).get('browseId', '')
			video_id = mr.get('playlistItemData', {}).get('videoId', '') or nav.get('watchEndpoint', {}).get('videoId', '')

			if page_type == 'MUSIC_PAGE_TYPE_ARTIST':
				item = Artist(name=title, yt_id=browse_id)
				item_type = 'artist'
			elif page_type in ('MUSIC_PAGE_TYPE_ALBUM', 'MUSIC_PAGE_TYPE_AUDIOBOOK'):
				item = Group(title=title, yt_id=browse_id)
				item_type = 'album'
			elif page_type == 'MUSIC_PAGE_TYPE_PLAYLIST':
				item = Group(title=title, yt_id=browse_id)
				item_type = 'playlist'
			elif video_id:
				author_name = ''
				if ' • ' in subtitle:
					parts = subtitle.split(' • ')
					if len(parts) > 1:
						author_name = parts[1]
				item = Song(
					title=title,
					author=Artist(name=author_name or subtitle),
					thumbnail=thumbnail,
					yt_id=video_id
				)
				item_type = 'song'
			else:
				continue

			items.append({
				'type': item_type,
				'title': title,
				'subtitle': subtitle,
				'thumbnail': thumbnail,
				'item': item
			})

	return {'queries': queries, 'items': items}


def get_related(video_id: str) -> dict:
	'''Get related content for a song (similar songs, playlists, artists).

	:param video_id: YouTube video ID of the song.
	:return: dict with 'songs', 'artists', 'playlists', 'description'.
	'''
	yt = get_yt_client(unauth=True)
	watch_res = get_watch_next(video_id=video_id)
	related_browse_id = watch_res.get('related_browse_id')
	if not related_browse_id:
		return {'songs': [], 'artists': [], 'playlists': [], 'description': ''}

	try:
		sections = yt.get_song_related(related_browse_id)
	except Exception as e:
		logboth.error(__name__, f'Failed to get related content: {e}')
		return {'songs': [], 'artists': [], 'playlists': [], 'description': ''}

	songs = []
	artists = []
	playlists = []
	description = ''

	for section in sections:
		title = section.get('title', '').lower()
		contents = section.get('contents', [])
		if isinstance(contents, str):
			if 'about' in title:
				description = contents
			continue

		for item in contents:
			if not isinstance(item, dict):
				continue
			if 'videoId' in item:
				s_artist = item.get('artists', [{}])[0] if item.get('artists') else {}
				thumbs = item.get('thumbnails', [])
				songs.append(Song(
					title=item.get('title', ''),
					author=Artist(name=s_artist.get('name', ''), yt_id=s_artist.get('id', '')),
					thumbnail=thumbs[-1].get('url', '') if thumbs else '',
					yt_id=item.get('videoId', '')
				))
			elif 'subscribers' in item or ('browseId' in item and item.get('browseId', '').startswith('UC')):
				artists.append(Artist(
					name=item.get('title', ''),
					yt_id=item.get('browseId', '')
				))
			elif 'playlistId' in item or 'browseId' in item:
				pl_id = item.get('playlistId', '') or item.get('browseId', '')
				playlists.append(Group(
					title=item.get('title', ''),
					yt_id=pl_id
				))

	return {'songs': songs, 'artists': artists, 'playlists': playlists, 'description': description}


def get_similar_songs(song: Song, ignore: Group | None=None) -> Group | None:
	'''Get group of songs similar to a song.

	:param song: Song.
	:param ignore: Group of songs to ignore while searching.
	:return: Group of similar songs, if found.
	'''
	logboth.info(
		__name__,
		f'Getting similar songs to "{song.yt_id}" ignoring '
		f'{len(ignore.songs) if ignore else 0} songs...'
	)
	ignore = ignore or Group()

	res = get_watch_next(video_id=song.yt_id, radio=True)
	data = res.get('tracks', [])

	available_songs = []
	for s in data:
		for ignore_song in ignore.songs:
			if ignore_song.yt_id == s.yt_id:
				break
		else:
			available_songs.append(s)

	if available_songs:
		logboth.info(__name__, f'Got {len(available_songs)} similar songs')
		return Group(songs=available_songs)

	logboth.error(__name__, 'Failed to get similar songs - no songs available')
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


def _get_playlist_v3(yt_id: str) -> Group | None:
	'''Fetch a user playlist and its tracks using YouTube Data API v3.'''
	if not is_authenticated() or not yt_id or yt_id in ('LM', 'FEmusic_liked_videos'):
		return None
	headers = _get_oauth_headers()
	if not headers:
		return None
	try:
		clean_pid = yt_id.removeprefix('VL')
		# Fetch playlist snippet to get the title
		title = clean_pid
		pr = requests.get(
			f'https://www.googleapis.com/youtube/v3/playlists?part=snippet&id={clean_pid}',
			headers=headers,
			timeout=10
		)
		if pr.status_code == 200:
			items = pr.json().get('items', [])
			if items:
				title = items[0].get('snippet', {}).get('title', clean_pid)

		songs = []
		page_token = ''
		while True:
			url = f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={clean_pid}&maxResults=50'
			if page_token:
				url += f'&pageToken={page_token}'
			r = requests.get(url, headers=headers, timeout=10)
			if r.status_code != 200:
				break
			data = r.json()
			for it in data.get('items', []):
				snippet = it.get('snippet', {})
				vid = snippet.get('resourceId', {}).get('videoId')
				if not vid:
					continue
				s_title = snippet.get('title', '')
				channel = snippet.get('videoOwnerChannelTitle', '') or snippet.get('channelTitle', '')
				thumbs = snippet.get('thumbnails', {})
				thumb = thumbs.get('high', {}).get('url') or thumbs.get('default', {}).get('url', '')
				songs.append(Song(title=s_title, author=Artist(name=channel), thumbnail=thumb, yt_id=vid))
			page_token = data.get('nextPageToken')
			if not page_token:
				break
		if songs:
			return Group(title=title, songs=songs, yt_id=yt_id)
	except Exception as e:
		logboth.warning(__name__, f'YouTube Data API v3 playlist fetch failed for "{yt_id}": {e}')
	return None


def _parse_playlist_dict(yt_id: str, data: dict) -> Group | None:
	if not data or not isinstance(data, dict):
		return None
	title = data.get('title', '')
	author_name = ''
	artists = data.get('artists', [])
	if artists and isinstance(artists, list):
		author_name = artists[0].get('name', '')
	elif isinstance(data.get('author'), str):
		author_name = data['author']
	elif isinstance(data.get('author'), dict):
		author_name = data['author'].get('name', '')

	songs = []
	for t in data.get('tracks', []):
		if not t or not isinstance(t, dict):
			continue
		vid = t.get('videoId') or t.get('id', '')
		if not vid:
			continue
		t_title = t.get('title', '') or vid
		artist_name = ''
		t_artists = t.get('artists', [])
		if t_artists and isinstance(t_artists, list):
			artist_name = t_artists[0].get('name', '')
		elif isinstance(t.get('byline'), str):
			artist_name = t['byline']

		length = t.get('duration', '') or t.get('length', '')
		thumb = ''
		thumbnails = t.get('thumbnails', [])
		if thumbnails and isinstance(thumbnails, list):
			thumb = thumbnails[-1].get('url', '')
		thumb = cache.get_high_res_thumbnail_url(thumb)

		songs.append(Song(
			title=t_title,
			author=Artist(name=artist_name),
			length=length,
			thumbnail=thumb,
			yt_id=vid
		))

	if songs:
		return Group(title=title, author=Artist(name=author_name), songs=songs, yt_id=yt_id)
	return None


def get_album_or_playlist(yt_id: str) -> Group | None:
	'''Get group from YT ID.

	:param yt_id: YT ID of album or playlist.
	:return: Group, if found.
	'''
	logboth.info(__name__, f'Getting album/playlist "{yt_id}"...')

	# 1. For special private library playlist 'LM', handle directly via authenticated TVHTML5
	if yt_id == 'LM' or yt_id.startswith('FEmusic_'):
		if is_authenticated():
			if tv_group := _get_playlist_tv(yt_id):
				logboth.info(__name__, f'Got album/playlist "{yt_id}" via TVHTML5 ({len(tv_group.songs)} songs)')
				return tv_group

	# 2. If it's an album browseId, fetch via get_album directly
	if yt_id.startswith('MPREb'):
		try:
			unauth = get_yt_client(unauth=True)
			album_data = unauth.get_album(yt_id)
			parsed_group = _parse_playlist_dict(yt_id, album_data)
			if parsed_group and parsed_group.songs:
				logboth.info(__name__, f'Got album "{yt_id}" via get_album ({len(parsed_group.songs)} songs)')
				return parsed_group
		except Exception as e:
			logboth.warning(__name__, f'get_album failed for "{yt_id}": {e}')

	# 3. Try unauthenticated WEB_REMIX client (vivi-music style: gets all tracks without OAuth HTTP 400 or 15-song TV limits)
	try:
		unauth = get_yt_client(unauth=True)
		pl_data = unauth.get_playlist(yt_id, limit=None)
		parsed_group = _parse_playlist_dict(yt_id, pl_data)
		if parsed_group and parsed_group.songs:
			logboth.info(__name__, f'Got album/playlist "{yt_id}" via WEB_REMIX ({len(parsed_group.songs)} songs)')
			return parsed_group
	except Exception as e:
		logboth.warning(__name__, f'Unauthenticated get_playlist failed for "{yt_id}": {e}')

	# 4. For authenticated users, try YouTube Data API v3 then TVHTML5
	if is_authenticated():
		if v3_group := _get_playlist_v3(yt_id):
			logboth.info(__name__, f'Got album/playlist "{yt_id}" via YouTube Data API v3 ({len(v3_group.songs)} songs)')
			return v3_group

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

	is_user_priority = True


	def _function(
		self, yt: ytmusicapi.YTMusic, data: list[dict], limit: int | None=None, load_tracks: bool = False
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

			try:
				parsed = _parse_single_result(yt, item, load_tracks=load_tracks)
			except Exception as e:
				logboth.warning(__name__, f'Failed to parse search result item {i}: {e}')
				parsed = None

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


def get_home_feeds(limit: int = 4) -> list[dict]:
	'''Get personalized or trending home feed sections from YouTube Music.

	:param limit: Number of sections to retrieve.
	:return: List of dicts with 'title' and 'items' (list of Song or Group).
	'''
	yt = get_yt_client()
	try:
		sections = yt.get_home(limit=limit)
	except Exception as e:
		logboth.warning(__name__, f'Failed to fetch home feeds ({e}), using unauthenticated client')
		try:
			unauth = get_yt_client(unauth=True)
			sections = unauth.get_home(limit=limit)
		except Exception as err:
			logboth.error(__name__, f'Failed to fetch home feeds: {err}')
			return []

	parsed_sections = []
	for sec in sections:
		sec_title = sec.get('title', '')
		parsed_items = []
		for item in sec.get('contents', []):
			if 'videoId' in item:
				artists = item.get('artists', [])
				art_name = artists[0].get('name', '') if artists and isinstance(artists, list) else ''
				art_id = artists[0].get('id', '') if artists and isinstance(artists, list) else ''
				thumbs = item.get('thumbnails', [])
				thumb = thumbs[-1].get('url', '') if thumbs else ''
				parsed_items.append(
					Song(
						title=item.get('title', ''),
						yt_id=item.get('videoId', ''),
						author=Artist(name=art_name, yt_id=art_id),
						thumbnail=thumb
					)
				)
			elif 'audioPlaylistId' in item or 'playlistId' in item or 'browseId' in item:
				gid = item.get('audioPlaylistId') or item.get('playlistId') or item.get('browseId')
				artists = item.get('artists', [])
				art_name = artists[0].get('name', '') if artists and isinstance(artists, list) else (item.get('description') or '')
				thumbs = item.get('thumbnails', [])
				thumb = thumbs[-1].get('url', '') if thumbs else ''
				grp = Group(
					title=item.get('title', ''),
					yt_id=gid,
					author=Artist(name=art_name),
					songs=[]
				)
				grp.thumbnail = thumb
				parsed_items.append(grp)
		if parsed_items:
			parsed_sections.append({'title': sec_title, 'items': parsed_items})

	logboth.info(__name__, f'Retrieved {len(parsed_sections)} home feed sections')
	return parsed_sections


class GetHomeFeedsTask(Task):
	'''Task for fetching YouTube Music home feeds.'''

	def _function(self, limit: int = 4) -> list[dict]:
		logboth.info(__name__, 'Fetching home feeds task started...')
		return get_home_feeds(limit)


def get_lyrics(
	video_id: str,
	title: str | None = None,
	artist: str | None = None
) -> dict | None:
	'''Fetch lyrics for a song from YouTube Music.

	:param video_id: YouTube video/song ID.
	:param title: Song title (used for fallback matching if needed).
	:param artist: Artist name (used for fallback matching if needed).
	:return: dict with 'lyrics' (str) and optional 'source' (str), or None.
	'''
	if not video_id:
		return None

	client = get_yt_client(unauth=True)
	# 1. Try watch next endpoint directly
	try:
		next_data = get_watch_next(video_id=video_id)
		l_id = next_data.get('lyrics_browse_id')
		if l_id:
			l = client.get_lyrics(l_id)
			if l and l.get('lyrics'):
				logboth.info(__name__, f'Retrieved lyrics for "{video_id}"')
				return l
	except Exception as e:
		logboth.warning(__name__, f'Failed to get lyrics for "{video_id}" via watch_next: {e}')

	# 2. Fallback: Search official song track on YouTube Music
	search_q = f'{title or ""} {artist or ""}'.strip()
	if search_q:
		try:
			results = client.search(search_q, filter='songs')
			if results:
				candidate_id = results[0].get('videoId')
				if candidate_id and candidate_id != video_id:
					candidate_next = get_watch_next(video_id=candidate_id)
					candidate_lid = candidate_next.get('lyrics_browse_id')
					if candidate_lid:
						l = client.get_lyrics(candidate_lid)
						if l and l.get('lyrics'):
							logboth.info(__name__, f'Retrieved lyrics for "{video_id}" via fallback search "{candidate_id}"')
							return l
		except Exception as err:
			logboth.warning(__name__, f'Failed to get lyrics via fallback search for "{search_q}": {err}')

	return None


class GetLyricsTask(Task):
	'''Task for asynchronously retrieving song lyrics.'''

	def _function(
		self,
		video_id: str,
		title: str | None = None,
		artist: str | None = None
	) -> dict | None:
		logboth.info(__name__, f'Fetching lyrics for video_id="{video_id}"...')
		return get_lyrics(video_id, title, artist)


_SEARCH_CACHE_TTL = 300
_search_cache: dict[str, tuple[float, list[SearchResult]]] = {}


def _get_cached_search(key: str) -> list[SearchResult] | None:
	if key in _search_cache:
		timestamp, results = _search_cache[key]
		if time.time() - timestamp < _SEARCH_CACHE_TTL:
			return results
		del _search_cache[key]
	return None


def _set_cached_search(key: str, results: list[SearchResult]):
	if len(_search_cache) > 50:
		oldest = min(_search_cache.keys(), key=lambda k: _search_cache[k][0])
		del _search_cache[oldest]
	_search_cache[key] = (time.time(), results)


class SearchTask(Task):
	'''Task for searching YT.

	.. code-block::

		SearchTask(
			args=(query, type_filter, limit)
		)

	'''

	is_user_priority = True

	def _on_parse_progress_update(self, task: ParseResultsTask, progress: float):
		if not task.is_canceled():
			self._update_progress(0.5 + progress / 2)

	def _function(
		self, query: str, filter_: str='', limit: int | None=None
	) -> list[SearchResult] | None:
		cache_key = f"{query.strip().lower()}:{filter_}:{limit}"
		cached = _get_cached_search(cache_key)
		if cached is not None:
			logboth.info(__name__, f'Returning cached search results for "{query}"')
			self._update_progress(1.0)
			return cached

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
			search_limit = limit if limit is not None else (30 if filter_ else None)
			while True:
				try:
					data = (
						yt.search(query, filter=filter_, limit=search_limit) if filter_
							else yt.search(query)
					)
				except Exception as e:
					logboth.warning(__name__, f'Search call failed ({e}), using unauthenticated fallback')
					unauth_yt = get_yt_client(unauth=True)
					data = (
						unauth_yt.search(query, filter=filter_, limit=search_limit) if filter_
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
			args=(yt, data, limit, False)
		)
		parse_task.start()
		while parse_task.is_running():
			time.sleep(0.05)
			if self.is_canceled():
				parse_task.cancel()
				logboth.info(__name__, 'Canceled search')
				return None

		if parse_task.result is not None:
			_set_cached_search(cache_key, parse_task.result)
			time.sleep(0.05)
			logboth.info(__name__, 'Done searching')
			return parse_task.result

		logboth.error(__name__, 'Failed to search')
		return None


class StartRadioTask(Task):
	'''Task for fetching a radio queue from YouTube.

	Inspired by Vivi Music's YouTubeQueue.radio implementation.

	.. code-block::

		StartRadioTask(
			args=(seed_item, params, continuation, playlist_id)
		)

	'''

	is_user_priority = True

	def _function(
		self,
		seed_item: Song | Group | Artist | None = None,
		params: str | None = None,
		continuation: str | None = None,
		playlist_id: str | None = None
	) -> dict | None:
		logboth.info(__name__, f'Starting radio task for {seed_item} (params={params})...')
		self._update_progress(0.1)

		if self.is_canceled():
			return None

		seed_song = seed_item if isinstance(seed_item, Song) else None
		seed_group = seed_item if isinstance(seed_item, Group) else None
		seed_artist = seed_item if isinstance(seed_item, Artist) else None

		self._update_progress(0.3)
		result = get_radio(
			seed_song=seed_song,
			seed_group=seed_group,
			seed_artist=seed_artist,
			params=params,
			continuation=continuation,
			playlist_id=playlist_id
		)

		if self.is_canceled():
			return None

		self._update_progress(1.0)
		logboth.info(__name__, f'Radio task completed: {len(result.get("tracks", []))} tracks, {len(result.get("chips", []))} chips')
		return result


class GetSearchSuggestionsTask(Task):
	'''Task for fetching search suggestions as user types.

	Inspired by Vivi Music's searchSuggestions implementation.

	.. code-block::

		GetSearchSuggestionsTask(
			args=(query,)
		)

	'''

	is_user_priority = True

	def _function(self, query: str) -> dict | None:
		if self.is_canceled():
			return None

		return get_search_suggestions(query)


class GetRelatedTask(Task):
	'''Task for fetching related content for a song (similar tracks, artists, playlists).

	Inspired by Vivi Music's related implementation.

	.. code-block::

		GetRelatedTask(
			args=(video_id,)
		)

	'''

	is_user_priority = True

	def _function(self, video_id: str) -> dict | None:
		if self.is_canceled():
			return None

		return get_related(video_id)

