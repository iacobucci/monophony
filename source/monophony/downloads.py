import contextlib
import glob
import json
import os
import subprocess
import traceback

from monophony import NAME, logging
from monophony.asynchronous import Task
from monophony.data import Artist, Group, Song

from gi.repository import GLib


def get_directory() -> str:
	return os.getenv(
		'XDG_DATA_HOME', os.path.expanduser('~/.local/share')
	) + f'/{NAME}/'


def get_temp_directory() -> str:
	return os.getenv('XDG_RUNTIME_DIR', '/var/tmp') + f'/{NAME}/downloads/'


def get_file(song: Song) -> str | None:
	files = [
		file for file in glob.glob(get_directory() + '*' + song.yt_id + '*')
		if not file.endswith('.' + NAME)
	]

	if files:
		if len(files) > 1:
			logging.warning(
				__name__,
				f'Multiple song files match id "{song.yt_id}"', '\n'.join(files)
			)
		return files[0]

	return None


def is_being_downloaded(song: Song) -> bool:
	return os.path.exists(get_directory() + song.yt_id + '.' + NAME)


def is_downloaded(song: Song) -> bool:
	return (
		song.yt_id and get_file(song) and not is_being_downloaded(song)
	)


class DownloadTask(Task):
	def _function(self, downloader: '_Downloader', group: Group) -> bool:
		downloader.lock.lock()
		logging.info(__name__, f'Downloading {len(group.songs)} songs...')

		path = get_directory()
		needed_ids = []
		new_group = Group()
		for song in group.songs:
			if not song.yt_id:
				logging.error(
					__name__, f'Failed to download song "{song.title}" - no id'
				)
				continue

			if is_downloaded(song) or is_being_downloaded(song):
				logging.info(
					__name__,
					f'Skipped download of song "{song.yt_id}" - already taken care of'
				)
				continue

			downloader.create_lock_file(song.yt_id)
			needed_ids.append(song.yt_id)
			new_group.songs.append(song)

		# *.NAME files act as locks for this part
		self._update_progress()
		downloader.lock.unlock()

		if not needed_ids:
			logging.info(
				__name__, 'Canceled download as there are no songs to download'
			)
			return True

		song_urls = [
			f'https://music.youtube.com/watch?v={yt_id}' for yt_id in needed_ids
		]
		ytdlp = subprocess.Popen(
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
				*song_urls
			],
			text=True,
			stderr=subprocess.STDOUT,
			stdout=subprocess.PIPE
		)
		return_code = ytdlp.wait()

		downloader.lock.lock()
		for yt_id in needed_ids:
			downloader.delete_lock_file(yt_id)

		if return_code != 0:
			logging.error(__name__, 'Failed to download songs', ytdlp.stdout.read())
			downloader.lock.unlock()
			return False

		new_group.songs = [song for song in new_group.songs if is_downloaded(song)]
		logging.info(
			__name__, f'Downloaded {len(new_group.songs)}/{len(group.songs)} songs'
		)
		logging.info(__name__, 'Saving data about newly downloaded songs...')
		downloader.write(Group(songs=new_group.songs + downloader.read().songs))
		logging.info(__name__, 'Saved newly downloaded song data')

		downloader.lock.unlock()
		return True


