from monophony.ui.pages.results_page import ResultsPage
from monophony.yt import SearchResult


class ArtistPage(ResultsPage):
	__gtype_name__ = __qualname__

	def __init__(self, results: list[SearchResult], filter_: str | None):
		super().__init__(results, filter_)

		self.props.title = _('Artist Page')
