from monophony.ui.popovers.group_row_popover import GroupRowPopover

from gi.repository import GObject


class SynchronizedGroupRowPopover(GroupRowPopover):
	__gtype_name__ = __qualname__
	actions = (*GroupRowPopover.actions, 'delete-playlist')

	def __init__(self):
		super().__init__(False)

		self.props.menu_model.append(
			_('Delete'), self.__gtype_name__ + '.delete-playlist'
		)

	@GObject.Signal(name='delete-playlist')
	def _delete_playlist(self):
		return

