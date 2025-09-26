import weakref

from monophony.debug import MemoryDebugger

from gi.repository import Adw, GObject, Gtk


class HeaderBar(MemoryDebugger, Adw.Bin):
	__gtype_name__ = __qualname__

	def __init__(self):
		super().__init__()

		about_button = Gtk.Button.new_from_icon_name('help-about-symbolic')
		about_button.props.tooltip_text = _('About')
		about_button.connect(
			'clicked',
			lambda _button, ref: ref().emit('show-about'),
			weakref.ref(self)
		)

		header_bar = Adw.HeaderBar()
		header_bar.pack_end(about_button)

		self.props.child = header_bar

	@GObject.Signal(name='show-about')
	def _show_about(self):
		return
