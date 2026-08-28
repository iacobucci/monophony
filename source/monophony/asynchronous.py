'''Custom threading wrapper.'''

import threading
from collections.abc import Callable
from typing import Any

from monophony.debug import MemoryDebugger

from gi.repository import GLib


_user_priority_counter = 0
_user_priority_lock = threading.Lock()
_user_priority_cond = threading.Condition(_user_priority_lock)


def acquire_user_priority():
	'''Increase active user-initiated priority task count.'''
	global _user_priority_counter
	with _user_priority_cond:
		_user_priority_counter += 1


def release_user_priority():
	'''Decrease active user-initiated priority task count and notify background tasks.'''
	global _user_priority_counter
	with _user_priority_cond:
		_user_priority_counter = max(0, _user_priority_counter - 1)
		if _user_priority_counter == 0:
			_user_priority_cond.notify_all()


def wait_if_user_priority():
	'''Pause background task execution while a user-initiated task (search, play) is running.'''
	with _user_priority_cond:
		while _user_priority_counter > 0:
			_user_priority_cond.wait(timeout=0.2)


class UserPriorityContext:
	'''Context manager to treat a block of code as a high priority user action.'''

	def __enter__(self):
		acquire_user_priority()
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		release_user_priority()


class Task(MemoryDebugger):
	'''Threaded function runner with main thread callback and thread-safe result.

	Inherit from this to create new types of tasks.
	'''

	is_user_priority = False

	def __init__(
		self,
		progress_callback: Callable | None=None,
		callback: Callable | None=None,
		callback_args: tuple | None=None,
		callback_kwargs: dict | None=None,
		args: tuple | None=None,
		kwargs: dict | None=None
	):
		'''Initialize with configuration.

		:param progress_callback: Function to call on main thread with progress info
			whenever progress is made.
		:param callback: Function to call on main thread when done.
		:param callback_args: Arguments to pass to callback function.
		:param callback_kwargs: Keyword arguments to pass to callback function.
		:param args: Arguments to pass to this task's function.
		:param kwargs: Keyword arguments to pass to this task's function.
		'''
		super().__init__()

		self.__args = args or ()
		self.__kwargs = kwargs or {}
		self.__callback = callback
		self.__callback_args = callback_args or ()
		self.__callback_kwargs = callback_kwargs or {}
		self.__progress_callback = progress_callback

		self.extra_data: Any = None
		'''For storing any additional data in the task.'''

		self.result: Any = None
		'''Return value of the task's function.

		Should only be accessed once the task is finished - usually in the callback.
		'''

		self._canceled = False
		self._thread = threading.Thread(
			target=self.__perform,
			args=self.__args,
			kwargs=self.__kwargs,
			name=self.__class__.__qualname__
		)
		self._thread.daemon = True

	def __perform(self, *args, **kwargs):
		if getattr(self, 'is_user_priority', False):
			acquire_user_priority()
		try:
			self.result = self._function(*args, **kwargs)
		finally:
			if getattr(self, 'is_user_priority', False):
				release_user_priority()

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
		'''Check if the task has been canceled.

		:return: Cancelation state.
		'''
		return self._canceled

	def is_running(self) -> bool:
		'''Check if the task is running.

		All of the following must be true:

		* The task has been started.
		* The task has not finished yet.
		* The task has not been canceled.

		:return: Running state.
		'''
		return self._thread.is_alive() and not self._canceled

	def cancel(self):
		'''Cancel the task.

		This does not actually stop the task or prevent it from calling its callback.
		Task implementations should periodically check if they have been canceled
		and exit from their functions as soon as possible to avoid wasting system
		resources. Callback functions should check their calling tasks and disregard
		calls from canceled ones.
		'''
		self._canceled = True

	def start(self):
		'''Start the task.

		If the task is already running, this has no effect. Tasks are not meant to be
		reused and this method should only be called once per task.
		'''
		if not self.is_running():
			self._thread.start()
