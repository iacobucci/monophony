from monophony.ui.popovers.row_popover import RowPopover

from gi.repository import Gio, GObject


class GroupRowPopover(RowPopover):
	__gtype_name__ = __qualname__
	actions = (
		*RowPopover.actions,
		'queue-group',
		'add-group-to',
		'view-artist',
		'download-group'
	)

	def __init__(self, viewable_artist: bool):
		super().__init__()

		menu = Gio.Menu()
		menu.append(_('Add to Queue'), self.__gtype_name__ + '.queue-group')
		menu.append(_('Add to...'), self.__gtype_name__ + '.add-group-to')
		if viewable_artist:
			menu.append(_('View Artist'), self.__gtype_name__ + '.view-artist')
		menu.append(_('Download'), self.__gtype_name__ + '.download-group')

		self.props.menu_model = menu

	@GObject.Signal(name='queue-group')
	def _queue_group(self):
		return

	@GObject.Signal(name='add-group-to')
	def _add_group_to(self):
		return

	@GObject.Signal(name='view-artist')
	def _view_artist(self):
		return

	@GObject.Signal(name='download-group')
	def _download_group(self):
		return
