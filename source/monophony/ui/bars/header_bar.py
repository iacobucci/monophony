'''Header bar widget.'''

import gettext

from monophony.debug import MemoryDebugger

from gi.repository import Adw, Gio, GObject, Gtk

_ = gettext.gettext


class HeaderBar(MemoryDebugger, Adw.Bin):
	'''Header bar widget with "account", "settings", and "info & logs" buttons.'''

	__gtype_name__ = __qualname__

	def __init__(self):
		'''Initialize the widget.'''
		super().__init__()

		settings_button = Gtk.Button.new_from_icon_name('emblem-system-symbolic')
		settings_button.props.tooltip_text = _('Settings & Cache')
		settings_button.connect(
			'clicked',
			lambda _button, ref: ref().emit('show-settings'),
			self.weak_ref()
		)

		account_button = Gtk.Button.new_from_icon_name('avatar-default-symbolic')
		account_button.props.tooltip_text = _('YouTube Account & Sync')
		account_button.connect(
			'clicked',
			lambda _button, ref: ref().emit('show-account'),
			self.weak_ref()
		)

		info_menu = Gio.Menu()
		info_menu.append(_('Logs'), 'win.show-logs')
		info_menu.append(_('About Monophony'), 'win.show-about')

		info_button = Gtk.MenuButton()
		info_button.props.icon_name = 'help-about-symbolic'
		info_button.props.tooltip_text = _('Info & Logs')
		info_button.props.menu_model = info_menu

		header_bar = Adw.HeaderBar()
		header_bar.pack_end(info_button)
		header_bar.pack_end(settings_button)
		header_bar.pack_end(account_button)

		self.props.child = header_bar

	@GObject.Signal(name='show-about')
	def _show_about(self):
		return

	@GObject.Signal(name='show-account')
	def _show_account(self):
		return

	@GObject.Signal(name='show-settings')
	def _show_settings(self):
		return

	@GObject.Signal(name='show-logs')
	def _show_logs(self):
		return