class _Downloader:
	def __init__(self):
		self.lock = GLib.Mutex()

		self.lock.lock()
		logging.info(__name__, 'Cleaning up downloads...')
		downloads_group = self.read()
		path = get_directory()
		os.makedirs(path, exist_ok=True)
		for file in os.listdir(path):
			if file.endswith(NAME):
				os.remove(path + file)
				logging.info(__name__, f'Removed abandoned temp file "{file}"')
				continue

			yt_id = 'null'
			with contextlib.suppress(IndexError):
				yt_id = file.split('.')[-2][-11:]
			if Song(yt_id=yt_id) not in downloads_group.songs:
				os.remove(path + file)
				logging.warning(__name__, f'Removed unexpected file "{file}"')

		logging.info(__name__, 'Cleaned up downloads')
		self.lock.unlock()

	def create_lock_file(self, name: str):
		logging.info(__name__, f'Creating lock file "{name}.{NAME}"...')

		# Always lock self.lock before calling this to prevent race conditions
		if self.lock.trylock():
			logging.warning(
				__name__, 'Creating lock file while self.lock is unlocked'
			)
			self.lock.unlock()

		try:
			open(f'{get_directory()}{name}.{NAME}', 'w').close()
		except OSError:
			logging.error(
				__name__, 'Failed to create lock file', traceback.format_exc()
			)
			return

		logging.info(__name__, 'Created lock file')

	def delete_lock_file(self, name: str):
		logging.info(__name__, f'Deleting lock file "{name}.{NAME}"...')

		# Always lock self.lock before calling this to prevent race conditions
		if self.lock.trylock():
			logging.warning(
				__name__, 'Deleting lock file while self.lock is unlocked'
			)
			self.lock.unlock()

		try:
			os.remove(f'{get_directory()}{name}.{NAME}')
		except (OSError, FileNotFoundError):
			logging.error(
				__name__,
				f'Failed to remove lock file "{name}.{NAME}"',
				traceback.format_exc()
			)

		logging.info(__name__, 'Deleted lock file')

	def read(self) -> Group:
		# Always lock self.lock before calling this to prevent race conditions
		if self.lock.trylock():
			logging.warning(__name__, 'Reading downloads while self.lock is unlocked')
			self.lock.unlock()

		songs_path = os.getenv(
			'XDG_CONFIG_HOME', os.path.expanduser('~/.config')
		) + f'/{NAME}/downloads.json'

		try:
			with open(songs_path) as songs_file:
				return Group(
					songs=[
						Song(
							title=item.get('title', ''),
							author=Artist(
								name=item.get('author', ''),
								yt_id=item.get('author_id', '')
							),
							length=item.get('length', ''),
							thumbnail=item.get('thumbnail', ''),
							yt_id=item.get('id', '')
						) for item in json.load(songs_file)
					]
				)
		except (OSError, json.decoder.JSONDecodeError):
			return Group()

	def write(self, group: Group):
		logging.info(__name__, f'Writing {len(group.songs)} songs to downloads...')

		# Always lock self.lock before calling this to prevent race conditions
		if self.lock.trylock():
			logging.warning(__name__, 'Writing downloads while self.lock is unlocked')
			self.lock.unlock()

		dir_path = os.getenv(
			'XDG_CONFIG_HOME', os.path.expanduser('~/.config')
		) + '/' + NAME
		downloads_path = dir_path + '/downloads.json'

		os.makedirs(dir_path, exist_ok=True)
		with open(downloads_path, 'w') as downloads_file:
			json.dump(group.serialize()['contents'], downloads_file, indent='\t')

		logging.info(__name__, 'Done writing to downloads')

	def get_downloads(self) -> Group:
		self.lock.lock()
		downloads = self.read()
		self.lock.unlock()
		return downloads

	def remove(self, song: Song):
		self.lock.lock()
		logging.info(__name__, f'Removing song "{song.yt_id}" from downloads...')

		# No race conditions here as long as lock files are only created and
		# deleted while holding the lock
		if not is_downloaded(song):
			logging.error(
				__name__, 'Failed remove song from downloads - not downloaded'
			)
			self.lock.unlock()
			return
		if is_being_downloaded(song):
			logging.error(
				__name__, 'Failed remove song from downloads - download in progress'
			)
			self.lock.unlock()
			return

		self.write(
			Group(songs=[s for s in self.read().songs if s.yt_id != song.yt_id])
		)

		file = get_file(song)
		if not file:
			logging.error(
				__name__, 'Failed remove song from downloads - file not found'
			)
		os.remove(file)

		logging.info(__name__, 'Removed song from downloads')
		self.lock.unlock()


# Singleton for thread safety
downloader = _Downloader()
