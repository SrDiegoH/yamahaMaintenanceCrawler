from log.log_manager import log_info
import cache.file_cache as file_cache
import cache.redis_cache as redis_cache

def _clear_cache(id):
    redis_cache.clear_cache(id)
    file_cache.clear_cache(id)

def _delete_cache():
    redis_cache.delete_cache()
    file_cache.delete_cache()

def _read_cache(id):
    try:
        return redis_cache.read_cache(id)
    except Exception as ex:
        log_info(f'Redis cache error: {ex}')
        return file_cache.read_cache(id)

def _upsert_cache(id, data):
    redis_cache.insert_cache_data(id, data)
    file_cache.insert_cache_data(id, data)

def get_data_from_cache(id, can_use_cache):
    if not can_use_cache:
        return None

    cached_data = _read_cache(id)
    if not cached_data:
        return None

    log_info(f'Data from Cache: {cached_data}')

    return cached_data

def preprocess_cache(id, should_delete_all_cache, should_clear_cached_data, should_use_cache):
    if should_delete_all_cache:
        _delete_cache()
    elif should_clear_cached_data:
        _clear_cache(id)

    can_use_cache = should_use_cache and not (should_delete_all_cache or should_clear_cached_data)

    return can_use_cache

def upsert_cache_data(id, data):
    _upsert_cache(id, data)