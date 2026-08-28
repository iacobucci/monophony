'''Home page widget.'''

from monophony import downloads, playlists, recents, recommendations
from monophony.data import Artist, Group, Song
from monophony.ui.bars.search_bar import SearchBar
from monophony.ui.pages.page import Page
from monophony.ui.row_groups.editable_group_row_group import EditableGroupRowGroup
from monophony.ui.row_groups.group_row_group import GroupRowGroup
from monophony.ui.row_groups.queueable_row_group import QueueableRowGroup
from monophony.ui.row_groups.synchronized_group_row_group import (
	SynchronizedGroupRowGroup,
)

from gi.repository import Adw, Gdk, Gio, GLib, GObject, Gtk


class HomePage(Page):
	'''Home page widget.

	Displays recommendations, playlists, external playlists, recent songs and downloads.
	'''

	__gtype_name__ = __qualname__

	def __init__(self):
		'''Initialize the widget.'''
		super().__init__()

		self._deleted_playlists = []

		self._recommended_group = GroupRowGroup()
		self._recommended_group.props.title = _('Recommended')
		self._recommended_group.props.margin_start = 12
		self._recommended_group.props.margin_end = 12
		self._recommended_group.connect(
			'play',
			lambda _group, song, group, ref: ref().emit('play', song, group),
			self.weak_ref()
		)
		self._recommended_group.connect(
			'queue-song',
			lambda _group, song, ref: ref().emit('queue-song', song),
			self.weak_ref()
		)
		self._recommended_group.connect(
			'add-song-to',
			lambda _group, song, ref: ref().emit('add-song-to', song),
			self.weak_ref()
		)
		self._recommended_group.connect(
			'view-artist',
			lambda _group, artist, ref: ref().emit('view-artist', artist),
			self.weak_ref()
		)
		self._recommended_group.connect(
			'undownload-song',
			lambda _group, song, ref: ref().emit('undownload-song', song),
			self.weak_ref()
		)
		self._recommended_group.connect(
			'download-song',
			lambda _group, song, ref: ref().emit('download-song', song),
			self.weak_ref()
		)
		self._recommended_group.connect(
			'queue-group',
			lambda _group, group, ref: ref().emit('queue-group', group),
			self.weak_ref()
		)
		self._recommended_group.connect(
			'add-group-to',
			lambda _group, group, ref: ref().emit('add-group-to', group),
			self.weak_ref()
		)
		self._recommended_group.connect(
			'download-group',
			lambda _group, group, ref: ref().emit('download-group', group),
			self.weak_ref()
		)

		open_dir_button = Gtk.Button.new_from_icon_name('folder-symbolic')
		open_dir_button.props.tooltip_text = _('Playlists Directory')
		open_dir_button.connect(
			'clicked',
			lambda _button:
				Gio.AppInfo.launch_default_for_uri(
					'file://' + playlists.get_directory()
				)
		)

		self._playlists_group = EditableGroupRowGroup()
		self._playlists_group.props.title = _('Your Playlists')
		self._playlists_group.props.margin_start = 12
		self._playlists_group.props.margin_end = 12
		self._playlists_group.connect(
			'play',
			lambda _group, song, group, ref: ref().emit('play', song, group),
			self.weak_ref()
		)
		self._playlists_group.connect(
			'queue-song',
			lambda _group, song, ref: ref().emit('queue-song', song),
			self.weak_ref()
		)
		self._playlists_group.connect(
			'add-song-to',
			lambda _group, song, ref: ref().emit('add-song-to', song),
			self.weak_ref()
		)
		self._playlists_group.connect(
			'view-artist',
			lambda _group, artist, ref: ref().emit('view-artist', artist),
			self.weak_ref()
		)
		self._playlists_group.connect(
			'undownload-song',
			lambda _group, song, ref: ref().emit('undownload-song', song),
			self.weak_ref()
		)
		self._playlists_group.connect(
			'download-song',
			lambda _group, song, ref: ref().emit('download-song', song),
			self.weak_ref()
		)
		self._playlists_group.connect(
			'queue-group',
			lambda _group, group, ref: ref().emit('queue-group', group),
			self.weak_ref()
		)
		self._playlists_group.connect(
			'add-group-to',
			lambda _group, group, ref: ref().emit('add-group-to', group),
			self.weak_ref()
		)
		self._playlists_group.connect(
			'download-group',
			lambda _group, group, ref: ref().emit('download-group', group),
			self.weak_ref()
		)
		self._playlists_group.connect(
			'delete-playlist',
			lambda _group, playlist, ref: HomePage._on_delete_playlist(ref(), playlist),
			self.weak_ref()
		)
		self._playlists_group.connect(
			'toggle-favorite',
			lambda _group, _playlist, ref: ref().update_playlists(),
			self.weak_ref()
		)
		self._playlists_group.props.header_suffix.prepend(open_dir_button)


		no_playlists_group = Adw.PreferencesGroup()
		no_playlists_group.props.title = _('Your Playlists')
		no_playlists_group.props.description = _(
			'Playlists you create will appear here'
		)
		no_playlists_group.props.margin_start = 12
		no_playlists_group.props.margin_end = 12
		no_playlists_group.bind_property(
			'visible',
			self._playlists_group,
			'visible',
			GObject.BindingFlags.BIDIRECTIONAL |
			GObject.BindingFlags.SYNC_CREATE |
			GObject.BindingFlags.INVERT_BOOLEAN
		)

		import_button = Adw.ButtonRow()
		import_button.props.start_icon_name = 'list-add-symbolic'
		import_button.props.title = _('Import')
		import_button.connect(
			'activated',
			lambda _button, ref: ref().emit('import-group', Group()),
			self.weak_ref()
		)

		import_group = Adw.PreferencesGroup()
		import_group.props.margin_start = 12
		import_group.props.margin_end = 12
		import_group.add(import_button)

		self._external_playlists_group = SynchronizedGroupRowGroup()
		self._external_playlists_group.props.title = _('Synchronized Playlists')
		self._external_playlists_group.props.margin_start = 12
		self._external_playlists_group.props.margin_end = 12
		self._external_playlists_group.connect(
			'play',
			lambda _group, song, group, ref: ref().emit('play', song, group),
			self.weak_ref()
		)
		self._external_playlists_group.connect(
			'queue-song',
			lambda _group, song, ref: ref().emit('queue-song', song),
			self.weak_ref()
		)
		self._external_playlists_group.connect(
			'add-song-to',
			lambda _group, song, ref: ref().emit('add-song-to', song),
			self.weak_ref()
		)
		self._external_playlists_group.connect(
			'view-artist',
			lambda _group, artist, ref: ref().emit('view-artist', artist),
			self.weak_ref()
		)
		self._external_playlists_group.connect(
			'undownload-song',
			lambda _group, song, ref: ref().emit('undownload-song', song),
			self.weak_ref()
		)
		self._external_playlists_group.connect(
			'download-song',
			lambda _group, song, ref: ref().emit('download-song', song),
			self.weak_ref()
		)
		self._external_playlists_group.connect(
			'queue-group',
			lambda _group, group, ref: ref().emit('queue-group', group),
			self.weak_ref()
		)
		self._external_playlists_group.connect(
			'add-group-to',
			lambda _group, group, ref: ref().emit('add-group-to', group),
			self.weak_ref()
		)
		self._external_playlists_group.connect(
			'download-group',
			lambda _group, group, ref: ref().emit('download-group', group),
			self.weak_ref()
		)
		self._external_playlists_group.connect(
			'delete-playlist',
			lambda _group, playlist, ref:
				HomePage._on_delete_external_playlist(ref(), playlist),
			self.weak_ref()
		)

		open_dir_button = Gtk.Button.new_from_icon_name('folder-symbolic')
		open_dir_button.props.tooltip_text = _('Downloads Directory')
		open_dir_button.connect(
			'clicked',
			lambda _button:
				Gio.AppInfo.launch_default_for_uri(
					'file://' + downloads.get_directory()
				)
		)

		self._downloads_group = QueueableRowGroup()
		self._downloads_group.props.title = _('Downloads')
		self._downloads_group.props.header_suffix = open_dir_button
		self._downloads_group.props.margin_start = 12
		self._downloads_group.props.margin_end = 12
		self._downloads_group.connect(
			'play',
			lambda _group, song, group, ref: ref().emit('play', song, group),
			self.weak_ref()
		)
		self._downloads_group.connect(
			'queue-song',
			lambda _group, song, ref: ref().emit('queue-song', song),
			self.weak_ref()
		)
		self._downloads_group.connect(
			'add-song-to',
			lambda _group, song, ref: ref().emit('add-song-to', song),
			self.weak_ref()
		)
		self._downloads_group.connect(
			'view-artist',
			lambda _group, artist, ref: ref().emit('view-artist', artist),
			self.weak_ref()
		)
		self._downloads_group.connect(
			'undownload-song',
			lambda _group, song, ref: ref().emit('undownload-song', song),
			self.weak_ref()
		)

		clear_button = Gtk.Button.new_from_icon_name('edit-clear-all-symbolic')
		clear_button.add_css_class('destructive-action')
		clear_button.props.tooltip_text = _('Clear')
		clear_button.connect(
			'clicked',
			lambda _button, ref: HomePage._on_clear_history(ref()),
			self.weak_ref()
		)

		self._history_group = QueueableRowGroup()
		self._history_group.props.title = _('Recently Played')
		self._history_group.props.header_suffix = clear_button
		self._history_group.props.margin_start = 12
		self._history_group.props.margin_end = 12
		self._history_group.connect(
			'play',
			lambda _group, song, group, ref: ref().emit('play', song, group),
			self.weak_ref()
		)
		self._history_group.connect(
			'queue-song',
			lambda _group, song, ref: ref().emit('queue-song', song),
			self.weak_ref()
		)
		self._history_group.connect(
			'add-song-to',
			lambda _group, song, ref: ref().emit('add-song-to', song),
			self.weak_ref()
		)
		self._history_group.connect(
			'view-artist',
			lambda _group, artist, ref: ref().emit('view-artist', artist),
			self.weak_ref()
		)
		self._history_group.connect(
			'undownload-song',
			lambda _group, song, ref: ref().emit('undownload-song', song),
			self.weak_ref()
		)
		self._history_group.connect(
			'download-song',
			lambda _group, song, ref: ref().emit('download-song', song),
			self.weak_ref()
		)

		donate_button = Adw.ButtonRow()
		donate_button.props.start_icon_name = 'emote-love-symbolic'
		donate_button.props.title = _('Donate')
		donate_button.add_css_class('donate-button')
		donate_button.connect(
			'activated',
			lambda _button, ref: HomePage._on_donate(ref()),
			self.weak_ref()
		)

		css = Gtk.CssProvider()
		css.load_from_data('''
			.donate-button {
				background-color: var(--accent-red);
				color: var(--light-1);
			}
		''', -1)
		Gtk.StyleContext.add_provider_for_display(
			Gdk.Display.get_default(),
			css,
			Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
		)

		donate_group = Adw.PreferencesGroup()
		donate_group.props.margin_start = 12
		donate_group.props.margin_end = 12
		donate_group.add(donate_button)

		self._page.add(self._recommended_group)
		self._page.add(self._playlists_group)
		self._page.add(no_playlists_group)
		self._page.add(import_group)
		self._page.add(self._external_playlists_group)
		self._page.add(self._history_group)
		self._page.add(self._downloads_group)
		self._page.add(donate_group)

		self._search_bar = SearchBar()
		self._search_bar.connect(
			'search',
			lambda _bar, query, filter_, ref: ref().emit('search', query, filter_),
			self.weak_ref()
		)

		self._toolbar_view.add_top_bar(self._search_bar)

		self.props.title = _('Home')
		self.update_playlists()
		self.update_recommendations()
		self.update_external_playlists()
		self.update_history()

	@GObject.Signal(name='play', arg_types=(object, object))
	def _play(self, _song: Song, _group: Group):
		return

	@GObject.Signal(name='search', arg_types=(str, str))
	def _search(self, _query: str, _filter: str):
		return

	@GObject.Signal(name='queue-song', arg_types=(object,))
	def _queue_song(self, _song: Song):
		return

	@GObject.Signal(name='add-song-to', arg_types=(object,))
	def _add_song_to(self, _song: Song):
		return

	@GObject.Signal(name='view-artist', arg_types=(object,))
	def _view_artist(self, _artist: Artist):
		return

	@GObject.Signal(name='undownload-song', arg_types=(object,))
	def _undownload_song(self, _song: Song):
		return

	@GObject.Signal(name='download-song', arg_types=(object,))
	def _download_song(self, _song: Song):
		return

	@GObject.Signal(name='queue-group', arg_types=(object,))
	def _queue_group(self, _group: Group):
		return

	@GObject.Signal(name='add-group-to', arg_types=(object,))
	def _add_group_to(self, _group: Group):
		return

	@GObject.Signal(name='download-group', arg_types=(object,))
	def _download_group(self, _group: Group):
		return

	@GObject.Signal(name='import-group', arg_types=(object,))
	def _import_group(self, _group: Group):
		return

	def _on_clear_history(self):
		recents.clear()
		self.update_history()

	def _on_delete_external_playlist(self, playlist: Group):
		playlists.delete_external(playlist.title)
		self._deleted_playlists.append(playlist)

		toast = Adw.Toast()
		toast.props.title = _('Deleted playlist "{name}"').format(
			name=GLib.markup_escape_text(playlist.title, -1)
		)
		toast.props.priority = Adw.ToastPriority.HIGH
		toast.props.button_label = _('Undo')
		toast.connect(
			'button-clicked',
			lambda _toast, ref: HomePage._on_delete_toast_undo(ref(), True),
			self.weak_ref()
		)
		toast.connect(
			'dismissed',
			lambda _toast, ref: HomePage._on_delete_toast_dismissed(ref()),
			self.weak_ref()
		)
		self._toast_overlay.add_toast(toast)
		self.update_external_playlists()

	def _on_delete_toast_dismissed(self):
		self._deleted_playlists.pop()
		self.update_playlists()
		self.update_external_playlists()
		self._toast_overlay.props.sensitive = True

	def _on_delete_playlist(self, playlist: Group):
		playlists.delete(playlist.title)
		self._deleted_playlists.append(playlist)

		toast = Adw.Toast()
		toast.props.title = _('Deleted playlist "{name}"').format(
			name=GLib.markup_escape_text(playlist.title, -1)
		)
		toast.props.priority = Adw.ToastPriority.HIGH
		toast.props.button_label = _('Undo')
		toast.connect(
			'button-clicked',
			lambda _toast, ref: HomePage._on_delete_toast_undo(ref(), False),
			self.weak_ref()
		)
		toast.connect(
			'dismissed',
			lambda _toast, ref: HomePage._on_delete_toast_dismissed(ref()),
			self.weak_ref()
		)
		self._toast_overlay.add_toast(toast)
		self.update_playlists()

	def _on_delete_toast_undo(self, external_playlist: bool):
		self._toast_overlay.props.sensitive = False
		if external_playlist:
			playlists.add_external(self._deleted_playlists[-1])
		else:
			playlists.add(self._deleted_playlists[-1])

	def _on_donate(self):
		launcher = Gtk.UriLauncher()
		launcher.props.uri = 'https://zeh-kira.itch.io/monophony/purchase'
		launcher.launch()

	def focus_search(self):
		'''Switch focus to search bar.'''
		self._search_bar.focus_search()

	def update_external_playlists(self):
		'''Update external playlists widget content with local data.'''
		self._external_playlists_group.update_contents(playlists.read_external())

	def update_downloads(self, downloads: Group):
		'''Update downloads widget with provided group.

		:param downloads: New downloads group.
		'''
		self._downloads_group.update_contents(downloads.songs)

	def update_download_status(self):
		'''Make all child widgets update their download statuses.'''
		for group in (
			self._recommended_group,
			self._playlists_group,
			self._external_playlists_group,
			self._downloads_group,
			self._history_group
		):
			group.update_download_status()

	def update_history(self):
		'''Update recent songs widget content.'''
		new_contents = recents.read().songs
		self._history_group.update_contents(new_contents)

	def update_playlists(self):
		'''Update playlists widget content.'''
		self._playlists_group.update_contents(playlists.get_sorted_playlists())


	def update_recommendations(self):
		'''Update recommendations widget content with local data.'''
		self._recommended_group.update_contents(recommendations.read())
