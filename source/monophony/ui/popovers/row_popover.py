'''Popover widget for rows.'''

from monophony.debug import MemoryDebugger

from gi.repository import Gtk


class RowPopover(MemoryDebugger, Gtk.PopoverMenu):
	'''Popover widget for rows.'''

	__gtype_name__ = __qualname__
	actions = ()
	'''Actions (signals) implemented in the class.'''

	def __init_subclass__(cls, **kwargs):
		'''Initialize subclass.

		Installs actions (signals) supported by the subclass.
		'''
		super().__init_subclass__(**kwargs)

		for action in cls.actions:
			cls.install_action(
				cls.__gtype_name__ + '.' + action, None, cls.emit_signal_from_action
			)

	def emit_signal_from_action(self, action: str, _property: None):
		'''Emit signal based on action name.

		:param action: Action to emit signal for.
		'''
		self.emit(action.rsplit('.', maxsplit=1)[-1])
