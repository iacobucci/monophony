from monophony.ui.popovers.group_row_popover import GroupRowPopover

from gi.repository import GObject


class ImportableGroupRowPopover(GroupRowPopover):
	__gtype_name__ = __qualname__
	actions = (*GroupRowPopover.actions, 'import-group')

	def __init__(self, viewable_artist: bool):
		super().__init__(viewable_artist)

		self.props.menu_model.append(
			_('Import...'), self.__gtype_name__ + '.import-group'
		)

	@GObject.Signal(name='import-group')
	def _import_group(self):
		return

