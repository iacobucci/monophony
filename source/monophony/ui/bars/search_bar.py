from gi.repository import Adw, GObject, Gtk


class SearchBar(Adw.Bin):
	__gtype_name__ = __qualname__

	def __init__(self):
		super().__init__()

		self._search_entry = Gtk.SearchEntry()
		self._search_entry.props.placeholder_text = _('Search...')
		self._search_entry.props.margin_start = 18
		self._search_entry.props.margin_end = 18
		self._search_entry.props.hexpand = True
		self._search_entry.props.halign = Gtk.Align.FILL
		self._search_entry.connect(
			'activate', lambda entry: self.emit('search', entry.props.text, '')
		)

		search_clamp = Adw.Clamp()
		search_clamp.props.maximum_size = 590
		search_clamp.props.child = self._search_entry

		search_bar = Adw.HeaderBar()
		search_bar.props.title_widget = search_clamp
		search_bar.props.show_back_button = False
		search_bar.props.show_start_title_buttons = False
		search_bar.props.show_end_title_buttons = False

		self.props.child = search_bar

	@GObject.Signal(name='search', arg_types=(str, str))
	def _search(self, _query: str, _filter: str):
		return

	def focus_search(self):
		self._search_entry.grab_focus()
