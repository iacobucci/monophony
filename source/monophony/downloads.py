'''Download functionality and downloaded song management.'''

import contextlib
import glob
import json
import os
import subprocess
import traceback

from monophony import NAME, get_user_config_dir
from monophony.asynchronous import Task, wait_if_user_priority

from monophony.data import Artist, Group, Song

import logboth
from gi.repository import GLib


def get_directory() -> str:
	'''Get downloaded song storage directory.

	:return: Directory path.
	'''
	return os.getenv(
		'XDG_DATA_HOME', os.path.expanduser('~/.local/share')
	) + f'/{NAME}/'


def get_temp_directory() -> str:
	'''Get working directory used for downloads.

	:return: Directory path.
	'''
	return os.getenv('XDG_RUNTIME_DIR', '/var/tmp') + f'/{NAME}/downloads/'


def get_file(song: Song) -> str | None:
	'''Get downloaded song path, if any.

	:return: Song file path.
	'''
	files = [
		file for file in glob.glob(get_directory() + '*' + song.yt_id + '*')
		if not file.endswith('.' + NAME)
	]

	if files:
		if len(files) > 1:
			logboth.warning(
				__name__,
				f'Multiple song files match id "{song.yt_id}"', '\n'.join(files)
			)
		return files[0]

	return None


def is_being_downloaded(song: Song) -> bool:
	'''Check if song is currently being downloaded.

	:return: Download state.
	'''
	return os.path.exists(get_directory() + song.yt_id + '.' + NAME)


def is_downloaded(song: Song) -> bool:
	'''Check if song has finished downloading.

	:return: Downloaded state.
	'''
	return (
		song.yt_id and get_file(song) and not is_being_downloaded(song)
	)


def resolve_song_metadata(song: Song) -> Song:
	'''Try to resolve title and author for a song with empty metadata.'''
	if song.title and song.author.name:
		return song

	file = get_file(song)
	if file:
		basename = os.path.splitext(os.path.basename(file))[0]
		parts = basename.rsplit('_', 1)
		if len(parts) == 2:
			title_author = parts[0]
			if '_-_' in title_author:
				t, a = title_author.rsplit('_-_', 1)
				if not song.title:
					song.title = t.replace('_', ' ')
				if not song.author.name:
					song.author = Artist(name=a.replace('_', ' '))
			elif not song.title:
				song.title = title_author.replace('_', ' ')

	if not song.title or not song.author.name:
		try:
			from monophony import playlists
			all_playlists = playlists.read()
			for pl in all_playlists.values():
				for s in pl.songs:
					if s.yt_id == song.yt_id:
						song.title = song.title or s.title
						if not song.author.name:
							song.author = s.author
						song.length = song.length or s.length
						song.thumbnail = song.thumbnail or s.thumbnail
						return song
		except Exception:
			pass

	return song


def get_missing_mandatory_songs(downloader: '_Downloader') -> list[Song]:
	'''Get list of songs specified in downloads.json that are missing locally.'''
	downloader.lock.lock()
	try:
		songs = downloader.read().songs
	finally:
		downloader.lock.unlock()

	return [
		song for song in songs
		if not is_downloaded(song) and not is_being_downloaded(song)
	]


class DownloadTask(Task):
	'''Task for downloading any number of songs.

	.. code-block::

		DownloadTask(
			args=(
				monophony.downloads.downloader,
				monophony.data.Group()
			)
		)

	'''

	def _function(self, downloader: '_Downloader', group: Group) -> bool:
		downloader.lock.lock()
		logboth.info(__name__, f'Downloading {len(group.songs)} songs...')

		path = get_directory()
		needed_songs: list[Song] = []
		for song in group.songs:
			if not song.yt_id:
				logboth.error(
					__name__, f'Failed to download song "{song.title}" - no id'
				)
				continue

			if is_downloaded(song) or is_being_downloaded(song):
				logboth.info(
					__name__,
					f'Skipped download of song "{song.yt_id}" - already taken care of'
				)
				continue

			downloader.create_lock_file(song.yt_id)
			needed_songs.append(song)

		# *.NAME files act as locks for this part
		self._update_progress()
		downloader.lock.unlock()

		if not needed_songs:
			logboth.info(
				__name__, 'Canceled download as there are no songs to download'
			)
			return True

		success_count = 0
		all_succeeded = True
		total = len(needed_songs)

		try:
			for idx, song in enumerate(needed_songs, start=1):
				if self.is_canceled():
					logboth.info(__name__, 'Download canceled by user')
					all_succeeded = False
					break

				wait_if_user_priority()

				song_url = f'https://music.youtube.com/watch?v={song.yt_id}'
				logboth.info(
					__name__,
					f'[{idx}/{total}] Downloading song "{song.title or song.yt_id}" ({song.yt_id})...'
				)

				result = subprocess.run(
					[
						'yt-dlp',
						'--extract-audio',
						'--no-cache-dir',
						'--audio-quality',
						'0',
						'--add-metadata',
						'--paths',
						'home:' + path,
						'--paths',
						'temp:' + get_temp_directory(),
						'--restrict-filenames',
						'--output',
						'%(title)s_-_%(creators)s_%(id)s.%(ext)s',
						song_url
					],
					text=True,
					capture_output=True
				)

				downloader.lock.lock()
				downloader.delete_lock_file(song.yt_id)

				if result.returncode != 0:
					all_succeeded = False
					logboth.error(
						__name__,
						f'Failed to download song "{song.title or song.yt_id}" ({song.yt_id})',
						(result.stdout or '') + (result.stderr or '')
					)
				elif is_downloaded(song):
					success_count += 1
					resolve_song_metadata(song)
					logboth.info(
						__name__,
						f'[{idx}/{total}] Successfully downloaded "{song.title or song.yt_id}"'
					)
					downloader.write(
						Group(songs=[song] + downloader.read().songs)
					)

				self._update_progress()
				downloader.lock.unlock()
		finally:
			downloader.lock.lock()
			for song in needed_songs:
				if is_being_downloaded(song):
					downloader.delete_lock_file(song.yt_id)
			downloader.lock.unlock()
			self._update_progress()

		logboth.info(
			__name__, f'Downloaded {success_count}/{total} songs'
		)
		return all_succeeded


