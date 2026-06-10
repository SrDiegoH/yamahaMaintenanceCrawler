import ast

from upstash_redis import Redis

from log.log_manager import log_info, log_debug

redis = Redis.from_env()

_ONE_MINUTE = 60
_ONE_HOUR   = 60 * _ONE_MINUTE
_ONE_DAY    = 24 * _ONE_HOUR
_ONE_WEEK   = 7  * _ONE_DAY

_build_key = lambda id: f'YAMAHAMAINTENANCECRAWLER:{id}'

def insert_cache_data(id, data):
    key = _build_key(id)

    log_info(f'New cache entry created for "{id}"') if not redis.set(key, f'{data}', ex=_ONE_WEEK, get=True) else log_info(f'Cache upserted for "{id}"')

def clear_cache(id):
    key = _build_key(id)

    if redis.delete(key) > 0:
        log_info(f'Cache cleaning completed for "{id}"')

def read_cache(id):
    log_debug('Reading cache')

    key = _build_key(id)

    data = redis.get(key)

    if data:
        return ast.literal_eval(data)

    log_info(f'No cache entry found for "{id}"')

def delete_cache():
    log_debug('Deleting cache')

    key_pattern = _build_key('*')

    keys = redis.keys(key_pattern)
    if not keys:
        return 0

    if redis.delete(*keys):
        log_info('Cache deletion completed')