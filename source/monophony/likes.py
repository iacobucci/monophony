'''Management of liked songs ("Liked Music" / LM on YouTube Music).

Thread-safe via module-wide lock.
'''

import json
import os
import threading
from typing import Callable

from monophony import get_user_config_dir, yt
from monophony.data import Artist, Group, Song

import logboth
from gi.repository import GLib

_lock = threading.Lock()
_cached_liked_group: Group | None = None
_listeners: list[Callable[[], None]] = []


def _get_file_path() -> str:
	return os.path.join(get_user_config_dir(), 'liked.json')


def add_listener(callback: Callable[[], None]):
	'''Add a listener called when likes change.'''
	if callback not in _listeners:
		_listeners.append(callback)


def remove_listener(callback: Callable[[], None]):
	'''Remove a listener.'''
	if callback in _listeners:
		_listeners.remove(callback)


def _notify_listeners():
	for cb in list(_listeners):
		try:
			GLib.idle_add(cb)
		except Exception as e:
			logboth.warning(__name__, f'Failed to notify like listener: {e}')


def read() -> Group:
	'''Get the Liked Songs group.

	:return: Group object with yt_id='LM'.
	'''
	global _cached_liked_group
	with _lock:
		if _cached_liked_group is not None:
			return _cached_liked_group

		path = _get_file_path()
		songs: list[Song] = []
		if os.path.exists(path):
			try:
				with open(path, encoding='utf-8') as f:
					raw = json.load(f)
					for item in raw.get('contents', []):
						songs.append(
							Song(
								title=item.get('title', ''),
								author=Artist(
									name=item.get('author', ''),
									yt_id=item.get('author_id', '')
								),
								length=item.get('length', ''),
								thumbnail=item.get('thumbnail', ''),
								yt_id=item.get('id', '')
							)
						)
			except Exception as e:
				logboth.warning(__name__, f'Failed to read liked songs from file: {e}')

		_cached_liked_group = Group(
			title=_('Liked Music'),
			yt_id='LM',
			songs=songs
		)
		return _cached_liked_group


def _write(group: Group):
	global _cached_liked_group
	_cached_liked_group = group
	path = _get_file_path()
	os.makedirs(os.path.dirname(path), exist_ok=True)
	data = {
		'id': 'LM',
		'title': group.title,
		'contents': [
			{
				'title': s.title,
				'author': s.author.name,
				'author_id': s.author.yt_id,
				'length': s.length,
				'thumbnail': s.thumbnail,
				'id': s.yt_id
			}
			for s in group.songs
		]
	}
	with open(path, 'w', encoding='utf-8') as f:
		json.dump(data, f, indent='\t')


def is_liked(yt_id: str) -> bool:
	'''Check if song is liked by YouTube ID.'''
	if not yt_id:
		return False
	grp = read()
	return any(s.yt_id == yt_id for s in grp.songs)


def toggle_like(song: Song) -> bool:
	'''Toggle like status for a song.

	Saves locally and sends rating to YouTube Music asynchronously.

	:param song: Song to toggle.
	:return: New like state (True if liked, False if unliked).
	'''
	if not song or not song.yt_id:
		return False

	with _lock:
		grp = read()
		current_songs = list(grp.songs)
		already_liked = any(s.yt_id == song.yt_id for s in current_songs)

		if already_liked:
			new_songs = [s for s in current_songs if s.yt_id != song.yt_id]
			new_state = False
			rating = 'INDIFFERENT'
		else:
			new_songs = [song] + [s for s in current_songs if s.yt_id != song.yt_id]
			new_state = True
			rating = 'LIKE'

		grp.songs = new_songs
		_write(grp)

	logboth.info(__name__, f'Toggled like for "{song.title}" ({song.yt_id}) -> {new_state}')
	_notify_listeners()

	# Asynchronously update YouTube Music rating
	def _sync_worker():
		yt.rate_song(song.yt_id, rating)

	threading.Thread(target=_sync_worker, daemon=True).start()
	return new_state


def sync_from_remote():
	'''Sync liked songs with remote YouTube Music LM playlist.'''
	if not yt.is_authenticated():
		return

	logboth.info(__name__, 'Syncing Liked Songs from YouTube Music...')
	remote_group = yt.get_album_or_playlist('LM')
	if not remote_group or not remote_group.songs:
		logboth.warning(__name__, 'Could not fetch remote Liked Songs')
		return

	with _lock:
		local_group = read()
		local_song_ids = {s.yt_id for s in local_group.songs}
		remote_song_ids = {s.yt_id for s in remote_group.songs}

		# Merge remote songs into local (keeping remote order first)
		merged = list(remote_group.songs)
		for local_s in local_group.songs:
			if local_s.yt_id not in remote_song_ids:
				merged.append(local_s)

		local_group.songs = merged
		_write(local_group)

	logboth.info(__name__, f'Synced {len(merged)} Liked Songs with YouTube Music')
	_notify_listeners()
