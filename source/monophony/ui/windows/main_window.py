'''Main window.'''

import json
import os
import time
import traceback

from monophony import (
	DISPLAY_NAME,
	GRESOURCES_PATH,
	ID,
	MIN_WIDTH,
	NAME,
	__version__,
	downloads,
	recommendations,
	settings,
	yt,
)
from monophony.asynchronous import Task
from monophony.data import Artist, Group, Song
from monophony.downloads import DownloadTask
from monophony.player import Player
from monophony.playlists import SyncPlaylistsTask, UpdateExternalTask
from monophony.ui.bars.player_bar import PlayerBar
from monophony.ui.pages.artist_page import ArtistPage
from monophony.ui.pages.home_page import HomePage
from monophony.ui.pages.loading_page import LoadingPage
from monophony.ui.pages.results_page import ResultsPage
from monophony.ui.pages.status_page import StatusPage
from monophony.ui.queue_sidebar import QueueSidebar
from monophony.ui.windows.account_window import AccountWindow
from monophony.ui.windows.add_window import AddWindow
from monophony.ui.windows.import_window import ImportWindow
from monophony.ui.windows.message_window import MessageWindow
from monophony.ui.windows.settings_window import SettingsWindow

from monophony.yt import GetArtistTask, GetRecommendationsTask, SearchTask


import logboth
from gi.repository import Adw, Gio, GLib, GObject, Gtk


class PrepareHomePageTask(Task):
	'''Task for initializing the home page's contents.'''

	def _on_progress_update(self, task: Task, progress: float):
		if isinstance(task, GetRecommendationsTask):
			self._recommendations_progress = progress
		else:
			self._externals_update_progress = progress

		self._update_progress(
			(self._recommendations_progress + self._externals_update_progress) / 2
		)

	def _function(self):
		self._recommendations_progress = 0
		self._externals_update_progress = 0
		recommendations_task = GetRecommendationsTask(
			progress_callback=self._on_progress_update
		)
		update_task = UpdateExternalTask(
			progress_callback=self._on_progress_update
		)
		recommendations_task.start()
		update_task.start()

		if yt.is_authenticated() and settings.load('auto_sync_playlists', True):
			sync_task = SyncPlaylistsTask()
			sync_task.start()
			while sync_task.is_running():
				time.sleep(0.5)

		while recommendations_task.is_running() or update_task.is_running():
			time.sleep(0.5)

		result = recommendations_task.result
		if result:
			recommendations.write(result)



