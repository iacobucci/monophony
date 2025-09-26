import weakref

from monophony.data import Group, Song
from monophony.ui.row_groups.row_group import RowGroup

from gi.repository import GObject, Gtk


class PlayableRowGroup(RowGroup):
	__gtype_name__ = __qualname__
	_row_type = Gtk.ListBoxRow # SongRow | GroupRow

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
		super().add(row)

		row.connect(
			'play',
			lambda _row, song, group, ref: ref().emit('play', song, group),
			weakref.ref(self)
		)
		row.connect(
			'add-song-to',
			lambda _row, song, ref: ref().emit('add-song-to', song),
			weakref.ref(self)
		)
		row.connect(
			'undownload-song',
			lambda _row, song, ref: ref().emit('undownload-song', song),
			weakref.ref(self)
		)
		row.connect(
			'download-song',
			lambda _row, song, ref: ref().emit('download-song', song),
			weakref.ref(self)
		)

	def update_download_status(self):
		for row in self._rows:
			row().update_download_status()
