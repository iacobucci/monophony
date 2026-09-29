'''Log management and terminal printing wrapper.

Captures all terminal output and log messages into an in-memory buffer
for real-time display and searching in the UI.
'''

import builtins
import collections
import gettext
import threading
import time
from typing import Any, Callable

import logboth
import logboth._core
from gi.repository import GLib

_ = gettext.gettext

MAX_ENTRIES = 5000

_lock = threading.Lock()
_entries: collections.deque[str] = collections.deque(maxlen=MAX_ENTRIES)
_listeners: list[Callable[[str], None]] = []
_wrapped = False

_orig_log = logboth._core._log
_orig_print = builtins.print


def _dispatch_listener(listener: Callable[[str], None], line: str):
	try:
		listener(line)
	except Exception:
		pass
	return GLib.SOURCE_REMOVE


def _notify_listeners(line: str):
	'''Notify all listeners on the GLib main loop.'''
	with _lock:
		listeners = list(_listeners)

	for listener in listeners:
		try:
			GLib.idle_add(_dispatch_listener, listener, line)
		except Exception:
			pass


def add_entry(line: str):
	'''Add a line to in-memory log buffer and notify listeners.'''
	with _lock:
		_entries.append(line)
	_notify_listeners(line)


def get_logs() -> list[str]:
	'''Return all logged lines in memory.'''
	with _lock:
		return list(_entries)


def get_logs_text() -> str:
	'''Return all logs as a single newline-delimited string.'''
	with _lock:
		return '\n'.join(_entries)


def clear_logs():
	'''Clear both in-memory log buffer and log file.'''
	with _lock:
		_entries.clear()
	try:
		logboth.clear()
	except Exception:
		pass
	_notify_listeners('__CLEAR__')


def add_listener(callback: Callable[[str], None]):
	'''Add a listener callback receiving new log lines (or '__CLEAR__').'''
	with _lock:
		if callback not in _listeners:
			_listeners.append(callback)


def remove_listener(callback: Callable[[str], None]):
	'''Remove a listener callback.'''
	with _lock:
		if callback in _listeners:
			_listeners.remove(callback)


def _custom_log(level: type, source: str, text: str, details: str):
	'''Wrapped logboth logging handler.'''
	text_clean = str(text).strip()
	details_clean = str(details).strip()
	level_letter = getattr(level, 'name', 'I')[0] if hasattr(level, 'name') else 'I'
	thread_name = threading.current_thread().name

	line_head = f'{time.strftime("%H:%M")} [{level_letter}] {source} ({thread_name}):'
	line_tail = f' {text_clean}'
	full_line = f'{line_head}{line_tail}'

	if details_clean:
		full_line += f'\n{details_clean}'

	add_entry(full_line)

	return _orig_log(level, source, text, details)


def _custom_print(*args: Any, **kwargs: Any):
	'''Wrapped builtins.print handler.'''
	sep = kwargs.get('sep', ' ')
	msg = sep.join(str(a) for a in args)
	thread_name = threading.current_thread().name
	line = f'{time.strftime("%H:%M")} [P] stdout ({thread_name}): {msg}'
	add_entry(line)

	return _orig_print(*args, **kwargs)


def init_logging_wrapper():
	'''Initialize wrappers for terminal printing and logging methods.'''
	global _wrapped
	with _lock:
		if _wrapped:
			return
		_wrapped = True

	# Pre-load any existing logs from log file if present
	try:
		existing = logboth.read()
		if existing:
			for line in existing.splitlines():
				if line.strip():
					_entries.append(line)
	except Exception:
		pass

	# Hook core log handler
	logboth._core._log = _custom_log

	# Hook individual methods in logboth to guarantee interception
	def _wrap_info(source: Any, text: Any, details: Any = ''):
		return logboth._core.info(source, text, details)

	def _wrap_warning(source: Any, text: Any, details: Any = ''):
		return logboth._core.warning(source, text, details)

	def _wrap_error(source: Any, text: Any, details: Any = ''):
		return logboth._core.error(source, text, details)

	def _wrap_success(source: Any, text: Any, details: Any = ''):
		return logboth._core.success(source, text, details)

	logboth.info = _wrap_info
	logboth.warning = _wrap_warning
	logboth.error = _wrap_error
	logboth.success = _wrap_success

	# Hook built-in print
	builtins.print = _custom_print
