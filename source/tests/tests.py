#!/usr/bin/env python3
# ruff: noqa: S101 - Asserts used in tests
# ruff: noqa: SLF001 - Private members used in tests
# ruff: noqa: D100 D101 D102

import os
import shutil
import sys
import time
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from monophony import ID, NAME, __version__, playlists, settings
from monophony.data import Group, Song
from monophony.playlists import ImportTask



import tempfile


class BaseTestCase(unittest.TestCase):
	def setUp(self):
		self.temp_config = tempfile.TemporaryDirectory()
		os.environ['XDG_CONFIG_HOME'] = self.temp_config.name

	def tearDown(self):
		if hasattr(self, 'temp_config'):
			try:
				self.temp_config.cleanup()
			except Exception:
				shutil.rmtree(self.temp_config.name, ignore_errors=True)




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


class YouTubeAccountTestCase(BaseTestCase):
	def test_auth_status(self):
		from monophony import yt
		assert(not yt.is_authenticated())

	def test_playlist_yt_id_persistence(self):
		playlist = Group(title='SyncList', yt_id='PL12345', songs=[Song(title='S1', yt_id='s1')])
		playlists._write([playlist])
		loaded = playlists.read()
		assert(len(loaded) == 1)
		assert(loaded[0].title == 'SyncList')
		assert(loaded[0].yt_id == 'PL12345')

	def test_sync_unauthenticated(self):
		from monophony.playlists import SyncPlaylistsTask
		task = SyncPlaylistsTask()
		task.start()
		while task.is_running():
			time.sleep(0.1)
		assert(task.result is False)


class CacheAndPrefetchTestCase(BaseTestCase):
	def test_cache_management(self):
		from monophony import cache
		song = Song(title='TestSong', yt_id='test_song_123')
		assert(not cache.is_cached(song))

		cache_dir = cache.get_cache_dir()
		os.makedirs(cache_dir, exist_ok=True)
		test_file = os.path.join(cache_dir, 'test_song_123.m4a')
		with open(test_file, 'w') as f:
			f.write('dummy audio data')

		assert(cache.is_cached(song))
		assert(cache.get_cached_file(song) == test_file)
		assert(cache.get_cache_size() > 0)

		cache.clear_cache()
		assert(not cache.is_cached(song))
		assert(cache.get_cache_size() == 0)

	def test_prefetch_manager(self):
		from monophony.prefetch import prefetch_manager
		queue = Group(songs=[
			Song(title='S1', yt_id='s1'),
			Song(title='S2', yt_id='s2'),
			Song(title='S3', yt_id='s3')
		])
		prefetch_manager.prefetch_upcoming(queue, 0)

	def test_vivi_features(self):
		import gettext
		gettext.install('monophony')
		from monophony.yt import get_search_suggestions, get_radio, get_related
		from monophony.data import Artist, Song
		from monophony.ui.bars.search_bar import SearchBar
		from monophony.ui.bars.player_bar import PlayerBar
		from monophony.ui.queue_sidebar import QueueSidebar
		from monophony.ui.pages.artist_page import ArtistPage

		# Test search suggestions parsing
		sugg = get_search_suggestions('radiohead')
		assert(isinstance(sugg, dict))
		assert('queries' in sugg and 'items' in sugg)
		assert(len(sugg['queries']) > 0)
		assert(len(sugg['items']) > 0)

		# Test radio generation
		song = Song(title='Creep', yt_id='k4V3Mo61fJM', author=Artist(name='Radiohead', yt_id='UCurvRO5ud-B0sbgq8U-b07w'))
		radio = get_radio(seed_song=song)
		assert(isinstance(radio, dict))
		assert(len(radio.get('tracks', [])) > 0)

		# Test related endpoint
		rel = get_related('k4V3Mo61fJM')
		assert(isinstance(rel, dict))
		assert('songs' in rel and 'artists' in rel)

		# Test UI widgets
		sb = SearchBar()
		assert(sb is not None)

		pb = PlayerBar()
		assert(pb is not None)

		qs = QueueSidebar()
		assert(qs is not None)
		qs.update_radio_chips([{'title': 'Discover', 'params': 'abc', 'is_selected': True}])

		ap = ArtistPage([], None, artist=Artist(name='Radiohead', yt_id='UCurvRO5ud-B0sbgq8U-b07w'))
		assert(ap is not None)


