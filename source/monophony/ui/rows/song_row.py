'''Song row widget.'''

import weakref

from monophony import downloads
from monophony.data import Artist, Group, Song, TimeString
from monophony.debug import MemoryDebugger
from monophony.ui.popovers.song_row_popover import SongRowPopover

from gi.repository import Adw, GLib, GObject, Gtk


class SongRow(MemoryDebugger, Adw.ActionRow):
	'''Song row widget.'''

	__gtype_name__ = __qualname__

	def __init__(self, song: Song):
		'''Initialize the widget for a song.

		:param song: Song to initialize for.
		'''
		super().__init__()

		self.song = song

		title = GLib.markup_escape_text(song.title, -1)
		length = GLib.markup_escape_text(song.length, -1)
		author = GLib.markup_escape_text(song.author.name, -1)
		subtitle = (
			f'{length} {author}' if TimeString(string=length).as_seconds() else author
		)

		self._downloaded_image = Gtk.Image.new_from_icon_name(
			'folder-download-symbolic'
		)
		self._downloaded_image.props.tooltip_text = _('Downloaded')

		self._spinner = Adw.Spinner()

		self._more_button = Gtk.MenuButton()
		self._more_button.props.tooltip_text = _('More')
		self._more_button.props.icon_name = 'view-more-symbolic'
		self._more_button.props.has_frame = False
		self._more_button.props.vexpand = False
		self._more_button.props.valign = Gtk.Align.CENTER
		self._more_button.set_create_popup_func(
			lambda button, ref: SongRow._on_show_more(ref(), button),
			weakref.ref(self)
		)

		self.props.title = title
		self.props.subtitle = subtitle
		self.props.tooltip_text = _('Play')
		self.props.activatable = True
		self.add_suffix(self._downloaded_image)
		self.add_suffix(self._spinner)
		self.add_suffix(self._more_button)
		self.connect(
			'activated', lambda row: row.emit('play', row.song, Group(songs=[row.song]))
		)
		self.update_download_status()

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

	def _on_show_more(self, button: Gtk.MenuButton):
		popover = SongRowPopover(
			downloads.is_downloaded(self.song), downloads.is_being_downloaded(self.song)
		)
		popover.connect(
			'queue-song',
			lambda _popover, row: row().emit('queue-song', row().song),
			weakref.ref(self)
		)
		popover.connect(
			'add-song-to',
			lambda _popover, row: row().emit('add-song-to', row().song),
			weakref.ref(self)
		)
		popover.connect(
			'view-artist',
			lambda _popover, row: row().emit('view-artist', row().song.author),
			weakref.ref(self)
		)
		popover.connect(
			'undownload-song',
			lambda _popover, row: row().emit('undownload-song', row().song),
			weakref.ref(self)
		)
		popover.connect(
			'download-song',
			lambda _popover, row: row().emit('download-song', row().song),
			weakref.ref(self)
		)
		button.props.popover = popover

	def update_download_status(self):
		'''Show spinner or downloaded symbol based on song download status.'''
		self._spinner.props.visible = downloads.is_being_downloaded(self.song)
		self._downloaded_image.props.visible = downloads.is_downloaded(self.song)
