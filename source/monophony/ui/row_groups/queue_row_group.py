'''Row group widget for queue song rows.'''

from monophony.data import Song
from monophony.ui.row_groups.playable_row_group import PlayableRowGroup
from monophony.ui.rows.queue_song_row import QueueSongRow

import logboth
from gi.repository import GObject


class QueueRowGroup(PlayableRowGroup):
	'''Row group widget for queue song rows.'''

	__gtype_name__ = __qualname__
	_row_type = QueueSongRow

	@GObject.Signal(name='move-song', arg_types=(object, object))
	def _move_song(self, _from: Song, _to: Song):
		return

	@GObject.Signal(name='unqueue-song', arg_types=(object,))
	def _unqueue_song(self, _song: Song):
		return

	def add(self, row: _row_type):
		'''Add a queue song row.

		:param row: Row to add.
		'''
		super().add(row)

		row.connect(
			'move-song',
			lambda _row, from_s, to_s, ref: ref().emit('move-song', from_s, to_s),
			self.weak_ref()
		)
		row.connect(
			'unqueue-song',
			lambda _row, song, ref: ref().emit('unqueue-song', song),
			self.weak_ref()
		)

	def update_contents(self, new_songs: list[Song], song_index: int):
		'''Replace current rows with rows generated from list of songs.

		:param new_songs: List of new songs to show.
		:param song_index: Currently playing song to highlight.
		'''
		super().update_contents(new_songs)

		for i, row_ref in enumerate(self._rows):
			if i == song_index:
				row = row_ref()
				if row is not None:
					row.add_css_class('accent')
				else:
					logboth.warning(__name__, 'Reference is None')
