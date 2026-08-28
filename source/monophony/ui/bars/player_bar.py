import threading

from monophony import ID, cache
from monophony.data import PlaybackMode, PlaybackState, Song

from gi.repository import Adw, Gdk, Gio, GLib, GObject, GstAudio, Gtk, Pango


class PlayerBar(Gtk.Box):
	'''Player bar widget with playback controls and song info.'''

	__gtype_name__ = __qualname__

	def __init__(self):
		'''Initialize the widget.'''
		super().__init__(orientation=Gtk.Orientation.VERTICAL)

		self._current_song_yt_id = None

		self._buffer_bar = Gtk.ProgressBar()
		self._buffer_bar.add_css_class('buffbar')

		self._progress_bar = Gtk.Scale.new_with_range(
			Gtk.Orientation.HORIZONTAL, 0, 1, 0.01
		)
		self._progress_bar.add_css_class('seekbar')
		self._progress_bar.props.draw_value = False
		self._progress_bar.props.halign = Gtk.Align.FILL
		self._progress_bar.props.valign = Gtk.Align.END
		self._progress_bar.connect(
			'change-value',
			lambda _bar, _scroll, value, ref: ref().emit('seek', value),
			self.weak_ref()
		)

		css = Gtk.CssProvider()
		css.load_from_data('''
			.title-link {
				padding-top: 0px;
				padding-bottom: 0px;
				padding-left: 0px;
				padding-right: 0px;
				margin-bottom: -8px;
				margin-top: -8px;
			}

			.player-thumbnail {
				border-radius: 6px;
				margin-right: 4px;
				margin-top: 2px;
				margin-bottom: 2px;
			}

			.buffbar {
				min-height: 10px;
				margin-bottom: -6px;
				margin-top: 0px;
			}

			.buffbar trough {
				border-radius: 0px;
				min-height: 10px;
			}

			.buffbar progress {
				border-radius: 0px;
				min-height: 10px;
				background-color: var(--sidebar-fg-color);
				opacity: 0.5;
			}

			.seekbar {
				margin-top: -10px;
				margin-bottom: 0px;
				padding: 0px;
				min-height: 10px;
			}

			.seekbar trough, .seekbar highlight {
				border-radius: 0px;
				border-left: none;
				border-right: none;
				min-height: 10px;
			}

			.seekbar highlight {
				border-left: none;
				border-right: none;
			}

			.player {
				padding: 0px;
				background-color: var(--headerbar-bg-color);
			}
		''', -1)
		Gtk.StyleContext.add_provider_for_display(
			Gdk.Display.get_default(),
			css,
			Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
		)

		self.queue_button = Gtk.ToggleButton()
		self.queue_button.props.icon_name = 'view-list-symbolic'
		self.queue_button.props.valign = Gtk.Align.CENTER
		self.queue_button.props.tooltip_text = _('Queue')

		self._thumbnail_picture = Gtk.Picture()
		self._thumbnail_picture.props.content_fit = Gtk.ContentFit.COVER
		self._thumbnail_picture.set_size_request(40, 40)
		self._thumbnail_picture.props.valign = Gtk.Align.CENTER
		self._thumbnail_picture.props.halign = Gtk.Align.CENTER
		self._thumbnail_picture.props.visible = False
		self._thumbnail_picture.add_css_class('player-thumbnail')

		self._title_link = Gtk.LinkButton.new_with_label('', '')
		self._title_link.props.margin_bottom = 2
		self._title_link.props.margin_top = 6
		self._title_link.props.halign = Gtk.Align.START
		self._title_link.props.child.props.ellipsize = Pango.EllipsizeMode.END
		self._title_link.add_css_class('title-link')

		self._artist_label = Gtk.Label()
		self._artist_label.props.halign = Gtk.Align.START
		self._artist_label.props.ellipsize = Pango.EllipsizeMode.END
		self._artist_label.add_css_class('caption')
		self._artist_label.add_css_class('dim-label')

		info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		info_box.props.spacing = 4
		info_box.props.margin_start = 2
		info_box.props.margin_end = 6
		info_box.props.halign = Gtk.Align.START
		info_box.props.valign = Gtk.Align.CENTER
		info_box.props.hexpand = True
		info_box.append(self._title_link)
		info_box.append(self._artist_label)

		song_details_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		song_details_box.props.spacing = 6
		song_details_box.props.valign = Gtk.Align.CENTER
		song_details_box.props.halign = Gtk.Align.START
		song_details_box.props.hexpand = True
		song_details_box.append(self._thumbnail_picture)
		song_details_box.append(info_box)

		self._mode_button = Gtk.MenuButton()
		self._mode_button.props.icon_name = 'media-playlist-repeat-song-symbolic'
		self._mode_button.props.tooltip_text = _('Playback Mode')
		self._mode_button.props.valign = Gtk.Align.CENTER
		self._mode_button.props.halign = Gtk.Align.END
		self._mode_button.props.hexpand = True
		self._mode_button.set_create_popup_func(self._on_create_mode_popup)

		previous_button = Gtk.Button.new_from_icon_name('media-skip-backward-symbolic')
		previous_button.props.tooltip_text = _('Previous')
		previous_button.props.valign = Gtk.Align.CENTER
		previous_button.connect(
			'clicked',
			lambda _button, ref: ref().emit('previous-song'),
			self.weak_ref()
		)

		self._spinner = Adw.Spinner()
		self._spinner.props.margin_start = 9
		self._spinner.props.margin_end = 9
		self._spinner.props.visible = False

		self._pause_button = Gtk.Button.new_from_icon_name(
			'media-playback-pause-symbolic'
		)
		self._pause_button.props.tooltip_text = _('Pause')
		self._pause_button.props.valign = Gtk.Align.CENTER
		self._pause_button.connect(
			'clicked',
			lambda _button, ref: ref().emit('pause'),
			self.weak_ref()
		)

		next_button = Gtk.Button.new_from_icon_name('media-skip-forward-symbolic')
		next_button.props.tooltip_text = _('Next')
		next_button.props.valign = Gtk.Align.CENTER
		next_button.connect(
			'clicked', lambda _button, ref: ref().emit('next-song'), self.weak_ref()
		)

		self._volume_button = Gtk.ScaleButton.new(0, 1, 0.02, [
			'audio-volume-muted-symbolic',
			'audio-volume-high-symbolic',
			'audio-volume-low-symbolic',
			'audio-volume-medium-symbolic',
			'audio-volume-high-symbolic'
		])
		self._volume_button.props.tooltip_text = _('Volume')
		self._volume_button.props.valign = Gtk.Align.CENTER
		self._volume_button.props.halign = Gtk.Align.END
		self._volume_button.connect(
			'value-changed',
			lambda _button, value, ref: ref().emit(
				'volume-changed',
				GstAudio.stream_volume_convert_volume(
					GstAudio.StreamVolumeFormat.CUBIC,
					GstAudio.StreamVolumeFormat.LINEAR,
					value
				)
			),
			self.weak_ref()
		)

		controls_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		controls_box.props.spacing = 6
		controls_box.props.margin_top = 2
		controls_box.props.margin_bottom = 8
		controls_box.props.margin_start = 8
		controls_box.props.margin_end = 8
		controls_box.props.halign = Gtk.Align.FILL
		controls_box.props.hexpand = True
		controls_box.append(self.queue_button)
		controls_box.append(song_details_box)
		controls_box.append(self._mode_button)
		controls_box.append(previous_button)
		controls_box.append(self._spinner)
		controls_box.append(self._pause_button)
		controls_box.append(next_button)
		controls_box.append(self._volume_button)

		self._mode = PlaybackMode.NORMAL
		self.add_css_class('toolbar')
		self.add_css_class('player')
		self.append(self._buffer_bar)
		self.append(self._progress_bar)
		self.append(controls_box)

	@GObject.Signal(name='mode-changed')
	def _mode_changed(self, _mode: int):
		return

	@GObject.Signal(name='next-song')
	def _next_song(self):
		return

	@GObject.Signal(name='pause')
	def _pause(self):
		return

	@GObject.Signal(name='previous-song')
	def _previous_song(self):
		return

	@GObject.Signal(name='seek')
	def _seek(self, _value: float):
		return

	@GObject.Signal(name='volume-changed')
	def _volume_changed(self, _volume: float):
		return

	def _on_create_mode_popup(self, button: Gtk.MenuButton):
		menu = Gio.Menu()
		popover_menu = Gtk.PopoverMenu()
		popover_menu.props.menu_model = menu

		button_group = None
		for mode, label in {
			PlaybackMode.NORMAL: _('Normal Playback'),
			PlaybackMode.LOOP_SONG: _('Repeat Song'),
			PlaybackMode.LOOP_QUEUE: _('Repeat Queue'),
			PlaybackMode.RADIO: _('Autoplay Similar')
		}.items():
			check_button = Gtk.CheckButton.new_with_label(label)
			check_button.props.margin_bottom = 6
			check_button.props.margin_start = 6
			check_button.props.margin_end = 6
			check_button.props.active = self._mode == mode
			check_button.connect('toggled', self._on_mode_toggled, mode)
			if button_group:
				check_button.props.group = button_group
			else:
				check_button.props.margin_top = 6
				button_group = check_button

			item = Gio.MenuItem()
			item.set_attribute_value('custom', GLib.Variant.new_string(str(mode)))
			menu.append_item(item)
			popover_menu.add_child(check_button, str(mode))

		button.props.popover = popover_menu

	def _on_mode_toggled(self, _button: Gtk.CheckButton, mode: int):
		self.emit('mode-changed', mode)

	def update_song(self, song: Song):
		'''Update displayed song info.

		:param song: Song to display.
		'''
		self._current_song_yt_id = song.yt_id
		self._title_link.props.child.props.label = song.title
		self._title_link.props.uri = (
			'https://music.youtube.com/watch?v=' + song.yt_id
		)
		self._artist_label.props.label = song.author.name

		self._update_thumbnail(song)

	def _update_thumbnail(self, song: Song):
		if not song or not song.yt_id:
			self._thumbnail_picture.props.visible = False
			return

		cached_path = cache.get_cached_thumbnail(song.yt_id)
		if cached_path:
			self._thumbnail_picture.set_file(Gio.File.new_for_path(cached_path))
			self._thumbnail_picture.props.visible = True
		elif song.thumbnail:
			def _fetch_and_show():
				path = cache.cache_thumbnail(song.yt_id, song.thumbnail)
				if path:
					GLib.idle_add(self._show_thumbnail_file, path, song.yt_id)

			self._thumbnail_picture.props.visible = False
			threading.Thread(target=_fetch_and_show, daemon=True).start()
		else:
			self._thumbnail_picture.props.visible = False

	def _show_thumbnail_file(self, path: str, yt_id: str):
		if getattr(self, '_current_song_yt_id', None) == yt_id:
			self._thumbnail_picture.set_file(Gio.File.new_for_path(path))
			self._thumbnail_picture.props.visible = True


	def update_pause(self, pause: bool):
		'''Update the displayed pause state.

		:param pause: Pause state.
		'''
		self._pause_button.props.icon_name = (
			f'media-playback-{"start" if pause else "pause"}-symbolic'
		)

	def update_progress(self, progress: float):
		'''Update the progress bar.

		:param progress: Progress fraction (0.0-1.0).
		'''
		self._progress_bar.set_value(progress)

	def update_state(self, state: int):
		'''Update the displayed playback state.

		:param state: ``PlaybackState``.
		'''
		self._spinner.props.visible = state == PlaybackState.LOADING
		self._pause_button.props.visible = not self._spinner.props.visible
		self._progress_bar.props.sensitive = state != PlaybackState.LOADING

	def update_buffering(self, progress: float):
		'''Update the buffer bar progress.

		:param progress: Progress fraction (0.0-1.0).
		'''
		self._buffer_bar.props.fraction = progress

	def update_volume(self, volume: float):
		'''Update volume slider.

		:param volume: Volume.
		'''
		self._volume_button.props.value = GstAudio.stream_volume_convert_volume(
			GstAudio.StreamVolumeFormat.LINEAR,
			GstAudio.StreamVolumeFormat.CUBIC,
			volume
		)

	def update_mode(self, mode: int):
		'''Update displayed player mode.

		:param mode: ``PlaybackMode``.
		'''
		self._mode = mode
		self._mode_button.props.icon_name = {
			PlaybackMode.NORMAL: 'media-playlist-consecutive-symbolic',
			PlaybackMode.LOOP_SONG: 'media-playlist-repeat-song-symbolic',
			PlaybackMode.LOOP_QUEUE: 'media-playlist-repeat-symbolic',
			PlaybackMode.RADIO: ID + '-symbolic',
		}[self._mode]
