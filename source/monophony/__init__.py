'''This package contains everything used by the app executable.'''

import os
import pathlib
import tempfile

import logboth


__version__ = '4.4.11'
'''App version, same as in metainfo.'''

ID = 'io.gitlab.zehkira.Monophony'
'''Full ID per Freedesktop standards.'''

NAME = 'monophony'
'''Use for app executable, directories and so on.'''

DISPLAY_NAME = 'Monophony'
'''For window titles and such - do not use in logic.'''

GRESOURCES_PATH = '/io/gitlab/zehkira/Monophony'
'''For loading bundled GResources.'''

MIN_WIDTH = 360
'''Minimum window width, same as in metainfo.'''

wanted_levels_names = os.getenv(
	'MONOPHONY_LOG_LEVELS', 'Info,Warning,Error,Success'
).split(',')
levels = [level for level in logboth.config.levels if level.name in wanted_levels_names]
logboth.config.levels = levels
logboth.config.directory = pathlib.Path(
	os.getenv('XDG_RUNTIME_DIR', '') or tempfile.gettempdir()
) / pathlib.Path(NAME)
logboth.config.file = 'log.txt'
logboth.basic_info()


def get_user_config_dir() -> str:
	'''Get permanent user config directory.

	Always uses ~/.config/monophony on the real host filesystem,
	bypassing sandboxed Flatpak .var redirects.
	'''
	xdg = os.getenv('XDG_CONFIG_HOME', '')
	if xdg and '/.var/app/' not in xdg:
		config_dir = os.path.join(xdg, NAME)
	else:

		home = os.path.expanduser('~')
		config_dir = os.path.join(home, '.config', NAME)

		# Auto-migrate files from sandboxed .var dir if present
		var_dir = os.path.join(home, '.var', 'app', ID, 'config', NAME)
		if os.path.exists(var_dir):
			os.makedirs(config_dir, exist_ok=True)
			with contextlib.suppress(Exception):
				import shutil
				for fname in os.listdir(var_dir):
					src = os.path.join(var_dir, fname)
					dst = os.path.join(config_dir, fname)
					if os.path.isfile(src) and not os.path.exists(dst):
						shutil.copy2(src, dst)

	os.makedirs(config_dir, exist_ok=True)
	return config_dir