class LogTestCase(BaseTestCase):
	def test_log_wrapper_and_ui(self):
		import logboth
		from gi.repository import Adw, Gio, GLib
		from monophony import log
		from monophony.ui.bars.header_bar import HeaderBar
		from monophony.ui.windows.log_window import LogWindow

		# 1. Test log capture
		log.clear_logs()
		logboth.info('test_source', 'Test info message for test_case')
		logboth.warning('test_source', 'Test warning message for test_case')
		print('Test print statement for test_case')

		logs = log.get_logs()
		assert(any('Test info message for test_case' in l for l in logs))
		assert(any('Test warning message for test_case' in l for l in logs))
		assert(any('Test print statement for test_case' in l for l in logs))

		# 2. Test HeaderBar menu button
		hb = HeaderBar()
		assert(hb is not None)
		assert(hb.props.child is not None)

		# 3. Test LogWindow creation and filter
		window = LogWindow()
		assert(window is not None)
		assert(window.props.title == 'Logs')
		assert(len(window._raw_lines) > 0)

		# Test filter
		window._filter_entry.set_text('warning message')
		window._on_filter_changed(window._filter_entry)
		filtered_text = window._buffer.get_text(
			window._buffer.get_start_iter(), window._buffer.get_end_iter(), False
		)
		assert('Test warning message for test_case' in filtered_text)
		assert('Test info message for test_case' not in filtered_text)

		# Cleanup
		window._on_closed(window)
		log.clear_logs()
		assert(len(log.get_logs()) == 0)


