import threading
from collections.abc import Callable
from typing import Any

from monophony.debug import MemoryDebugger

from gi.repository import GLib


class Task(MemoryDebugger):
	def __init__(
		self,
		progress_callback: Callable | None=None,
		callback: Callable | None=None,
		callback_args: tuple | None=None,
		callback_kwargs: dict | None=None,
		args: tuple | None=None,
		kwargs: dict | None=None
	):
		super().__init__()

		self.__args = args or ()
		self.__kwargs = kwargs or {}
		self.__callback = callback
		self.__callback_args = callback_args or ()
		self.__callback_kwargs = callback_kwargs or {}
		self.__progress_callback = progress_callback
		self.extra_data = None
		self.result = None
		self._canceled = False
		self._thread = threading.Thread(
			target=self.__perform,
			args=self.__args,
			kwargs=self.__kwargs,
			name=self.__class__.__qualname__
		)
		self._thread.daemon = True

	def __perform(self, *args, **kwargs):
		self.result = self._function(*args, **kwargs)
		if self.__callback:
			GLib.idle_add(
				self.__callback, self, *self.__callback_args, **self.__callback_kwargs
			)

	def _function(self, *args, **kwargs) -> Any:
		...

	def _update_progress(self, *args, **kwargs):
		if self.__progress_callback:
			GLib.idle_add(self.__progress_callback, self, *args, **kwargs)

	def is_canceled(self) -> bool:
		return self._canceled

	def is_running(self) -> bool:
		return self._thread.is_alive() and not self._canceled

	def cancel(self):
		self._canceled = True

	def start(self):
		if not self.is_running():
			self._thread.start()
