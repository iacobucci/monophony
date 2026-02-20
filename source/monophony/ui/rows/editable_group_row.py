'''Group row widget for editable song rows.'''

import weakref

from monophony import playlists
from monophony.data import Group, Song
from monophony.ui.popovers.editable_group_row_popover import EditableGroupRowPopover
from monophony.ui.rows.editable_song_row import EditableSongRow
from monophony.ui.rows.group_row import GroupRow
from monophony.ui.windows.rename_window import RenameWindow

import logboth
from gi.repository import GLib, GObject, Gtk


class EditableGroupRow(GroupRow):
	'''Group row widget for editable song rows.'''

	__gtype_name__ = __qualname__
	_row_type = EditableSongRow

	def __init__(self, group: Group):
		'''Initialize the widget for a group.'''
		super().__init__(group)

		self._more_button.set_create_popup_func(
			lambda button, ref: EditableGroupRow._on_show_more(ref(), button),
			weakref.ref(self)
		)

	@GObject.Signal(name='delete-playlist', arg_types=(object,))
	def _delete_playlist(self, _playlist: Group):
		return

	def _on_show_more(self, button: Gtk.MenuButton):
		self._popover = EditableGroupRowPopover()
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
			'download-group',
			lambda _popover, row: row().emit('download-group', row().group),
			weakref.ref(self)
		)
		self._popover.connect(
			'delete-playlist',
			lambda _popover, row: row().emit('delete-playlist', row().group),
			weakref.ref(self)
		)
		self._popover.connect(
			'rename-playlist',
			lambda _popover, row: EditableGroupRow._on_rename_playlist(row()),
			weakref.ref(self)
		)
		button.set_popover(self._popover)

	def add_row(self, row: _row_type):
		'''Add an editable song row.

		:param row: Row to add.
		'''
		super().add_row(row)
		row.connect(
			'move-song',
			lambda _row, from_s, to_s, ref:
				EditableGroupRow._on_move_song(ref(), from_s, to_s),
			weakref.ref(self)
		)
		row.connect(
			'remove-song',
			lambda _row, song, ref: EditableGroupRow._on_remove_song(ref(), song),
			weakref.ref(self)
		)

	def update_contents(self):
		'''Replace rows with new rows generated from playlist backend.

		The playlist fetched is one matching the current group title.
		'''
		logboth.info(
			__name__, f'Updating row contents for playlist "{self.group.title}"...'
		)

		for playlist in playlists.read():
			if playlist.title == self.group.title:
				self.group = playlist
				break
		else:
			logboth.error(
				__name__,
				'Failed to update row contents - '
				f'playlist "{self.group.title}" does not exist'
			)
			return

		super().update_contents()
		logboth.info(__name__, 'Updated row contents')

	def _on_move_song(self, from_song: Song, to_song: Song):
		i = self.group.songs.index(from_song)
		j = self.group.songs.index(to_song)
		if abs(i - j) == 1:
			playlists.swap_songs(self.group.title, i, j)
		else:
			playlists.move_song(self.group.title, i, j)

		self.update_contents()

	def _on_remove_song(self, song: Song):
		playlists.remove_song(song, self.group.title)
		self.update_contents()

	def _on_rename_confirmed(self, name: str):
		self.group.title = playlists.rename(self.group.title, name)
		self.props.title = GLib.markup_escape_text(self.group.title, -1)

	def _on_rename_playlist(self):
		rename_window = RenameWindow(self.group.title)
		rename_window.connect(
			'rename',
			lambda _window, name, ref:
				EditableGroupRow._on_rename_confirmed(ref(), name),
			weakref.ref(self),
		)
		rename_window.present(self)
