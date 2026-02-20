#!/usr/bin/env python3
# ruff: noqa: S101 - Asserts used in tests
# ruff: noqa: SLF001 - Private members used in tests
# ruff: noqa: D100 D101 D102

import os
import shutil
import time
import unittest

from monophony import ID, NAME, __version__, playlists, settings
from monophony.data import Group, Song
from monophony.playlists import ImportTask


class BaseTestCase(unittest.TestCase):
	def tearDown(self):
		shutil.rmtree(
			os.getenv(
				'XDG_CONFIG_HOME', os.path.expanduser('~/.config')
			) + '/' + NAME,
			ignore_errors=True
		)
		shutil.rmtree(
			os.getenv(
				'XDG_DATA_HOME', os.path.expanduser('~/.local/share')
			) + '/' + NAME,
			ignore_errors=True
		)


class MetadataTestCase(BaseTestCase):
	def test_version(self):
		for path in os.getenv('XDG_DATA_DIRS', '/usr/share/').split(':'):
			file_path = (
				path if path.endswith('/') else path + '/'
			) + f'metainfo/{ID}.metainfo.xml'

			if not os.path.isfile(file_path):
				continue

			with open(file_path) as metainfo:
				version = metainfo.read().split('<release version="')[1].split('"')[0]
				assert(version == __version__)
				return

		raise(FileNotFoundError)


class PlaylistsTestCase(BaseTestCase):
	def test_add_delete(self):
		playlist = Group(title='a', songs=[Song(title='c', yt_id='d')])
		external_playlist = Group(
			title='e', yt_id='f', songs=[Song(title='g', yt_id='h')]
		)

		assert(playlists.read() == [])
		playlists.add(playlist)
		assert(playlists.read()[0].songs == playlist.songs)
		assert(playlists.read_external() == [])
		playlists.add_external(external_playlist)
		assert(playlists.read_external()[0].songs == external_playlist.songs)
		playlists.delete(playlist.title)
		assert(playlists.read() == [])
		playlists.delete_external(external_playlist.title)
		assert(playlists.read_external() == [])

	def test_add_remove_songs(self):
		playlist = Group(title='a', yt_id='b')
		song = Song(title='c', yt_id='d')

		assert(playlists.read() == [])
		playlists._write([playlist])
		playlists.add_songs(Group(songs=[song]), playlist.title)
		assert(playlists.read()[0].songs[0] == song)

	def test_import(self):
		url = (
			'https://music.youtube.com/playlist?list='
			'OLAK5uy_k_lweiBStMgoHOTyUzrzYRPHorT9LogLI'
		)

		assert(playlists.read() == [])
		task = ImportTask(args=('a', url, True))
		task.start()
		while task.is_running():
			time.sleep(1)
		assert(playlists.read()[0].songs[0].title == 'Waiting For Love')
		assert(playlists.read_external() == [])
		external_task = ImportTask(args=('', url, False))
		external_task.start()
		while external_task.is_running():
			time.sleep(1)
		assert(
			playlists.read_external()[0].songs[0].title == 'Waiting For Love'
		)

	def test_make_unique_name(self):
		playlist = Group(title='a', yt_id='b')

		assert(playlists.make_unique_name('a') == 'a')
		playlists._write([playlist])
		assert(playlists.make_unique_name('a') != 'a')

	def test_move_swap_songs(self):
		playlist = Group(
			title='a',
			yt_id='b',
			songs=[Song(title='c', yt_id='d'), Song(title='e', yt_id='f')]
		)

		assert(playlists.read() == [])
		playlists._write([playlist])
		playlists.move_song(playlist.title, 1, 0)
		assert(playlists.read()[0].songs[0].title == 'e')
		assert(playlists.read()[0].songs[1].title == 'c')
		playlists.swap_songs(playlist.title, 0, 1)
		assert(playlists.read()[0].songs[0].title == 'c')
		assert(playlists.read()[0].songs[1].title == 'e')

	def test_rename(self):
		playlist = Group(title='a', yt_id='b', songs=[Song(title='c', yt_id='d')])

		assert(playlists.read() == [])
		playlists._write([playlist])
		assert(playlists.rename(playlist.title, 'e') == 'e')
		assert(playlists.read()[0].title == 'e')

	def test_write_read(self):
		lists = [Group(title='a', songs=[Song(title='b', yt_id='c')])]
		external_lists = [
			Group(title='d', yt_id='e', songs=[Song(title='f', yt_id='g')])
		]

		assert(playlists.read() == [])
		assert(playlists.read_external() == [])
		playlists._write(lists, external_lists)
		assert(playlists.read() == lists)
		assert(playlists.read_external() == external_lists)


class SettingsTestCase(BaseTestCase):
	def test_save_load(self):
		values = {'int': 1, 'float': 1.1, 'str': 'a'}

		assert(settings._read() == {})
		settings.save(values)
		for key, value in values.items():
			assert(value == settings.load(key))

	def test_write_read(self):
		values = {'int': 1, 'float': 1.1, 'str': 'a'}

		assert(settings._read() == {})
		settings._write(values)
		assert(settings._read() == values)


if __name__ == '__main__':
	unittest.main()
