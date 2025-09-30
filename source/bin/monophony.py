#!/usr/bin/env python3
# ruff: noqa: E402 - Allow gi.require_versions()

import gettext
import os
import sys
import threading
import traceback

import gi


gi.require_versions({
	'Adw': '1', 'Gdk': '4.0', 'Gst': '1.0', 'GstAudio': '1.0', 'Gtk': '4.0'
})


from monophony import NAME, logging
from monophony.app import Application

from gi.repository import Gio, GLib


sys.excepthook = lambda exception, value, trace: logging.error(
	__name__,
	'Unhandled exception',
	''.join(traceback.format_exception(exception, value, trace))
)
threading.excepthook = lambda args: logging.error(
	f'{__name__} (thread "{args.thread.name}")',
	'Unhandled exception in thread',
	''.join(
		traceback.format_exception(args.exc_type, args.exc_value, args.exc_traceback)
	)
)

container = os.getenv('container', 'unknown') # noqa: SIM112 - Container is lowercase
if container != 'flatpak':
	logging.warning(
		__name__,
		f'App was installed from unofficial source. Container type: {container}'
	)

logging.info(__name__, 'Loading GResources...')
resources_file = 'resources.gresource'
for path in os.getenv('XDG_DATA_DIRS', '/usr/share/').split(':'):
	data_path = f'{path}{NAME}' if path.endswith('/') else f'{path}/{NAME}'
	logging.info(__name__, f'Trying to load GResources from "{data_path}"...')
	try:
		resource = Gio.Resource.load(data_path + '/' + resources_file)
	except GLib.GError:
		continue

	Gio.resources_register(resource)
	logging.info(__name__, f'Loaded GResources from "{data_path}/{resources_file}"')
	break
else:
	logging.error(__name__, 'Failed to load GResources: not found')
	sys.exit(1)

logging.info(__name__, 'Installing translation...')
for path in os.getenv('XDG_DATA_DIRS', '/usr/share/').split(':'):
	locale_path = f'{path}locale' if path.endswith('/') else f'{path}/locale'
	logging.info(__name__, f'Trying to install translation from "{locale_path}"...')
	if 'share' in path and os.path.isdir(locale_path):
		gettext.translation(NAME, locale_path, fallback=True).install()
		logging.info(
			__name__, f'Installed translation from "{locale_path}/{NAME}/"'
		)
		break
else:
	logging.error(__name__, 'Failed to install translation: not found')
	sys.exit(1)

Application().run()
logging.info(__name__, 'Exited')
