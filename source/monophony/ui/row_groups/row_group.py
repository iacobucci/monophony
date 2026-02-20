'''Row group widget.'''

import weakref

from monophony.data import Artist, YTItem
from monophony.debug import MemoryDebugger

from gi.repository import Adw, GObject, Gtk


class RowGroup(MemoryDebugger, Adw.PreferencesGroup):
	'''Row group widget.'''

	__gtype_name__ = __qualname__
	_row_type = Gtk.ListBoxRow

	def __init__(self):
		'''Initialize the widget.'''
		super().__init__()

		self.props.visible = False
		self._rows = []

	@GObject.Signal(name='view-artist', arg_types=(object,))
	def _view_artist(self, _artist: Artist):
		return

	def add(self, row: _row_type):
		'''Add a row.

		:param row: Row to add.
		'''
		super().add(row)

		self._rows.append(weakref.ref(row))

		row.connect(
			'view-artist',
			lambda _row, artist, ref: ref().emit('view-artist', artist),
			weakref.ref(self)
		)
		self.props.visible = True

	def clear(self):
		'''Remove all rows and hide self.'''
		for reference in self._rows:
			super().remove(reference())

		self._rows.clear()
		self.props.visible = False

	def remove(self, row: _row_type):
		'''Remove a child row.

		If no rows remain, hide self.

		:param row: Row to remove.
		'''
		super().remove(row)

		self._rows = [reference for reference in self._rows if reference() is not row]
		self.props.visible = bool(self._rows)

	def update_contents(self, new_contents: list[YTItem]):
		'''Replace rows with new rows generated from list of items.

		:param new_contents: List of items for new rows.
		'''
		self.clear()

		for item in new_contents:
			self.add(self._row_type(item))
