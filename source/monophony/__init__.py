import os
import pathlib

import logboth


__version__ = '4.3.0'
ID = 'io.gitlab.zehkira.Monophony' # Full ID per Freedesktop standards
NAME = 'monophony' # Use for app executable, directories and so on
DISPLAY_NAME = 'Monophony' # For window titles and such - do not use in logic
GRESOURCES_PATH = '/io/gitlab/zehkira/Monophony'
MIN_WIDTH = 360 # Same as in metainfo.xml

wanted_levels_names = os.getenv(
	'MONOPHONY_LOG_LEVELS', 'INFO,WARN,ERRO,SUCC'
).split(',')
levels = [level for level in logboth.config.levels if level.name in wanted_levels_names]
logboth.config.levels = levels
logboth.config.directory /= pathlib.Path(NAME)
logboth.config.file = 'log.txt'
logboth.basic_info()
