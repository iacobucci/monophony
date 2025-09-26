import weakref

from monophony.debug import MemoryDebugger

from gi.repository import Adw, GObject


class RenameWindow(MemoryDebugger, Adw.Dialog):
	def __init__(self, original_name: str):
		super().__init__()

		self.original_name = original_name

		entry_row = Adw.EntryRow()
		entry_row.props.title = _('Playlist Name')
		entry_row.props.show_apply_button = True
		entry_row.props.text = original_name
		entry_row.connect(
			'apply',
			lambda entry, ref:
				RenameWindow._on_apply(ref(), entry.props.text),
			weakref.ref(self)
		)

		group = Adw.PreferencesGroup()
		group.add(entry_row)

		page = Adw.PreferencesPage()
		page.add(group)

		toolbar_view = Adw.ToolbarView()
		toolbar_view.props.content = page
		toolbar_view.add_top_bar(Adw.HeaderBar())

		self.props.title = _('Rename Playlist...')
		self.props.child = toolbar_view

	@GObject.Signal(name='rename', arg_types=(str,))
	def _rename(self, _new_name: str):
		return

	def _on_apply(self, text: str):
		if text and text != self.original_name:
			self.emit('rename', text)
		self.close()
