'''Row group widget for group rows.'''

import weakref

from monophony.data import Group
from monophony.ui.row_groups.queueable_row_group import QueueableRowGroup
from monophony.ui.rows.group_row import GroupRow

import logboth
from gi.repository import GObject


class GroupRowGroup(QueueableRowGroup):
	'''Row group widget for group rows.'''

	__gtype_name__ = __qualname__
	_row_type = GroupRow

	@GObject.Signal(name='queue-group', arg_types=(object,))
	def _queue_group(self, _group: Group):
		return

	@GObject.Signal(name='add-group-to', arg_types=(object,))
	def _add_group_to(self, _group: Group):
		return

	@GObject.Signal(name='download-group', arg_types=(object,))
	def _download_group(self, _group: Group):
		return

	def add(self, row: _row_type):
		'''Add a group row.

		:param row: Row to add.
		'''
		super().add(row)

		row.connect(
			'queue-group',
			lambda _row, group, ref: ref().emit('queue-group', group),
			weakref.ref(self)
		)
		row.connect(
			'add-group-to',
			lambda _row, group, ref: ref().emit('add-group-to', group),
			weakref.ref(self)
		)
		row.connect(
			'download-group',
			lambda _row, group, ref: ref().emit('download-group', group),
			weakref.ref(self)
		)

	def on_play_all(self):
		'''Emit play signal with all songs.'''
		group = Group()
		for row_ref in self._rows:
			row = row_ref()
			if row is not None:
				group.songs += row.group.songs
			else:
				logboth.warning(__name__, 'Reference is None')

		self.emit('play', group.songs[0], group)

	def update_contents(self, new_groups: list[Group]):
		'''Replace currently displayed rows with new rows created from list of groups.

		:param new_groups: New groups to display.
		'''
		new_titles = [group.title for group in new_groups]
		existing_titles = []
		for row in self._rows.copy():
			if row().group.title in new_titles and row().props.expanded:
				row().update_contents()
				existing_titles.append(row().group.title)
			else:
				self.remove(row())

		for group in new_groups:
			if group.title not in existing_titles:
				self.add(self._row_type(group))
