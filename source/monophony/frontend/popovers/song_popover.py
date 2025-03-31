import monophony.backend.cache
import monophony.backend.playlists

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gio, GLib, Gtk


class MonophonySongPopover(Gtk.PopoverMenu):
	def __init__(self, btn: Gtk.MenuButton, song: dict):
		super().__init__()

		self.song = song
		menu = Gio.Menu()
		btn.set_popover(self)
		window = self.get_ancestor(Gtk.Window)

		if monophony.backend.cache.is_song_being_cached(song['id']):
			pass
		elif monophony.backend.cache.is_song_cached(song['id']):
			menu.append(_('Remove From Downloads'), 'uncache-song')
			window.install_action(
				'uncache-song', None, lambda *_: self._on_uncache(song)
			)
		else:
			menu.append(_('Download'), 'cache-song')
			window.install_action(
				'cache-song', None, lambda *_: self._on_cache(song)
			)

		menu.append(_('Add to...'), 'add-song-to')
		window.install_action(
			'add-song-to', None, lambda w, *_: w._on_add_clicked(song)
		)
		menu.append(_('View Artist'), 'view-artist')
		window.install_action(
			'view-artist', None, lambda w, *_: w._on_show_artist(song['author_id'])
		)
		self.set_menu_model(menu)

	def _on_cache(self, song):
		window = self.get_ancestor(Gtk.Window)
		row = self.get_ancestor(Gtk.ListBoxRow)
		window._on_cache_song(song)
		row.spinner.set_visible(True)
		GLib.timeout_add_seconds(1, row.update_download_status)

	def _on_uncache(self, song):
		window = self.get_ancestor(Gtk.Window)
		row = self.get_ancestor(Gtk.ListBoxRow)
		window._on_uncache_song(song)
		row.spinner.set_visible(False)
		row.checkmark.set_visible(False)
