import weakref

from monophony.data import Artist, Group, Song, TimeString
from monophony.debug import MemoryDebugger
from monophony.ui.popovers.group_row_popover import GroupRowPopover
from monophony.ui.rows.song_row import SongRow

from gi.repository import Adw, GLib, GObject, Gtk


class GroupRow(MemoryDebugger, Adw.ExpanderRow):
	__gtype_name__ = __qualname__
	_row_type = SongRow

	def __init__(self, group: Group):
		super().__init__()

		self.group = group
		self._rows = []

		self._more_button = Gtk.MenuButton()
		self._more_button.props.tooltip_text = _('More')
		self._more_button.props.icon_name = 'view-more-symbolic'
		self._more_button.props.has_frame = False
		self._more_button.props.vexpand = False
		self._more_button.props.valign = Gtk.Align.CENTER
		self._more_button.set_create_popup_func(
			lambda button, ref: GroupRow._on_show_more(ref(), button),
			weakref.ref(self)
		)

		self.props.title = GLib.markup_escape_text(group.title, -1)
		self.props.expanded = False
		self.add_suffix(self._more_button)
		self.connect('notify::expanded', GroupRow._on_expanded)
		self.update_subtitle()

	@GObject.Signal(name='play', arg_types=(object, object))
	def _play(self, _song: Song, _group: Group):
		return

	@GObject.Signal(name='queue-song', arg_types=(object,))
	def _queue_song(self, _song: Song):
		return

	@GObject.Signal(name='add-song-to', arg_types=(object,))
	def _add_song_to(self, _song: Song):
		return

	@GObject.Signal(name='view-artist', arg_types=(object,))
	def _view_artist(self, _artist: Artist):
		return

	@GObject.Signal(name='undownload-song', arg_types=(object,))
	def _undownload_song(self, _song: Song):
		return

	@GObject.Signal(name='download-song', arg_types=(object,))
	def _download_song(self, _song: Song):
		return

	@GObject.Signal(name='queue-group', arg_types=(object,))
	def _queue_group(self, _group: Group):
		return

	@GObject.Signal(name='add-group-to', arg_types=(object,))
	def _add_group_to(self, _group: Group):
		return

	@GObject.Signal(name='download-group', arg_types=(object,))
	def _download_group(self, _group: Group):
		return

	def _on_expanded(self, _param):
		if self.props.expanded:
			self.update_contents()

	def _on_show_more(self, button: Gtk.MenuButton):
		self._popover = GroupRowPopover(bool(self.group.author.yt_id))
		self._popover.connect(
			'queue-group',
			lambda _popover, row: row().emit('queue-group', row().group),
			weakref.ref(self)
		)
		self._popover.connect(
			'add-group-to',
			lambda _popover, row: row().emit('add-group-to', row().group),
			weakref.ref(self)
		)
		self._popover.connect(
			'view-artist',
			lambda _popover, row: row().emit('view-artist', row().group.author),
			weakref.ref(self)
		)
		self._popover.connect(
			'download-group',
			lambda _popover, row: row().emit('download-group', row().group),
			weakref.ref(self)
		)
		button.set_popover(self._popover)

	def add_row(self, row: _row_type):
		row.connect(
			'play',
			lambda _row, song, _group, g_row: g_row().emit('play', song, g_row().group),
			weakref.ref(self)
		)
		row.connect(
			'queue-song',
			lambda _row, song, g_row: g_row().emit('queue-song', song),
			weakref.ref(self)
		)
		row.connect(
			'add-song-to',
			lambda _row, song, g_row: g_row().emit('add-song-to', song),
			weakref.ref(self)
		)
		row.connect(
			'view-artist',
			lambda _row, artist, g_row: g_row().emit('view-artist', artist),
			weakref.ref(self)
		)
		row.connect(
			'download-song',
			lambda _row, song, g_row: g_row().emit('download-song', song),
			weakref.ref(self)
		)
		row.connect(
			'undownload-song',
			lambda _row, song, g_row: g_row().emit('undownload-song', song),
			weakref.ref(self)
		)
		self._rows.append(weakref.ref(row))
		super().add_row(row)

	def add_song(self, song: Song):
		self.add_row(self._row_type(song))

	def update_download_status(self):
		for row_ref in self._rows:
			row_ref().update_download_status()

	def update_contents(self):
		for row_ref in self._rows:
			self.remove(row_ref())

		self._rows.clear()

		for song in self.group.songs:
			self.add_song(song)

		self.update_subtitle()

	def update_subtitle(self):
		total_seconds = 0
		for song in self.group.songs:
			total_seconds += TimeString(string=song.length).as_seconds()

		self.props.subtitle = (
			TimeString(seconds=total_seconds).as_string() +
			' ' +
			GLib.markup_escape_text(self.group.author.name, -1)
		) if total_seconds else ''
