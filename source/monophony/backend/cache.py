import contextlib, glob, json, os, subprocess


### --- CACHE FUNCTIONS --- ###


def is_song_being_cached(video_id: str) -> bool:
	has_temp = False
	has_result = False
	for file in os.listdir(get_cache_directory()):
		parts = file.split('.')
		if parts[0] == video_id:
			if parts[-1] == 'monophony':
				has_temp = True
			elif parts[-1] == video_id:
				has_result = True

	if not has_result:
		return has_temp

	return False


def is_song_cached(video_id: str) -> bool:
	if video_id is None:
		return False

	return os.path.exists(get_cache_directory() + video_id)


def get_song_uri(video_id: str) -> str:
	if video_id is None:
		return ''

	local_path = get_cache_directory() + video_id
	if os.path.exists(local_path):
		return 'file://' + local_path

	return ''


def cache_songs(songs: list):
	path = get_cache_directory()
	needed_ids = []
	for song in songs:
		if not is_song_cached(song['id']):
			needed_ids.append(song['id'])
			open(f'{path}{song["id"]}.monophony', 'w').close()
			new_songs = read_songs()
			new_songs.append(song)
			write_songs(new_songs)


	subprocess.Popen(
		'yt-dlp -x '
		'--no-cache-dir --audio-quality 0 --add-metadata '
		f'-o "{path}%(id)s.%(ext)s" https://music.youtube.com/watch?v=' +
		(' https://music.youtube.com/watch?v='.join(needed_ids)),
		shell = True,
		stdout = subprocess.PIPE
	).communicate()

	for video_id in needed_ids:
		with contextlib.suppress(OSError, FileNotFoundError):
			os.remove(f'{path}{video_id}.monophony')

	# rename id.* files to id
	for file in glob.glob(path + '*.*'):
		os.rename(file, '.'.join(file.split('.')[:-1]))


def uncache_song(song: dict):
	write_songs([s for s in read_songs() if s['id'] != song['id']])

	with contextlib.suppress(OSError, FileNotFoundError):
		os.remove(get_cache_directory() + song['id'])


def clean_up():
	path = get_cache_directory()
	for file in os.listdir(path):
		if file.endswith(('.part', '.monophony')):
			os.remove(path + file)

	write_songs([s for s in read_songs() if is_song_cached(s['id'])])


### --- UTILITY FUNCTIONS --- ###


def get_cache_directory() -> str:
	path = os.getenv(
		'XDG_DATA_HOME', os.path.expanduser('~/.local/share')
	) + '/monophony/'
	os.makedirs(path, exist_ok=True)
	return path


def write_songs(songs: list):
	dir_path = os.getenv(
		'XDG_CONFIG_HOME', os.path.expanduser('~/.config')
	) + '/monophony'
	downloads_path = dir_path + '/downloads.json'

	try:
		with open(str(downloads_path), 'w') as downloads_file:
			json.dump(songs, downloads_file, indent='\t')
	except FileNotFoundError:
		os.makedirs(str(dir_path))
		write_songs(songs)


def read_songs() -> list:
	songs_path = os.getenv(
		'XDG_CONFIG_HOME', os.path.expanduser('~/.config')
	) + '/monophony/downloads.json'

	try:
		with open(songs_path) as songs_file:
			return json.load(songs_file)
	except (OSError, json.decoder.JSONDecodeError):
		return []
