'''Main application module.'''

import threading

import logboth
from monophony import ID
from monophony.ui.windows.main_window import MainWindow

from gi.repository import Adw, Gio, GLib


class Application(Adw.Application):
	'''Manages windows and application state on a high level.'''

	__gtype_name__ = __qualname__

	def __init__(self):
		'''Initialize without a window.'''
		super().__init__(
			application_id=ID,
			flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE
		)
		self._window = None

		self.add_main_option(
			'search',
			ord('s'),
			GLib.OptionFlags.NONE,
			GLib.OptionArg.STRING,
			'Search query',
			'QUERY'
		)
		self.add_main_option(
			'play-song',
			0,
			GLib.OptionFlags.NONE,
			GLib.OptionArg.STRING,
			'Play song by YouTube ID',
			'ID'
		)
		self.add_main_option(
			'play-group',
			0,
			GLib.OptionFlags.NONE,
			GLib.OptionArg.STRING,
			'Play album or playlist by YouTube ID',
			'ID'
		)
		self.add_main_option(
			'title',
			0,
			GLib.OptionFlags.NONE,
			GLib.OptionArg.STRING,
			'Title of item to play',
			'TITLE'
		)
		self.add_main_option(
			'artist',
			0,
			GLib.OptionFlags.NONE,
			GLib.OptionArg.STRING,
			'Artist of song to play',
			'ARTIST'
		)

	def do_startup(self):
		'''Run application startup.'''
		Adw.Application.do_startup(self)

	def do_activate(self):
		'''Raise a window if one exists, otherwise create one.'''
		if self._window is not None:
			logboth.info(__name__, 'Activating existing window from background...')
			self._window.present()
			return

		quit_action = Gio.SimpleAction.new('quit', None)
		quit_action.connect('activate', self._on_quit)
		self.add_action(quit_action)
		self.set_accels_for_action('app.quit', ['<Control>q'])

		close_window_action = Gio.SimpleAction.new('close-window', None)
		close_window_action.connect('activate', self._on_close_window)
		self.add_action(close_window_action)
		self.set_accels_for_action('app.close-window', ['<Control>w'])

		self._window = MainWindow(application=self)
		self._window.present()

		self.set_accels_for_action('win.focus-search', ['<Control>f'])
		self.set_accels_for_action('win.show-logs', ['<Control><Shift>l'])

	def do_command_line(self, command_line):
		'''Handle command-line options and activate the application.'''
		options = command_line.get_options_dict().end().unpack()
		self.activate()

		if self._window is not None:
			title = options.get('title', '')
			artist = options.get('artist', '')

			if 'search' in options:
				query = options['search']
				if query:
					self._window._on_search(query)
			elif 'play-song' in options:
				song_id = options['play-song']
				if song_id:
					self._play_song_by_id(song_id, title=title, artist=artist)
			elif 'play-group' in options:
				group_id = options['play-group']
				if group_id:
					self._play_group_by_id(group_id, title=title)
			else:
				args = command_line.get_arguments()
				if len(args) > 1 and not args[1].startswith('-'):
					query = ' '.join(args[1:])
					if query:
						self._window._on_search(query)

		return 0

	def _play_song_by_id(self, song_id: str, title: str = '', artist: str = ''):
		if not self._window:
			return
		from monophony.data import Artist, Group, Song

		if title:
			song = Song(
				title=title,
				author=Artist(name=artist) if artist else None,
				yt_id=song_id
			)
			self._window._on_play(song, Group(songs=[song]))
			return

		def _worker():
			from monophony import yt
			song = None
			try:
				song = yt.get_song(song_id)
			except Exception as e:
				logboth.warning(__name__, f'Failed to get song "{song_id}": {e}')
			if not song:
				song = Song(title=song_id, yt_id=song_id)
			GLib.idle_add(lambda: self._window._on_play(song, Group(songs=[song])) if self._window else None)

		threading.Thread(target=_worker, daemon=True).start()

	def _play_group_by_id(self, group_id: str, title: str = ''):
		if not self._window:
			return
		from monophony.data import Group
		group = Group(title=title, yt_id=group_id)
		self._window._on_play(None, group)

	def _on_close_window(self, _action, _param):
		if self._window is not None:
			self._window._on_close()

	def _on_quit(self, _action, _param):
		logboth.info(__name__, 'Application quit requested')
		if self._window is not None:
			self._window.cleanup()
			self._window = None

		self.quit()
