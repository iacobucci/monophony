import monophony.backend.cache
from monophony.backend.utils import sanitize_str
from monophony.frontend.popovers.song_popover import MonophonySongPopover

import gi
gi.require_version('Adw', '1')
gi.require_version('Gtk', '4.0')
from gi.repository import Adw, GLib, GObject, Gtk


class MonophonySongRow(Adw.ActionRow, GObject.Object):
	def __init__(self, song: dict, player: object, group: dict | None = None):
		super().__init__()

		self.player = player
		self.song = song
		self.group = group

		self.set_tooltip_text(_('Play'))
		self.set_property('activatable', True)
		self.connect('activated', lambda row: row._on_play_clicked())

		title = GLib.markup_escape_text(song.get('title', '') or '', -1)
		length = GLib.markup_escape_text(song.get('length', '0:00') or '0:00', -1)
		author = GLib.markup_escape_text(song.get('author', '') or '', -1)
		subtitle = sanitize_str(author)
		if length:
			subtitle = length + ' ' + subtitle

		self.checkmark = Gtk.Image.new_from_icon_name('emblem-ok-symbolic')
		self.checkmark.set_tooltip_text(_('Downloaded'))
		self.checkmark.set_visible(False)
		self.add_suffix(self.checkmark)
		self.spinner = Adw.Spinner()
		self.spinner.set_visible(False)
		self.add_suffix(self.spinner)
		self.set_title(sanitize_str(title))
		self.set_subtitle(sanitize_str(subtitle))

		self.btn_more = Gtk.MenuButton()
		self.btn_more.set_tooltip_text(_('More actions'))
		self.btn_more.set_icon_name('view-more-symbolic')
		self.btn_more.set_has_frame(False)
		self.btn_more.set_vexpand(False)
		self.btn_more.set_valign(Gtk.Align.CENTER)
		self.btn_more.set_create_popup_func(MonophonySongPopover, self.song)
		self.add_suffix(self.btn_more)

		self.update_download_status()

	def _on_play_clicked(self):
		queue = [self.song]
		if self.group:
			queue = self.group['contents']

		GLib.Thread.new(
			None, self.player.play_queue, queue, queue.index(self.song)
		)

	def update_download_status(self) -> bool:
		if monophony.backend.cache.is_song_being_cached(self.song['id']):
			self.spinner.set_visible(True)
			return True

		self.spinner.set_visible(False)
		self.checkmark.set_visible(
			monophony.backend.cache.is_song_cached(self.song['id'])
		)

		return False