class StreamingAndSeamlessRadioTestCase(BaseTestCase):
	def test_prefetch_decoupled_from_active_song(self):
		from monophony.prefetch import prefetch_manager
		queue = Group(songs=[
			Song(title='S0', yt_id='s0'),
			Song(title='S1', yt_id='s1'),
			Song(title='S2', yt_id='s2'),
		])
		# Prefetch upcoming tracks starting after active song (index 0)
		# Should prefetch indices 1 and 2, never index 0
		prefetch_manager.prefetch_upcoming(queue, 0)

	def test_seamless_radio_transition(self):
		from monophony.player import Player
		from monophony.data import PlaybackState, PlaybackMode
		from unittest.mock import patch

		with patch('mprisify.Server.publish'):
			p = Player()
			song0 = Song(title='Track 0', yt_id='trk0')
			song1 = Song(title='Track 1', yt_id='trk1')
			p._queue = Group(title='Queue', songs=[song0, song1])
			p._queue_index = 0
			p.state = PlaybackState.PLAYING

			# Trigger radio with seed matching active song
			p.start_radio(song0)
			self.assertEqual(p.state, PlaybackState.PLAYING)
			self.assertEqual(p.mode, PlaybackMode.RADIO)

			# Mock task completion
			class DummyTask:
				cancelled = False
				extra_data = (song0, True)
				result = {
					'title': 'Radio (Track 0)',
					'tracks': [
						song0,
						Song(title='Radio Track 2', yt_id='r2'),
						Song(title='Radio Track 3', yt_id='r3')
					],
					'chips': [],
					'continuation': None
				}

				def is_canceled(self):
					return self.cancelled

				def is_running(self):
					return False

			dt = DummyTask()
			p._radio_task.cancel()
			p._radio_task = dt
			p._on_start_radio_done(dt)

			# Active song must remain at index 0, queue updated seamlessly
			self.assertEqual(len(p._queue.songs), 3)
			self.assertEqual(p._queue.songs[0].yt_id, 'trk0')
			self.assertEqual(p._queue.songs[1].yt_id, 'r2')
			self.assertEqual(p._queue.songs[2].yt_id, 'r3')
			self.assertEqual(p._queue_index, 0)
			self.assertEqual(p.state, PlaybackState.PLAYING)

			# When song ends or next() is called in PlaybackMode.RADIO:
			# Verify it moves to the next song without repeating the current one
			with patch.object(p, 'play') as mock_play:
				p.next()
				mock_play.assert_called_once_with(p._queue.songs[1], p._queue)

			# Now test when queue has ended and next() fetches radio:
			# It must NEVER replay the song that just ended!
			p._queue = Group(title='Queue', songs=[song0])
			p._queue_index = 0
			p.state = PlaybackState.PLAYING
			p.next()
			self.assertEqual(p.state, PlaybackState.LOADING)

			class DummyEndTask:
				cancelled = False
				extra_data = p._radio_task.extra_data
				result = {
					'title': 'Radio',
					'tracks': [
						song0,
						Song(title='Radio Next Track', yt_id='r_next'),
						Song(title='Radio Track 5', yt_id='r5')
					],
					'chips': [],
					'continuation': None
				}

				def is_canceled(self):
					return self.cancelled

				def is_running(self):
					return False

			end_task = DummyEndTask()
			p._radio_task.cancel()
			p._radio_task = end_task
			with patch.object(p, 'play') as mock_play:
				p._on_start_radio_done(end_task)
				mock_play.assert_called_once()
				played_song = mock_play.call_args[0][0]
				self.assertNotEqual(played_song.yt_id, song0.yt_id)
				self.assertEqual(played_song.yt_id, 'r_next')

	def test_fast_uri_extraction(self):
		from monophony import yt
		ydl = yt._get_ydl()
		self.assertIsNotNone(ydl)

	def test_fast_search_and_caching(self):
		from monophony import yt
		# Test fast parsing of album search item with load_tracks=False
		client = yt.get_yt_client(unauth=True)
		album_item = {
			'category': None,
			'resultType': 'album',
			'title': 'Test Album',
			'playlistId': 'OLAK5uy_test',
			'artists': [{'name': 'Test Artist', 'id': 'AR123'}],
			'thumbnails': [{'url': 'http://example.com/thumb.jpg'}]
		}
		res = yt._parse_single_result(client, album_item, load_tracks=False)
		self.assertIsNotNone(res)
		self.assertEqual(res.item.title, 'Test Album')
		self.assertEqual(res.item.yt_id, 'OLAK5uy_test')
		self.assertEqual(res.item.author.name, 'Test Artist')
		self.assertEqual(len(res.item.songs), 0)

		# Test search caching
		yt._set_cached_search('test:query:None', [res])
		cached = yt._get_cached_search('test:query:None')
		self.assertIsNotNone(cached)
		self.assertEqual(len(cached), 1)
		self.assertEqual(cached[0].item.title, 'Test Album')


