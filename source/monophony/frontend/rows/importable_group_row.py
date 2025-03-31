from monophony.frontend.popovers.importable_group_popover import \
	MonophonyImportableGroupPopover
from monophony.frontend.rows.group_row import MonophonyGroupRow
from monophony.frontend.rows.song_row import MonophonySongRow

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk


class MonophonyImportableGroupRow(MonophonyGroupRow):
	def __init__(self, group: dict, player: object):
		super().__init__(group, player)

		for item in group['contents']:
			self.add_row(MonophonySongRow(item, player, group))

		btn_more = Gtk.MenuButton()
		btn_more.set_tooltip_text(_('More actions'))
		btn_more.set_icon_name('view-more-symbolic')
		btn_more.set_has_frame(False)
		btn_more.set_vexpand(False)
		btn_more.set_valign(Gtk.Align.CENTER)
		group = self.group.copy()
		btn_more.set_create_popup_func(MonophonyImportableGroupPopover, group)
		self.add_action(btn_more)
		super().update()
