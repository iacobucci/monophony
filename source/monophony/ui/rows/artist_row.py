'''Artist row widget.'''

from monophony.data import Artist
from monophony.debug import MemoryDebugger

from gi.repository import Adw, GLib, GObject, Gtk


class ArtistRow(MemoryDebugger, Adw.ActionRow):
	'''Artist row widget.'''

	__gtype_name__ = __qualname__

	def __init__(self, artist: Artist):
		'''Initialize the widget for an artist.

		:param artist: Artist to initialize for.
		'''
		super().__init__()

		self.artist = artist

		self.props.tooltip_text = _('View Artist')
		self.props.activatable = True
		self.props.title = GLib.markup_escape_text(artist.name, -1)

		view_button = Gtk.Button.new_from_icon_name('go-next-symbolic')
		view_button.props.tooltip_text = _('View Artist')
		view_button.props.vexpand = False
		view_button.props.valign = Gtk.Align.CENTER
		view_button.props.has_frame = False
		self.add_suffix(view_button)
		self.connect('activated', lambda row: row.emit('view-artist', row.artist))

	@GObject.Signal(name='view-artist', arg_types=(object,))
	def _view_artist(self, _artist: Artist):
		return
