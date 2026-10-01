'''Search bar widget with search suggestions.'''

from monophony.data import Artist, Group, Song
from monophony.yt import GetSearchSuggestionsTask

from gi.repository import Adw, Gdk, GLib, GObject, Gtk, Pango


class SearchBar(Adw.Bin):
	'''Search bar widget.'''

	__gtype_name__ = __qualname__

	def __init__(self):
		'''Initialize the widget.'''
		super().__init__()

		self._debounce_source_id: int | None = None
		self._suggestion_task: GetSearchSuggestionsTask | None = None

		self._search_entry = Gtk.SearchEntry()
		self._search_entry.props.placeholder_text = _('Search...')
		self._search_entry.props.margin_start = 18
		self._search_entry.props.margin_end = 18
		self._search_entry.props.hexpand = True
		self._search_entry.props.halign = Gtk.Align.FILL
		self._search_entry.connect(
			'activate', self._on_entry_activate
		)
		self._search_entry.connect(
			'search-changed', self._on_search_changed
		)

		key_controller = Gtk.EventControllerKey()
		key_controller.connect('key-pressed', self._on_entry_key_pressed)
		self._search_entry.add_controller(key_controller)

		self._list_box = Gtk.ListBox()
		self._list_box.props.selection_mode = Gtk.SelectionMode.SINGLE
		self._list_box.add_css_class('boxed-list')
		self._list_box.connect('row-activated', self._on_row_activated)

		list_key_controller = Gtk.EventControllerKey()
		list_key_controller.connect('key-pressed', self._on_list_key_pressed)
		self._list_box.add_controller(list_key_controller)

		self._popover_scroll = Gtk.ScrolledWindow()
		self._popover_scroll.props.hscrollbar_policy = Gtk.PolicyType.NEVER
		self._popover_scroll.props.vscrollbar_policy = Gtk.PolicyType.AUTOMATIC
		self._popover_scroll.props.max_content_height = 360
		self._popover_scroll.props.propagate_natural_height = True
		self._popover_scroll.props.min_content_width = 420
		self._popover_scroll.set_child(self._list_box)

		self._popover = Gtk.Popover()
		self._popover.set_parent(self._search_entry)
		self._popover.props.position = Gtk.PositionType.BOTTOM
		self._popover.props.autohide = True
		self._popover.props.has_arrow = False
		self._popover.set_child(self._popover_scroll)

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

	@GObject.Signal(name='play', arg_types=(object, object))
	def _play(self, _song: Song, _group: Group):
		return

	@GObject.Signal(name='view-artist', arg_types=(object,))
	def _view_artist(self, _artist: Artist):
		return

	def focus_search(self):
		'''Make the search entry grab input focus.'''
		self._search_entry.grab_focus()

	def _cancel_debounce(self):
		if self._debounce_source_id:
			GLib.source_remove(self._debounce_source_id)
			self._debounce_source_id = None

	def _cancel_task(self):
		if self._suggestion_task:
			self._suggestion_task.cancel()
			self._suggestion_task = None

	def _on_entry_activate(self, entry: Gtk.SearchEntry):
		self._cancel_debounce()
		self._cancel_task()
		self._popover.popdown()
		while child := self._list_box.get_first_child():
			self._list_box.remove(child)
		text = entry.props.text.strip()
		if text:
			self.emit('search', text, '')

	def _on_entry_key_pressed(self, _controller, keyval, _keycode, _state):
		if keyval == Gdk.KEY_Escape:
			self._cancel_debounce()
			self._cancel_task()
			self._popover.popdown()
			return True
		if keyval == Gdk.KEY_Down:
			if self._popover.get_visible():
				first_row = self._list_box.get_row_at_index(0)
				if first_row:
					self._list_box.select_row(first_row)
					first_row.grab_focus()
					return True
			else:
				root = self._search_entry.get_root()
				if root:
					root.child_focus(Gtk.DirectionType.DOWN)
					return True
		return False

	def _on_list_key_pressed(self, _controller, keyval, _keycode, _state):
		if keyval == Gdk.KEY_Escape:
			self._popover.popdown()
			self._search_entry.grab_focus()
			return True
		if keyval == Gdk.KEY_Up:
			selected = self._list_box.get_selected_row()
			if selected and selected.get_index() == 0:
				self._search_entry.grab_focus()
				return True
		return False

	def _on_search_changed(self, entry: Gtk.SearchEntry):
		self._cancel_debounce()
		query = entry.props.text.strip()
		if len(query) < 2:
			self._cancel_task()
			self._popover.popdown()
			while child := self._list_box.get_first_child():
				self._list_box.remove(child)
			return

		self._debounce_source_id = GLib.timeout_add(
			250, self._fetch_suggestions, query
		)

	def _fetch_suggestions(self, query: str):
		self._debounce_source_id = None
		self._cancel_task()
		self._suggestion_task = GetSearchSuggestionsTask(
			args=(query,),
			callback=self._on_suggestions_ready
		)
		self._suggestion_task.extra_data = query
		self._suggestion_task.start()
		return GLib.SOURCE_REMOVE

	def _on_suggestions_ready(self, task: GetSearchSuggestionsTask):
		if task.is_canceled() or task != self._suggestion_task:
			return
		self._suggestion_task = None

		current_text = self._search_entry.props.text.strip()
		if not current_text or current_text != task.extra_data:
			return

		results = task.result
		if not results:
			self._popover.popdown()
			return

		while child := self._list_box.get_first_child():
			self._list_box.remove(child)

		items = results.get('items', [])
		queries = results.get('queries', [])

		has_rows = False

		for item_data in items:
			row = self._create_item_row(item_data)
			if row:
				self._list_box.append(row)
				has_rows = True

		for q in queries:
			if q.lower() == current_text.lower():
				continue
			row = self._create_query_row(q)
			self._list_box.append(row)
			has_rows = True

		if has_rows and self._search_entry.has_focus():
			self._popover.popup()
			# Ensure the search entry retains keyboard focus so typing is never interrupted
			self._search_entry.grab_focus()
		else:
			self._popover.popdown()

	def _create_query_row(self, query: str) -> Gtk.ListBoxRow:
		row = Gtk.ListBoxRow()
		row._data = {'kind': 'query', 'query': query}

		box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
		box.props.margin_start = 12
		box.props.margin_end = 12
		box.props.margin_top = 8
		box.props.margin_bottom = 8

		icon = Gtk.Image.new_from_icon_name('edit-find-symbolic')
		icon.props.opacity = 0.6
		box.append(icon)

		label = Gtk.Label(label=query, xalign=0)
		label.props.hexpand = True
		label.props.ellipsize = Pango.EllipsizeMode.END
		box.append(label)

		arrow = Gtk.Image.new_from_icon_name('go-next-symbolic')
		arrow.props.opacity = 0.3
		box.append(arrow)

		row.set_child(box)
		return row

	def _create_item_row(self, item_data: dict) -> Gtk.ListBoxRow:
		row = Gtk.ListBoxRow()
		row._data = {'kind': 'item', 'item_data': item_data}

		box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
		box.props.margin_start = 12
		box.props.margin_end = 12
		box.props.margin_top = 6
		box.props.margin_bottom = 6

		item_type = item_data.get('type')
		if item_type == 'artist':
			icon_name = 'avatar-default-symbolic'
		elif item_type == 'song':
			icon_name = 'audio-x-generic-symbolic'
		else:
			icon_name = 'media-optical-symbolic'

		icon = Gtk.Image.new_from_icon_name(icon_name)
		icon.set_pixel_size(24)
		icon.props.valign = Gtk.Align.CENTER
		box.append(icon)

		text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
		text_box.props.hexpand = True
		text_box.props.valign = Gtk.Align.CENTER

		title_label = Gtk.Label(label=item_data.get('title', ''), xalign=0)
		title_label.props.ellipsize = Pango.EllipsizeMode.END
		text_box.append(title_label)

		subtitle = item_data.get('subtitle', '')
		if subtitle:
			sub_label = Gtk.Label(label=subtitle, xalign=0)
			sub_label.props.ellipsize = Pango.EllipsizeMode.END
			sub_label.add_css_class('dim-label')
			sub_label.add_css_class('caption')
			text_box.append(sub_label)

		box.append(text_box)

		if item_type == 'song':
			action_icon = Gtk.Image.new_from_icon_name('media-playback-start-symbolic')
		elif item_type == 'artist':
			action_icon = Gtk.Image.new_from_icon_name('go-next-symbolic')
		else:
			action_icon = Gtk.Image.new_from_icon_name('edit-find-symbolic')
		action_icon.props.opacity = 0.5
		action_icon.props.valign = Gtk.Align.CENTER
		box.append(action_icon)

		row.set_child(box)
		return row

	def _on_row_activated(self, _list_box: Gtk.ListBox, row: Gtk.ListBoxRow):
		self._popover.popdown()
		self._cancel_debounce()
		self._cancel_task()

		data = getattr(row, '_data', None)
		if not data:
			return

		if data['kind'] == 'query':
			query = data['query']
			self._search_entry.props.text = query
			self.emit('search', query, '')
		elif data['kind'] == 'item':
			item_data = data['item_data']
			item_type = item_data.get('type')
			item_obj = item_data.get('item')
			if item_type == 'artist' and isinstance(item_obj, Artist):
				self.emit('view-artist', item_obj)
			elif item_type == 'song' and isinstance(item_obj, Song):
				self.emit('play', item_obj, Group(songs=[item_obj]))
			elif isinstance(item_obj, Group):
				self._search_entry.props.text = item_obj.title
				self.emit('search', item_obj.title, '')
			else:
				title = item_data.get('title', '')
				self._search_entry.props.text = title
				self.emit('search', title, '')
