import json
import os
import time

from monophony import NAME, yt
from monophony.asynchronous import Task
from monophony.data import Artist, Group, Song

import logboth
from gi.repository import GLib


def get_directory() -> str:
	return os.getenv(
		'XDG_CONFIG_HOME', os.path.expanduser('~/.config')
	) + '/' + NAME


def _get_file_path() -> str:
	return get_directory() + '/playlists.json'


def _get_external_file_path() -> str:
	return get_directory() + '/external-playlists.json'


def add(playlist: Group) -> str:
	logboth.info(__name__, f'Adding playlist "{playlist.title}"...')
	new_lists = read()
	old_title = playlist.title
	playlist.title = make_unique_name(playlist.title)

	song_ids = []
	unique_songs = []
	for song in playlist.songs:
		if song.yt_id not in song_ids:
			unique_songs.append(song)
			song_ids.append(song.yt_id)

	playlist.songs = unique_songs
	new_lists.append(playlist)
	_write(playlists=new_lists)
	logboth.info(__name__, f'Added playlist "{old_title}" as "{playlist.title}"')
	return playlist.title


def add_external(playlist: Group):
	logboth.info(__name__, f'Adding external playlist "{playlist.yt_id}"...')
	lists = read_external()

	song_ids = []
	unique_songs = []
	for song in playlist.songs:
		if song.yt_id not in song_ids:
			unique_songs.append(song)
			song_ids.append(song.yt_id)

	playlist.songs = unique_songs
	lists.append(playlist)
	_write(ext_playlists=lists)
	logboth.info(__name__, 'Added external playlist')


def rename(name: str, new_name: str) -> str:
	new_name = make_unique_name(new_name)
	logboth.info(__name__, f'Renaming playlist "{name}" to "{new_name}"...')

	new_lists = read()
	for playlist in new_lists:
		if playlist.title == name:
			playlist.title = new_name
			_write(playlists=new_lists)
			logboth.info(__name__, 'Renamed playlist')
			return new_name

	logboth.error(__name__, 'Failed to rename: playlist not found')
	return name


def delete(playlist_name: str):
	logboth.info(__name__, f'Deleting playlist "{playlist_name}"...')
	_write(
		playlists=[playlist for playlist in read() if playlist.title != playlist_name]
	)
	logboth.info(__name__, 'Deleted playlist')


def delete_external(playlist_name: str):
	logboth.info(__name__, f'Deleting external playlist "{playlist_name}"...')
	_write(
		ext_playlists=[
			playlist for playlist in read_external() if playlist.title != playlist_name
		]
	)
	logboth.info(__name__, 'Deleted external playlist')


def add_songs(songs: Group, playlist_name: str):
	logboth.info(
		__name__, f'Adding {len(songs.songs)} songs to playlist "{playlist_name}"...'
	)
	new_lists = read()
	for song in songs.songs:
		for playlist in new_lists:
			if playlist.title == playlist_name:
				for existing_song in playlist.songs:
					if song.yt_id == existing_song.yt_id:
						return
				playlist.songs.append(song)
				break

	_write(playlists=new_lists)
	logboth.info(__name__, 'Added songs to playlist')


def swap_songs(playlist_name: str, i: int, j: int):
	logboth.info(
		__name__, f'Swapping songs #{i} and #{j} in playlist "{playlist_name}"...'
	)
	new_lists = read()
	for playlist in new_lists:
		if playlist.title == playlist_name:
			i = 0 if i >= len(playlist.songs) else i
			j = 0 if j >= len(playlist.songs) else j
			playlist.songs[i], playlist.songs[j] = playlist.songs[j], playlist.songs[i]
			break

	_write(playlists=new_lists)
	logboth.info(__name__, 'Swapped songs')


def move_song(playlist_name: str, from_i: int, to_i: int):
	logboth.info(
		__name__,
		f'Moving song from #{from_i} to #{to_i} in playlist "{playlist_name}"...'
	)
	new_lists = read()
	for playlist in new_lists:
		if playlist.title == playlist_name:
			to_song = playlist.songs[to_i]
			from_song = playlist.songs.pop(from_i)
			playlist.songs.insert(playlist.songs.index(to_song), from_song)
			break

	_write(playlists=new_lists)
	logboth.info(__name__, 'Moved song')


def remove_song(song: Song, playlist_name: str):
	logboth.info(
		__name__, f'Removing song "{song.yt_id}" from playlist "{playlist_name}"...'
	)
	new_lists = read()
	for playlist in new_lists:
		if playlist.title == playlist_name:
			playlist.songs = [s for s in playlist.songs if s.yt_id != song.yt_id]
			break

	_write(playlists=new_lists)
	logboth.info(__name__, 'Removed song')


