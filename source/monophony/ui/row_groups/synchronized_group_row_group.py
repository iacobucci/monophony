from monophony.ui.row_groups.editable_group_row_group import EditableGroupRowGroup
from monophony.ui.rows.synchronized_group_row import SynchronizedGroupRow


class SynchronizedGroupRowGroup(EditableGroupRowGroup):
	__gtype_name__ = __qualname__
	_row_type = SynchronizedGroupRow

