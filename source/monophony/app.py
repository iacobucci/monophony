'''Main application module.'''

import logboth
from monophony import ID
from monophony.ui.windows.main_window import MainWindow

from gi.repository import Adw, Gio


class Application(Adw.Application):
	'''Manages windows and application state on a high level.'''

	__gtype_name__ = __qualname__

	def __init__(self):
		'''Initialize without a window.'''
		super().__init__(
			application_id=ID,
			flags=Gio.ApplicationFlags.DEFAULT_FLAGS
		)
		self._window = None
		self._search_provider = None

	def do_startup(self):
		'''Run application startup and register D-Bus search provider.'''
		Adw.Application.do_startup(self)
		try:
			from monophony.search_provider import SearchProvider
			self._search_provider = SearchProvider(self)
			self._search_provider.register()
		except Exception as e:
			logboth.error(__name__, f'Failed to register SearchProvider: {e}')

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

	def _on_close_window(self, _action, _param):
		if self._window is not None:
			self._window._on_close()

	def _on_quit(self, _action, _param):
		logboth.info(__name__, 'Application quit requested')
		if self._search_provider is not None:
			self._search_provider.unregister()
			self._search_provider = None
		if self._window is not None:
			self._window.cleanup()
			self._window = None

		self.quit()
