'''Synchronized group row widget.'''

import weakref

from monophony import playlists
from monophony.data import Group
from monophony.ui.popovers.synchronized_group_row_popover import (
	SynchronizedGroupRowPopover,
)
from monophony.ui.rows.group_row import GroupRow
from monophony.ui.rows.song_row import SongRow

import logboth
from gi.repository import GObject, Gtk


class SynchronizedGroupRow(GroupRow):
	'''Synchronized group row widget.'''

	__gtype_name__ = __qualname__
	_row_type = SongRow

	def __init__(self, group: Group):
		'''Initialize the widget for a group.

		:param group: Group to initialize for.
		'''
		super().__init__(group)

		self._more_button.set_create_popup_func(
			lambda button, ref: SynchronizedGroupRow._on_show_more(ref(), button),
			weakref.ref(self)
		)

	@GObject.Signal(name='delete-playlist', arg_types=(object,))
	def _delete_playlist(self, _playlist: Group):
		return

	def _on_show_more(self, button: Gtk.MenuButton):
		self._popover = SynchronizedGroupRowPopover()
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
		button.set_popover(self._popover)

	def update_contents(self):
		'''Replace rows with new rows generated from playlist backend.

		The playlist fetched is one matching the current group title.
		'''
		logboth.info(
			__name__,
			f'Updating row contents for external playlist "{self.group.title}"...'
		)

		for playlist in playlists.read_external():
			if playlist.title == self.group.title:
				self.group = playlist
				break
		else:
			logboth.error(
				__name__,
				'Failed to update row contents - '
				f'external playlist "{self.group.title}" does not exist'
			)
			return

		super().update_contents()
		logboth.info(__name__, 'Updated row contents')
