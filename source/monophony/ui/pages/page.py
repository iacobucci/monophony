'''Page widget.'''

from monophony.debug import MemoryDebugger
from monophony.ui.bars.header_bar import HeaderBar

from gi.repository import Adw, GObject


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

		self._page = Adw.PreferencesPage()

		self._toolbar_view = Adw.ToolbarView()
		self._toolbar_view.props.top_bar_style = Adw.ToolbarStyle.RAISED
		self._toolbar_view.props.bottom_bar_style = Adw.ToolbarStyle.RAISED
		self._toolbar_view.props.content = self._page
		self._toolbar_view.add_top_bar(self._header_bar)

		self._toast_overlay = Adw.ToastOverlay()
		self._toast_overlay.props.child = self._toolbar_view

		self.props.child = self._toast_overlay

	@GObject.Signal(name='show-about')
	def _show_about(self):
		return

	@GObject.Signal(name='show-account')
	def _show_account(self):
		return

	@GObject.Signal(name='show-settings')
	def _show_settings(self):
		return


