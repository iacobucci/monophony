'''Status page widget.'''

from monophony.ui.pages.page import Page

from gi.repository import Adw


class StatusPage(Page):
	'''Status page widget.'''

	__gtype_name__ = __qualname__

	def __init__(self, title: str, details: str, icon: str):
		'''Initialize the widget with a title, details and an icon.

		The icon must exist in the specific version of the icon theme shipped along with
		the app. Otherwise the icon will not be displayed on some systems.

		:param title: Page title.
		:param details: Additional information to display.
		:param icon: Icon name.
		'''
		super().__init__()

		status_page = Adw.StatusPage()
		status_page.props.title = title
		status_page.props.description = details
		status_page.props.icon_name = icon

		self._toolbar_view.props.content = status_page

		self.props.title = title
