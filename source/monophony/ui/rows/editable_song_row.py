'''Editable song row widget.'''

from monophony import downloads
from monophony.data import Song
from monophony.ui.popovers.editable_song_row_popover import EditableSongRowPopover
from monophony.ui.rows.draggable_song_row import DraggableSongRow

from gi.repository import GObject, Gtk


class EditableSongRow(DraggableSongRow):
	'''Editable song row widget.'''

	__gtype_name__ = __qualname__

	def __init__(self, song: Song):
		'''Initialize the widget for a song.'''
		super().__init__(song)

		self._more_button.set_create_popup_func(
			lambda button, ref: EditableSongRow._on_show_more(ref(), button),
			self.weak_ref()
		)

	@GObject.Signal(name='remove-song', arg_types=(object,))
	def _remove_song(self, _song: Song):
		return

	def _on_show_more(self, button: Gtk.MenuButton):
		popover = EditableSongRowPopover(
			downloads.is_downloaded(self.song), downloads.is_being_downloaded(self.song)
		)
		popover.connect(
			'queue-song',
			lambda _popover, row: row().emit('queue-song', row().song),
			self.weak_ref()
		)
		popover.connect(
			'add-song-to', lambda _popover, row: row().emit('add-song-to', row().song),
			self.weak_ref()
		)
		popover.connect(
			'view-artist',
			lambda _popover, row: row().emit('view-artist', row().song.author),
			self.weak_ref()
		)
		popover.connect(
			'undownload-song',
			lambda _popover, row: row().emit('undownload-song', row().song),
			self.weak_ref()
		)
		popover.connect(
			'download-song',
			lambda _popover, row: row().emit('download-song', row().song),
			self.weak_ref()
		)
		popover.connect(
			'remove-song',
			lambda _popover, row: row().emit('remove-song', row().song),
			self.weak_ref()
		)
		button.set_popover(popover)
