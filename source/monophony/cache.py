'''Audio caching management module.'''

import os
import shutil
import subprocess

from monophony import NAME, settings
from monophony.data import Song

import logboth


def get_cache_dir() -> str:
	'''Get path to audio cache directory.

	:return: Cache directory path.
	'''
	base_cache = os.getenv('XDG_CACHE_HOME', os.path.expanduser('~/.cache'))
	return os.path.join(base_cache, NAME, 'audio_cache')


def _get_uri_cache_file() -> str:
	base_cache = os.getenv('XDG_CACHE_HOME', os.path.expanduser('~/.cache'))
	return os.path.join(base_cache, NAME, 'uri_cache.json')


def get_cached_uri(yt_id: str) -> str | None:
	'''Get cached streaming URI if valid and not expired.

	:param yt_id: YouTube song ID.
	:return: Streaming URI if valid, else None.
	'''
	cache_file = _get_uri_cache_file()
	if not os.path.exists(cache_file):
		return None
	try:
		import json, time
		with open(cache_file, encoding='utf-8') as f:
			data = json.load(f)
		entry = data.get(yt_id)
		if entry and isinstance(entry, dict):
			# YouTube URIs expire after ~6 hours (21600s), use 4 hour safety margin
			if time.time() - entry.get('timestamp', 0) < 14400:
				return entry.get('uri')
	except Exception:
		pass
	return None


def save_cached_uri(yt_id: str, uri: str):
	'''Save streaming URI to cache.

	:param yt_id: YouTube song ID.
	:param uri: Streaming URI.
	'''
	if not yt_id or not uri or uri == '[nonexistent]':
		return
	cache_file = _get_uri_cache_file()
	try:
		import json, time
		os.makedirs(os.path.dirname(cache_file), exist_ok=True)
		data = {}
		if os.path.exists(cache_file):
			try:
				with open(cache_file, encoding='utf-8') as f:
					data = json.load(f)
			except Exception:
				data = {}
		data[yt_id] = {'uri': uri, 'timestamp': time.time()}
		with open(cache_file, 'w', encoding='utf-8') as f:
			json.dump(data, f, indent=True)
	except Exception as e:
		logboth.error(__name__, f'Failed to save URI cache: {e}')



def get_cached_file(song: Song) -> str | None:
	'''Get cached audio file path if song is cached.

	:param song: Song to check.
	:return: Absolute file path if cached, else None.
	'''
	if not song or not song.yt_id:
		return None
	dest_dir = get_cache_dir()
	for ext in ('.m4a', '.opus', '.mp3', '.webm'):
		path = os.path.join(dest_dir, f'{song.yt_id}{ext}')
		if os.path.exists(path) and os.path.getsize(path) > 0:
			return path
	return None


def is_cached(song: Song) -> bool:
	'''Check if song audio is cached.

	:param song: Song to check.
	:return: True if cached.
	'''
	return bool(get_cached_file(song))


def get_cache_size() -> int:
	'''Get total byte size of audio cache directory.

	:return: Size in bytes.
	'''
	cache_dir = get_cache_dir()
	if not os.path.exists(cache_dir):
		return 0
	total_bytes = 0
	for root, _dirs, files in os.walk(cache_dir):
		for f in files:
			fp = os.path.join(root, f)
			if os.path.isfile(fp):
				total_bytes += os.path.getsize(fp)
	return total_bytes


def get_cache_size_mb() -> float:
	'''Get total size of audio cache in Megabytes (MB).

	:return: Size in MB.
	'''
	return get_cache_size() / (1024 * 1024)


def clear_cache() -> bool:
	'''Delete all cached audio files.

	:return: True if successful.
	'''
	cache_dir = get_cache_dir()
	if os.path.exists(cache_dir):
		try:
			shutil.rmtree(cache_dir)
			os.makedirs(cache_dir, exist_ok=True)
			logboth.info(__name__, 'Cleared audio cache')
			return True
		except OSError as e:
			logboth.error(__name__, f'Failed to clear cache: {e}')
			return False
	return True


def enforce_cache_limits():
	'''Enforce maximum cache size limit by deleting oldest cached files (LRU).'''
	if not settings.load('cache_enabled', True):
		return

	max_mb = settings.load('cache_max_size_mb', 1000)
	max_bytes = max_mb * 1024 * 1024

	cache_dir = get_cache_dir()
	if not os.path.exists(cache_dir):
		return

	files_info = []
	total_size = 0
	for f in os.listdir(cache_dir):
		fp = os.path.join(cache_dir, f)
		if os.path.isfile(fp):
			size = os.path.getsize(fp)
			mtime = os.path.getmtime(fp)
			files_info.append((mtime, fp, size))
			total_size += size

	if total_size <= max_bytes:
		return

	# Sort by modification time ascending (oldest first)
	files_info.sort(key=lambda x: x[0])

	for _mtime, fp, size in files_info:
		if total_size <= max_bytes:
			break
		try:
			os.remove(fp)
			total_size -= size
			logboth.info(__name__, f'Cache cleanup: removed old cache file {os.path.basename(fp)}')
		except OSError:
			pass


def cache_song(song: Song) -> str | None:
	'''Download and cache audio for a song.

	:param song: Song to cache.
	:return: Path to cached file if successful, else None.
	'''
	if not settings.load('cache_enabled', True) or not song or not song.yt_id:
		return None

	existing = get_cached_file(song)
	if existing:
		try:
			os.utime(existing, None)
		except OSError:
			pass
		return existing

	dest_dir = get_cache_dir()
	os.makedirs(dest_dir, exist_ok=True)
	target_pattern = os.path.join(dest_dir, f'{song.yt_id}.%(ext)s')

	logboth.info(__name__, f'Caching song "{song.yt_id}" ({song.title})...')
	try:
		_out, err = subprocess.Popen(
			[
				'yt-dlp',
				'-f', 'bestaudio/best',
				'--output', target_pattern,
				'--quiet',
				'--no-warnings',
				f'https://music.youtube.com/watch?v={song.yt_id}'
			],
			text=True,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE
		).communicate()

		if err:
			logboth.warning(__name__, f'yt-dlp cache warning/error for "{song.yt_id}": {err}')

		if cached_path := get_cached_file(song):
			logboth.info(__name__, f'Successfully cached song "{song.yt_id}" ({os.path.getsize(cached_path)} bytes)')
			enforce_cache_limits()
			return cached_path

		logboth.error(__name__, f'Failed to cache song "{song.yt_id}": output file missing or empty')
		return None
	except Exception as e:
		logboth.error(__name__, f'Exception caching song "{song.yt_id}": {e}')
		return None

