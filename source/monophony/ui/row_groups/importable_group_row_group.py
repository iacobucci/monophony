import weakref

from monophony.data import Group
from monophony.ui.row_groups.group_row_group import GroupRowGroup
from monophony.ui.rows.importable_group_row import ImportableGroupRow

from gi.repository import GObject


class ImportableGroupRowGroup(GroupRowGroup):
	__gtype_name__ = __qualname__
	_row_type = ImportableGroupRow

	@GObject.Signal(name='import-group', arg_types=(object,))
	def _import_group(self, _group: Group):
		return

	def add(self, row: _row_type):
		super().add(row)

		row.connect(
			'import-group',
			lambda _row, group, ref: ref().emit('import-group', group),
			weakref.ref(self)
		)
