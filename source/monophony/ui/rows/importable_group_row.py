'''Importable group row widget.'''

import weakref

from monophony.data import Group
from monophony.ui.popovers.importable_group_row_popover import ImportableGroupRowPopover
from monophony.ui.rows.group_row import GroupRow
from monophony.ui.rows.song_row import SongRow

from gi.repository import GObject, Gtk


class ImportableGroupRow(GroupRow):
	'''Importable group row widget.'''

	__gtype_name__ = __qualname__
	_row_type = SongRow

	def __init__(self, group: Group):
		'''Initialize the widget for a group.

		:param group: Group to initialize for.
		'''
		super().__init__(group)

		self._more_button.set_create_popup_func(
			lambda button, ref: ImportableGroupRow._on_show_more(ref(), button),
			weakref.ref(self)
		)

	@GObject.Signal(name='import-group', arg_types=(object,))
	def _import_group(self, _group: Group):
		return

	def _on_show_more(self, button: Gtk.MenuButton):
		self._popover = ImportableGroupRowPopover(bool(self.group.author.yt_id))
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
		self._popover.connect(
			'import-group',
			lambda _popover, row: row().emit('import-group', row().group),
			weakref.ref(self)
		)
		button.set_popover(self._popover)
