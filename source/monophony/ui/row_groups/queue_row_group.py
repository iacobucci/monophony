import weakref

from monophony.data import Song
from monophony.ui.row_groups.playable_row_group import PlayableRowGroup
from monophony.ui.rows.queue_song_row import QueueSongRow

from gi.repository import GObject


class QueueRowGroup(PlayableRowGroup):
	__gtype_name__ = __qualname__
	_row_type = QueueSongRow

	@GObject.Signal(name='move-song', arg_types=(object, object))
	def _move_song(self, _from: Song, _to: Song):
		return

	@GObject.Signal(name='unqueue-song', arg_types=(object,))
	def _unqueue_song(self, _song: Song):
		return

	def add(self, row: QueueSongRow):
		super().add(row)

		row.connect(
			'move-song',
			lambda _row, from_s, to_s, ref: ref().emit('move-song', from_s, to_s),
			weakref.ref(self)
		)
		row.connect(
			'unqueue-song',
			lambda _row, song, ref: ref().emit('unqueue-song', song),
			weakref.ref(self)
		)

	def update_contents(self, new_songs: list[Song], song_index: int):
		super().update_contents(new_songs)

		for i, row_ref in enumerate(self._rows):
			if i == song_index:
				row_ref().add_css_class('accent')
