import weakref

from monophony.data import Artist, Group, Song, TimeString
from monophony.ui.row_groups.queue_row_group import QueueRowGroup
from monophony.ui.rows.queue_song_row import QueueSongRow

from gi.repository import Adw, GObject, Gtk


class QueueSidebar(Adw.Bin):
	__gtype_name__ = __qualname__
	_min_songs_for_shuffle = 3

	def __init__(self):
		super().__init__()

		self._queue_group = QueueRowGroup()
		self._queue_group.props.margin_start = 12
		self._queue_group.props.margin_end = 12
		self._queue_group.connect(
			'play',
			lambda _group, song, group, ref: ref().emit('play', song, group),
			weakref.ref(self)
		)
		self._queue_group.connect(
			'add-song-to',
			lambda _group, song, ref: ref().emit('add-song-to', song),
			weakref.ref(self)
		)
		self._queue_group.connect(
			'view-artist',
			lambda _group, artist, ref: ref().emit('view-artist', artist),
			weakref.ref(self)
		)
		self._queue_group.connect(
			'undownload-song',
			lambda _group, song, ref: ref().emit('undownload-song', song),
			weakref.ref(self)
		)
		self._queue_group.connect(
			'download-song',
			lambda _group, song, ref: ref().emit('download-song', song),
			weakref.ref(self)
		)
		self._queue_group.connect(
			'move-song',
			lambda _group, from_s, to_s, ref:
				ref().emit('move-song', from_s, to_s),
			weakref.ref(self)
		)
		self._queue_group.connect(
			'unqueue-song',
			lambda _group, song, ref: ref().emit('unqueue-song', song),
			weakref.ref(self)
		)

		queue_page = Adw.PreferencesPage()
		queue_page.props.valign = Gtk.Align.FILL
		queue_page.props.vexpand = True
		queue_page.props.visible = False
		queue_page.add(self._queue_group)

		self._status_page = Adw.StatusPage()
		self._status_page.props.valign = Gtk.Align.FILL
		self._status_page.props.vexpand = True
		self._status_page.props.title = _('Queue Empty')
		self._status_page.props.description = _('Nothing is playing right now')
		self._status_page.props.icon_name = 'view-list-symbolic'
		self._status_page.bind_property(
			'visible',
			queue_page,
			'visible',
			GObject.BindingFlags.BIDIRECTIONAL |
			GObject.BindingFlags.INVERT_BOOLEAN |
			GObject.BindingFlags.SYNC_CREATE
		)

		pages_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		pages_box.props.valign = Gtk.Align.FILL
		pages_box.props.vexpand = True
		pages_box.append(queue_page)
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
			weakref.ref(self)
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
			weakref.ref(self)
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
			weakref.ref(self)
		)

		buttons_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		buttons_box.props.margin_top = 9
		buttons_box.props.margin_bottom = 8
		buttons_box.props.spacing = 6
		buttons_box.props.halign = Gtk.Align.CENTER
		buttons_box.hexpand = False
		buttons_box.append(clear_button)
		buttons_box.append(add_button)
		buttons_box.append(self._shuffle_button)

		controls_bar = Adw.HeaderBar()
		controls_bar.props.title_widget = buttons_box

		self._toolbar_view = Adw.ToolbarView()
		self._toolbar_view.props.reveal_bottom_bars = False
		self._toolbar_view.props.content = pages_box
		self._toolbar_view.add_top_bar(header_bar)
		self._toolbar_view.add_bottom_bar(controls_bar)

		self.props.child = self._toolbar_view

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

	@GObject.Signal(name='clear-queue')
	def _clear_queue(self):
		return

	def add_song_row(self, song: Song):
		self._queue_group.add(QueueSongRow(song))

	def update_contents(self, group: Group, song_index: int):
		self._queue_group.update_contents(group.songs, song_index)
		self._status_page.props.visible = not bool(group.songs)
		self._toolbar_view.props.reveal_bottom_bars = bool(group.songs)
		self._shuffle_button.props.sensitive = (
			len(group.songs) >= self._min_songs_for_shuffle
		)

		total_seconds = 0
		for song in group.songs:
			total_seconds += TimeString(string=song.length).as_seconds()

		self._title_widget.props.subtitle = TimeString(
			seconds=total_seconds
		).as_string()

	def update_download_status(self):
		self._queue_group.update_download_status()
