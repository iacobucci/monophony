'''Window for showing messages.'''

from monophony.debug import MemoryDebugger

from gi.repository import Adw


class MessageWindow(MemoryDebugger, Adw.AlertDialog):
	'''Message window.'''

	def __init__(self, title: str, details: str):
		'''Initialize with title and message.

		:param title: Window title.
		:param details: Text to place inside the window.
		'''
		super().__init__()

		self.props.heading = title
		self.props.body = details
		self.add_response('dismiss', _('Ok'))
