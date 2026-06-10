import json

from fastapi import FastAPI, HTTPException
from playwright.async_api import async_playwright

_MOTORCYCLES = {
    'R3 ABS 70th': '30176', 
    'FACTOR 150 UBS 2016 A 2024': '30093', 
    'FZ15 2023 A 2024': '30094', 
    'FAZER 250 2018 A 2024': '30095', 
    'CROSSER XTZ150 Z 2015 A 2024': '30097', 
    'CROSSER XTZ150 S 2015 A 2024': '30096', 
    'XMAX 2021 A 2024': '30098', 
    'NMAX CONNECTED 2023 A 2024': '30101', 
    'LANDER 250 2020 A 2024': '30105', 
    'FACTOR 125 i (UBS) 2017 A 2025': '30106', 
    'FAZER 150 UBS 2014 A 2025': '30107', 
    'FLUO ABS 2022 A 2025': '30108', 
    'NEO 125 2017 A 2024': '30115', 
    'MT03 ABS 2021 A 2025': '30121', 
    'NOVA NMAX CONNECTED 2025': '30127', 
    'XMAX CONNECTED 2025': '30123', 
    'LANDER 250 ABS CONNECTED 2025': '30126', 
    'CROSSER XTZ150 S 2025': '30125', 
    'CROSSER XTZ150 Z 2025': '30131', 
    'YZF-R3 ABS 2020 A 2025': '30109', 
    'FACTOR': '30129', 
    'NOVA FACTOR DX 2025': '30132', 
    'FLUO ABS HYBRID CONNECTED': '30171', 
    "NEO'S DUAL CONNECTED 2026": '30130', 
    'YZF R3 ABS CONNECTED 2026': '30140', 
    'NOVA MT-03 CONNECTED 2026': '30141', 
    'NOVA MT-07 CONNECTED 2026': '30142', 
    'NOVA XMAX 300 CONNECTED': '30147', 
    'TÉNÉRÉ 700': '30143', 
    'AEROX ABS CONNECTED': '30164', 
    'FAZER FZ15 ABS CONNECTED 2025 A 2026': '30160', 
    'R15 ABS 2024 A 2026': '30163', 
    'FZ25 CONNECTED DE 2025 A 2026': '30161', 
    'LANDER CONNECTED 2025 a 2026': '30167', 
    'NOVA NMAX ABS CONNECTED': '30168', 
    'FAZER FZ25 CONNECTED': '30173', 
    'YAMAHA ZR HYBRID CONNECTED': '30175', 
    'Nova Factor 2025 a 2026': '30174', 
    'NOVA FACTOR DX 2025 a 2026': '30172', 
    'CROSSER 150 Z ABS 2025 a 2026': '30170', 
    'CROSSER 150 S ABS 2025 a 2026': '30169'
}

app = FastAPI()

_get_revision_data = lambda revision: {
    'revisionByKm': revision.revisionByKm,
    'revisionByMonth': revision.revisionByMonth,
    'revisionPriceInCash': revision.priceInCash
}

def _refine_data(data):
    if '1:' not in data:
        raise HTTPException(status_code=500, detail=f'Erro ao consultar dados da Yamaha. Data: {data}')

    content = data.split('1:')[1]
    parsed_json = json.loads(content)
    items = parsed_json.get('result', {}).get('items', [])

    if not items:
        raise HTTPException(status_code=404, detail=f'Nenhum dado de revisão encontrado para este veiculo. Data: {data}')

    revisions = items[0].get('revisions', [])

    return list(map(_get_revision_data, revisions))

async def _get_yamaha_data(name):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36 OPR/132.0.0.0'
    domain = 'www.yamaha-motor.com.br'

    async with async_playwright() as playwrite:
        browser = await playwrite.chromium.launch(headless=True)
        context = await browser.new_context(user_agent=user_agent)

        await context.add_cookies([
            {
                'name': 'SOFT_LOGIN',
                'value': 'eyJraWQiOiJTb2Z0TG9naW5LZXkiLCJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIzOTgyMzc3NDA3IiwiaXNzIjoic3RvcmVmcm9udFVJIiwiZXhwIjoxNzk3OTY2NzIzOTE3LCJpYXQiOjE3NjM4Mzg3MjM5MTd9.VbKqvVknOQ_p7WHhYhHiW5kx0LfG96knAo8bcKo3j6g',
                'domain': domain,
                'path': '/'
            },
            {
                'name': 'carrinho-id',
                'value': '3786ad2c-490e-4ba3-8c62-6854957c6bcd',
                'domain': domain,
                'path': '/'
            }
        ])

        page = await context.new_page()

        await page.goto(f'https://www.yamaha-motor.com.br')

        headers = {
            'accept': 'text/x-component',
            'accept-language': 'pt-BR,pt;q=0.9,en;q=0.8,ko;q=0.7,es;q=0.6,fr;q=0.5',
            'cache-control': 'no-cache',
            'content-type': 'text/plain;charset=UTF-8',
            'dnt': '1',
            'next-action': '40c45b238c8f88d9e47b69c4b53f4dfe78655b653d',
            'next-router-state-tree': '%5B%22%22%2C%7B%22children%22%3A%5B%5B%22slug%22%2C%22servicos%22%2C%22c%22%2Cnull%5D%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%2Cnull%2Cnull%2C0%5D%7D%2Cnull%2Cnull%2C0%5D%7D%2Cnull%2Cnull%2C16%5D',
            'origin': f'https://www.yamaha-motor.com.br',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Chromium";v="148", "Opera GX";v="132", "Not/A)Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1'
        }

        response = await page.request.post(
            f'https://www.yamaha-motor.com.br/servicos',
            headers=headers,
            data=f'[{{"productIds":["{_MOTORCYCLES[name]}"]}}]'
        )

        response_text = await response.text()
        await browser.close()

        return response.status, response_text

@app.get('/')
async def index(name=None):
    if not name:
        raise HTTPException(status_code=400, detail='O parâmetro "name" é obrigatório')

    status, response = await _get_yamaha_data(name)

    print('Status:', status, 'Response:', response)

    if status == 200:
        data = _refine_data(response)
        print('Data:', data)
        return data

    raise HTTPException(status_code=status, detail='Erro ao consultar dados da Yamaha')