class LikesAndHomeFeedsTestCase(BaseTestCase):
	def test_likes_management(self):
		from monophony import likes
		from monophony.data import Artist, Song

		# Reset cache in test env
		likes._cached_liked_group = None
		grp = likes.read()
		self.assertEqual(grp.yt_id, 'LM')
		self.assertFalse(likes.is_liked('test_vid_1'))

		notified = []
		def _on_changed():
			notified.append(True)

		likes.add_listener(_on_changed)

		song1 = Song(title='Liked Song 1', yt_id='test_vid_1', author=Artist(name='Artist 1'))
		# Toggle ON
		res1 = likes.toggle_like(song1)
		self.assertTrue(res1)
		self.assertTrue(likes.is_liked('test_vid_1'))
		self.assertEqual(len(likes.read().songs), 1)

		# Toggle OFF
		res2 = likes.toggle_like(song1)
		self.assertFalse(res2)
		self.assertFalse(likes.is_liked('test_vid_1'))
		self.assertEqual(len(likes.read().songs), 0)

		likes.remove_listener(_on_changed)

	def test_home_feeds_parsing(self):
		from monophony import yt
		from unittest.mock import MagicMock, patch

		mock_sections = [
			{
				'title': 'Quick picks',
				'contents': [
					{
						'title': 'Track One',
						'videoId': 'vid1',
						'artists': [{'name': 'Artist A', 'id': 'art1'}],
						'thumbnails': [{'url': 'http://img/1.jpg'}]
					}
				]
			},
			{
				'title': 'Featured playlists',
				'contents': [
					{
						'title': 'Playlist One',
						'playlistId': 'pl1',
						'artists': [{'name': 'Various'}],
						'thumbnails': [{'url': 'http://img/pl1.jpg'}]
					}
				]
			}
		]

		mock_client = MagicMock()
		mock_client.get_home.return_value = mock_sections

		with patch('monophony.yt.get_yt_client', return_value=mock_client):
			feeds = yt.get_home_feeds(limit=2)
			self.assertEqual(len(feeds), 2)
			self.assertEqual(feeds[0]['title'], 'Quick picks')
			self.assertEqual(len(feeds[0]['items']), 1)
			self.assertEqual(feeds[0]['items'][0].title, 'Track One')
			self.assertEqual(feeds[0]['items'][0].yt_id, 'vid1')

			self.assertEqual(feeds[1]['title'], 'Featured playlists')
			self.assertEqual(len(feeds[1]['items']), 1)
			self.assertEqual(feeds[1]['items'][0].title, 'Playlist One')
			self.assertEqual(feeds[1]['items'][0].yt_id, 'pl1')

	def test_lyrics_fetch(self):
		from monophony import yt
		from unittest.mock import MagicMock, patch

		mock_client = MagicMock()
		mock_client.get_lyrics.return_value = {
			'lyrics': 'Test lyrics text\nSecond line',
			'source': 'Source: Test'
		}

		with patch('monophony.yt.get_yt_client', return_value=mock_client), \
		     patch('monophony.yt.get_watch_next', return_value={'lyrics_browse_id': 'MPLYt_123'}):
			lyrics = yt.get_lyrics('dummy_vid', 'Test Title', 'Test Artist')
			self.assertIsNotNone(lyrics)
			self.assertEqual(lyrics['lyrics'], 'Test lyrics text\nSecond line')
			self.assertEqual(lyrics['source'], 'Source: Test')


