'''Playlist management.

Playlists can be local (editable) or external (synchronized with YT).

Thread-safe via module-wide lock.
'''

import json
import os
import time

from monophony import NAME, yt
from monophony.asynchronous import Task
from monophony.data import Artist, Group, Song

import logboth
from gi.repository import GLib


def get_directory() -> str:
	'''Get playlist storage directory.

	:return: Directory path.
	'''
	return os.getenv(
		'XDG_CONFIG_HOME', os.path.expanduser('~/.config')
	) + '/' + NAME


def _get_file_path() -> str:
	return get_directory() + '/playlists.json'


def _get_external_file_path() -> str:
	return get_directory() + '/external-playlists.json'


def add(playlist: Group) -> str:
	'''Create a new local playlist.

	:param playlist: The playlist to create.
	'''
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
	'''Create a new external playlist.

	:param playlist: The playlist to create.
	'''
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
	'''Rename a local playlist.

	If the new name is not unique, it will be altered. Always use the returned value.

	External playlists cannot be renamed.

	:param name: Old playlist name.
	:param new_name: New playlist name.
	:return: The final playlist name.
	'''
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
	'''Delete a local playlist.

	:playlist_name: Name of playlist to delete.
	'''
	logboth.info(__name__, f'Deleting playlist "{playlist_name}"...')
	current_lists = read()
	for playlist in current_lists:
		if playlist.title == playlist_name and playlist.yt_id and yt.is_authenticated():
			yt.delete_user_playlist(playlist.yt_id)

	_write(
		playlists=[playlist for playlist in current_lists if playlist.title != playlist_name]
	)
	logboth.info(__name__, 'Deleted playlist')


def delete_external(playlist_name: str):
	'''Delete an external playlist.

	:playlist_name: Name of playlist to delete.
	'''
	logboth.info(__name__, f'Deleting external playlist "{playlist_name}"...')
	_write(
		ext_playlists=[
			playlist for playlist in read_external() if playlist.title != playlist_name
		]
	)
	logboth.info(__name__, 'Deleted external playlist')


def add_songs(songs: Group, playlist_name: str):
	'''Add a group of songs to a local playlist.

	:param songs: Group of songs to add.
	:param playlist_name: Name of playlist to add to.
	'''
	logboth.info(
		__name__, f'Adding {len(songs.songs)} songs to playlist "{playlist_name}"...'
	)
	new_lists = read()
	added_song_ids = []
	target_yt_id = ''
	for playlist in new_lists:
		if playlist.title == playlist_name:
			target_yt_id = playlist.yt_id
			for song in songs.songs:
				if not any(existing_song.yt_id == song.yt_id for existing_song in playlist.songs):
					playlist.songs.append(song)
					added_song_ids.append(song.yt_id)
			break

	_write(playlists=new_lists)
	if target_yt_id and added_song_ids and yt.is_authenticated():
		yt.add_songs_to_user_playlist(target_yt_id, added_song_ids)

	logboth.info(__name__, 'Added songs to playlist')


def swap_songs(playlist_name: str, i: int, j: int):
	'''Swap song positions in local playlist.

	:param playlist_name: Name of playlist to modify.
	:param i: First song index.
	:param j: Second song index.
	'''
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
	'''Move song to index in local playlist.

	:param playlist_name: Name of playlist to modify.
	:param from_i: Index of song to move.
	:param to_i: Index to move song to.
	'''
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
	'''Remove song from local playlist.

	:param song: Song to remove.
	:param playlist_name: Name of playlist to remove.
	'''
	logboth.info(
		__name__, f'Removing song "{song.yt_id}" from playlist "{playlist_name}"...'
	)
	new_lists = read()
	target_yt_id = ''
	for playlist in new_lists:
		if playlist.title == playlist_name:
			target_yt_id = playlist.yt_id
			playlist.songs = [s for s in playlist.songs if s.yt_id != song.yt_id]
			break

	_write(playlists=new_lists)
	if target_yt_id and song.yt_id and yt.is_authenticated():
		yt.remove_songs_from_user_playlist(target_yt_id, [song.yt_id])

	logboth.info(__name__, 'Removed song')


def make_unique_name(name: str) -> str:
	'''Generate a unique playlist name from a name.

	If the name is already unique and non-empty, it will be returned as-is.

	:name: Original playlist name.
	'''
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
	_lock.lock()
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
			data = {'contents': playlist.serialize()['contents']}
			if playlist.yt_id:
				data['id'] = playlist.yt_id
			serialized_playlists[playlist.title] = data
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
	_lock.unlock()


