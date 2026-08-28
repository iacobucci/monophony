'''Song prefetching management module.'''

from monophony import cache, downloads, settings
from monophony.asynchronous import Task
from monophony.data import Group, Song

import logboth


class PrefetchTask(Task):
	'''Task for prefetching upcoming queue/playlist songs in the background.'''

	def _function(self, songs_to_prefetch: list[Song]):
		logboth.info(__name__, f'Starting prefetching for {len(songs_to_prefetch)} upcoming songs...')
		for i, song in enumerate(songs_to_prefetch):
			if self.is_canceled():
				logboth.info(__name__, 'Prefetching canceled')
				return

			if cache.is_cached(song) or downloads.is_downloaded(song):
				logboth.info(__name__, f'Song "{song.yt_id}" already cached/downloaded')
				continue

			logboth.info(__name__, f'Prefetching upcoming song #{i + 1} "{song.yt_id}" ({song.title})...')
			cache.cache_song(song)
			self._update_progress((i + 1) / len(songs_to_prefetch))

		logboth.info(__name__, 'Prefetching completed')


class PrefetchManager:
	'''Manager for prefetching upcoming tracks in playlists/queue.'''

	def __init__(self):
		self._current_task = PrefetchTask()

	def prefetch_upcoming(self, queue: Group, current_index: int):
		'''Prefetch upcoming tracks from current queue/playlist.

		:param queue: Group representing current playback queue.
		:param current_index: Current song index in queue.
		'''
		if not settings.load('prefetch_enabled', True):
			return

		prefetch_count = int(settings.load('prefetch_count', 2))
		if prefetch_count <= 0 or not queue or not queue.songs:
			return

		start_i = current_index + 1
		end_i = min(start_i + prefetch_count, len(queue.songs))
		if start_i >= len(queue.songs):
			return

		upcoming_songs = queue.songs[start_i:end_i]
		songs_to_prefetch = [
			s for s in upcoming_songs
			if not cache.is_cached(s) and not downloads.is_downloaded(s)
		]

		if not songs_to_prefetch:
			return

		self._current_task.cancel()
		self._current_task = PrefetchTask(args=(songs_to_prefetch,))
		self._current_task.start()


# Singleton instance
prefetch_manager = PrefetchManager()
