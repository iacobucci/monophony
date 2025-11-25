import gc
import os

import logboth
from gi.repository import GLib, GObject


_DEBUG_VARIABLE = 'MONOPHONY_DEBUG'


def log_memory_status() -> bool:
	gobject_count = 0
	other_count = 0
	gc.collect()
	for obj in gc.get_objects():
		if isinstance(obj, GObject.Object):
			gobject_count += 1
		else:
			other_count += 1

	logboth.info(
		__name__,
		f'{gobject_count} GObjects and {other_count} other objects in memory'
	)
	return True


# Use with multiple inheriance: class Class(MemoryDebugger, ...)
class MemoryDebugger:
	def __del__(self):
		logboth.info(__name__, f'Collected {self.__class__.__name__}')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		logboth.info(__name__, f'Initialized {self.__class__.__name__}')


debug_active = os.getenv(_DEBUG_VARIABLE)
if debug_active:
	logboth.warning(__name__, 'Debug mode enabled, expect low performance')
	GLib.timeout_add_seconds(2, log_memory_status)
else:
	del MemoryDebugger.__del__
	del MemoryDebugger.__init__
