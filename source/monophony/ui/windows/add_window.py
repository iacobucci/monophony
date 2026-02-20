'''Window for adding a group to playlists and creating new playlists.'''

import weakref

from monophony import MIN_WIDTH, playlists
from monophony.data import Group
from monophony.debug import MemoryDebugger

from gi.repository import Adw, Gtk


class AddWindow(MemoryDebugger, Adw.Dialog):
	'''Add window.'''

	def __init__(self, group: Group):
		'''Initialize the window.

		:param group: Group to add to playlists.
		'''
		super().__init__()

		self._selected_lists = []
		self._group = group
		self.did_anything = False

		self._playlists_group = Adw.PreferencesGroup()
		self._playlists_group.props.visible = False
		lists = playlists.read()
		for playlist in lists:
			self._add_playlist_row(playlist)

		new_playlist_row = Adw.EntryRow()
		new_playlist_row.props.title = _('New Playlist')
		new_playlist_row.props.show_apply_button = True
		new_playlist_row.connect(
			'apply',
			lambda row, ref: AddWindow._on_create_playlist(ref(), row),
			weakref.ref(self)
		)

		new_playlist_group = Adw.PreferencesGroup()
		new_playlist_group.add(new_playlist_row)

		playlists_page = Adw.PreferencesPage()
		playlists_page.add(self._playlists_group)
		playlists_page.add(new_playlist_group)

		self.add_button = Gtk.Button()
		self.add_button.props.label = _('Add')
		self.add_button.props.sensitive = False
		self.add_button.add_css_class('suggested-action')
		self.add_button.connect(
			'clicked', lambda _button, ref: AddWindow._on_add(ref()), weakref.ref(self)
		)

		add_bar = Gtk.ActionBar()
		add_bar.pack_end(self.add_button)

		toolbar_view = Adw.ToolbarView()
		toolbar_view.props.content = playlists_page
		toolbar_view.add_top_bar(Adw.HeaderBar())
		toolbar_view.add_bottom_bar(add_bar)

		self.props.title = _('Add to Playlists...')
		self.props.child = toolbar_view
		self.props.follows_content_size = True
		self.props.width_request = MIN_WIDTH

	def _add_playlist_row(self, playlist: Group, checked: bool=False):
		check_button = Gtk.CheckButton()
		check_button.connect(
			'toggled',
			lambda button, ref, playlist:
				AddWindow._on_check_playlist(ref(), button.props.active, playlist),
			weakref.ref(self),
			playlist
		)
		check_button.props.active = checked

		check_row = Adw.ActionRow()
		check_row.props.title = playlist.title
		check_row.props.activatable_widget = check_button
		check_row.add_prefix(check_button)

		self._playlists_group.props.visible = True
		self._playlists_group.add(check_row)

	def _on_check_playlist(self, check: bool, playlist: Group):
		if check:
			self._selected_lists.append(playlist)
			self.add_button.props.sensitive = True
		else:
			self._selected_lists.remove(playlist)

	def _on_create_playlist(self, entry_row: Adw.EntryRow):
		if not entry_row.props.text:
			return

		self._add_playlist_row(
			Group(title=playlists.add(Group(title=entry_row.props.text))), True
		)
		entry_row.props.text = ''
		self.add_button.props.sensitive = True
		self.did_anything = True

	def _on_add(self):
		for playlist in self._selected_lists:
			playlists.add_songs(self._group, playlist.title)

		self.did_anything = True
		self.close()
