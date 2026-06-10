from fastapi import FastAPI, HTTPException

from cache.cache_manager import preprocess_cache, upsert_cache_data
from common.util import get_cache_parameter
from service.service import get_yamaha_revision_table
from log.log_manager import log_info

app = FastAPI()

@app.get('/')
async def index(name, should_delete_all_cache, should_clear_cached_data, should_use_cache):
    should_delete_all_cache  = get_cache_parameter(should_delete_all_cache)
    should_clear_cached_data = get_cache_parameter(should_clear_cached_data)
    should_use_cache         = get_cache_parameter(should_use_cache, 'true')

    log_info(f'Name: {name} - Should delete all cache? {should_delete_all_cache} - Should clear cached data? {should_clear_cached_data} - Should use cache? {should_use_cache}')

    if not name:
        raise HTTPException(status_code=400, detail='O parâmetro "name" é obrigatório')

    can_use_cache = preprocess_cache(name, should_delete_all_cache, should_clear_cached_data, should_use_cache)

    should_update_cache, data = await get_yamaha_revision_table(name, can_use_cache)

    log_info(f'Final Data: {data}')

    if not data:
        raise HTTPException(status_code=404, detail='Não foram encontrados dados de revisão encontrado para o veiculo {name}')

    if can_use_cache and should_update_cache:
        upsert_cache_data(name, data)

    return data