def read() -> list[Group]:
	'''Get all local playlists.

	:return: List of playlists.
	'''
	_lock.lock()
	try:
		with open(_get_file_path()) as lists_file:
			raw_data = json.load(lists_file)
			result = []
			for name, val in raw_data.items():
				yt_id = ''
				if isinstance(val, dict):
					songs_raw = val.get('contents', [])
					yt_id = val.get('id', '')
				else:
					songs_raw = val
				songs = [
					Song(
						title=song.get('title', ''),
						author=Artist(
							name=song.get('author', ''),
							yt_id=song.get('author_id', '')
						),
						length=song.get('length', ''),
						thumbnail=song.get('thumbnail', ''),
						yt_id=song.get('id', '')
					) for song in songs_raw
				]
				result.append(Group(title=name, yt_id=yt_id, songs=songs))
			_lock.unlock()
			return result
	except (OSError, json.decoder.JSONDecodeError):
		_lock.unlock()
		return []


def read_external() -> list[Group]:
	'''Get all external playlists.

	:return: List of playlists.
	'''
	_lock.lock()
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
			_lock.unlock()
			return result
	except (OSError, json.decoder.JSONDecodeError):
		_lock.unlock()
		return []


class ImportTask(Task):
	'''Task for importing playlists from YT as local or external.

	.. code-block::

		ImportTask(
			args=(name, url, local, overwrite)
		)

	'''

	def _function(
		self, name: str, url: str, local: bool, overwrite: bool=False
	) -> bool:
		logboth.info(__name__, f'Importing playlist "{url}"...')
		new_lists = [playlist for playlist in read() if playlist.title != name]
		new_ext_lists = [
			playlist for playlist in read_external() if playlist.title != name
		]

		if not (playlist := yt.get_album_or_playlist(
			url.rsplit('list=', maxsplit=1)[-1].split('&', maxsplit=1)[0]
		)):
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
	'''Task for updating (synchronizing) external playlists.'''

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


class SyncPlaylistsTask(Task):
	'''Task for 2-way synchronization of playlists with YouTube account.'''

	def _function(self) -> bool:
		logboth.info(__name__, 'Starting 2-way YouTube playlist synchronization...')
		if not yt.is_authenticated():
			logboth.warning(__name__, 'Cannot sync playlists: Not authenticated')
			return False

		try:
			remote_playlists_meta = yt.get_user_playlists()
			local_playlists = read()

			remote_yt_ids = {p['playlistId']: p for p in remote_playlists_meta if 'playlistId' in p}
			local_by_yt_id = {p.yt_id: p for p in local_playlists if p.yt_id}
			local_by_title = {p.title: p for p in local_playlists}

			updated_local = list(local_playlists)
			total = len(remote_playlists_meta) + len(local_playlists)
			count = 0

			# 1. Process Remote Playlists -> Local
			for r_id, r_meta in remote_yt_ids.items():
				if self.is_canceled():
					return False
				count += 1
				self._update_progress(count / (total or 1))

				remote_group = yt.get_album_or_playlist(r_id)
				if not remote_group:
					continue

				if r_id in local_by_yt_id:
					local_group = local_by_yt_id[r_id]
					local_song_ids = {s.yt_id for s in local_group.songs}
					remote_song_ids = {s.yt_id for s in remote_group.songs}

					for s in remote_group.songs:
						if s.yt_id not in local_song_ids:
							local_group.songs.append(s)

					songs_to_push = [s.yt_id for s in local_group.songs if s.yt_id not in remote_song_ids]
					if songs_to_push:
						yt.add_songs_to_user_playlist(r_id, songs_to_push)

				elif r_meta.get('title') in local_by_title:
					local_group = local_by_title[r_meta['title']]
					local_group.yt_id = r_id
					local_song_ids = {s.yt_id for s in local_group.songs}
					remote_song_ids = {s.yt_id for s in remote_group.songs}

					for s in remote_group.songs:
						if s.yt_id not in local_song_ids:
							local_group.songs.append(s)

					songs_to_push = [s.yt_id for s in local_group.songs if s.yt_id not in remote_song_ids]
					if songs_to_push:
						yt.add_songs_to_user_playlist(r_id, songs_to_push)
				else:
					remote_group.yt_id = r_id
					remote_group.title = make_unique_name(remote_group.title)
					updated_local.append(remote_group)

			# 2. Push Local Playlists without yt_id to Remote YouTube Account
			for local_group in updated_local:
				if self.is_canceled():
					return False
				count += 1
				self._update_progress(count / (total or 1))

				if not local_group.yt_id and local_group.songs:
					song_ids = [s.yt_id for s in local_group.songs if s.yt_id]
					new_yt_id = yt.create_user_playlist(local_group.title, '', song_ids)
					if new_yt_id:
						local_group.yt_id = new_yt_id

			_write(playlists=updated_local)
			logboth.info(__name__, '2-way playlist sync finished')
			return True

		except Exception as e:
			logboth.error(__name__, f'Failed to sync playlists: {e}')
			return False


# Singleton
_lock = GLib.Mutex()

