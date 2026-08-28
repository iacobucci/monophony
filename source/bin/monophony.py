#!/usr/bin/env python3
# ruff: noqa: E402 - Allow gi.require_versions()

'''App executable.'''

import gettext
import os
import platform
import sys
import threading
import traceback

import gi


gi.require_versions({
	'Adw': '1', 'Gdk': '4.0', 'Gst': '1.0', 'GstAudio': '1.0', 'Gtk': '4.0'
})

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from monophony import NAME, __version__
from monophony.app import Application


import logboth
from gi.repository import Gio, GLib


sys.excepthook = lambda exception, value, trace: logboth.error(
	__name__,
	'Unhandled exception',
	''.join(traceback.format_exception(exception, value, trace))
)
threading.excepthook = lambda args: logboth.error(
	f'{__name__} (thread "{args.thread.name}")',
	'Unhandled exception in thread',
	''.join(
		traceback.format_exception(args.exc_type, args.exc_value, args.exc_traceback)
	)
)

os_release = {}
try:
	os_release = platform.freedesktop_os_release()
except OSError:
	logboth.warning(__name__, 'Could not read OS release file')

os_info_string = ''
for key in ('PRETTY_NAME', 'NAME', 'ID', 'ID_LIKE', 'VERSION', 'VERSION_ID'):
	if value := os_release.get(key):
		os_info_string += f'{key}: {value}\n'

container = os.getenv('container', 'unknown') # noqa: SIM112 - Container is lowercase
if container != 'flatpak':
	logboth.warning(
		__name__,
		f'App was installed from unofficial source. Container type: {container}'
	)
elif 'LD_PRELOAD' in os.environ:
	# Older versions of Flatpak inherit environment variables from the system.
	# LD_PRELOAD is used for loading extra libraries, which won't work from inside
	# the Flatpak sandbox and will cause errors. gtk3-nocsd is a real life example
	# of this
	try:
		os.environ.pop('LD_PRELOAD')
	except KeyError:
		logboth.error(__name__, 'Failed to unset LD_PRELOAD')
	else:
		logboth.warning(__name__, 'Unset LD_PRELOAD to prevent issues')

logboth.info(
	__name__,
	f'{NAME} {__version__} on {platform.platform(aliased=True)}',
	os_info_string.strip('\n')
)

logboth.info(__name__, 'Loading GResources...')
resources_file = 'resources.gresource'
for path in os.getenv('XDG_DATA_DIRS', '/usr/share/').split(':'):
	data_path = f'{path}{NAME}' if path.endswith('/') else f'{path}/{NAME}'
	logboth.info(__name__, f'Trying to load GResources from "{data_path}"...')
	try:
		resource = Gio.Resource.load(data_path + '/' + resources_file)
	except GLib.GError:
		continue

	Gio.resources_register(resource)
	logboth.info(__name__, f'Loaded GResources from "{data_path}/{resources_file}"')
	break
else:
	logboth.error(__name__, 'Failed to load GResources: not found')
	sys.exit(1)

logboth.info(__name__, 'Installing translation...')
for path in os.getenv('XDG_DATA_DIRS', '/usr/share/').split(':'):
	locale_path = f'{path}locale' if path.endswith('/') else f'{path}/locale'
	logboth.info(__name__, f'Trying to install translation from "{locale_path}"...')
	if 'share' in path and os.path.isdir(locale_path):
		gettext.translation(NAME, locale_path, fallback=True).install()
		logboth.info(
			__name__, f'Installed translation from "{locale_path}/{NAME}/"'
		)
		break
else:
	logboth.error(__name__, 'Failed to install translation: not found')
	sys.exit(1)

Application().run()
logboth.info(__name__, 'Exited')
