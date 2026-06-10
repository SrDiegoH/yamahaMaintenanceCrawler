import ast
from datetime import datetime, timedelta
import os

from log.log_manager import log_info, log_debug

_CACHE_EXPIRY = timedelta(days=1)

_DATE_FORMAT = '%d-%m-%Y %H:%M:%S'

_SEPARATOR = '#@#'

_FILE = '/tmp/cache.txt'

def _cache_exists():
    if os.path.exists(_FILE):
        return True

    log_info('No cache file found')
    return False

def insert_cache_data(id, data):
    clear_cache(id)

    with open(_FILE, 'a') as cache_file:
        new_line = f'{id}{_SEPARATOR}{datetime.now().strftime(_DATE_FORMAT)}{_SEPARATOR}{data}\n'
        cache_file.write(new_line)

def clear_cache(id):
    if not _cache_exists():
        return

    log_debug('Cleaning cache')

    with open(_FILE, 'r') as cache_file:
        lines = cache_file.readlines()

    with open(_FILE, 'w') as cache_file:
        cache_file.writelines(line for line in lines if not line.startswith(id))

    log_info(f'Cache cleaning completed for "{id}"')

def read_cache(id):
    if not _cache_exists():
        return None

    log_debug('Reading cache')

    clear_cache_control = False

    with open(_FILE, 'r') as cache_file:
        for line in cache_file:
            if not line.startswith(id):
                continue

            _, cached_date_as_text, data = line.strip().split(_SEPARATOR)
            cached_date = datetime.strptime(cached_date_as_text, _DATE_FORMAT)

            if datetime.now() - cached_date <= _CACHE_EXPIRY:
                log_debug(f'Cache hit for "{id}" (Date: {cached_date_as_text})')
                return ast.literal_eval(data)

            log_debug(f'Cache expired for "{id}" (Date: {cached_date_as_text})')
            clear_cache_control = True
            break

    if clear_cache_control:
        clear_cache(id)

    log_info(f'No cache entry found for "{id}"')
    return None

def delete_cache():
    if not _cache_exists():
        return

    log_debug('Deleting cache')

    os.remove(_FILE)

    log_info('Cache deletion completed')