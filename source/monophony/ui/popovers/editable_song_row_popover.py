from monophony.ui.popovers.song_row_popover import SongRowPopover

from gi.repository import GObject


class EditableSongRowPopover(SongRowPopover):
	__gtype_name__ = __qualname__
	actions = (*SongRowPopover.actions, 'remove-song')

	def __init__(self, downloaded: bool, being_downloaded: bool):
		super().__init__(downloaded, being_downloaded)

		self.props.menu_model.append(
			_('Remove From Playlist'), self.__gtype_name__ + '.remove-song'
		)

	@GObject.Signal(name='remove-song')
	def _remove_song(self):
		return
