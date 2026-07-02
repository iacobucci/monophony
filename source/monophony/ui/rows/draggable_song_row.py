'''Draggable song row widget.'''

from monophony.data import Song
from monophony.ui.rows.song_row import SongRow

from gi.repository import Gdk, GObject, Gtk


class DraggableSongRow(SongRow):
	'''Draggable song row widget.'''

	__gtype_name__ = __qualname__

	def __init__(self, song: Song):
		'''Initialize the widget for a song.

		:param song: Song to initialize for.
		'''
		super().__init__(song)

		self.drag_source = Gtk.DragSource()
		self.drag_source.props.actions = Gdk.DragAction.MOVE
		self.drag_source.set_icon(Gtk.WidgetPaintable.new(self), 0, 0)
		self.drag_source.connect(
			'prepare',
			lambda _source, _x, _y, row: DraggableSongRow._on_drag_prepare(row()),
			self.weak_ref()
		)
		self.drag_source.connect(
			'drag-end',
			lambda _source, _drag, _data, row: DraggableSongRow._on_drag_end(row()),
			self.weak_ref()
		)
		self.drag_source.connect(
			'drag-cancel',
			lambda _source, _drag, _data, row: DraggableSongRow._on_drag_end(row()),
			self.weak_ref()
		)

		handle_image = Gtk.Image.new_from_icon_name('list-drag-handle-symbolic')
		handle_image.add_css_class('dimmed')

		drop_target = Gtk.DropTarget.new(self.__gtype__, Gdk.DragAction.MOVE)
		drop_target.connect(
			'drop',
			lambda _target, drop, _x, _y, row: DraggableSongRow._on_drop(row(), drop),
			self.weak_ref()
		)
		drop_target.connect(
			'enter',
			lambda target, _x, _y, row: DraggableSongRow._on_drag_enter(row(), target),
			self.weak_ref()
		)

		self.add_controller(self.drag_source)
		self.add_controller(drop_target)
		self.add_prefix(handle_image)

	@GObject.Signal(name='move-song', arg_types=(object, object))
	def _move_song(self, _from: Song, _to: Song):
		return

	def _on_drag_prepare(self) -> Gdk.ContentProvider:
		self.add_css_class('background')
		return Gdk.ContentProvider.new_for_value(self)

	def _on_drag_enter(self, drop_target: Gtk.DropTarget) -> int:
		if self.drag_source.get_drag():
			drop_target.reject()
			return 0

		i = 0
		while row := self.get_parent().get_row_at_index(i):
			i += 1
			if row.drag_source.get_drag():
				return Gdk.DragAction.MOVE

		drop_target.reject()
		return 0

	def _on_drag_end(self):
		self.remove_css_class('background')

	def _on_drop(self, dropped_row: SongRow) -> bool:
		self.emit('move-song', dropped_row.song, self.song)
		return True
