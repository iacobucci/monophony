from monophony.backend.utils import sanitize_str, sec_to_time_str, time_str_to_sec

import gi
gi.require_version('Adw', '1')
gi.require_version('Gtk', '4.0')
from gi.repository import Adw, GLib


class MonophonyGroupRow(Adw.ExpanderRow):
	def __init__(self, group: dict, player: object):
		super().__init__()

		self.player = player
		self.group = group

		self.set_title(GLib.markup_escape_text(
			sanitize_str(group.get('title', '') or ''), -1
		))
		self.set_expanded(False)

	def update(self):
		total_seconds = 0
		for song in self.group.get('contents', []):
			total_seconds += time_str_to_sec(song.get('length', '0'))

		self.set_subtitle(
			sec_to_time_str(total_seconds) +
			' ' +
			GLib.markup_escape_text(
				sanitize_str(self.group.get('author', '') or ''), -1
			)
		)
