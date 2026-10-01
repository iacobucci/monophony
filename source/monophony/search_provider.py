'''GNOME Shell Search Provider implementation for Monophony.'''

import os
import shutil
import subprocess
import threading

import logboth
from monophony import yt
from monophony.data import Group, Song

from gi.repository import Gio, GLib

SEARCH_PROVIDER_XML = '''
<node>
  <interface name='org.gnome.Shell.SearchProvider2'>
    <method name='GetInitialResultSet'>
      <arg type='as' name='terms' direction='in'/>
      <arg type='as' name='results' direction='out'/>
    </method>
    <method name='GetSubsearchResultSet'>
      <arg type='as' name='previous_results' direction='in'/>
      <arg type='as' name='new_terms' direction='in'/>
      <arg type='as' name='results' direction='out'/>
    </method>
    <method name='GetResultMetas'>
      <arg type='as' name='results' direction='in'/>
      <arg type='aa{sv}' name='metas' direction='out'/>
    </method>
    <method name='ActivateResult'>
      <arg type='s' name='identifier' direction='in'/>
      <arg type='as' name='terms' direction='in'/>
      <arg type='u' name='timestamp' direction='in'/>
    </method>
    <method name='LaunchSearch'>
      <arg type='as' name='terms' direction='in'/>
      <arg type='u' name='timestamp' direction='in'/>
    </method>
  </interface>
</node>
'''

BUS_NAME = 'io.gitlab.zehkira.Monophony.SearchProvider'
OBJECT_PATH = '/io/gitlab/zehkira/Monophony/SearchProvider'


