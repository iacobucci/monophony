'''Dialog for viewing song lyrics.'''

import gettext

from monophony.data import Song
from monophony.debug import MemoryDebugger
from monophony.yt import GetLyricsTask

from gi.repository import Adw, Gdk, GLib, Gtk, Pango

_ = gettext.gettext


class LyricsWindow(MemoryDebugger, Adw.Dialog):
	'''Dialog showing lyrics for a given song.'''

	__gtype_name__ = __qualname__

	def __init__(self, song: Song):
		'''Initialize the lyrics dialog.

		:param song: Song to display lyrics for.
		'''
		super().__init__()

		self.song = song
		self._lyrics_text = ''
		self.props.content_width = 520
		self.props.content_height = 600

		self._toast_overlay = Adw.ToastOverlay()
		self.set_child(self._toast_overlay)

		self._build_ui()
		self._load_lyrics()

	def _build_ui(self):
		toolbar_view = Adw.ToolbarView()
		self._toast_overlay.set_child(toolbar_view)

		header_bar = Adw.HeaderBar()
		title_widget = Adw.WindowTitle()
		title_widget.props.title = _('Lyrics')
		title_widget.props.subtitle = f'{self.song.title} • {self.song.author.name}'
		header_bar.props.title_widget = title_widget

		# Copy button
		self._copy_btn = Gtk.Button.new_from_icon_name('edit-copy-symbolic')
		self._copy_btn.props.tooltip_text = _('Copy Lyrics')
		self._copy_btn.props.sensitive = False
		self._copy_btn.connect('clicked', lambda _b: self._on_copy())
		header_bar.pack_start(self._copy_btn)

		toolbar_view.add_top_bar(header_bar)

		# Content Stack
		self._stack = Gtk.Stack()
		self._stack.props.transition_type = Gtk.StackTransitionType.CROSSFADE

		# 1. Loading page
		spinner_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
		spinner_box.props.valign = Gtk.Align.CENTER
		spinner_box.props.halign = Gtk.Align.CENTER
		spinner = Adw.Spinner()
		spinner.props.width_request = 48
		spinner.props.height_request = 48
		loading_label = Gtk.Label(label=_('Loading lyrics…'))
		loading_label.add_css_class('dim-label')
		spinner_box.append(spinner)
		spinner_box.append(loading_label)
		self._stack.add_named(spinner_box, 'loading')

		# 2. Lyrics page
		scrolled = Gtk.ScrolledWindow()
		scrolled.props.hscrollbar_policy = Gtk.PolicyType.NEVER
		scrolled.props.vscrollbar_policy = Gtk.PolicyType.AUTOMATIC

		content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=18)
		content_box.props.margin_start = 24
		content_box.props.margin_end = 24
		content_box.props.margin_top = 28
		content_box.props.margin_bottom = 28

		self._lyrics_label = Gtk.Label()
		self._lyrics_label.props.selectable = True
		self._lyrics_label.props.wrap = True
		self._lyrics_label.props.wrap_mode = Pango.WrapMode.WORD_CHAR
		self._lyrics_label.props.justify = Gtk.Justification.CENTER
		self._lyrics_label.add_css_class('body')
		self._lyrics_label.add_css_class('lyrics-text')

		self._source_label = Gtk.Label()
		self._source_label.props.selectable = False
		self._source_label.add_css_class('dim-label')
		self._source_label.add_css_class('caption')

		content_box.append(self._lyrics_label)
		content_box.append(self._source_label)
		scrolled.set_child(content_box)
		self._stack.add_named(scrolled, 'lyrics')

		# 3. Empty / Not available page
		self._status_page = Adw.StatusPage()
		self._status_page.props.icon_name = 'music-note-symbolic'
		self._status_page.props.title = _('No Lyrics Available')
		self._status_page.props.description = _(
			'Lyrics could not be found for this song.'
		)
		self._stack.add_named(self._status_page, 'empty')

		toolbar_view.props.content = self._stack
		self._stack.set_visible_child_name('loading')

	def _load_lyrics(self):
		task = GetLyricsTask(
			args=(self.song.yt_id, self.song.title, self.song.author.name),
			callback=lambda t, ref: (r := ref()) and r._on_lyrics_loaded(t),
			callback_args=(self.weak_ref(),)
		)
		task.start()

	def _on_lyrics_loaded(self, task: GetLyricsTask):
		res = task.result
		if res and res.get('lyrics'):
			self._lyrics_text = res['lyrics']
			self._lyrics_label.props.label = self._lyrics_text
			source_text = res.get('source') or ''
			self._source_label.props.label = source_text
			self._source_label.props.visible = bool(source_text)
			self._copy_btn.props.sensitive = True
			self._stack.set_visible_child_name('lyrics')
		else:
			self._stack.set_visible_child_name('empty')

	def _on_copy(self):
		if not self._lyrics_text:
			return
		clipboard = Gdk.Display.get_default().get_clipboard()
		clipboard.set(self._lyrics_text)
		toast = Adw.Toast.new(_('Lyrics copied to clipboard'))
		self._toast_overlay.add_toast(toast)
