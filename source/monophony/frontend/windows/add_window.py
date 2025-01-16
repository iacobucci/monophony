import monophony.backend.playlists

import gi
gi.require_version('Adw', '1')
gi.require_version('Gtk', '4.0')
from gi.repository import Adw, GLib, Gtk


class MonophonyAddWindow(Adw.Window):
	def __init__(self, song: dict, player, callback):
		super().__init__()

		self.song = song
		self.player = player
		self.callback = callback
		self.add_to_queue = False
		self.add_to_playlists = []

		self.set_title(_('Add to...'))
		self.set_modal(True)

		btn_cancel = Gtk.Button.new_with_label(_('Cancel'))
		btn_cancel.connect('clicked', lambda _b: self.destroy())
		btn_add = Gtk.Button.new_with_label(_('Add'))
		btn_add.add_css_class('suggested-action')
		btn_add.connect('clicked', self._on_submit)
		headerbar = Adw.HeaderBar.new()
		headerbar.set_decoration_layout('')
		headerbar.pack_start(btn_cancel)
		headerbar.pack_end(btn_add)

		ent_name = Gtk.Entry.new()
		ent_name.connect('activate', self._on_create)
		ent_name.set_hexpand(True)
		ent_name.set_halign(Gtk.Align.FILL)
		ent_name.set_placeholder_text(_('New Playlist Name...'))

		btn_create = Gtk.Button.new_with_label(_('Create'))
		btn_create.connect('clicked', lambda _b: self._on_create(ent_name))

		toolbar_view = Adw.ToolbarView()
		toolbar_view.add_top_bar(headerbar)
		toolbar_view.add_bottom_bar(bar_name)
		toolbar_view.set_content(page_list)

		self.add_shortcut(Gtk.Shortcut.new(
			Gtk.ShortcutTrigger.parse_string('Escape'),
			Gtk.CallbackAction.new((lambda w, _: w.close()))
		))
		self.set_content(toolbar_view)
		self.update_groups()

	def update_groups(self):

		for queue_song in self.player.queue.copy():
			if queue_song['id'] == self.song['id']:
				self.add_to_queue = False
				break

		for playlist, contents in monophony.backend.playlists.read_playlists().items():
			chk_list = Gtk.CheckButton.new()

			for check_song in contents:
				if check_song['id'] == self.song['id']:
					chk_list.set_active(True)
					chk_list.set_sensitive(False)
					break

			chk_list.connect('toggled', self._on_add_to_playlist_toggled)

	def _on_add_to_queue_toggled(self, btn: Gtk.CheckButton):
		self.add_to_queue = btn.get_active()

	def _on_add_to_playlist_toggled(self, btn: Gtk.CheckButton):
		if btn.get_active():
			self.add_to_playlists.append(toggled_list)
		else:
			self.add_to_playlists.remove(toggled_list)

	def _on_submit(self, _btn: Gtk.CheckButton):
		for playlist in self.add_to_playlists:
			monophony.backend.playlists.add_song(self.song, playlist)

		if self.add_to_queue:
			GLib.Thread.new(None, self.player.queue_song, self.song)

		self.destroy()
		self.callback()

	def _on_create(self, ent: Gtk.Entry):
		text = ent.get_text()
		ent.set_text('')

		if text.strip():
			monophony.backend.playlists.add_playlist(text)
			self.update_groups()
