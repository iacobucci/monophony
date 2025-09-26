from monophony.ui.pages.page import Page

from gi.repository import Adw


class LoadingPage(Page):
	__gtype_name__ = __qualname__

	def __init__(self):
		super().__init__()

		spinner = Adw.SpinnerPaintable()

		self._status_page = Adw.StatusPage()
		self._status_page.props.paintable = spinner
		self._status_page.props.description = '0%'
		spinner.props.widget = self._status_page

		self._toolbar_view.props.content = self._status_page

		self.props.title = _('Loading...')

	def update_progress(self, progress: float):
		self._status_page.props.description = f'{int(progress * 100)}%'