def make_unique_name(name: str) -> str:
	taken_names = (
		[playlist.title for playlist in read()] +
		[playlist.title for playlist in read_external()]
	)
	new_name = name or _('Playlist')

	i = 1
	while new_name in taken_names:
		new_name = f'{name} ({i})'
		i += 1

	return new_name


def _write(playlists: list[Group] | None=None, ext_playlists: list[Group] | None=None):
	lock.lock()
	logboth.info(
		__name__,
		f'Writing {len(playlists) if playlists else "no"} playlists and '
		f'{len(ext_playlists) if ext_playlists else "no"} external playlists...'
	)
	lists_path = _get_file_path()
	ext_lists_path = _get_external_file_path()
	os.makedirs(get_directory(), exist_ok=True)

	if playlists is not None:
		serialized_playlists = {}
		for playlist in playlists:
			serialized_playlists[playlist.title] = playlist.serialize()['contents']
		with open(lists_path, 'w') as lists_file:
			json.dump(serialized_playlists, lists_file, indent='\t')

	if ext_playlists is not None:
		with open(ext_lists_path, 'w') as ext_lists_file:
			json.dump(
				[playlist.serialize() for playlist in ext_playlists],
				ext_lists_file,
				indent='\t'
			)

	logboth.info(__name__, 'Done writing playlist and external playlists')
	lock.unlock()


def read() -> list[Group]:
	lock.lock()
	try:
		with open(_get_file_path()) as lists_file:
			result = [
				Group(
					title=name,
					songs=[
						Song(
							title=song.get('title', ''),
							author=Artist(
								name=song.get('author', ''),
								yt_id=song.get('author_id', '')
							),
							length=song.get('length', ''),
							thumbnail=song.get('thumbnail', ''),
							yt_id=song.get('id', '')
						) for song in songs
					]
				) for name, songs in json.load(lists_file).items()
			]
			lock.unlock()
			return result
	except (OSError, json.decoder.JSONDecodeError):
		lock.unlock()
		return []


def read_external() -> list[Group]:
	lock.lock()
	try:
		with open(_get_external_file_path()) as lists_file:
			result = [
				Group(
					title=playlist.get('title', ''),
					yt_id=playlist.get('id', ''),
					songs=[
						Song(
							title=song.get('title', ''),
							author=Artist(
								name=song.get('author', ''),
								yt_id=song.get('author_id', '')
							),
							length=song.get('length', ''),
							thumbnail=song.get('thumbnail', ''),
							yt_id=song.get('id', '')
						) for song in playlist.get('contents', [])
					]
				) for playlist in json.load(lists_file)
			]
			lock.unlock()
			return result
	except (OSError, json.decoder.JSONDecodeError):
		lock.unlock()
		return []


class ImportTask(Task):
	def _function(
		self, name: str, url: str, local: bool, overwrite: bool=False
	) -> bool:
		logboth.info(__name__, f'Importing playlist "{url}"...')
		new_lists = [playlist for playlist in read() if playlist.title != name]
		new_ext_lists = [
			playlist for playlist in read_external() if playlist.title != name
		]

		if not (
			playlist := yt.get_album_or_playlist(url.split('list=')[-1].split('&')[0])
		):
			logboth.error(__name__, 'Failed to import playlist')
			return False

		playlist.title = make_unique_name(
			name if local else playlist.title
		) if not overwrite else name

		if local:
			new_lists.append(playlist)
			_write(playlists=new_lists)
		else:
			new_ext_lists.append(playlist)
			_write(ext_playlists=new_ext_lists)

		logboth.info(__name__, 'Imported playlist')
		return True


class UpdateExternalTask(Task):
	def _function(self):
		logboth.info(__name__, 'Updating external playlists...')
		tasks = []
		external = read_external()
		for i, playlist in enumerate(external):
			task = ImportTask(args=(playlist.title, playlist.yt_id, False, True))
			task.start()
			tasks.append(task)

			# Rate limit
			if i % 4 == 0:
				self._update_progress((i / len(external)) / 2)
				while task.is_running():
					time.sleep(0.5)

		for i, task in enumerate(tasks):
			while task.is_running():
				self._update_progress((i / len(tasks)) / 2 + 0.5)
				time.sleep(0.5)

		logboth.info(__name__, 'Updated external playlists')


# Signleton
lock = GLib.Mutex()
