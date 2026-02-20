'''Window for importing playlists.'''

import weakref

from monophony import MIN_WIDTH
from monophony.data import Group
from monophony.debug import MemoryDebugger
from monophony.playlists import ImportTask

from gi.repository import Adw, GObject, Gtk


class ImportWindow(MemoryDebugger, Adw.Dialog):
	'''Import window.'''

	def __init__(self, group: Group | None=None):
		'''Initialize the window.

		:param group: Group to import. If not provided, a URL can be entered.
		'''
		super().__init__()

		self._group = Group() if group is None else group

		self._url_entry = Adw.EntryRow()
		self._url_entry.props.title = _('Playlist URL')
		self._url_entry.props.text = (
			'https://www.youtube.com/playlist?list=' + self._group.yt_id
		) if self._group.yt_id else ''
		self._url_entry.connect(
			'changed',
			lambda _entry, ref: ImportWindow._on_url_changed(ref()),
			weakref.ref(self)
		)

		self._name_entry = Adw.EntryRow()
		self._name_entry.props.title = _('Playlist Name')
		self._name_entry.props.text = self._group.title

		self._sync_switch = Adw.SwitchRow()
		self._sync_switch.props.title = _('Synchronized')
		self._sync_switch.props.subtitle = _(
			"Synchronized playlists are updated automatically and can't be edited"
		)
		self._sync_switch.connect(
			'notify::active',
			lambda _switch, _param, ref: ImportWindow._on_sync_switched(ref()),
			weakref.ref(self)
		)

		row_group = Adw.PreferencesGroup()
		row_group.add(self._url_entry)
		row_group.add(self._name_entry)
		row_group.add(self._sync_switch)

		page = Adw.PreferencesPage()
		page.add(row_group)

		self._import_button = Gtk.Button()
		self._import_button.props.label = _('Import')
		self._import_button.props.sensitive = bool(self._group.yt_id)
		self._import_button.add_css_class('suggested-action')
		self._import_button.connect(
			'clicked',
			lambda _button, ref: ImportWindow._on_import(ref()),
			weakref.ref(self)
		)

		action_bar = Gtk.ActionBar()
		action_bar.pack_end(self._import_button)

		toolbar_view = Adw.ToolbarView()
		toolbar_view.props.content = page
		toolbar_view.add_top_bar(Adw.HeaderBar())
		toolbar_view.add_bottom_bar(action_bar)

		self.props.title = _('Import Playlist...')
		self.props.child = toolbar_view
		self.props.content_width = MIN_WIDTH

	@GObject.Signal(name='import')
	def _import(self):
		return

	@GObject.Signal(name='import-failed')
	def _import_failed(self):
		return

	def _on_import(self):
		if not self._url_entry.props.text:
			return

		self.props.sensitive = False
		self.props.can_close = False
		self._import_button.props.child = Adw.Spinner()
		ImportTask(
			callback=self._on_import_finished,
			args=(
				self._name_entry.props.text,
				self._url_entry.props.text,
				not self._sync_switch.props.active
			)
		).start()

	def _on_import_finished(self, task: ImportTask):
		self.props.can_close = True
		self.close()
		self.emit('import' if task.result else 'import-failed')

	def _on_sync_switched(self):
		if self._sync_switch.props.active:
			self._name_entry.props.text = self._group.title
			self._name_entry.props.sensitive = False
		else:
			self._name_entry.props.sensitive = True

	def _on_url_changed(self):
		self._import_button.props.sensitive = bool(self._url_entry.props.text)
