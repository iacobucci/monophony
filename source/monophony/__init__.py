'''This package contains everything used by the app executable.'''

import os
import pathlib
import tempfile

import logboth


__version__ = '4.4.7'
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
