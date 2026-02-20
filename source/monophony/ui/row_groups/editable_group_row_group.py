'''Row group widget for editable group rows.'''

import weakref

from monophony.data import Group
from monophony.ui.row_groups.group_row_group import GroupRowGroup
from monophony.ui.rows.editable_group_row import EditableGroupRow

from gi.repository import GObject


class EditableGroupRowGroup(GroupRowGroup):
	'''Row group widget for editable group rows.'''

	__gtype_name__ = __qualname__
	_row_type = EditableGroupRow

	@GObject.Signal(name='delete-playlist', arg_types=(object,))
	def _delete_playlist(self, _playlist: Group):
		return

	def add(self, row: _row_type):
		'''Add an editable group row.

		:param row: Row to add.
		'''
		super().add(row)

		row.connect(
			'delete-playlist',
			lambda _row, playlist, ref: ref().emit('delete-playlist', playlist),
			weakref.ref(self)
		)
