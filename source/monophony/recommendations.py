import json
import os

from monophony import NAME
from monophony.data import Artist, Group, Song

import logboth


def _get_directory() -> str:
	return os.getenv(
		'XDG_CONFIG_HOME', os.path.expanduser('~/.config')
	) + '/' + NAME


def _get_file_path() -> str:
	return _get_directory() + '/recommendations.json'


def write(recommendations: list[Group]):
	logboth.info(__name__, f'Writing {len(recommendations)} recommendations...')
	recommendations_path = _get_file_path()
	os.makedirs(_get_directory(), exist_ok=True)

	serialized_recommendations = {}
	for group in recommendations:
		serialized_recommendations[group.title] = group.serialize()['contents']
	with open(recommendations_path, 'w') as recommendations_file:
		json.dump(serialized_recommendations, recommendations_file, indent='\t')

	logboth.info(__name__, 'Done writing recommendations')


def read() -> list[Group]:
	try:
		with open(_get_file_path()) as recommendations_file:
			return [
				Group(
					title=name,
					songs=[
						Song(
							title=song.get('title', ''),
							author=Artist(
								name=song.get('author', ''),
								yt_id=song.get('author_id', '')
							),
							length=song.get('length', ''),
							thumbnail=song.get('thumbnail', ''),
							yt_id=song.get('id', '')
						) for song in songs
					]
				) for name, songs in json.load(recommendations_file).items()
			]
	except (OSError, json.decoder.JSONDecodeError):
		return []
