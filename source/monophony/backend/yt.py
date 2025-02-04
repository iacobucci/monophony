import traceback, random, subprocess

import ytmusicapi


class YT:
	def __init__(self):
		self.yt = None
		self._connect()

	def _connect(self) -> bool:
		if self.yt:
			return True

		try:
			self.yt = ytmusicapi.YTMusic()
		except:
			print('Failed to connect to YTM:\033[0;33m')
			traceback.print_exc()
			print('\033[0m')
			return False

		return True

	def _get_artist_names(self, artists: list) -> list:
		return [artist['name'] for artist in artists if artist['id']]

	def _get_artist_id(self, artists: list) -> str:
		a_id = ''
		for i in range(len(artists)):
			a_id = artists[i]['id']
			if a_id:
				break

		return a_id

	def _parse_results(self, data: list) -> list:
		if not self._connect():
			return []

		results = []
		exp_types = {'album', 'song', 'video', 'playlist', 'artist', 'single'}
		for result in data:
			if 'resultType' not in result or result['resultType'] not in exp_types:
				continue

			if result['resultType'] == 'single':
				result['resultType'] = 'album'

			item = {'type': result['resultType'], 'top': False}
			if 'category' in result:
				item['top'] = (result['category'] == 'Top result')
				if result['category'] in ['Profiles', 'Episodes']:
					continue

			if result['resultType'] == 'artist':
				try:
					if result['category'] == 'Top result':
						item['author'] = ', '.join(
							self._get_artist_names(result['artists'])
						)
						item['id'] = self._get_artist_id(result['artists'])
					else:
						item['author'] = result['artist']
						item['id'] = result['browseId']
				except:
					print('Failed to parse artist result:\033[0;33m')
					traceback.print_exc()
					print('\033[0m')
					continue
			elif result['resultType'] == 'album':
				try:
					item['author'] = result['artists'][0]['name']
					item['id'] = result['browseId']
					item['title'] = result['title']

					album = (
						self.yt.get_playlist(result['playlistId']) if
						result['playlistId'] else
						self.yt.get_album(result['browseId'])
					)
					item['contents'] = [
						{
							'id': str(s['videoId']),
							'title': s['title'],
							'type': 'song',
							'author': ', '.join(self._get_artist_names(s['artists'])),
							'author_id': self._get_artist_id(s['artists']),
							'length': s['duration'],
							'thumbnail': result['thumbnails'][0]['url']
						} for s in album['tracks'] if s['videoId']
					]
				except:
					print('Failed to parse album result:\033[0;33m')
					traceback.print_exc()
					print('\033[0m')
					continue
			elif result['resultType'] == 'playlist':
				try:
					album = self.yt.get_playlist(result['browseId'], limit=None)
					if 'author' in result:
						item['author'] = result['author']
					else:
						item['author'] = ', '.join(
							self._get_artist_names(result['artists'])
						)
					item['id'] = result['browseId']
					item['title'] = result['title']
					item['contents'] = [
						{
							'id': str(s['videoId']),
							'title': s['title'],
							'type': 'song',
							'author': ', '.join(self._get_artist_names(s['artists'])),
							'author_id': self._get_artist_id(s['artists']),
							'length': s['duration'],
							'thumbnail': s['thumbnails'][0]['url']
						} for s in album['tracks'] if s['videoId']
					]
				except:
					print('Failed to parse playlist result:\033[0;33m')
					traceback.print_exc()
					print('\033[0m')
					continue
			elif result['resultType'] in {'song', 'video'}:
				try:
					if not result['videoId']:
						continue
					item['id'] = str(result['videoId'])
					item['title'] = result['title']
					item['author'] = ', '.join(
						self._get_artist_names(result['artists'])
					)
					item['author_id'] = self._get_artist_id(result['artists'])
					if 'duration' in result:
						item['length'] = result['duration']
					item['thumbnail'] = result['thumbnails'][0]['url']

					# ytm sometimes returns videos as song results when filtered
					if 'category' in result and result['category'] == 'Songs':
						item['type'] = 'song'
				except:
					print('Failed to parse song/video result:\033[0;33m')
					traceback.print_exc()
					print('\033[0m')
					continue

			results.append(item)

		return results

	def get_song_uri(self, video_id: str) -> str | None:
		out, err = subprocess.Popen(
			f'yt-dlp -g -x --no-warnings https://music.youtube.com/watch?v={video_id}',
			shell=True,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
		).communicate()
		if err:
			print(err.decode())
			return None

		return out.decode().split('\n')[0]

	def get_similar_song(self, video_id: str, ignore: list | None = None) -> dict:
		if not self._connect():
			return {}

		ignore = ignore if ignore else []
		try:
			data = self.yt.get_watch_playlist(video_id, radio=True)['tracks']
		except:
			return {}

		acceptable_tracks = []
		for item in data:
			track = {
				'title': item['title'],
				'author': ', '.join(self._get_artist_names(item['artists'])),
				'author_id': self._get_artist_id(item['artists']),
				'length': item['length'],
				'id': item['videoId'],
				'thumbnail': item['thumbnail'][0]['url']
			}
			if not track['id']:
				continue

			for id_ in ignore:
				if id_ == track['id']:
					break
			else: # nobreak
				acceptable_tracks.append(track)

		if acceptable_tracks:
			return random.choice(acceptable_tracks)
		return {}

	def get_recommendations(self) -> dict:
		if not self._connect():
			return {}

		try:
			data = self.yt.get_home()
		except:
			return {}

		categories = {}
		for group in data:
			songs = [
				{
					'title': item['title'],
					'author': ', '.join(self._get_artist_names(item['artists'])),
					'author_id': self._get_artist_id(item['artists']),
					'id': item['videoId'],
				} for item in group['contents'] if 'videoId' in item
			]

			if songs:
				categories[group['title']] = songs

		return categories

	def get_song(self, id_: str) -> dict | None:
		if not self._connect():
			return None

		try:
			result = self.yt.get_song(id_)['videoDetails']
		except:
			return None

		seconds = int(result['lengthSeconds'])
		minutes = seconds // 60
		seconds %= 60
		return {
			'top': True,
			'type': 'video',
			'id': result['videoId'],
			'title': result['title'],
			'author': result['author'],
			'author_id': result['channelId'],
			'length': f'{minutes}:{seconds:02}',
			'thumbnail': result['thumbnail']['thumbnails'][0]
		}


	def get_artist(self, browse_id: str) -> list:
		if not self._connect():
			return []

		try:
			metadata = self.yt.get_artist(browse_id)
			artist = {'name': metadata['name']}
			for group in ['albums', 'singles']:
				artist[group] = {}
				artist[group]['results'] = []
				if group not in metadata:
					continue

				if 'params' in metadata[group]:
					artist[group]['results'] = self.yt.get_artist_albums(
						metadata[group]['browseId'], metadata[group]['params']
					)
				else:
					artist[group]['results'] = metadata[group]['results']

			for group in ['songs', 'videos', 'playlists']:
				if group in metadata:
					artist[group] = metadata[group]
				else:
					print('Artist has no', group)
		except:
			try:
				artist = self.yt.get_user(browse_id)
			except:
				print('Could not get artist:\033[0;31m')
				traceback.print_exc()
				print('\033[0m')
				return []

		data = []
		for group in ['songs', 'albums', 'singles', 'videos', 'playlists']:
			content = []
			if group in artist:
				if group in {'songs', 'videos'}:
					try:
						content = self.yt.get_playlist(
							artist[group]['browseId'], limit=None
						)['tracks']
					except:
						content = artist[group]['results']
				else:
					content = []
					for alb in artist[group]['results']:
						if not ('browseId' in alb or 'playlistId' in alb):
							print(f'Failed to get artist {group}:\033[0;33m')
							print('browseId/playlistId missing')
							print('\033[0m')
							continue

						content.append({
							'title': alb['title'],
							'browseId': (
								alb['browseId' if 'browseId' in alb else 'playlistId']
							),
							'playlistId': alb.get(
								'audioPlaylistId', alb.get('playlistId', None)
							),
							'artists': [{'name': artist['name'], 'id': browse_id}],
							'thumbnails': alb['thumbnails']
						})

				for item in content:
					item['resultType'] = group[:-1]

				data.extend(content)

		return self._parse_results(data)

	def search(self, query: str, filter_: str='') -> list:
		if not self._connect():
			return []

		try:
			if '?v=' in query and '/' in query:
				song = self.get_song(query.split('?v=')[-1].split('&')[0])
				return [song] if song else []
			if 'youtu.be/' in query:
				song = self.get_song(query.split('youtu.be/')[-1].split('?')[0])
				return [song] if song else []

			data = (
				self.yt.search(query, filter=filter_, limit=100) if filter_
				else self.yt.search(query)
			)
		except:
			return []

		return self._parse_results(data)
