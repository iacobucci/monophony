#!/usr/bin/env python3

'''GNOME Shell Search Provider daemon for Monophony.'''

import os
import signal
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gi.repository import GLib
import logboth
from monophony.search_provider import SearchProviderService


def main():
	loop = GLib.MainLoop()

	def _sig_handler(_sig, _frame):
		loop.quit()

	signal.signal(signal.SIGINT, _sig_handler)
	signal.signal(signal.SIGTERM, _sig_handler)

	service = SearchProviderService()
	service.start()
	logboth.info(__name__, 'Monophony search provider daemon started')
	try:
		loop.run()
	finally:
		service.stop()
	logboth.info(__name__, 'Monophony search provider daemon exited')


if __name__ == '__main__':
	main()
