from monophony.ui.pages.page import Page

from gi.repository import Adw


class StatusPage(Page):
	__gtype_name__ = __qualname__

	def __init__(self, title: str, details: str, icon: str):
		super().__init__()

		status_page = Adw.StatusPage()
		status_page.props.title = title
		status_page.props.description = details
		status_page.props.icon_name = icon

		self._toolbar_view.props.content = status_page

		self.props.title = title
