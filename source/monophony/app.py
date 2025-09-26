from monophony import ID
from monophony.ui.windows.main_window import MainWindow

from gi.repository import Adw, Gio


class Application(Adw.Application):
	__gtype_name__ = __qualname__

	def __init__(self):
		super().__init__(
			application_id=ID,
			flags=Gio.ApplicationFlags.DEFAULT_FLAGS
		)
		self._window = None

	def do_activate(self):
		windows = self.get_windows()

		if len(windows) > 0:
			windows[0].props.visible = True
		else:
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

	def _on_close_window(self, _action, _param):
		windows = self.get_windows()
		if windows:
			windows[0].close()

	def _on_quit(self, _action, _param):
		if self._window:
			self._window.close()

		self.quit()
