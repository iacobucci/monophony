import os
import platform
import sys
import threading
import time
import traceback
from typing import Any

from monophony import NAME, __version__

from gi.repository import GLib


_LOG_LEVELS_VARIABLE = 'MONOPHONY_LOG_LEVELS'
_DEFAULT_LOG_LEVELS = 'INFO,WARN,ERRO'


class LogLevel:
	name = ''
	color = ''


class InfoLevel(LogLevel):
	name = 'INFO'
	color = '\033[0m'


class WarningLevel(LogLevel):
	name = 'WARN'
	color = '\033[1;33m'


class ErrorLevel(LogLevel):
	name = 'ERRO'
	color = '\033[1;31m'


def get_log() -> str:
	if threading.current_thread() is not threading.main_thread():
		warning(__name__, 'Reading log from non-main thread')

	try:
		with open(_get_directory() + '/log') as log_file:
			return log_file.read()
	except OSError:
		error(__name__, 'Failed to read log file', traceback.format_exc())

	return ''


# For status updates
def info(source: str, text: Any, details: Any=''):
	_log(InfoLevel, source, str(text), str(details))


# For unusual but possibly acceptable things
def warning(source: str, text: Any, details: Any=''):
	_log(WarningLevel, source, str(text), str(details))


# For failures of all sorts
def error(source: str, text: Any, details: Any=''):
	_log(ErrorLevel, source, str(text), str(details))


def _log(level: type, source: str, text: str, details: str):
	if threading.current_thread() is not threading.main_thread():
		GLib.idle_add(_log, level, source, text, details)
		return

	if level.name not in os.getenv(
		_LOG_LEVELS_VARIABLE, _DEFAULT_LOG_LEVELS
	).split(','):
		return

	text = text.strip()
	details = details.strip()
	line = f'{time.strftime("%H:%M")} [{level.name}] {source}: {text}'
	sys.stdout.write(f'{level.color}{line}\n')
	if details:
		sys.stdout.write(details + '\n')
	sys.stdout.write('\033[0m')

	log_directory = _get_directory()
	os.makedirs(log_directory, exist_ok=True)
	try:
		with open(f'{log_directory}/log', 'a+') as log:
			log.write(line + '\n')
			if details:
				log.write(details + '\n')
	except (OSError, ValueError):
		sys.stdout.write(
			f'{ErrorLevel.color}[{ErrorLevel.name}] {__name__}: '
			'Failed to write to log file\033[0m\n'
			f'{traceback.format_exc()}\n'
		)


def _get_directory() -> str:
	return os.getenv('XDG_RUNTIME_DIR', '/var/tmp') + '/' + NAME


log_directory = _get_directory()
os.makedirs(log_directory, exist_ok=True)
open(f'{log_directory}/log', 'a+').close()

max_log_lines = 1000
with open(f'{log_directory}/log', 'r+') as log_file:
	lines = log_file.readlines()
	if len(lines) > max_log_lines:
		lines = lines[-max_log_lines:]
	log_file.seek(0)
	log_file.truncate()
	log_file.writelines(lines)

info(__name__, f'Logging initiated. Logs will be written to {log_directory}/log')

os_release = {}
try:
	os_release = platform.freedesktop_os_release()
except OSError:
	warning(__name__, 'Could not read OS release file')

os_info_string = ''
for key in ('PRETTY_NAME', 'NAME', 'ID', 'ID_LIKE', 'VERSION', 'VERSION_ID'):
	if value := os_release.get(key):
		os_info_string += f'{key}: {value}\n'

info(
	__name__,
	f'{NAME} {__version__} on {platform.platform(aliased=True)}',
	os_info_string.strip('\n')
)
