'''Row group widget for playable rows.'''

from monophony.data import Group, Song
from monophony.ui.row_groups.row_group import RowGroup

from gi.repository import GObject, Gtk


class PlayableRowGroup(RowGroup):
	'''Row group widget for playable rows.

	Song rows and group rows are playable, as opposed to artist rows.
	'''

	__gtype_name__ = __qualname__
	_row_type = Gtk.ListBoxRow

	@GObject.Signal(name='play', arg_types=(object, object))
	def _play(self, _song: Song, _group: Group):
		return

	@GObject.Signal(name='add-song-to', arg_types=(object,))
	def _add_song_to(self, _song: Song):
		return

	@GObject.Signal(name='undownload-song', arg_types=(object,))
	def _undownload_song(self, _song: Song):
		return

	@GObject.Signal(name='download-song', arg_types=(object,))
	def _download_song(self, _song: Song):
		return

	def add(self, row: _row_type):
		'''Add a playable row.

		:param row: Row to add.
		'''
		super().add(row)

		row.connect(
			'play',
			lambda _row, song, group, ref: ref().emit('play', song, group),
			self.weak_ref()
		)
		row.connect(
			'add-song-to',
			lambda _row, song, ref: ref().emit('add-song-to', song),
			self.weak_ref()
		)
		row.connect(
			'undownload-song',
			lambda _row, song, ref: ref().emit('undownload-song', song),
			self.weak_ref()
		)
		row.connect(
			'download-song',
			lambda _row, song, ref: ref().emit('download-song', song),
			self.weak_ref()
		)

	def update_download_status(self):
		'''Make child rows update their download statuses.'''
		for row in self._rows:
			row().update_download_status()