class MainWindow(Adw.ApplicationWindow):
	'''Main window.'''

	__gtype_name__ = __qualname__

	def __init__(self, **kwargs):
		'''Initialize the window.'''
		super().__init__(**kwargs)

		self._downloader = downloads.downloader
		self._downloader.clean_up()

		self._inhibit_suspend_cookie = 0
		self._last_search_query = None
		self._last_artist = None
		self._current_browsing_task = SearchTask()

		self._application = self.props.application
		self._application.hold()

		self._download_fail_window = MessageWindow(
			_('Download Failed'), _('Some songs could not be downloaded')
		)

		self._player = Player()
		self._player.connect(
			'recents-changed',
			lambda _player, ref:
				MainWindow._on_recents_changed(ref()),
			self.weak_ref()
		)
		self._player.connect(
			'queue-changed',
			lambda _player, queue, i, ref:
				MainWindow._on_queue_changed(ref(), queue, i),
			self.weak_ref()
		)
		self._player.connect(
			'progress-changed',
			lambda _player, progress, ref:
				MainWindow._on_progress_changed(ref(), progress),
			self.weak_ref()
		)
		self._player.connect(
			'buffering-changed',
			lambda _player, progress, ref:
				MainWindow._on_buffering_changed(ref(), progress),
			self.weak_ref()
		)
		self._player.connect(
			'state-changed',
			lambda _player, state, ref:
				MainWindow._on_state_changed(ref(), state),
			self.weak_ref()
		)
		self._player.connect(
			'volume-changed',
			lambda _player, volume, ref:
				MainWindow._on_volume_changed_in_backend(ref(), volume),
			self.weak_ref()
		)
		self._player.connect(
			'mode-changed',
			lambda _player, mode, ref:
				MainWindow._on_mode_changed_in_backend(ref(), mode),
			self.weak_ref()
		)
		self._player.connect(
			'pause-changed',
			lambda _player, pause, ref:
				MainWindow._on_pause_changed_in_backend(ref(), pause),
			self.weak_ref()
		)
		self._player.connect(
			'raise', lambda _player, ref: ref().present(), self.weak_ref()
		)

		self._queue_sidebar = QueueSidebar()
		self._queue_sidebar.connect(
			'play',
			lambda _sidebar, song, _group, ref, player_ref:
				MainWindow._on_play(ref(), song, player_ref().get_queue()),
			self.weak_ref(),
			self._player.weak_ref()
		)
		self._queue_sidebar.connect(
			'add-group-to',
			lambda _sidebar, _group, ref: MainWindow._on_add_queue_to(ref()),
			self.weak_ref()
		)
		self._queue_sidebar.connect(
			'add-song-to',
			lambda _sidebar, song, ref: MainWindow._on_add_song_to(ref(), song),
			self.weak_ref()
		)
		self._queue_sidebar.connect(
			'undownload-song',
			lambda _sidebar, song, ref:
				MainWindow._on_remove_song_from_downloads(ref(), song),
			self.weak_ref()
		)
		self._queue_sidebar.connect(
			'download-song',
			lambda _sidebar, song, ref:
				MainWindow._on_download_songs(ref(), Group(songs=[song])),
			self.weak_ref()
		)
		self._queue_sidebar.connect(
			'move-song',
			lambda _sidebar, from_s, to_s, ref:
				MainWindow._on_queue_move_song(ref(), from_s, to_s),
			self.weak_ref()
		)
		self._queue_sidebar.connect(
			'unqueue-song',
			lambda _sidebar, song, ref: MainWindow._on_remove_from_queue(ref(), song),
			self.weak_ref()
		)
		self._queue_sidebar.connect(
			'view-artist',
			lambda _sidebar, artist, ref:
				MainWindow._on_view_artist(ref(), artist, True),
			self.weak_ref()
		)
		self._queue_sidebar.connect(
			'clear-queue',
			lambda _sidebar, ref: MainWindow._on_clear_queue(ref()),
			self.weak_ref()
		)
		self._queue_sidebar.connect(
			'shuffle-queue',
			lambda _sidebar, ref: MainWindow._on_shuffle_queue(ref()),
			self.weak_ref()
		)
		self._queue_sidebar.hide_button.connect(
			'clicked',
			lambda _b, ref: MainWindow._on_hide_sidebar(ref()),
			self.weak_ref()
		)

		self._home_page = HomePage()
		self._home_page.connect(
			'play',
			lambda _page, song, group, ref: MainWindow._on_play(ref(), song, group),
			self.weak_ref()
		)
		self._home_page.connect(
			'queue-group',
			lambda _page, group, ref: MainWindow._on_add_to_queue(ref(), group),
			self.weak_ref()
		)
		self._home_page.connect(
			'queue-song',
			lambda _page, song, ref:
				MainWindow._on_add_to_queue(ref(), Group(songs=[song])),
			self.weak_ref()
		)
		self._home_page.connect(
			'add-song-to',
			lambda _page, song, ref: MainWindow._on_add_song_to(ref(), song),
			self.weak_ref()
		)
		self._home_page.connect(
			'view-artist',
			lambda _page, artist, ref: MainWindow._on_view_artist(ref(), artist, True),
			self.weak_ref()
		)
		self._home_page.connect(
			'undownload-song',
			lambda _page, song, ref:
				MainWindow._on_remove_song_from_downloads(ref(), song),
			self.weak_ref()
		)
		self._home_page.connect(
			'download-song',
			lambda _page, song, ref:
				MainWindow._on_download_songs(ref(), Group(songs=[song])),
			self.weak_ref()
		)
		self._home_page.connect(
			'add-group-to',
			lambda _page, group, ref: MainWindow._on_add_group_to(ref(), group),
			self.weak_ref()
		)
		self._home_page.connect(
			'download-group',
			lambda _page, group, ref: MainWindow._on_download_songs(ref(), group),
			self.weak_ref()
		)
		self._home_page.connect(
			'import-group',
			lambda _page, group, ref: MainWindow._on_import_group(ref(), group),
			self.weak_ref()
		)
		self._home_page.connect(
			'search',
			lambda _page, query, filter_, ref:
				MainWindow._on_search(ref(), query, filter_),
			self.weak_ref()
		)
		self._home_page.connect(
			'show-about',
			lambda _page, ref: MainWindow._on_show_about(ref()),
			self.weak_ref()
		)
		self._home_page.connect(
			'show-account',
			lambda _page, ref: MainWindow._on_show_account(ref()),
			self.weak_ref()
		)
		self._home_page.connect(
			'show-settings',
			lambda _page, ref: MainWindow._on_show_settings(ref()),
			self.weak_ref()
		)
		self._home_page.update_downloads(self._downloader.get_downloads())

		loading_page = LoadingPage()
		loading_page.connect(
			'show-about',
			lambda _page, ref: MainWindow._on_show_about(ref()),
			self.weak_ref()
		)
		loading_page.connect(
			'show-account',
			lambda _page, ref: MainWindow._on_show_account(ref()),
			self.weak_ref()
		)
		loading_page.connect(
			'show-settings',
			lambda _page, ref: MainWindow._on_show_settings(ref()),
			self.weak_ref()
		)



		self._navigation_view = Adw.NavigationView()
		self._navigation_view.connect(
			'popped',
			lambda _view, page, ref: MainWindow._on_page_popped(ref(), page),
			self.weak_ref()
		)
		self._navigation_view.add(loading_page)

		self._player_bar = PlayerBar()
		self._player_bar.connect(
			'mode-changed',
			lambda _bar, mode, ref:
				MainWindow._on_mode_changed_in_frontend(ref(), mode),
			self.weak_ref()
		)
		self._player_bar.connect(
			'next-song',
			lambda _bar, ref: MainWindow._on_next_song(ref()),
			self.weak_ref()
		)
		self._player_bar.connect(
			'previous-song',
			lambda _bar, ref: MainWindow._on_previous_song(ref()),
			self.weak_ref()
		)
		self._player_bar.connect(
			'seek',
			lambda _bar, value, ref:
				MainWindow._on_seek(ref(), value),
			self.weak_ref()
		)
		self._player_bar.connect(
			'volume-changed',
			lambda _bar, volume, ref:
				MainWindow._on_volume_changed_in_frontend(ref(), volume),
			self.weak_ref()
		)
		self._player_bar.connect(
			'pause',
			lambda _bar, ref: MainWindow._on_pause_changed_in_frontend(ref()),
			self.weak_ref()
		)

		self._toolbar_view = Adw.ToolbarView()
		self._toolbar_view.props.content = self._navigation_view
		self._toolbar_view.props.reveal_bottom_bars = False
		self._toolbar_view.add_bottom_bar(self._player_bar)

		self._split_view = Adw.OverlaySplitView()
		self._split_view.props.content = self._toolbar_view
		self._split_view.props.sidebar = self._queue_sidebar
		self._split_view.props.min_sidebar_width = MIN_WIDTH
		self._split_view.bind_property(
			'show-sidebar',
			self._player_bar.queue_button,
			'active',
			GObject.BindingFlags.BIDIRECTIONAL |
			GObject.BindingFlags.SYNC_CREATE
		)
		self._split_view.bind_property(
			'collapsed',
			self._player_bar.queue_button,
			'visible',
			GObject.BindingFlags.BIDIRECTIONAL |
			GObject.BindingFlags.SYNC_CREATE
		)
		self._split_view.bind_property(
			'collapsed',
			self._queue_sidebar.hide_button,
			'visible',
			GObject.BindingFlags.BIDIRECTIONAL |
			GObject.BindingFlags.SYNC_CREATE
		)

		view_breakpoint = Adw.Breakpoint()
		view_breakpoint.props.condition = Adw.BreakpointCondition.parse(
			'max-width: 700'
		)
		view_breakpoint.add_setter(self._split_view, 'collapsed', True)

		focus_search_action = Gio.SimpleAction.new('focus-search', None)
		focus_search_action.connect('activate', self._on_focus_search)
		self.add_action(focus_search_action)

		self.props.title = DISPLAY_NAME
		self.props.icon_name = ID
		self.props.content = self._split_view
		self.props.width_request = MIN_WIDTH
		self.props.height_request = MIN_WIDTH
		self.set_default_size(
			int(settings.load('window-width', 720)),
			int(settings.load('window-height', 600))
		)
		self.connect('close-request', MainWindow._on_close)
		self.add_breakpoint(view_breakpoint)

		self._current_browsing_task = PrepareHomePageTask(
			progress_callback=self._on_loading_progress,
			callback=self._on_home_page_prepared
		)
		self._current_browsing_task.start()
		self._on_volume_changed_in_backend(self._player.get_volume())
		self._on_mode_changed_in_backend(self._player.mode)

	def _inhibit_suspend(self):
		self._uninhibit_suspend()
		self._inhibit_suspend_cookie = self._application.inhibit(
			self,
			Gtk.ApplicationInhibitFlags.SUSPEND,
			_('Playing')
		)

	def _uninhibit_suspend(self):
		if self._inhibit_suspend_cookie != 0:
			self._application.uninhibit(self._inhibit_suspend_cookie)
			self._inhibit_suspend_cookie = 0

	def _update_external_playlists(self):
		self._home_page.update_external_playlists()

	def _update_playlists(self):
		self._home_page.update_playlists()

	def _update_downloads(self):
		self._queue_sidebar.update_download_status()
		for page in self._navigation_view.props.navigation_stack:
			if not isinstance(page, LoadingPage):
				page.update_download_status()

		self._home_page.update_downloads(self._downloader.get_downloads())

	def _on_add_group_to(self, group: Group):
		add_window = AddWindow(group)
		add_window.connect(
			'closed',
			lambda window, ref: MainWindow._on_add_window_closed(ref(), window),
			self.weak_ref()
		)
		add_window.present(self)

	def _on_add_song_to(self, song: Song):
		add_window = AddWindow(Group(songs=[song]))
		add_window.connect(
			'closed',
			lambda _window, ref: MainWindow._update_playlists(ref()),
			self.weak_ref()
		)
		add_window.present(self)

	def _on_add_queue_to(self):
		self._on_add_group_to(self._player.get_queue())

	def _on_add_to_queue(self, group: Group):
		self._player.add_to_queue(group)

	def _on_add_window_closed(self, window: AddWindow):
		if window.did_anything:
			self._update_playlists()

	def _on_buffering_changed(self, progress: float):
		self._player_bar.update_buffering(progress)

	def _on_clear_queue(self):
		self._player.stop()

	def _on_close(self) -> bool:
		logboth.info(__name__, 'Close requested')
		if self._player.get_queue().songs:
			logboth.info(__name__, 'Still playing - hiding instead of closing')
			self.props.visible = False
			return True

		size = self.get_default_size()
		settings.save({
			'window-width': size.width,
			'window-height': size.height
		})
		self._application.release()
		return False

	def _on_download_songs(self, group: Group):
		DownloadTask(
			progress_callback=self._on_download_status_changed,
			callback=self._on_download_finished,
			args=(
				self._downloader,
				group
			)
		).start()

	def _on_download_finished(self, task: DownloadTask):
		self._on_download_status_changed(task)
		if not task.result:
			self._download_fail_window.present(self)

	def _on_download_status_changed(self, _task: DownloadTask | None=None):
		# Never canceled
		self._update_downloads()

	def _on_home_page_prepared(self, _task: PrepareHomePageTask):
		self._navigation_view.replace([self._home_page])
		self._update_external_playlists()
		self._update_playlists()
		self._home_page.update_recommendations()


	def _on_filter_artist(self, filter_: str):
		if isinstance(
			self._navigation_view.get_previous_page(
				self._navigation_view.get_visible_page()
			),
			ArtistPage
		):
			self._navigation_view.pop()
		self._on_view_artist(self._last_artist, False, filter_)

	def _on_filter_results(self, filter_: str):
		if isinstance(
			self._navigation_view.get_previous_page(
				self._navigation_view.get_visible_page()
			),
			ResultsPage
		):
			self._navigation_view.pop()
		self._on_search(self._last_search_query, filter_)

	def _on_focus_search(self, _action, _param):
		self._home_page.focus_search()

	def _on_hide_sidebar(self):
		self._split_view.props.show_sidebar = False

	def _on_import_group(self, group: Group):
		import_window = ImportWindow(group)
		import_window.connect(
			'import',
			lambda _window, ref: MainWindow._on_import_success(ref()),
			self.weak_ref()
		)
		import_window.connect(
			'import-failed',
			lambda _window, ref:
				MessageWindow(
					_('Failed to Import'),
					_('Check your internet connection and try again')
				).present(ref()),
			self.weak_ref()
		)
		import_window.present(self)

	def _on_import_success(self):
		self._update_playlists()
		self._update_external_playlists()

	def _on_loading_progress(self, task: Task, progress: float):
		if task.is_canceled() or task is not self._current_browsing_task:
			logboth.info(
				__name__, f'Ignoring progress update "{progress}" from canceled task'
			)
			return

		page = self._navigation_view.props.visible_page
		if not isinstance(page, LoadingPage):
			logboth.info(
				__name__, f'Ignoring progress update "{progress}" as loading is done'
			)
			return

		page.update_progress(progress)

	def _on_mode_changed_in_backend(self, mode: int):
		self._player_bar.update_mode(mode)

	def _on_mode_changed_in_frontend(self, mode: int):
		self._player.set_mode(mode)

	def _on_next_song(self):
		self._player.next(from_user=True)

	def _on_page_popped(self, page: Adw.NavigationPage):
		if isinstance(page, LoadingPage):
			self._current_browsing_task.cancel()

		if isinstance(self._navigation_view.get_visible_page(), LoadingPage):
			self._navigation_view.pop()

	def _on_pause_changed_in_backend(self, pause: bool):
		if pause:
			self._uninhibit_suspend()
		else:
			self._inhibit_suspend()

		self._player_bar.update_pause(pause)

	def _on_pause_changed_in_frontend(self):
		self._player.set_pause(not self._player.paused)

	def _on_play(self, song: Song, group: Group):
		self._player.play(song, group)

	def _on_previous_song(self):
		self._player.previous()

	def _on_queue_move_song(self, song: Song, to_song: Song):
		self._player.move_song(song, to_song)

	def _on_recents_changed(self):
		self._home_page.update_history()

	def _on_remove_from_queue(self, song: Song):
		self._player.remove_from_queue(song)

	def _on_remove_song_from_downloads(self, song: Song):
		self._downloader.remove(song)
		self._update_downloads()

	def _on_search(self, query: str, filter_: str=''):
		query = query.strip()
		if not query:
			return

		self._last_search_query = query

		loading_page = LoadingPage()
		loading_page.connect(
			'show-about',
			lambda _page, ref: MainWindow._on_show_about(ref()),
			self.weak_ref()
		)
		self._navigation_view.push(loading_page)

		logboth.info(__name__, f'Searching for "{query}" with filter "{filter_}"...')

		self._current_browsing_task.cancel()
		self._current_browsing_task = SearchTask(
			progress_callback=self._on_loading_progress,
			callback=self._on_search_finished,
			args=(
				query, filter_, None if filter_ else 4
			)
		)
		self._current_browsing_task.extra_data = filter_
		self._current_browsing_task.start()

	def _on_search_finished(self, task: SearchTask):
		if task.is_canceled() or self._current_browsing_task is not task:
			logboth.info(__name__, 'Ignoring callback from canceled search task')
			return

		filter_ = task.extra_data
		results = task.result
		if isinstance(self._navigation_view.get_visible_page(), LoadingPage):
			self._navigation_view.pop()

		page = None
		if results is None:
			logboth.error(__name__, 'Failed to search')
			page = StatusPage(
				_('Failed to Search'),
				_('Check your internet connection and try again'),
				'dialog-error-symbolic'
			)
		elif results == []:
			logboth.warning(__name__, 'Done searching, no results')
			page = StatusPage(
				_('No Results'),
				_('Try searching for something else'),
				'dialog-information-symbolic'
			)
		else:
			logboth.info(__name__, 'Done searching')
			page = ResultsPage(results, filter_)
			page.connect(
				'play',
				lambda _page, song, group, ref: MainWindow._on_play(ref(), song, group),
				self.weak_ref()
			)
			page.connect(
				'filter-results',
				lambda _page, filter_, ref:
					MainWindow._on_filter_results(ref(), filter_),
				self.weak_ref()
			)
			page.connect(
				'queue-song',
				lambda _page, song, ref:
					MainWindow._on_add_to_queue(ref(), Group(songs=[song])),
				self.weak_ref()
			)
			page.connect(
				'add-song-to',
				lambda _page, song, ref: MainWindow._on_add_song_to(ref(), song),
				self.weak_ref()
			)
			page.connect(
				'undownload-song',
				lambda _page, song, ref:
					MainWindow._on_remove_song_from_downloads(ref(), song),
				self.weak_ref()
			)
			page.connect(
				'download-song',
				lambda _page, song, ref:
					MainWindow._on_download_songs(ref(), Group(songs=[song])),
				self.weak_ref()
			)
			page.connect(
				'queue-group',
				lambda _page, group, ref: MainWindow._on_add_to_queue(ref(), group),
				self.weak_ref()
			)
			page.connect(
				'add-group-to',
				lambda _page, group, ref: MainWindow._on_add_group_to(ref(), group),
				self.weak_ref()
			)
			page.connect(
				'download-group',
				lambda _page, group, ref: MainWindow._on_download_songs(ref(), group),
				self.weak_ref()
			)
			page.connect(
				'import-group',
				lambda _page, group, ref: MainWindow._on_import_group(ref(), group),
				self.weak_ref()
			)
			page.connect(
				'view-artist',
				lambda _page, artist, ref:
					MainWindow._on_view_artist(ref(), artist, True),
				self.weak_ref()
			)

		page.connect(
			'show-about',
			lambda _page, ref: MainWindow._on_show_about(ref()),
			self.weak_ref()
		)
		page.connect(
			'show-account',
			lambda _page, ref: MainWindow._on_show_account(ref()),
			self.weak_ref()
		)
		page.connect(
			'show-settings',
			lambda _page, ref: MainWindow._on_show_settings(ref()),
			self.weak_ref()
		)
		self._navigation_view.push(page)

	def _on_seek(self, value: float):
		self._player.seek(value)

	def _on_show_account(self):
		account_dialog = AccountWindow()
		account_dialog.connect(
			'sync-finished',
			lambda _dlg, ref: ref()._home_page.update_playlists(),
			self.weak_ref()
		)
		account_dialog.present(self)

	def _on_show_settings(self):
		settings_dialog = SettingsWindow()
		settings_dialog.present(self)


	def _on_show_about(self):

		about_dialog = Adw.AboutDialog.new_from_appdata(
			GRESOURCES_PATH + '/metainfo.xml', __version__
		)
		about_dialog.props.debug_info = logboth.read()
		about_dialog.props.debug_info_filename = 'log.txt'
		about_dialog.props.translator_credits = _('translator-credits')
		about_dialog.props.copyright = 'Copyright © Zehkira and contributors'
		about_dialog.add_link(
			_('Donate'), 'https://zeh-kira.itch.io/monophony/purchase'
		)

		spdx_licenses = {
			'': Gtk.License.CUSTOM,
			'GPL-2.0-or-later': Gtk.License.GPL_2_0,
			'GPL-3.0-or-later': Gtk.License.GPL_3_0,
			'LGPL-2.1-or-later': Gtk.License.LGPL_2_1,
			'LGPL-3.0-or-later': Gtk.License.LGPL_3_0,
			'BSD-2-Clause': Gtk.License.BSD,
			'MIT': Gtk.License.MIT_X11,
			'Artistic-2.0': Gtk.License.ARTISTIC,
			'GPL-2.0-only': Gtk.License.GPL_2_0_ONLY,
			'GPL-3.0-only': Gtk.License.GPL_3_0_ONLY,
			'LGPL-2.1-only': Gtk.License.LGPL_2_1_ONLY,
			'LGPL-3.0-only': Gtk.License.LGPL_3_0_ONLY,
			'AGPL-3.0-or-later': Gtk.License.AGPL_3_0,
			'AGPL-3.0-only': Gtk.License.AGPL_3_0_ONLY,
			'BSD-3-Clause': Gtk.License.BSD_3,
			'Apache-2.0': Gtk.License.APACHE_2_0,
			'MPL-2.0': Gtk.License.MPL_2_0,
			'0BSD': getattr(Gtk.License, '0BSD')
		}

		licenses_data = []
		logboth.info(__name__, 'Loading licenses...')
		for path in os.getenv('XDG_DATA_DIRS', '/usr/share/').split(':'):
			file_path = f'{path}{"" if path.endswith("/") else "/"}{NAME}/licenses.json'
			logboth.info(__name__, f'Trying to load licenses from "{file_path}"...')
			try:
				with open(file_path) as licenses_file:
					licenses_data = json.load(licenses_file)
					logboth.info(
						__name__, f'Loaded licenses from "{file_path}"'
					)
					break
			except OSError:
				continue
			except json.decoder.JSONDecodeError:
				logboth.error(
					__name__, 'Failed to load licenses', traceback.format_exc()
				)
				break
		else:
			logboth.error(__name__, 'Failed to load licenses file: not found')

		for data in licenses_data:
			about_dialog.add_legal_section(
				GLib.markup_escape_text(data['name'], -1),
				GLib.markup_escape_text(data['copyright'], -1),
				spdx_licenses[data['license']],
				GLib.markup_escape_text(data['text'], -1)
			)

		about_dialog.present(self)

	def _on_shuffle_queue(self):
		self._player.shuffle()

	def _on_progress_changed(self, progress: float):
		self._player_bar.update_progress(progress)

	def _on_queue_changed(self, queue: Group, song_index: int):
		self._queue_sidebar.update_contents(queue, song_index)
		if not queue.songs:
			self._toolbar_view.props.reveal_bottom_bars = False
			self._uninhibit_suspend()
			if not self.props.visible:
				logboth.info(__name__, 'Playback ended while window hidden')
				self.close()
			return

		self._toolbar_view.props.reveal_bottom_bars = True
		self._inhibit_suspend()
		self._player_bar.update_song(queue.songs[song_index])

	def _on_state_changed(self, state: int):
		self._player_bar.update_state(state)

	def _on_view_artist(self, artist: Artist, replace_page: bool, filter_: str=''):
		self._last_artist = artist

		if (
			replace_page and
			isinstance(
				self._navigation_view.get_visible_page(), ArtistPage | StatusPage
			)
		):
			self._navigation_view.pop()

		loading_page = LoadingPage()
		loading_page.connect(
			'show-about',
			lambda _page, ref: MainWindow._on_show_about(ref()),
			self.weak_ref()
		)
		self._navigation_view.push(loading_page)

		logboth.info(__name__, f'Showing artist "{artist.yt_id}"...')
		self._current_browsing_task.cancel()
		self._current_browsing_task = GetArtistTask(
			progress_callback=self._on_loading_progress,
			callback=self._on_view_artist_finished,
			args=(
				artist.yt_id, filter_, None if filter_ else 4
			)
		)
		self._current_browsing_task.extra_data = filter_
		self._current_browsing_task.start()

	def _on_view_artist_finished(self, task: GetArtistTask):
		if task.is_canceled() or self._current_browsing_task is not task:
			logboth.info(__name__, 'Ignoring callback from canceled view artist task')
			return

		results = task.result
		filter_ = task.extra_data
		if isinstance(self._navigation_view.get_visible_page(), LoadingPage):
			self._navigation_view.pop()

		page = None
		if results is None:
			logboth.error(__name__, 'Failed to load artist page')
			page = StatusPage(
				_('Failed to Load Artist Page'),
				_('Check your internet connection and try again'),
				'dialog-error-symbolic'
			)
		elif results == []:
			logboth.warning(__name__, 'Loaded empty artist page')
			page = StatusPage(
				_('Empty Artist Page'),
				_('No content found from this artist'),
				'dialog-information-symbolic'
			)
		else:
			logboth.info(__name__, 'Loaded artist page')
			page = ArtistPage(results, filter_)
			page.connect(
				'play',
				lambda _page, song, group, ref: MainWindow._on_play(ref(), song, group),
				self.weak_ref()
			)
			page.connect(
				'filter-results',
				lambda _page, filter_, ref:
					MainWindow._on_filter_artist(ref(), filter_),
				self.weak_ref()
			)
			page.connect(
				'queue-song',
				lambda _page, song, ref:
					MainWindow._on_add_to_queue(ref(), Group(songs=[song])),
				self.weak_ref()
			)
			page.connect(
				'add-song-to',
				lambda _page, song, ref: MainWindow._on_add_song_to(ref(), song),
				self.weak_ref()
			)
			page.connect(
				'undownload-song',
				lambda _page, song, ref:
					MainWindow._on_remove_song_from_downloads(ref(), song),
				self.weak_ref()
			)
			page.connect(
				'download-song',
				lambda _page, song, ref:
					MainWindow._on_download_songs(ref(), Group(songs=[song])),
				self.weak_ref()
			)
			page.connect(
				'queue-group',
				lambda _page, group, ref: MainWindow._on_add_to_queue(ref(), group),
				self.weak_ref()
			)
			page.connect(
				'add-group-to',
				lambda _page, group, ref: MainWindow._on_add_group_to(ref(), group),
				self.weak_ref()
			)
			page.connect(
				'download-group',
				lambda _page, group, ref: MainWindow._on_download_songs(ref(), group),
				self.weak_ref()
			)
			page.connect(
				'import-group',
				lambda _page, group, ref: MainWindow._on_import_group(ref(), group),
				self.weak_ref()
			)
			page.connect(
				'view-artist',
				lambda _page, artist, ref:
					MainWindow._on_view_artist(ref(), artist, True),
				self.weak_ref()
			)

		page.connect(
			'show-about',
			lambda _page, ref: MainWindow._on_show_about(ref()),
			self.weak_ref()
		)
		self._navigation_view.push(page)

	def _on_volume_changed_in_backend(self, volume: float):
		self._player_bar.update_volume(volume)

	def _on_volume_changed_in_frontend(self, volume: float):
		self._player.set_volume(volume, notify_frontend=False)

	def present(self):
		'''Present the window.'''
		logboth.info(__name__, 'Presenting window')
		super().present()
