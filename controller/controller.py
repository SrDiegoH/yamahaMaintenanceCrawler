from fastapi import FastAPI, HTTPException

from cache.cache_manager import preprocess_cache, upsert_cache_data
from service.service import get_yamaha_revision_table
from log.log_manager import log_debug

app = FastAPI()

@app.get('/')
async def index(name, should_delete_all_cache=0, should_clear_cached_data=0, should_use_cache=1):
    log_debug('Name: ', name, 'Should delete all cache?', should_delete_all_cache, 'Should clear cached data?', should_clear_cached_data, 'Should use cache?', should_use_cache)

    if not name:
        raise HTTPException(status_code=400, detail='O parâmetro "name" é obrigatório')

    can_use_cache = preprocess_cache(name, should_delete_all_cache, should_clear_cached_data, should_use_cache)

    should_update_cache, data = await get_yamaha_revision_table(name, can_use_cache)

    log_debug(f'Final Data: {data}')

    if not data:
        raise HTTPException(status_code=404, detail='Não encontrado')

    if can_use_cache and should_update_cache:
        upsert_cache_data(name, data)

    return data