'''Window for YouTube account integration and playlist synchronization.'''

import subprocess

from monophony import MIN_WIDTH, playlists, settings, yt
from monophony.debug import MemoryDebugger
from monophony.playlists import SyncPlaylistsTask

from gi.repository import Adw, Gdk, Gio, GLib, GObject, Gtk



# Default empty credentials requiring user's own matching OAuth client ID and Secret from Google Cloud Console
DEFAULT_CLIENT_ID = ''
DEFAULT_CLIENT_SECRET = ''


class AccountWindow(MemoryDebugger, Adw.Dialog):
	'''YouTube Account Integration Window.'''

	__gtype_name__ = __qualname__

	def __init__(self):
		'''Initialize the window.'''
		super().__init__()

		self.props.title = _('YouTube Account Integration')
		self.props.content_width = MIN_WIDTH

		self._oauth_code_info = None
		self._error_msg = ''
		self._build_ui()

	@GObject.Signal(name='sync-finished')
	def _sync_finished(self):
		return

	def _build_ui(self):
		self._page = Adw.PreferencesPage()

		if self._error_msg:
			err_group = Adw.PreferencesGroup()
			err_row = Adw.ActionRow()
			err_row.props.title = _('Authentication Error')
			err_row.props.subtitle = self._error_msg
			err_icon = Gtk.Image.new_from_icon_name('dialog-error-symbolic')
			err_row.add_prefix(err_icon)
			err_group.add(err_row)
			self._page.add(err_group)

		if yt.is_authenticated():
			status_row = Adw.ActionRow()
			status_row.props.title = _('Status')
			status_row.props.subtitle = _('Connected to YouTube Account')
			status_icon = Gtk.Image.new_from_icon_name('emblem-ok-symbolic')
			status_row.add_prefix(status_icon)

			self._auto_sync_switch = Adw.SwitchRow()
			self._auto_sync_switch.props.title = _('Auto-sync on startup')
			self._auto_sync_switch.props.subtitle = _('Automatically synchronize playlists when opening Monophony')
			self._auto_sync_switch.props.active = settings.load('auto_sync_playlists', True)
			self._auto_sync_switch.connect(
				'notify::active',
				lambda switch, _param: settings.save({'auto_sync_playlists': switch.props.active})
			)

			account_group = Adw.PreferencesGroup()
			account_group.props.title = _('Account Status')
			account_group.add(status_row)
			account_group.add(self._auto_sync_switch)

			self._sync_button = Gtk.Button()
			self._sync_button.props.label = _('Sync Playlists Now')
			self._sync_button.add_css_class('suggested-action')
			self._sync_button.connect('clicked', lambda _btn: self._on_sync_now())

			self._logout_button = Gtk.Button()
			self._logout_button.props.label = _('Disconnect Account')
			self._logout_button.add_css_class('destructive-action')
			self._logout_button.connect('clicked', lambda _btn: self._on_logout())

			action_bar = Gtk.ActionBar()
			action_bar.pack_start(self._logout_button)
			action_bar.pack_end(self._sync_button)

			self._page.add(account_group)
		else:
			creds_group = Adw.PreferencesGroup()
			creds_group.props.title = _('YouTube OAuth Authentication')
			creds_group.props.description = _(
				'Enter your Google Cloud OAuth Client ID and Secret (both from the same project) or import an oauth.json file.'
			)

			cid = settings.load('oauth_client_id', '')
			sec = settings.load('oauth_client_secret', '')

			self._client_id_entry = Adw.EntryRow()
			self._client_id_entry.props.title = _('OAuth Client ID')
			self._client_id_entry.props.text = cid

			self._client_secret_entry = Adw.EntryRow()
			self._client_secret_entry.props.title = _('OAuth Client Secret')
			self._client_secret_entry.props.text = sec

			def _on_id_changed(entry):
				val = entry.props.text.strip()
				if val:
					settings.save({'oauth_client_id': val})

			def _on_secret_changed(entry):
				val = entry.props.text.strip()
				if val:
					settings.save({'oauth_client_secret': val})

			self._client_id_entry.connect('changed', _on_id_changed)
			self._client_secret_entry.connect('changed', _on_secret_changed)

			creds_group.add(self._client_id_entry)
			creds_group.add(self._client_secret_entry)



			import_file_btn = Gtk.Button()
			import_file_btn.props.label = _('Import oauth.json File...')
			import_file_btn.connect('clicked', lambda _btn: self._on_import_file())

			import_row = Adw.ActionRow()
			import_row.props.title = _('Already have an oauth.json file?')
			import_row.add_suffix(import_file_btn)
			creds_group.add(import_row)

			self._page.add(creds_group)


			if self._oauth_code_info:
				flow_group = Adw.PreferencesGroup()
				flow_group.props.title = _('Authorization Steps')

				verification_url = self._oauth_code_info.get('verification_url', 'https://www.google.com/device')
				user_code = self._oauth_code_info.get('user_code', '')
				full_url = f"{verification_url}?user_code={user_code}" if user_code and 'user_code' not in verification_url else verification_url

				url_row = Adw.ActionRow()
				url_row.props.title = _('1. Authorization Web Address')
				url_row.props.subtitle = verification_url

				copy_url_btn = Gtk.Button()
				copy_url_btn.props.label = _('Copy Link')
				copy_url_btn.connect('clicked', lambda _btn, link=full_url: Gdk.Display.get_default().get_clipboard().set(link))
				url_row.add_suffix(copy_url_btn)
				flow_group.add(url_row)

				code_row = Adw.ActionRow()
				code_row.props.title = _('2. Your Code')
				code_label = Gtk.Label(label=f"<b>{user_code}</b>")
				code_label.props.use_markup = True
				code_label.add_css_class('title-1')

				copy_code_btn = Gtk.Button()
				copy_code_btn.props.label = _('Copy Code')
				copy_code_btn.connect('clicked', lambda _btn, code=user_code: Gdk.Display.get_default().get_clipboard().set(code))

				code_row.add_suffix(code_label)
				code_row.add_suffix(copy_code_btn)
				flow_group.add(code_row)

				open_browser_btn = Gtk.Button()
				open_browser_btn.props.label = _('Open Authorization Page')
				open_browser_btn.add_css_class('suggested-action')
				open_browser_btn.connect('clicked', lambda _btn: self._on_open_browser())

				browser_row = Adw.ActionRow()
				browser_row.props.title = _('3. Open Browser Automatically')
				browser_row.add_suffix(open_browser_btn)
				flow_group.add(browser_row)

				self._page.add(flow_group)

				self._finish_button = Gtk.Button()
				self._finish_button.props.label = _('Complete Authorization')
				self._finish_button.add_css_class('suggested-action')
				self._finish_button.connect('clicked', lambda _btn: self._on_finish_auth())

				action_bar = Gtk.ActionBar()
				action_bar.pack_end(self._finish_button)
			else:
				self._start_button = Gtk.Button()
				self._start_button.props.label = _('Connect YouTube Account')
				self._start_button.add_css_class('suggested-action')
				self._start_button.connect('clicked', lambda _btn: self._on_start_auth())

				action_bar = Gtk.ActionBar()
				action_bar.pack_end(self._start_button)

		toolbar_view = Adw.ToolbarView()
		toolbar_view.props.content = self._page
		toolbar_view.add_top_bar(Adw.HeaderBar())
		toolbar_view.add_bottom_bar(action_bar)

		self.props.child = toolbar_view

	def _on_start_auth(self):
		cid = self._client_id_entry.props.text.strip()
		sec = self._client_secret_entry.props.text.strip()
		if not cid or not sec:
			return

		settings.save({'oauth_client_id': cid, 'oauth_client_secret': sec})
		self.props.sensitive = False

		self._start_button.props.child = Adw.Spinner()
		code_info = yt.start_oauth_flow(cid, sec)
		self.props.sensitive = True
		if code_info:
			self._oauth_code_info = code_info
			self._build_ui()

	def _on_open_browser(self):
		if not self._oauth_code_info:
			return
		url = self._oauth_code_info.get('verification_url', 'https://www.google.com/device')
		user_code = self._oauth_code_info.get('user_code', '')
		if user_code and 'user_code' not in url:
			url = f"{url}?user_code={user_code}"
		try:
			Gio.AppInfo.launch_default_for_uri(url, None)
		except Exception:
			pass
		try:
			subprocess.Popen(['xdg-open', url])
		except Exception:
			pass


	def _on_finish_auth(self):
		if not self._oauth_code_info:
			return
		cid = self._client_id_entry.props.text.strip()
		sec = self._client_secret_entry.props.text.strip()
		device_code = self._oauth_code_info.get('device_code', '')

		self.props.sensitive = False
		self._finish_button.props.child = Adw.Spinner()
		success, err_msg = yt.finish_oauth_flow(cid, sec, device_code)
		self.props.sensitive = True

		if success:
			self._oauth_code_info = None
			self._error_msg = ''
			self._build_ui()
		else:
			self._error_msg = err_msg
			self._build_ui()


	def _on_logout(self):
		yt.logout_account()
		self._oauth_code_info = None
		self._build_ui()

	def _on_import_file(self):
		dialog = Gtk.FileDialog()
		dialog.set_title(_('Select oauth.json File'))
		dialog.open(self, None, self._on_file_selected)

	def _on_file_selected(self, dialog: Gtk.FileDialog, result):
		try:
			file = dialog.open_finish(result)
			if file:
				filepath = file.get_path()
				if yt.import_oauth_file(filepath):
					self._oauth_code_info = None
					self._error_msg = ''
					self._build_ui()
				else:
					self._error_msg = _('Invalid oauth.json file.')
					self._build_ui()
		except Exception:
			pass

	def _on_sync_now(self):
		self.props.sensitive = False
		self._sync_button.props.child = Adw.Spinner()
		task = SyncPlaylistsTask(callback=self._on_sync_finished_callback)
		task.start()

	def _on_sync_finished_callback(self, task: SyncPlaylistsTask):
		self.props.sensitive = True
		self._sync_button.props.child = None
		self._sync_button.props.label = _('Sync Playlists Now')
		self.emit('sync-finished')