class _Downloader:
	def __init__(self):
		self.lock = GLib.Mutex()

	def clean_up(self):
		self.lock.lock()
		logboth.info(__name__, 'Cleaning up downloads...')
		downloads_group = self.read()
		path = get_directory()
		os.makedirs(path, exist_ok=True)
		for file in os.listdir(path):
			if file.endswith(NAME):
				os.remove(path + file)
				logboth.info(__name__, f'Removed abandoned temp file "{file}"')
				continue

			yt_id = 'null'
			with contextlib.suppress(IndexError):
				yt_id = file.split('.')[-2][-11:]
			if Song(yt_id=yt_id) not in downloads_group.songs:
				os.remove(path + file)
				logboth.warning(__name__, f'Removed unexpected file "{file}"')

		logboth.info(__name__, 'Cleaned up downloads')
		self.lock.unlock()

	def create_lock_file(self, name: str):
		logboth.info(__name__, f'Creating lock file "{name}.{NAME}"...')

		# Always lock self.lock before calling this to prevent race conditions
		if self.lock.trylock():
			logboth.warning(
				__name__, 'Creating lock file while self.lock is unlocked'
			)
			self.lock.unlock()

		try:
			open(f'{get_directory()}{name}.{NAME}', 'w').close()
		except OSError:
			logboth.error(
				__name__, 'Failed to create lock file', traceback.format_exc()
			)
			return

		logboth.info(__name__, 'Created lock file')

	def delete_lock_file(self, name: str):
		logboth.info(__name__, f'Deleting lock file "{name}.{NAME}"...')

		# Always lock self.lock before calling this to prevent race conditions
		if self.lock.trylock():
			logboth.warning(
				__name__, 'Deleting lock file while self.lock is unlocked'
			)
			self.lock.unlock()

		try:
			os.remove(f'{get_directory()}{name}.{NAME}')
		except (OSError, FileNotFoundError):
			logboth.error(
				__name__,
				f'Failed to remove lock file "{name}.{NAME}"',
				traceback.format_exc()
			)

		logboth.info(__name__, 'Deleted lock file')

	def read(self) -> Group:
		# Always lock self.lock before calling this to prevent race conditions
		if self.lock.trylock():
			logboth.warning(__name__, 'Reading downloads while self.lock is unlocked')
			self.lock.unlock()

		songs_path = os.path.join(get_user_config_dir(), 'downloads.json')

		try:
			with open(songs_path) as songs_file:
				data = json.load(songs_file)
				if not isinstance(data, list):
					return Group()

				songs = []
				for item in data:
					if isinstance(item, str):
						yt_id = item.strip()
						title = ''
						author_name = ''
						author_id = ''
						length = ''
						thumbnail = ''
					elif isinstance(item, dict):
						yt_id = str(item.get('id') or item.get('yt_id', '')).strip()
						title = str(item.get('title', ''))
						author_name = str(item.get('author', ''))
						author_id = str(item.get('author_id', ''))
						length = str(item.get('length', ''))
						thumbnail = str(item.get('thumbnail', ''))
					else:
						continue

					if not yt_id:
						continue

					song = Song(
						title=title,
						author=Artist(
							name=author_name,
							yt_id=author_id
						),
						length=length,
						thumbnail=thumbnail,
						yt_id=yt_id
					)
					resolve_song_metadata(song)
					songs.append(song)

				return Group(songs=songs)
		except (OSError, json.decoder.JSONDecodeError):
			return Group()

	def write(self, group: Group):
		logboth.info(__name__, f'Writing {len(group.songs)} songs to downloads...')

		# Always lock self.lock before calling this to prevent race conditions
		if self.lock.trylock():
			logboth.warning(__name__, 'Writing downloads while self.lock is unlocked')
			self.lock.unlock()

		dir_path = get_user_config_dir()
		downloads_path = os.path.join(dir_path, 'downloads.json')

		os.makedirs(dir_path, exist_ok=True)
		with open(downloads_path, 'w') as downloads_file:
			json.dump(group.serialize()['contents'], downloads_file, indent='\t')

		logboth.info(__name__, 'Done writing to downloads')


	def get_downloads(self) -> Group:
		self.lock.lock()
		downloads = self.read()
		self.lock.unlock()
		return downloads

	def remove(self, song: Song):
		self.lock.lock()
		logboth.info(__name__, f'Removing song "{song.yt_id}" from downloads...')

		# No race conditions here as long as lock files are only created and
		# deleted while holding the lock
		if not is_downloaded(song):
			logboth.error(
				__name__, 'Failed remove song from downloads - not downloaded'
			)
			self.lock.unlock()
			return
		if is_being_downloaded(song):
			logboth.error(
				__name__, 'Failed remove song from downloads - download in progress'
			)
			self.lock.unlock()
			return

		self.write(
			Group(songs=[s for s in self.read().songs if s.yt_id != song.yt_id])
		)

		file = get_file(song)
		if not file:
			logboth.error(
				__name__, 'Failed remove song from downloads - file not found'
			)
		os.remove(file)

		logboth.info(__name__, 'Removed song from downloads')
		self.lock.unlock()


downloader = _Downloader()
'''Downloader singleton for thread safety.

For use with ``DownloadTask``.
'''
