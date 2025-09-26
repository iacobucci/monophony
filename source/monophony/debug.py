import gc
import os

from monophony import logging

from gi.repository import GLib, GObject


_DEBUG_VARIABLE = 'DEBUG'


def is_active() -> bool:
	return bool(os.getenv(_DEBUG_VARIABLE))


def log_memory_status() -> bool:
	gobject_count = 0
	other_count = 0
	gc.collect()
	for obj in gc.get_objects():
		if isinstance(obj, GObject.Object):
			gobject_count += 1
		else:
			other_count += 1

	logging.info(
		__name__,
		f'{gobject_count} GObjects and {other_count} other objects in memory'
	)
	return True


# Use with multiple inheriance: class Class(MemoryDebugger, ...)
class MemoryDebugger:
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		if is_active():
			logging.info(__name__, f'Initialized {self.__class__.__name__}')

	def __del__(self):
		if is_active():
			logging.info(__name__, f'Collected {self.__class__.__name__}')


if is_active():
	logging.warning(__name__, 'Debug mode enabled, expect low performance')
	GLib.timeout_add_seconds(2, log_memory_status)
