'''Song playback history.

Not thread-safe.
'''

import json
import os
import traceback

from monophony import NAME
from monophony.data import Artist, Group, Song

import logboth


_MAX_SONGS = 15


def _get_directory() -> str:
	return os.getenv(
		'XDG_CONFIG_HOME', os.path.expanduser('~/.config')
	) + f'/{NAME}'


def _get_file_path() -> str:
	return _get_directory() + '/recent-songs.json'


def _write(group: Group):
	if len(group.songs) > _MAX_SONGS:
		group.songs = group.songs[:_MAX_SONGS]

	logboth.info(__name__, f'Writing {len(group.songs)} songs to recents...')
	os.makedirs(_get_directory(), exist_ok=True)
	try:
		with open(_get_file_path(), 'w') as recents_file:
			json.dump(group.serialize()['contents'], recents_file, indent='\t')
	except OSError:
		logboth.error(__name__, 'Failed to write to recents', traceback.format_exc())
		return

	logboth.info(__name__, 'Done writing to recents')


def add(song: Song):
	'''Add song to recently played.

	Duplicates handled automatically by ``Group``.

	:param song: Song to add.
	'''
	logboth.info(__name__, f'Adding song "{song.yt_id}" to recents...')
	group = read()
	group.songs = [song, *group.songs]
	_write(group)
	logboth.info(__name__, 'Added song to recents')


def clear():
	'''Clear playback history.'''
	_write(Group())


def read() -> Group:
	'''Get recently played songs.

	:return: Group of songs.
	'''
	try:
		with open(_get_file_path()) as recents_file:
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
					) for item in json.load(recents_file)
				]
			)
	except (OSError, json.decoder.JSONDecodeError):
		return Group()
