'''Popover widget for editable song rows.'''

from monophony.ui.popovers.song_row_popover import SongRowPopover

from gi.repository import GObject


class EditableSongRowPopover(SongRowPopover):
	'''Popover widget for editable song rows.'''

	__gtype_name__ = __qualname__
	actions = (*SongRowPopover.actions, 'remove-song')
	'''Actions (signals) supported by this widget.'''

	def __init__(self, downloaded: bool, being_downloaded: bool):
		'''Initialize the widget with download state information.

		:param downloaded: Whether the song has been downloaded.
		:param being_downloaded: Whether the song is being downloaded.
		'''
		super().__init__(downloaded, being_downloaded)

		self.props.menu_model.append(
			_('Remove From Playlist'), self.__gtype_name__ + '.remove-song'
		)

	@GObject.Signal(name='remove-song')
	def _remove_song(self):
		return
