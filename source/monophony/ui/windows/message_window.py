from monophony.debug import MemoryDebugger

from gi.repository import Adw


class MessageWindow(MemoryDebugger, Adw.AlertDialog):
	def __init__(self, title: str, details: str):
		super().__init__()

		self.props.heading = title
		self.props.body = details
		self.add_response('dismiss', _('Ok'))
