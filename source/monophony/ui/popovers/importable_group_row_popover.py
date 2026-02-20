'''Popover widget for importable group rows.'''

from monophony.ui.popovers.group_row_popover import GroupRowPopover

from gi.repository import GObject


class ImportableGroupRowPopover(GroupRowPopover):
	'''Popover widget for importable group rows.'''

	__gtype_name__ = __qualname__
	actions = (*GroupRowPopover.actions, 'import-group')
	'''Actions (signals) supported by this widget.'''

	def __init__(self, viewable_artist: bool):
		'''Initialize the widget.

		:param viewable_artist: Whether the group has a viewable artist.
		'''
		super().__init__(viewable_artist)

		self.props.menu_model.append(
			_('Import...'), self.__gtype_name__ + '.import-group'
		)

	@GObject.Signal(name='import-group')
	def _import_group(self):
		return
