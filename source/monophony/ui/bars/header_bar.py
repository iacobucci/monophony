'''Header bar widget.'''

from monophony.debug import MemoryDebugger

from gi.repository import Adw, GObject, Gtk


class HeaderBar(MemoryDebugger, Adw.Bin):
	'''Header bar widget with "about", "account", and "settings" buttons.'''

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

		about_button = Gtk.Button.new_from_icon_name('help-about-symbolic')
		about_button.props.tooltip_text = _('About')
		about_button.connect(
			'clicked',
			lambda _button, ref: ref().emit('show-about'),
			self.weak_ref()
		)

		header_bar = Adw.HeaderBar()
		header_bar.pack_end(about_button)
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


