'''Queue sidebar widget.'''

from monophony.data import Artist, Group, Song, TimeString
from monophony.ui.row_groups.queue_row_group import QueueRowGroup
from monophony.ui.rows.queue_song_row import QueueSongRow

from gi.repository import Adw, Gdk, GObject, Gtk


class QueueSidebar(Adw.Bin):
	'''Queue sidebar widget.'''

	__gtype_name__ = __qualname__
	_min_songs_for_shuffle = 3

	def __init__(self):
		'''Initialize the widget.'''
		super().__init__()

		self._queue_group = QueueRowGroup()
		self._queue_group.props.margin_start = 12
		self._queue_group.props.margin_end = 12
		self._queue_group.connect(
			'play',
			lambda _group, song, group, ref: ref().emit('play', song, group),
			self.weak_ref()
		)
		self._queue_group.connect(
			'add-song-to',
			lambda _group, song, ref: ref().emit('add-song-to', song),
			self.weak_ref()
		)
		self._queue_group.connect(
			'view-artist',
			lambda _group, artist, ref: ref().emit('view-artist', artist),
			self.weak_ref()
		)
		self._queue_group.connect(
			'undownload-song',
			lambda _group, song, ref: ref().emit('undownload-song', song),
			self.weak_ref()
		)
		self._queue_group.connect(
			'download-song',
			lambda _group, song, ref: ref().emit('download-song', song),
			self.weak_ref()
		)
		self._queue_group.connect(
			'move-song',
			lambda _group, from_s, to_s, ref:
				ref().emit('move-song', from_s, to_s),
			self.weak_ref()
		)
		self._queue_group.connect(
			'unqueue-song',
			lambda _group, song, ref: ref().emit('unqueue-song', song),
			self.weak_ref()
		)
		self._queue_group.connect(
			'start-radio',
			lambda _group, item, ref: ref().emit('start-radio', item),
			self.weak_ref()
		)

		self._queue_page = Adw.PreferencesPage()
		self._queue_page.props.valign = Gtk.Align.FILL
		self._queue_page.props.vexpand = True
		self._queue_page.props.visible = False
		self._queue_page.add(self._queue_group)

		self._status_page = Adw.StatusPage()
		self._status_page.props.valign = Gtk.Align.FILL
		self._status_page.props.vexpand = True
		self._status_page.props.title = _('Queue Empty')
		self._status_page.props.description = _('Nothing is playing right now')
		self._status_page.props.icon_name = 'view-list-symbolic'
		self._status_page.bind_property(
			'visible',
			self._queue_page,
			'visible',
			GObject.BindingFlags.BIDIRECTIONAL |
			GObject.BindingFlags.INVERT_BOOLEAN |
			GObject.BindingFlags.SYNC_CREATE
		)

		pages_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		pages_box.props.valign = Gtk.Align.FILL
		pages_box.props.vexpand = True
		pages_box.append(self._queue_page)
		pages_box.append(self._status_page)

		self.hide_button = Gtk.Button.new_from_icon_name('go-previous-symbolic')
		self.hide_button.props.tooltip_text = _('Back')

		self._title_widget = Adw.WindowTitle(
			title=_('Queue'), subtitle='00:00:00'
		)

		header_bar = Adw.HeaderBar()
		header_bar.props.title_widget = self._title_widget
		header_bar.pack_start(self.hide_button)

		clear_button = Gtk.Button.new_from_icon_name('media-playback-stop-symbolic')
		clear_button.props.tooltip_text = _('Stop')
		clear_button.props.halign = Gtk.Align.FILL
		clear_button.props.hexpand = False
		clear_button.add_css_class('destructive-action')
		clear_button.add_css_class('raised')
		clear_button.connect(
			'clicked',
			lambda _button, ref: ref().emit('clear-queue'),
			self.weak_ref()
		)

		self._radio_button = Gtk.Button.new_from_icon_name('audio-radio-symbolic')
		self._radio_button.props.tooltip_text = _('Start Radio')
		self._radio_button.props.halign = Gtk.Align.FILL
		self._radio_button.props.hexpand = False
		self._radio_button.add_css_class('raised')
		self._radio_button.connect(
			'clicked',
			lambda _button, ref: ref().emit('start-radio', None),
			self.weak_ref()
		)

		self._shuffle_button = Gtk.Button.new_from_icon_name(
			'media-playlist-shuffle-symbolic'
		)
		self._shuffle_button.props.tooltip_text = _('Shuffle')
		self._shuffle_button.props.halign = Gtk.Align.FILL
		self._shuffle_button.props.hexpand = False
		self._shuffle_button.props.sensitive = False
		self._shuffle_button.add_css_class('raised')
		self._shuffle_button.connect(
			'clicked',
			lambda _button, ref: ref().emit('shuffle-queue'),
			self.weak_ref()
		)

		self._lyrics_button = Gtk.Button.new_from_icon_name(
			'audio-input-microphone-symbolic'
		)
		self._lyrics_button.props.tooltip_text = _('Lyrics')
		self._lyrics_button.props.halign = Gtk.Align.FILL
		self._lyrics_button.props.hexpand = False
		self._lyrics_button.props.sensitive = False
		self._lyrics_button.add_css_class('raised')
		self._lyrics_button.connect(
			'clicked',
			lambda _button, ref: ref().emit('show-lyrics'),
			self.weak_ref()
		)

		button_content = Adw.ButtonContent()
		button_content.props.label = _('Add to...')
		button_content.props.icon_name = 'list-add-symbolic'
		add_button = Gtk.Button()
		add_button.props.child = button_content
		add_button.add_css_class('raised')
		add_button.connect(
			'clicked',
			lambda _button, ref: ref().emit('add-group-to', Group()),
			self.weak_ref()
		)

		buttons_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		buttons_box.props.margin_top = 9
		buttons_box.props.margin_bottom = 8
		buttons_box.props.spacing = 6
		buttons_box.props.halign = Gtk.Align.CENTER
		buttons_box.hexpand = False
		buttons_box.append(clear_button)
		buttons_box.append(add_button)
		buttons_box.append(self._radio_button)
		buttons_box.append(self._shuffle_button)
		buttons_box.append(self._lyrics_button)

		controls_bar = Adw.HeaderBar()
		controls_bar.props.show_back_button = False
		controls_bar.props.show_end_title_buttons = False
		controls_bar.props.show_start_title_buttons = False
		controls_bar.props.title_widget = buttons_box

		self._toolbar_view = Adw.ToolbarView()
		self._toolbar_view.props.reveal_bottom_bars = False
		self._toolbar_view.props.content = pages_box
		self._toolbar_view.add_top_bar(header_bar)
		self._toolbar_view.add_bottom_bar(controls_bar)

		self.props.child = self._toolbar_view

		key_controller = Gtk.EventControllerKey()
		key_controller.set_propagation_phase(Gtk.PropagationPhase.BUBBLE)
		key_controller.connect(
			'key-pressed',
			lambda _c, keyval, _k, _s, ref=self.weak_ref(): (
				ref()._on_key_pressed(keyval) if ref() else False
			)
		)
		self.add_controller(key_controller)

	def _on_key_pressed(self, keyval: int) -> bool:
		if keyval in (Gdk.KEY_Up, Gdk.KEY_Down, Gdk.KEY_Page_Up, Gdk.KEY_Page_Down):
			return self.scroll_vertical(
				direction_down=keyval in (Gdk.KEY_Down, Gdk.KEY_Page_Down),
				page_step=keyval in (Gdk.KEY_Page_Up, Gdk.KEY_Page_Down)
			)
		return False

	def scroll_vertical(self, direction_down: bool, page_step: bool = False) -> bool:
		'''Scroll the queue list vertically.

		:param direction_down: True to scroll down, False to scroll up.
		:param page_step: True to scroll by page, False to scroll by small step.
		:return: True if scrolled, False otherwise.
		'''
		scrolled = self._queue_page.get_first_child()
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

	@GObject.Signal(name='play', arg_types=(object, object))
	def _play(self, _song: Song, _group: Group):
		return

	@GObject.Signal(name='add-song-to', arg_types=(object,))
	def _add_song_to(self, _song: Song):
		return

	@GObject.Signal(name='undownload-song', arg_types=(object,))
	def _undownload_song(self, _song: Song):
		return

	@GObject.Signal(name='download-song', arg_types=(object,))
	def _download_song(self, _song: Song):
		return

	@GObject.Signal(name='move-song', arg_types=(object, object))
	def _move_song(self, _from: Song, _to: Song):
		return

	@GObject.Signal(name='unqueue-song', arg_types=(object,))
	def _unqueue_song(self, _song: Song):
		return

	@GObject.Signal(name='add-group-to', arg_types=(object,))
	def _add_group_to(self, _group: Group):
		return

	@GObject.Signal(name='view-artist', arg_types=(object,))
	def _view_artist(self, _artist: Artist):
		return

	@GObject.Signal(name='shuffle-queue')
	def _shuffle_queue(self):
		return

	@GObject.Signal(name='show-lyrics')
	def _show_lyrics_signal(self):
		return

	@GObject.Signal(name='clear-queue')
	def _clear_queue(self):
		return

	@GObject.Signal(name='start-radio', arg_types=(object,))
	def _start_radio(self, _item: object):
		return

	@GObject.Signal(name='select-radio-chip', arg_types=(object,))
	def _select_radio_chip(self, _chip: object):
		return

	def update_radio_chips(self, chips: list[dict] | None = None):
		'''Update radio chip buttons above queue (no-op: pills removed).'''
		pass

	def add_song_row(self, song: Song):
		'''Add song row to queue display.

		:param song: Song to add row for.
		'''
		self._queue_group.add(QueueSongRow(song))

	def update_contents(self, group: Group, song_index: int):
		'''Display a song group with a specific song highlighted.

		:param group: Group of songs to display.
		:param song_index: Currently playing song.
		'''
		self._queue_group.update_contents(group.songs, song_index)
		self._status_page.props.visible = not bool(group.songs)
		self._toolbar_view.props.reveal_bottom_bars = bool(group.songs)
		self._shuffle_button.props.sensitive = (
			len(group.songs) >= self._min_songs_for_shuffle
		)
		self._lyrics_button.props.sensitive = bool(group.songs)

		total_seconds = 0
		for song in group.songs:
			total_seconds += TimeString(string=song.length).as_seconds()

		self._title_widget.props.subtitle = TimeString(
			seconds=total_seconds
		).as_string()

	def update_download_status(self):
		'''Make the child group widget update its download status.'''
		self._queue_group.update_download_status()
