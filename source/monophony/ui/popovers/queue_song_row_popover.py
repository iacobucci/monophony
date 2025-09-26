from monophony.ui.popovers.song_row_popover import SongRowPopover

from gi.repository import GObject


class QueueSongRowPopover(SongRowPopover):
	__gtype_name__ = __qualname__
	actions = (*SongRowPopover.actions, 'unqueue-song')

	def __init__(self, downloaded: bool, being_downloaded: bool):
		super().__init__(downloaded, being_downloaded)

		self.props.menu_model.remove(0) # queue-song
		self.props.menu_model.append(
			_('Remove From Queue'), self.__gtype_name__ + '.unqueue-song'
		)

	@GObject.Signal(name='unqueue-song')
	def _unqueue_song(self):
		return
