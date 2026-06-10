import json

from fastapi import HTTPException

from cache.cache_manager import get_data_from_cache
from client.yamaha import request_yamaha_data
from log.log_manager import log_debug

_get_revision_data = lambda revision: {
    'revisionByKm': revision['revisionByKm'],
    'revisionByMonth': revision['revisionByMonth'],
    'revisionPriceInCash': revision['priceInCash']
}

def _refine_data(data):
    if '1:' not in data:
        raise HTTPException(status_code=500, detail=f'Erro ao consultar dados da Yamaha. Data: {data}')

    content = data.split('1:')[1].replace('1:', '')
    parsed_json = json.loads(content)
    items = parsed_json.get('result', {}).get('items', [])

    if not items:
        raise HTTPException(status_code=404, detail=f'Nenhum dado de revisão encontrado para este veiculo. Data: {data}')

    revisions = items[0].get('revisions', [])

    return list(map(_get_revision_data, revisions))

async def _get_data_from_source(name):
    status, response = await request_yamaha_data(name)

    log_debug(f'Status: {status} - Response: {response}')

    if status == 200:
        data = _refine_data(response)
        return data

    raise HTTPException(status_code=status, detail='Erro ao consultar dados da Yamaha')

async def get_yamaha_revision_table(name, can_use_cache):
    cached_data = get_data_from_cache(name, can_use_cache)

    log_debug(f'Cached data: {cached_data}')

    should_update_cache = True

    if can_use_cache and cached_data:
        return not should_update_cache, cached_data

    source_data = await _get_data_from_source(name)

    log_debug(f'Source data: {source_data}')

    if source_data:
        return should_update_cache, source_data

    return not should_update_cache, cached_data