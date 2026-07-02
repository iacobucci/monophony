'''Results page widget.'''

from monophony.data import Artist, Group, Song
from monophony.ui.pages.page import Page
from monophony.ui.row_groups.importable_group_row_group import ImportableGroupRowGroup
from monophony.ui.row_groups.playable_row_group import PlayableRowGroup
from monophony.ui.row_groups.queueable_row_group import QueueableRowGroup
from monophony.ui.row_groups.row_group import RowGroup
from monophony.ui.rows.artist_row import ArtistRow
from monophony.ui.rows.importable_group_row import ImportableGroupRow
from monophony.ui.rows.song_row import SongRow
from monophony.yt import SearchResult

from gi.repository import Adw, GLib, GObject


class ResultsPage(Page):
	'''Results page widget for displaying search results.'''

	__gtype_name__ = __qualname__

	def __init__(self, results: list[SearchResult], filter_: str | None):
		'''Initialize the widget with results and optional filter.

		:param results: List of search results to display.
		:param filter: Search filter used.
		'''
		super().__init__()

		self._results = results

		songs_button = Adw.ButtonRow()
		songs_button.props.end_icon_name = 'go-next-symbolic'
		songs_button.props.title = _('Show All')
		if filter_ == 'songs':
			songs_button.connect(
				'activated',
				lambda _button, ref: ref().emit('filter-results', ''),
				self.weak_ref()
			)
		else:
			songs_button.connect(
				'activated',
				lambda _button, ref: ref().emit('filter-results', 'songs'),
				self.weak_ref()
			)

		self._songs_button_group = Adw.PreferencesGroup()
		self._songs_button_group.props.visible = False
		self._songs_button_group.add(songs_button)

		videos_button = Adw.ButtonRow()
		videos_button.props.end_icon_name = 'go-next-symbolic'
		videos_button.props.title = _('Show All')
		if filter_ == 'videos':
			videos_button.connect(
				'activated',
				lambda _button, ref: ref().emit('filter-results', ''),
				self.weak_ref()
			)
		else:
			videos_button.connect(
				'activated',
				lambda _button, ref: ref().emit('filter-results', 'videos'),
				self.weak_ref()
			)

		self._videos_button_group = Adw.PreferencesGroup()
		self._videos_button_group.props.visible = False
		self._videos_button_group.add(videos_button)

		albums_button = Adw.ButtonRow()
		albums_button.props.end_icon_name = 'go-next-symbolic'
		albums_button.props.title = _('Show All')
		if filter_ == 'albums':
			albums_button.connect(
				'activated',
				lambda _button, ref: ref().emit('filter-results', ''),
				self.weak_ref()
			)
		else:
			albums_button.connect(
				'activated',
				lambda _button, ref: ref().emit('filter-results', 'albums'),
				self.weak_ref()
			)

		self._albums_button_group = Adw.PreferencesGroup()
		self._albums_button_group.props.visible = False
		self._albums_button_group.add(albums_button)

		playlists_button = Adw.ButtonRow()
		playlists_button.props.end_icon_name = 'go-next-symbolic'
		playlists_button.props.title = _('Show All')
		if filter_ == 'playlists':
			playlists_button.connect(
				'activated',
				lambda _button, ref: ref().emit('filter-results', ''),
				self.weak_ref()
			)
		else:
			playlists_button.connect(
				'activated',
				lambda _button, ref: ref().emit('filter-results', 'playlists'),
				self.weak_ref()
			)

		self._playlists_button_group = Adw.PreferencesGroup()
		self._playlists_button_group.props.visible = False
		self._playlists_button_group.add(playlists_button)

		artists_button = Adw.ButtonRow()
		artists_button.props.end_icon_name = 'go-next-symbolic'
		artists_button.props.title = _('Show All')
		if filter_ == 'artists':
			artists_button.connect(
				'activated',
				lambda _button, ref: ref().emit('filter-results', ''),
				self.weak_ref()
			)
		else:
			artists_button.connect(
				'activated',
				lambda _button, ref: ref().emit('filter-results', 'artists'),
				self.weak_ref()
			)

		self._artists_button_group = Adw.PreferencesGroup()
		self._artists_button_group.props.visible = False
		self._artists_button_group.add(artists_button)

		self._songs_group = QueueableRowGroup()
		self._songs_group.props.title = _('Songs')

		self._videos_group = QueueableRowGroup()
		self._videos_group.props.title = _('Videos')

		self._albums_group = ImportableGroupRowGroup()
		self._albums_group.props.title = _('Albums and Singles')

		self._playlists_group = ImportableGroupRowGroup()
		self._playlists_group.props.title = _('Playlists')

		self._artists_group = RowGroup()
		self._artists_group.props.title = _('Artists')

		self._top_group = QueueableRowGroup()
		for result in self._results:
			if result.top:
				if result.type == 'artist':
					self._top_group = RowGroup()
				elif result.type in ('album', 'playlist'):
					self._top_group = ImportableGroupRowGroup()
		self._top_group.props.title = _('Top Result')
		if self._top_group.props.header_suffix:
			self._top_group.props.header_suffix.props.visible = False

		for group, button_group in {
			self._top_group: None,
			self._songs_group: self._songs_button_group,
			self._videos_group: self._videos_button_group,
			self._albums_group: self._albums_button_group,
			self._playlists_group: self._playlists_button_group,
			self._artists_group: self._artists_button_group
		}.items():
			group.props.margin_start = 12
			group.props.margin_end = 12
			group.connect(
				'view-artist',
				lambda _group, artist, ref: ref().emit('view-artist', artist),
				self.weak_ref()
			)
			if isinstance(group, QueueableRowGroup):
				group.connect(
					'queue-song',
					lambda _group, song, ref: ref().emit('queue-song', song),
					self.weak_ref()
				)
			if isinstance(group, PlayableRowGroup):
				group.connect(
					'play',
					lambda _group, song, group, ref: ref().emit('play', song, group),
					self.weak_ref()
				)
				group.connect(
					'add-song-to',
					lambda _group, song, ref: ref().emit('add-song-to', song),
					self.weak_ref()
				)
				group.connect(
					'undownload-song',
					lambda _group, song, ref: ref().emit('undownload-song', song),
					self.weak_ref()
				)
				group.connect(
					'download-song',
					lambda _group, song, ref: ref().emit('download-song', song),
					self.weak_ref()
				)
			if isinstance(group, ImportableGroupRowGroup):
				group.connect(
					'import-group',
					lambda _group, group, ref: ref().emit('import-group', group),
					self.weak_ref()
				)
				group.connect(
					'queue-group',
					lambda _group, group, ref: ref().emit('queue-group', group),
					self.weak_ref()
				)
				group.connect(
					'add-group-to',
					lambda _group, group, ref: ref().emit('add-group-to', group),
					self.weak_ref()
				)
				group.connect(
					'download-group',
					lambda _group, group, ref: ref().emit('download-group', group),
					self.weak_ref()
				)

			self._page.add(group)
			if button_group and not filter_:
				button_group.props.margin_start = 12
				button_group.props.margin_end = 12
				self._page.add(button_group)

		self.props.title = _('Search Results')
		self.props.sensitive = False

		GLib.idle_add(self._load)

	@GObject.Signal(name='add-group-to', arg_types=(object,))
	def _add_group_to(self, _group: Group):
		return

	@GObject.Signal(name='add-song-to', arg_types=(object,))
	def _add_song_to(self, _song: Song):
		return

	@GObject.Signal(name='download-group', arg_types=(object,))
	def _download_group(self, _group: Group):
		return

	@GObject.Signal(name='download-song', arg_types=(object,))
	def _download_song(self, _song: Song):
		return

	@GObject.Signal(name='filter-results', arg_types=(str,))
	def _filter_results(self, _filter: str):
		return

	@GObject.Signal(name='import-group', arg_types=(object,))
	def _import_group(self, _group: Group):
		return

	@GObject.Signal(name='play', arg_types=(object, object))
	def _play(self, _song: Song, _group: Group):
		return

	@GObject.Signal(name='queue-group', arg_types=(object,))
	def _queue_group(self, _group: Group):
		return

	@GObject.Signal(name='queue-song', arg_types=(object,))
	def _queue_song(self, _song: Song):
		return

	@GObject.Signal(name='undownload-song', arg_types=(object,))
	def _undownload_song(self, _song: Song):
		return

	@GObject.Signal(name='view-artist', arg_types=(object,))
	def _view_artist(self, _artist: Artist):
		return

	def _load(self) -> bool:
		if self._results:
			result = self._results.pop(0)
			row = None

			if isinstance(result.item, Group):
				row = ImportableGroupRow(result.item)
			elif isinstance(result.item, Song):
				row = SongRow(result.item)
			else:
				row = ArtistRow(result.item)

			if result.top:
				self._top_group.add(row)
			elif result.type == 'artist':
				self._artists_button_group.props.visible = True
				self._artists_group.add(row)
			elif result.type == 'album':
				self._albums_button_group.props.visible = True
				self._albums_group.add(row)
			elif result.type == 'playlist':
				self._playlists_button_group.props.visible = True
				self._playlists_group.add(row)
			elif result.type == 'song':
				self._songs_button_group.props.visible = True
				self._songs_group.add(row)
			else:
				self._videos_button_group.props.visible = True
				self._videos_group.add(row)

			return True

		self.props.sensitive = True
		return False

	def update_download_status(self):
		'''Make all child widgets update their download statuses.'''
		for group in (
			self._top_group,
			self._songs_group,
			self._videos_group,
			self._albums_group,
			self._playlists_group,
		):
			# Top group is non-playable when top result is an artist
			if isinstance(group, PlayableRowGroup):
				group.update_download_status()
