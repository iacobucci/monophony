from monophony.backend.utils import sanitize_str, sec_to_time_str, time_str_to_sec

import gi
gi.require_version('Adw', '1')
gi.require_version('Gtk', '4.0')
from gi.repository import Adw, GLib, Gtk


class MonophonyGroupRow(Adw.ExpanderRow):
	def __init__(self, group: dict, player: object):
		super().__init__()

		self.player = player
		self.group = group

		self.set_title(GLib.markup_escape_text(
			sanitize_str(group.get('title', '')), -1
		))

		btn_play = Gtk.Button.new_from_icon_name('media-playback-start-symbolic')
		btn_play.set_tooltip_text(_('Play'))
		btn_play.set_vexpand(False)
		btn_play.set_valign(Gtk.Align.CENTER)
		btn_play.connect('clicked', self._on_play_clicked)
		self.add_prefix(btn_play)
		self.set_expanded(False)

	def _on_play_clicked(self, _b):
		if not self.group:
			return

		GLib.Thread.new(None, self.player.play_queue, self.group['contents'], 0)

	def update(self):
		total_seconds = 0
		for song in self.group.get('contents', []):
			total_seconds += time_str_to_sec(song.get('length', '0'))

		self.set_subtitle(
			sec_to_time_str(total_seconds) +
			' ' +
			GLib.markup_escape_text(sanitize_str(self.group.get('author', '')), -1)
		)