class SearchProvider:
	'''Implements org.gnome.Shell.SearchProvider2 for GNOME Shell search integration.'''

	def __init__(self, application=None):
		self._app = application
		self._registration_id = None
		self._connection = None
		self._results_cache = {}
		self._lock = threading.Lock()

	def register(self, connection=None):
		'''Register the SearchProvider on the application's or session D-Bus connection.'''
		if connection is None:
			if self._app and hasattr(self._app, 'get_dbus_connection'):
				connection = self._app.get_dbus_connection()
			else:
				connection = Gio.bus_get_sync(Gio.BusType.SESSION, None)

		if not connection:
			logboth.warning(__name__, 'Cannot register SearchProvider: no D-Bus connection')
			return

		self._connection = connection
		node_info = Gio.DBusNodeInfo.new_for_xml(SEARCH_PROVIDER_XML)
		interface_info = node_info.interfaces[0]

		self._registration_id = connection.register_object(
			OBJECT_PATH,
			interface_info,
			self._handle_method_call,
			None,
			None
		)
		logboth.info(__name__, f'Registered GNOME Shell SearchProvider at {OBJECT_PATH}')

	def unregister(self):
		'''Unregister the SearchProvider from D-Bus.'''
		if self._registration_id and self._connection:
			self._connection.unregister_object(self._registration_id)
			self._registration_id = None

	def _handle_method_call(
		self, connection, sender, object_path, interface_name, method_name, parameters, invocation
	):
		if method_name == 'GetInitialResultSet':
			terms = parameters.unpack()[0]
			self._handle_search(terms, invocation)
		elif method_name == 'GetSubsearchResultSet':
			_prev, new_terms = parameters.unpack()
			self._handle_search(new_terms, invocation)
		elif method_name == 'GetResultMetas':
			results = parameters.unpack()[0]
			self._handle_get_metas(results, invocation)
		elif method_name == 'ActivateResult':
			identifier, terms, timestamp = parameters.unpack()
			invocation.return_value(None)
			def _activate():
				self._activate_result(identifier, terms, timestamp)
				return GLib.SOURCE_REMOVE
			GLib.idle_add(_activate)
		elif method_name == 'LaunchSearch':
			terms, timestamp = parameters.unpack()
			invocation.return_value(None)
			def _launch():
				self._launch_search(terms, timestamp)
				return GLib.SOURCE_REMOVE
			GLib.idle_add(_launch)
		else:
			invocation.return_error_literal(
				Gio.dbus_error_quark(),
				Gio.DBusError.UNKNOWN_METHOD,
				f'Unknown method: {method_name}'
			)

	def _handle_search(self, terms: list[str], invocation):
		query = ' '.join(terms).strip()
		if not query:
			invocation.return_value(GLib.Variant('(as)', ([],)))
			return

		# First entry is always the search action
		search_id = f'search:{query}'
		with self._lock:
			self._results_cache[search_id] = {
				'id': search_id,
				'name': f'Cerca "{query}" su Monophony',
				'description': 'Visualizza i risultati della ricerca in Monophony',
				'type': 'search',
				'query': query,
				'icon': 'io.gitlab.zehkira.Monophony'
			}

		if self._app and hasattr(self._app, 'hold'):
			self._app.hold()

		def _worker():
			try:
				suggestions_data = yt.get_search_suggestions(query)
				items = suggestions_data.get('items', [])

				# Prioritize songs over playlists/albums
				songs = [item for item in items if item.get('type') == 'song']
				others = [item for item in items if item.get('type') in ('playlist', 'album')]

				# Priority: songs first, then playlists/albums
				ordered = songs + others
				# Limit to maximum 4 suggestions in total
				selected = ordered[:4]

				result_ids = [search_id]
				with self._lock:
					for s in selected:
						item_obj = s.get('item')
						item_type = s.get('type')
						title = s.get('title', '')
						subtitle = s.get('subtitle', '')

						if item_type == 'song' and item_obj and getattr(item_obj, 'yt_id', None):
							res_id = f'song:{item_obj.yt_id}'
							result_ids.append(res_id)
							desc = f'{subtitle} • Brano' if subtitle else 'Brano'
							self._results_cache[res_id] = {
								'id': res_id,
								'name': title,
								'description': desc,
								'type': 'song',
								'item': item_obj,
								'icon': 'audio-x-generic-symbolic'
							}
						elif item_type in ('playlist', 'album') and item_obj and getattr(item_obj, 'yt_id', None):
							res_id = f'{item_type}:{item_obj.yt_id}'
							result_ids.append(res_id)
							type_label = 'Playlist' if item_type == 'playlist' else 'Album'
							desc = f'{subtitle} • {type_label}' if subtitle else type_label
							self._results_cache[res_id] = {
								'id': res_id,
								'name': title,
								'description': desc,
								'type': item_type,
								'item': item_obj,
								'icon': 'media-optical-symbolic'
							}

				def _reply():
					invocation.return_value(GLib.Variant('(as)', (result_ids,)))
					return GLib.SOURCE_REMOVE
				GLib.idle_add(_reply)
			except Exception as e:
				logboth.error(__name__, f'Failed to fetch search suggestions for GNOME Shell: {e}')
				def _fail_reply():
					invocation.return_value(GLib.Variant('(as)', ([search_id],)))
					return GLib.SOURCE_REMOVE
				GLib.idle_add(_fail_reply)
			finally:
				if self._app and hasattr(self._app, 'release'):
					def _release():
						self._app.release()
						return GLib.SOURCE_REMOVE
					GLib.idle_add(_release)

		threading.Thread(target=_worker, daemon=True).start()

	def _handle_get_metas(self, results: list[str], invocation):
		metas = []
		with self._lock:
			for res_id in results:
				cached = self._results_cache.get(res_id)
				if not cached:
					if res_id.startswith('search:'):
						q = res_id[len('search:'):]
						cached = {
							'id': res_id,
							'name': f'Cerca "{q}" su Monophony',
							'description': 'Visualizza i risultati della ricerca in Monophony',
							'icon': 'io.gitlab.zehkira.Monophony'
						}
					else:
						continue

				icon_name = cached.get('icon', 'io.gitlab.zehkira.Monophony')
				icon = Gio.ThemedIcon.new(icon_name)
				meta = {
					'id': GLib.Variant('s', cached['id']),
					'name': GLib.Variant('s', cached['name']),
					'description': GLib.Variant('s', cached.get('description', '')),
					'gicon': GLib.Variant('s', icon_name),
					'icon': icon.serialize()
				}
				metas.append(meta)

		invocation.return_value(GLib.Variant('(aa{sv})', (metas,)))

	def _launch_monophony(self, args: list[str]):
		cmd = shutil.which('monophony') or '/app/bin/monophony'
		logboth.info(__name__, f'Launching Monophony with {args} via "{cmd}"')
		try:
			subprocess.Popen([cmd, *args])
		except Exception as e:
			logboth.error(__name__, f'Failed to launch Monophony: {e}')

	def _activate_result(self, identifier: str, terms: list[str], _timestamp: int = 0):
		logboth.info(__name__, f'Activating search result: {identifier}')

		# If running with an attached application window (e.g. tests)
		if self._app and getattr(self._app, '_window', None):
			win = self._app._window
			with self._lock:
				cached = self._results_cache.get(identifier)

			if identifier.startswith('search:'):
				query = identifier[len('search:'):] or ' '.join(terms)
				win._on_search(query)
			elif identifier.startswith('song:'):
				song = cached.get('item') if cached else None
				if not song:
					yt_id = identifier[len('song:'):]
					name = cached.get('name', 'Song') if cached else 'Song'
					song = Song(title=name, yt_id=yt_id)
				win._on_play(song, Group(songs=[song]))
			elif identifier.startswith(('playlist:', 'album:')):
				group = cached.get('item') if cached else None
				if not group:
					_kind, yt_id = identifier.split(':', 1)
					name = cached.get('name', 'Playlist') if cached else 'Playlist'
					group = Group(title=name, yt_id=yt_id)
				win._on_play(None, group)
			else:
				query = ' '.join(terms)
				win._on_search(query)
			return

		# Standalone headless search provider daemon:
		with self._lock:
			cached = self._results_cache.get(identifier, {})

		if identifier.startswith('search:'):
			query = identifier[len('search:'):] or ' '.join(terms)
			self._launch_monophony(['--search', query])
		elif identifier.startswith('song:'):
			song_id = identifier[len('song:'):]
			cmd_args = ['--play-song', song_id]
			if cached.get('name'):
				cmd_args.extend(['--title', cached['name']])
			item = cached.get('item')
			if item and getattr(item, 'author', None) and getattr(item.author, 'name', None):
				cmd_args.extend(['--artist', item.author.name])
			elif cached.get('description'):
				desc = cached['description'].split(' • ')[0]
				if desc and desc != 'Brano':
					cmd_args.extend(['--artist', desc])
			self._launch_monophony(cmd_args)
		elif identifier.startswith(('playlist:', 'album:')):
			group_id = identifier.split(':', 1)[1]
			cmd_args = ['--play-group', group_id]
			if cached.get('name'):
				cmd_args.extend(['--title', cached['name']])
			self._launch_monophony(cmd_args)
		else:
			query = ' '.join(terms)
			self._launch_monophony(['--search', query])

	def _launch_search(self, terms: list[str], timestamp: int = 0):
		query = ' '.join(terms).strip()
		logboth.info(__name__, f'Launching search from GNOME Shell: {query}')
		self._activate_result(f'search:{query}', terms, timestamp)


class SearchProviderService:
	'''Owns the D-Bus bus name and registers the SearchProvider object.'''

	def __init__(self):
		self._provider = SearchProvider()
		self._owner_id = None

	def start(self):
		'''Acquire the D-Bus name and register the search provider.'''
		self._owner_id = Gio.bus_own_name(
			Gio.BusType.SESSION,
			BUS_NAME,
			Gio.BusNameOwnerFlags.NONE,
			self._on_bus_acquired,
			self._on_name_acquired,
			self._on_name_lost
		)

	def stop(self):
		'''Release the D-Bus name and unregister.'''
		if self._owner_id:
			Gio.bus_unown_name(self._owner_id)
			self._owner_id = None
		self._provider.unregister()

	def _on_bus_acquired(self, connection, _name):
		self._provider.register(connection)

	def _on_name_acquired(self, _connection, name):
		logboth.info(__name__, f'Acquired D-Bus bus name "{name}"')

	def _on_name_lost(self, _connection, name):
		logboth.warning(__name__, f'Lost or could not acquire D-Bus bus name "{name}"')
