'''Row group widget for queueable rows.'''

import weakref

from monophony.data import Group, Song
from monophony.ui.row_groups.playable_row_group import PlayableRowGroup
from monophony.ui.rows.song_row import SongRow

from gi.repository import GObject, Gtk


class QueueableRowGroup(PlayableRowGroup):
	'''Row group widget for queueable rows.

	Song rows are queueable.
	'''

	__gtype_name__ = __qualname__
	_row_type = SongRow

	def __init__(self):
		'''Initialize the widget.'''
		super().__init__()

		play_button = Gtk.Button.new_from_icon_name(
			'media-playback-start-symbolic'
		)
		play_button.props.tooltip_text = _('Play All')
		play_button.connect(
			'clicked',
			lambda _button, ref: ref().on_play_all(),
			weakref.ref(self)
		)

		box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		box.props.spacing = 6
		box.append(play_button)

		self.props.header_suffix = box

	@GObject.Signal(name='queue-song', arg_types=(object,))
	def _queue_song(self, _song: Song):
		return

	def add(self, row: _row_type):
		'''Add a queueable row.

		:param row: Row to add.
		'''
		super().add(row)

		row.connect(
			'queue-song',
			lambda _row, song, ref: ref().emit('queue-song', song),
			weakref.ref(self)
		)

	def on_play_all(self):
		'''Emit play signal with all songs.'''
		group = Group(songs=[row_ref().song for row_ref in self._rows])
		self.emit('play', group.songs[0], group)
