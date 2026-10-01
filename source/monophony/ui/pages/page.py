'''Page widget.'''

from monophony.debug import MemoryDebugger
from monophony.ui.bars.header_bar import HeaderBar

from gi.repository import Adw, GObject, Gtk


class Page(MemoryDebugger, Adw.NavigationPage):
	'''Page widget with header bar, toast overlay and toolbar view.

	Inherit from this instead of using it directly.
	'''

	__gtype_name__ = __qualname__

	def __init__(self):
		'''Initialize the widget.'''
		super().__init__()

		# Must hold reference, otherwise the bar's weakref to self fails
		self._header_bar = HeaderBar()
		self._header_bar.connect(
			'show-about',
			lambda _bar, ref: ref().emit('show-about'),
			self.weak_ref()
		)
		self._header_bar.connect(
			'show-account',
			lambda _bar, ref: ref().emit('show-account'),
			self.weak_ref()
		)
		self._header_bar.connect(
			'show-settings',
			lambda _bar, ref: ref().emit('show-settings'),
			self.weak_ref()
		)
		self._header_bar.connect(
			'show-logs',
			lambda _bar, ref: ref().emit('show-logs'),
			self.weak_ref()
		)

		self._page = Adw.PreferencesPage()

		self._toolbar_view = Adw.ToolbarView()
		self._toolbar_view.props.top_bar_style = Adw.ToolbarStyle.RAISED
		self._toolbar_view.props.bottom_bar_style = Adw.ToolbarStyle.RAISED
		self._toolbar_view.props.content = self._page
		self._toolbar_view.add_top_bar(self._header_bar)

		self._toast_overlay = Adw.ToastOverlay()
		self._toast_overlay.props.child = self._toolbar_view

		self.props.child = self._toast_overlay

	def scroll_vertical(self, direction_down: bool, page_step: bool = False) -> bool:
		'''Scroll the preferences page vertically.

		:param direction_down: True to scroll down, False to scroll up.
		:param page_step: True to scroll by page, False to scroll by small step.
		:return: True if scrolled, False otherwise.
		'''
		scrolled = self._page.get_first_child()
		if not isinstance(scrolled, Gtk.ScrolledWindow):
			return False
		adj = scrolled.get_vadjustment()
		if not adj:
			return False
		step = (adj.get_page_size() * 0.8) if page_step else 70.0
		val = adj.get_value() + (step if direction_down else -step)
		max_val = max(adj.get_lower(), adj.get_upper() - adj.get_page_size())
		val = max(adj.get_lower(), min(val, max_val))
		adj.set_value(val)
		return True

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


