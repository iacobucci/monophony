'''Artist page widget.'''

from monophony.data import Artist
from monophony.ui.pages.results_page import ResultsPage
from monophony.yt import SearchResult

from gi.repository import Gtk


class ArtistPage(ResultsPage):
	'''Artist page widget.'''

	__gtype_name__ = __qualname__

	def __init__(
		self,
		results: list[SearchResult],
		filter_: str | None,
		artist: Artist | None = None
	):
		'''Initialize the widget.'''
		super().__init__(results, filter_)

		self.artist = artist
		if artist and artist.name:
			self.props.title = artist.name
		else:
			self.props.title = _('Artist Page')

		if artist:
			radio_button = Gtk.Button.new_from_icon_name('audio-radio-symbolic')
			radio_button.props.tooltip_text = _('Start Artist Radio')
			radio_button.add_css_class('raised')
			radio_button.connect(
				'clicked',
				lambda _btn, ref: ref().emit('start-radio', self.artist) if ref() else None,
				self.weak_ref()
			)
			if hasattr(self, '_header_bar') and self._header_bar.props.child:
				self._header_bar.props.child.pack_end(radio_button)
