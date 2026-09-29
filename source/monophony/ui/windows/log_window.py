'''Window for viewing and filtering application and terminal logs.'''

import gettext
import re

from monophony import log
from monophony.debug import MemoryDebugger

from gi.repository import Adw, Gdk, GLib, GObject, Gtk, Pango

_ = gettext.gettext

_LOG_LINE_RE = re.compile(r'^(\d{2}:\d{2}(?::\d{2})?)\s+\[([A-Z])\]\s+([^:]+):\s*(.*)$')


class LogWindow(MemoryDebugger, Adw.Dialog):
	'''Application and terminal logs viewer dialog.'''

	__gtype_name__ = __qualname__

	def __init__(self):
		'''Initialize the log viewer dialog.'''
		super().__init__()

		self.props.title = _('Logs')
		self.props.content_width = 750
		self.props.content_height = 520

		self._raw_lines: list[str] = []
		self._filter_query: str = ''
		self._listener_registered = False

		self._build_ui()
		self._load_existing_logs()

		self.connect('closed', self._on_closed)
		log.add_listener(self._on_log_entry)
		self._listener_registered = True

	def _build_ui(self):
		toolbar_view = Adw.ToolbarView()

		header_bar = Adw.HeaderBar()

		# Clear logs button
		clear_btn = Gtk.Button.new_from_icon_name('user-trash-symbolic')
		clear_btn.props.tooltip_text = _('Clear Logs')
		clear_btn.connect('clicked', lambda _b: self._on_clear_logs())
		header_bar.pack_start(clear_btn)

		# Copy logs button
		copy_btn = Gtk.Button.new_from_icon_name('edit-copy-symbolic')
		copy_btn.props.tooltip_text = _('Copy Logs')
		copy_btn.connect('clicked', lambda _b: self._on_copy_logs())
		header_bar.pack_start(copy_btn)

		# Search / filter entry in the header bar
		self._filter_entry = Gtk.SearchEntry()
		self._filter_entry.props.placeholder_text = _('Filter logs…')
		self._filter_entry.props.tooltip_text = _('Filter logs by keyword')
		self._filter_entry.props.hexpand = True
		self._filter_entry.props.max_width_chars = 32
		self._filter_entry.connect('search-changed', self._on_filter_changed)
		header_bar.set_title_widget(self._filter_entry)

		# Auto-scroll toggle button
		self._autoscroll_btn = Gtk.ToggleButton()
		self._autoscroll_btn.props.icon_name = 'go-bottom-symbolic'
		self._autoscroll_btn.props.tooltip_text = _('Auto-scroll to latest log')
		self._autoscroll_btn.props.active = True
		header_bar.pack_end(self._autoscroll_btn)

		toolbar_view.add_top_bar(header_bar)

		# Text view for logs
		self._text_view = Gtk.TextView()
		self._text_view.props.editable = False
		self._text_view.props.cursor_visible = False
		self._text_view.props.monospace = True
		self._text_view.props.wrap_mode = Gtk.WrapMode.NONE
		self._text_view.props.top_margin = 12
		self._text_view.props.bottom_margin = 12
		self._text_view.props.left_margin = 12
		self._text_view.props.right_margin = 12
		self._text_view.add_css_class('monospace')

		self._buffer = self._text_view.get_buffer()
		self._end_mark = self._buffer.create_mark('end-mark', self._buffer.get_end_iter(), False)

		# Styling tags
		self._tag_info = self._buffer.create_tag('level_I', foreground='#3584e4')
		self._tag_warn = self._buffer.create_tag(
			'level_W', foreground='#ff7800', weight=Pango.Weight.BOLD
		)
		self._tag_error = self._buffer.create_tag(
			'level_E', foreground='#e01b24', weight=Pango.Weight.BOLD
		)
		self._tag_success = self._buffer.create_tag(
			'level_S', foreground='#2ec27e', weight=Pango.Weight.BOLD
		)
		self._tag_print = self._buffer.create_tag('level_P', foreground='#9141ac')
		self._tag_dim = self._buffer.create_tag('dim', foreground='#777777')

		self._level_tags = {
			'I': self._tag_info,
			'W': self._tag_warn,
			'E': self._tag_error,
			'S': self._tag_success,
			'P': self._tag_print
		}

		self._scrolled_window = Gtk.ScrolledWindow()
		self._scrolled_window.props.hexpand = True
		self._scrolled_window.props.vexpand = True
		self._scrolled_window.props.hscrollbar_policy = Gtk.PolicyType.AUTOMATIC
		self._scrolled_window.props.vscrollbar_policy = Gtk.PolicyType.AUTOMATIC
		self._scrolled_window.props.child = self._text_view

		self._toast_overlay = Adw.ToastOverlay()
		self._toast_overlay.props.child = self._scrolled_window

		toolbar_view.props.content = self._toast_overlay
		self.props.child = toolbar_view

	def _load_existing_logs(self):
		'''Load all current logs into buffer.'''
		lines = log.get_logs()
		self._raw_lines = list(lines)
		self._rebuild_buffer()

	def _rebuild_buffer(self):
		'''Re-render buffer contents according to active filter.'''
		self._buffer.set_text('')
		for line in self._raw_lines:
			if not self._filter_query or self._filter_query in line.lower():
				self._insert_log_line(line)

		if self._autoscroll_btn.props.active:
			self._scroll_to_end()

	def _insert_log_line(self, line: str):
		'''Parse and insert a color-coded log line into buffer.'''
		buf = self._buffer
		end_iter = buf.get_end_iter()

		match = _LOG_LINE_RE.match(line)
		if match:
			time_str, level_str, source_thread, msg = match.groups()
			buf.insert_with_tags(end_iter, f'{time_str} ', self._tag_dim)
			tag_level = self._level_tags.get(level_str, self._tag_dim)
			buf.insert_with_tags(end_iter, f'[{level_str}] ', tag_level)
			buf.insert_with_tags(end_iter, f'{source_thread}: ', self._tag_dim)
			if level_str in ('W', 'E'):
				buf.insert_with_tags(end_iter, f'{msg}\n', tag_level)
			else:
				buf.insert(end_iter, f'{msg}\n')
		else:
			buf.insert(end_iter, f'{line}\n')

	def _scroll_to_end(self):
		'''Scroll view to end mark.'''
		end_iter = self._buffer.get_end_iter()
		self._buffer.move_mark(self._end_mark, end_iter)
		self._text_view.scroll_to_mark(self._end_mark, 0.0, True, 0.0, 1.0)

	def _on_filter_changed(self, entry: Gtk.SearchEntry):
		'''Handle filter text change.'''
		self._filter_query = entry.get_text().strip().lower()
		self._rebuild_buffer()

	def _on_log_entry(self, line: str):
		'''Callback when a new log arrives or buffer is cleared.'''
		if line == '__CLEAR__':
			self._raw_lines.clear()
			self._buffer.set_text('')
			return

		self._raw_lines.append(line)
		if not self._filter_query or self._filter_query in line.lower():
			self._insert_log_line(line)
			if self._autoscroll_btn.props.active:
				self._scroll_to_end()

	def _on_copy_logs(self):
		'''Copy all visible logs to clipboard.'''
		start = self._buffer.get_start_iter()
		end = self._buffer.get_end_iter()
		text = self._buffer.get_text(start, end, False)
		if not text:
			text = '\n'.join(self._raw_lines)

		display = Gdk.Display.get_default()
		if display:
			display.get_clipboard().set(text)

		toast = Adw.Toast.new(_('Logs copied to clipboard'))
		self._toast_overlay.add_toast(toast)

	def _on_clear_logs(self):
		'''Clear logs from memory, file, and UI.'''
		log.clear_logs()
		toast = Adw.Toast.new(_('Logs cleared'))
		self._toast_overlay.add_toast(toast)

	def _on_closed(self, _dialog):
		'''Clean up log listener on dialog close.'''
		if self._listener_registered:
			log.remove_listener(self._on_log_entry)
			self._listener_registered = False

	def __del__(self):
		'''Clean up listener on garbage collection.'''
		if self._listener_registered:
			log.remove_listener(self._on_log_entry)
			self._listener_registered = False
		super().__del__()
