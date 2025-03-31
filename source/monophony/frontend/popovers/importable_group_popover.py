import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gio, Gtk


class MonophonyImportableGroupPopover(Gtk.PopoverMenu):
	def __init__(self, btn: Gtk.MenuButton, group: dict):
		super().__init__()

		window = btn.get_ancestor(Gtk.Window)
		mnu_actions = Gio.Menu()
		mnu_actions.append(_('Download'), 'cache-playlist')
		window.install_action(
			'cache-playlist',
			None,
			lambda w, *_: w._on_cache_playlist(group['contents'])
		)
		mnu_actions.append(_('Import...'), 'import-playlist')
		window.install_action(
			'import-playlist',
			None,
			lambda w, *_: w._on_import_clicked(group=group)
		)
		self.set_menu_model(mnu_actions)
		btn.set_popover(self)
