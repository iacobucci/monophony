import json
import os
from typing import Any

from monophony import NAME, logging


def save(values: dict):
	logging.info(__name__, f'Saving settings "{values}"...')

	settings = _read()
	for key, value in values.items():
		settings[key] = value

	_write(settings)
	logging.info(__name__, 'Saved settings')


def load(key: str, default: Any=None) -> Any:
	return _read().get(key, default)


def _write(settings: dict):
	logging.info(__name__, 'Writing settings...')
	directory = os.getenv(
		'XDG_CONFIG_HOME', os.path.expanduser('~/.config')
	) + '/' + NAME
	settings_path = directory + '/settings.json'

	os.makedirs(directory, exist_ok=True)
	with open(settings_path, 'w') as settings_file:
		json.dump(settings, settings_file, indent='\t')

	logging.info(__name__, 'Done writing settings')


def _read() -> dict:
	settings_path = os.getenv(
		'XDG_CONFIG_HOME', os.path.expanduser('~/.config')
	) + f'/{NAME}/settings.json'

	try:
		with open(settings_path) as settings_file:
			return json.load(settings_file)
	except (OSError, json.decoder.JSONDecodeError):
		return {}
