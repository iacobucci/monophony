'''Popover widget for editable group rows.'''

from monophony.ui.popovers.group_row_popover import GroupRowPopover

from gi.repository import GObject


class EditableGroupRowPopover(GroupRowPopover):
	'''Popover widget for editable group rows.'''

	__gtype_name__ = __qualname__

	actions = (*GroupRowPopover.actions, 'rename-playlist', 'delete-playlist')
	'''Actions (signals) supported by this widget.'''

	def __init__(self):
		'''Initialize the widget.'''
		super().__init__(False)

		self.props.menu_model.append(
			_('Rename...'), self.__gtype_name__ + '.rename-playlist'
		)
		self.props.menu_model.append(
			_('Delete'), self.__gtype_name__ + '.delete-playlist'
		)

	@GObject.Signal(name='rename-playlist')
	def _rename_playlist(self):
		return

	@GObject.Signal(name='delete-playlist')
	def _delete_playlist(self):
		return
