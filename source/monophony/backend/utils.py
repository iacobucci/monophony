import contextlib, datetime


def time_str_to_sec(string: str) -> int:
	if not string:
		return 0

	seconds = 0
	parts = string.split(':')
	if len(parts) > 0:
		with contextlib.suppress(ValueError):
			seconds += int(parts[-1])
	if len(parts) > 1:
		with contextlib.suppress(ValueError):
			seconds += int(parts[-2]) * 60
	if len(parts) > 2:
		with contextlib.suppress(ValueError):
			seconds += int(parts[-3]) * 60 * 60

	return seconds


def sec_to_time_str(seconds: int) -> str:
	return str(datetime.timedelta(seconds=seconds))


def sanitize_str(string: str) -> str:
	bad_unicode = ['\u3011']
	for symbol in bad_unicode:
		string = string.replace(symbol, '')

	return string
