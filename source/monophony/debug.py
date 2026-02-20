'''Debugging tools.

When the environment variable ``MONOPHONY_DEBUG`` is set, memory status is logged
automatically every 2 seconds.
'''

import gc
import os

import logboth
from gi.repository import GLib, GObject


_DEBUG_VARIABLE = 'MONOPHONY_DEBUG'


def _log_memory_status() -> bool:
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


class MemoryDebugger:
	'''An object that logs information about its own initialization and deletion.

	The environment variable ``MONOPHONY_DEBUG`` must be set for this class to
	do anything.

	Most classes should inherit from this first to allow for better debugging:

	.. code-block::

		class Class(MemoryDebugger, ...)

	'''

	def __del__(self):
		'''Log own class name on deletion.'''
		logboth.info(__name__, f'Collected {self.__class__.__name__}')

	def __init__(self, *args, **kwargs):
		'''Log own class name on initialization.'''
		super().__init__(*args, **kwargs)

		logboth.info(__name__, f'Initialized {self.__class__.__name__}')


if os.getenv(_DEBUG_VARIABLE):
	logboth.warning(__name__, 'Debug mode enabled, expect low performance')
	GLib.timeout_add_seconds(2, _log_memory_status)
else:
	del MemoryDebugger.__del__
	del MemoryDebugger.__init__
