from monophony.debug import MemoryDebugger

from gi.repository import Gtk


class RowPopover(MemoryDebugger, Gtk.PopoverMenu):
	__gtype_name__ = __qualname__
	actions = ()

	def __init_subclass__(cls, **kwargs):
		super().__init_subclass__(**kwargs)

		for action in cls.actions:
			cls.install_action(
				cls.__gtype_name__ + '.' + action, None, cls.emit_signal_from_action
			)

	def emit_signal_from_action(self, action: str, _property: None):
		self.emit(action.rsplit('.', maxsplit=1)[-1])
