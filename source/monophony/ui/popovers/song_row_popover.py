'''Popover widget for song rows.'''

from monophony.ui.popovers.row_popover import RowPopover

from gi.repository import Gio, GObject


class SongRowPopover(RowPopover):
	'''Popover widget for song rows.'''

	__gtype_name__ = __qualname__
	actions = (
		*RowPopover.actions,
		'queue-song',
		'add-song-to',
		'view-artist',
		'undownload-song',
		'download-song'
	)
	'''Actions (signals) supported by this widget.'''

	def __init__(self, downloaded: bool, being_downloaded: bool):
		'''Initialize the widget.

		:param downloaded: Whether the song has been downloaded.
		:param being_downloaded: Whether the song is being downloaded.
		'''
		super().__init__()

		menu = Gio.Menu()
		menu.append(_('Add to Queue'), self.__gtype_name__ + '.queue-song')
		menu.append(_('Add to...'), self.__gtype_name__ + '.add-song-to')
		menu.append(_('View Artist'), self.__gtype_name__ + '.view-artist')
		if downloaded:
			menu.append(
				_('Remove From Downloads'), self.__gtype_name__ + '.undownload-song'
			)
		elif not being_downloaded:
			menu.append(_('Download'), self.__gtype_name__ + '.download-song')

		self.props.menu_model = menu

	@GObject.Signal(name='queue-song')
	def _queue_song(self):
		return

	@GObject.Signal(name='add-song-to')
	def _add_song_to(self):
		return

	@GObject.Signal(name='view-artist')
	def _view_artist(self):
		return

	@GObject.Signal(name='undownload-song')
	def _undownload_song(self):
		return

	@GObject.Signal(name='download-song')
	def _download_song(self):
		return
