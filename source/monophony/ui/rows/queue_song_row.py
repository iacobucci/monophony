'''Queue song row widget.'''

import weakref

from monophony import downloads
from monophony.data import Song
from monophony.ui.popovers.queue_song_row_popover import QueueSongRowPopover
from monophony.ui.rows.draggable_song_row import DraggableSongRow

from gi.repository import GObject, Gtk


class QueueSongRow(DraggableSongRow):
	'''Queue song row widget.'''

	__gtype_name__ = __qualname__

	def __init__(self, song: Song):
		'''Initialize the widget for a song.

		:param song: Song to initialize for.
		'''
		super().__init__(song)

		self._more_button.set_create_popup_func(
			lambda button, ref: QueueSongRow._on_show_more(ref(), button),
			weakref.ref(self)
		)

	@GObject.Signal(name='unqueue-song', arg_types=(object,))
	def _unqueue_song(self, _song: Song):
		return

	def _on_show_more(self, button: Gtk.MenuButton):
		popover = QueueSongRowPopover(
			downloads.is_downloaded(self.song), downloads.is_being_downloaded(self.song)
		)
		popover.connect(
			'add-song-to', lambda _popover, row: row().emit('add-song-to', row().song),
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
		popover.connect(
			'unqueue-song',
			lambda _popover, row: row().emit('unqueue-song', row().song),
			weakref.ref(self)
		)
		button.set_popover(popover)