class UIKeyboardAndLayoutTestCase(unittest.TestCase):
	'''Tests for keyboard navigation, button deduplication, and home page reordering.'''

	@classmethod
	def setUpClass(cls):
		import gi
		gi.require_version('Gtk', '4.0')
		gi.require_version('Adw', '1')
		from gi.repository import Gtk, Adw
		Gtk.init()

	def test_buttons_deduplication(self):
		from monophony.ui.bars.player_bar import PlayerBar
		from monophony.ui.queue_sidebar import QueueSidebar

		pb = PlayerBar()
		# PlayerBar should NOT have lyrics or start radio buttons
		self.assertFalse(hasattr(pb, '_lyrics_button'))
		self.assertFalse(hasattr(pb, '_radio_button'))

		qs = QueueSidebar()
		# QueueSidebar SHOULD have lyrics and start radio buttons
		self.assertTrue(hasattr(qs, '_lyrics_button'))
		self.assertTrue(hasattr(qs, '_radio_button'))

	def test_home_page_quick_picks_filtered(self):
		from monophony.data import Song, Artist
		from monophony.ui.pages.home_page import HomePage

		hp = HomePage()
		# Verify liked_group is not present on HomePage
		self.assertFalse(hasattr(hp, '_liked_group'))

		# Test quick picks and new releases filtering in update_home_feeds
		sample_song = Song(title='Song 1', yt_id='id1', author=Artist(name='Artist'))
		feeds = [
			{'title': 'Quick picks', 'items': [sample_song]},
			{'title': 'New releases', 'items': [sample_song]},
			{'title': 'Recently played', 'items': [sample_song]},
		]
		hp.update_home_feeds(feeds)
		# Only 'Recently played' should be included
		titles = [grp.props.title for grp in hp._home_feed_groups]
		self.assertNotIn('Quick picks', titles)
		self.assertNotIn('New releases', titles)
		self.assertIn('Recently played', titles)

	def test_scroll_vertical_methods(self):
		from monophony.ui.pages.page import Page
		from monophony.ui.queue_sidebar import QueueSidebar

		p = Page()
		self.assertTrue(callable(getattr(p, 'scroll_vertical', None)))

		qs = QueueSidebar()
		self.assertTrue(callable(getattr(qs, 'scroll_vertical', None)))

	def test_search_provider_results_and_prioritization(self):
		import time
		from unittest.mock import MagicMock, patch
		from monophony.search_provider import SearchProvider
		from monophony.data import Song, Group, Artist

		mock_app = MagicMock()
		sp = SearchProvider(mock_app)

		mock_items = [
			{'type': 'artist', 'title': 'Artist 1', 'subtitle': 'Artist', 'item': Artist(name='Artist 1')},
			{'type': 'album', 'title': 'Album 1', 'subtitle': 'Album', 'item': Group(title='Album 1', yt_id='alb1')},
			{'type': 'song', 'title': 'Song 1', 'subtitle': 'Artist 1', 'item': Song(title='Song 1', yt_id='s1')},
			{'type': 'song', 'title': 'Song 2', 'subtitle': 'Artist 1', 'item': Song(title='Song 2', yt_id='s2')},
			{'type': 'playlist', 'title': 'Playlist 1', 'subtitle': 'Playlist', 'item': Group(title='Playlist 1', yt_id='pl1')},
			{'type': 'song', 'title': 'Song 3', 'subtitle': 'Artist 1', 'item': Song(title='Song 3', yt_id='s3')},
		]

		with patch('monophony.yt.get_search_suggestions', return_value={'items': mock_items, 'queries': []}):
			from gi.repository import GLib
			invocation = MagicMock()
			sp._handle_search(['test', 'query'], invocation)
			time.sleep(0.05)
			for _ in range(20):
				GLib.MainContext.default().iteration(False)

			invocation.return_value.assert_called_once()
			variant = invocation.return_value.call_args[0][0]
			result_ids = variant.unpack()[0]

			# 1. First entry must be the search action
			self.assertEqual(result_ids[0], 'search:test query')

			# 2. Maximum 4 suggestions in total (total items <= 5)
			self.assertLessEqual(len(result_ids), 5)

			# 3. Songs are prioritized
			self.assertEqual(result_ids[1], 'song:s1')
			self.assertEqual(result_ids[2], 'song:s2')
			self.assertEqual(result_ids[3], 'song:s3')
			self.assertIn(result_ids[4], ('album:alb1', 'playlist:pl1'))

			# Test GetResultMetas
			meta_invoc = MagicMock()
			sp._handle_get_metas(result_ids, meta_invoc)
			meta_invoc.return_value.assert_called_once()
			metas_var = meta_invoc.return_value.call_args[0][0]
			metas = metas_var.unpack()[0]
			self.assertEqual(len(metas), len(result_ids))
			self.assertIn('Search "test query"', metas[0]['name'])
			self.assertEqual(metas[1]['name'], 'Song 1')

			# Test standalone activation via subprocess
			import shutil
			standalone_sp = SearchProvider()
			with patch('subprocess.Popen') as mock_popen:
				expected_cmd = shutil.which('monophony') or '/app/bin/monophony'
				standalone_sp._activate_result('search:coldplay', ['coldplay'])
				mock_popen.assert_called_with([expected_cmd, '--search', 'coldplay'])

				standalone_sp._activate_result('song:song123', [])
				mock_popen.assert_called_with([expected_cmd, '--play-song', 'song123'])

				standalone_sp._results_cache['song:song123'] = {'name': 'Viva La Vida', 'description': 'Coldplay • Song'}
				standalone_sp._activate_result('song:song123', [])
				mock_popen.assert_called_with([expected_cmd, '--play-song', 'song123', '--title', 'Viva La Vida', '--artist', 'Coldplay'])

				standalone_sp._activate_result('playlist:pl456', [])
				mock_popen.assert_called_with([expected_cmd, '--play-group', 'pl456'])

				standalone_sp._launch_search(['imagine', 'dragons'])
				mock_popen.assert_called_with([expected_cmd, '--search', 'imagine dragons'])

	def test_user_playlist_crud_and_tv_context(self):
		from unittest.mock import MagicMock, patch
		from monophony import yt

		# Test _tv_context
		mock_client = MagicMock()
		mock_client.context = {'context': {'client': {'clientName': 'WEB_REMIX', 'clientVersion': '1.0'}}}
		with yt._tv_context(mock_client):
			self.assertEqual(mock_client.context['context']['client']['clientName'], 'TVHTML5')
		self.assertEqual(mock_client.context['context']['client']['clientName'], 'WEB_REMIX')

		# Test _tv_context restores on exception
		try:
			with yt._tv_context(mock_client):
				raise RuntimeError('test exception')
		except RuntimeError:
			pass
		self.assertEqual(mock_client.context['context']['client']['clientName'], 'WEB_REMIX')

		# Test add_songs_to_user_playlist with TVHTML5 success
		with patch('monophony.yt.is_authenticated', return_value=True), \
		     patch('monophony.yt.get_yt_client', return_value=mock_client):
			mock_client.add_playlist_items.return_value = {'status': 'STATUS_SUCCEEDED'}
			success = yt.add_songs_to_user_playlist('PL123', ['s1', 's2'])
			self.assertTrue(success)
			mock_client.add_playlist_items.assert_called_with('PL123', ['s1', 's2'])

		# Test rate_song with TVHTML5
		with patch('monophony.yt.is_authenticated', return_value=True), \
		     patch('monophony.yt.get_yt_client', return_value=mock_client):
			success = yt.rate_song('s1', 'LIKE')
			self.assertTrue(success)
			mock_client.rate_song.assert_called_with('s1', 'LIKE')

	def test_get_artist_task_fallback(self):
		from unittest.mock import MagicMock, patch
		from monophony import yt

		task = yt.GetArtistTask(lambda *args: None)
		mock_auth = MagicMock()
		mock_auth.get_artist.side_effect = Exception("Server returned HTTP 400: Bad Request")
		mock_unauth = MagicMock()
		mock_unauth.get_artist.return_value = {
			'name': 'Fallback Artist',
			'channelId': 'UC123',
			'thumbnails': [],
			'songs': {
				'browseId': 'VLPL123',
				'results': [{
					'videoId': 'vid1',
					'title': 'Track 1',
					'artists': [{'name': 'Fallback Artist', 'id': 'UC123'}],
					'duration': '3:00',
					'thumbnails': []
				}]
			},
			'albums': {'results': []},
			'singles': {'results': []}
		}
		mock_unauth.get_playlist.return_value = {
			'tracks': [{
				'videoId': 'vid1',
				'title': 'Track 1',
				'artists': [{'name': 'Fallback Artist', 'id': 'UC123'}],
				'duration': '3:00',
				'thumbnails': []
			}]
		}

		def fake_get_yt_client(unauth=False):
			if unauth:
				return mock_unauth
			return mock_auth

		with patch('monophony.yt.get_yt_client', side_effect=fake_get_yt_client):
			res = task._function('UC123', '', 4)
			self.assertIsNotNone(res)
			self.assertEqual(len(res), 1)
			self.assertEqual(res[0].item.title, 'Track 1')
			self.assertEqual(res[0].item.author.name, 'Fallback Artist')
			mock_auth.get_artist.assert_called_once_with('UC123')
			mock_unauth.get_artist.assert_called_once_with('UC123')


if __name__ == '__main__':
	unittest.main()



