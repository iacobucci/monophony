'''Window for managing application settings, caching, and prefetching options.'''

from monophony import MIN_WIDTH, cache, settings
from monophony.debug import MemoryDebugger

from gi.repository import Adw, GObject, Gtk


class SettingsWindow(MemoryDebugger, Adw.Dialog):
	'''Settings Window.'''

	__gtype_name__ = __qualname__

	def __init__(self):
		'''Initialize the window.'''
		super().__init__()

		self.props.title = _('Settings')
		self.props.content_width = MIN_WIDTH

		self._build_ui()

	def _build_ui(self):
		page = Adw.PreferencesPage()

		# --- Cache Group ---
		cache_group = Adw.PreferencesGroup()
		cache_group.props.title = _('Audio Caching')
		cache_group.props.description = _(
			'Store played and prefetched tracks locally for instant, zero-buffer playback.'
		)

		self._cache_switch = Adw.SwitchRow()
		self._cache_switch.props.title = _('Enable Audio Cache')
		self._cache_switch.props.subtitle = _('Save tracks locally to eliminate buffering delays')
		self._cache_switch.props.active = settings.load('cache_enabled', True)
		self._cache_switch.connect(
			'notify::active',
			lambda switch, _param: settings.save({'cache_enabled': switch.props.active})
		)
		cache_group.add(self._cache_switch)

		self._cache_size_entry = Adw.EntryRow()
		self._cache_size_entry.props.title = _('Max Cache Size (MB)')
		self._cache_size_entry.props.text = str(settings.load('cache_max_size_mb', 1000))
		self._cache_size_entry.connect(
			'changed',
			lambda entry: self._on_cache_size_changed(entry.props.text)
		)
		cache_group.add(self._cache_size_entry)

		self._usage_row = Adw.ActionRow()
		self._usage_row.props.title = _('Cache Usage')
		self._update_usage_subtitle()

		clear_cache_btn = Gtk.Button()
		clear_cache_btn.props.label = _('Clear Cache')
		clear_cache_btn.add_css_class('destructive-action')
		clear_cache_btn.connect('clicked', lambda _btn: self._on_clear_cache())
		self._usage_row.add_suffix(clear_cache_btn)
		cache_group.add(self._usage_row)

		page.add(cache_group)

		# --- Prefetch Group ---
		prefetch_group = Adw.PreferencesGroup()
		prefetch_group.props.title = _('Playlist Prefetching')
		prefetch_group.props.description = _(
			'Pre-download upcoming songs in your playlist queue in the background.'
		)

		self._prefetch_switch = Adw.SwitchRow()
		self._prefetch_switch.props.title = _('Enable Prefetching')
		self._prefetch_switch.props.subtitle = _('Download upcoming playlist tracks before they start playing')
		self._prefetch_switch.props.active = settings.load('prefetch_enabled', True)
		self._prefetch_switch.connect(
			'notify::active',
			lambda switch, _param: settings.save({'prefetch_enabled': switch.props.active})
		)
		prefetch_group.add(self._prefetch_switch)

		self._prefetch_count_entry = Adw.EntryRow()
		self._prefetch_count_entry.props.title = _('Tracks to Prefetch')
		self._prefetch_count_entry.props.text = str(settings.load('prefetch_count', 2))
		self._prefetch_count_entry.connect(
			'changed',
			lambda entry: self._on_prefetch_count_changed(entry.props.text)
		)
		prefetch_group.add(self._prefetch_count_entry)

		page.add(prefetch_group)

		toolbar_view = Adw.ToolbarView()
		toolbar_view.props.content = page
		toolbar_view.add_top_bar(Adw.HeaderBar())

		self.props.child = toolbar_view

	def _update_usage_subtitle(self):
		mb_used = cache.get_cache_size_mb()
		max_mb = settings.load('cache_max_size_mb', 1000)
		self._usage_row.props.subtitle = _(f'{mb_used:.1f} MB used of {max_mb} MB limit')

	def _on_cache_size_changed(self, text: str):
		try:
			val = int(text.strip())
			if val > 0:
				settings.save({'cache_max_size_mb': val})
				cache.enforce_cache_limits()
				self._update_usage_subtitle()
		except ValueError:
			pass

	def _on_prefetch_count_changed(self, text: str):
		try:
			val = int(text.strip())
			if val >= 0:
				settings.save({'prefetch_count': val})
		except ValueError:
			pass

	def _on_clear_cache(self):
		cache.clear_cache()
		self._update_usage_subtitle()
