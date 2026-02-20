'''Artist page widget.'''

from monophony.ui.pages.results_page import ResultsPage
from monophony.yt import SearchResult


class ArtistPage(ResultsPage):
	'''Artist page widget.'''

	__gtype_name__ = __qualname__

	def __init__(self, results: list[SearchResult], filter_: str | None):
		'''Initialize the widget.'''
		super().__init__(results, filter_)

		self.props.title = _('Artist Page')
