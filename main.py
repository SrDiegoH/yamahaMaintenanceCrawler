from fastapi import FastAPI
from playwright.async_api import async_playwright

app = FastAPI()

@app.get('/')
async def rodar_automacao():
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36 OPR/132.0.0.0'
    domain = 'www.yamaha-motor.com.br'

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent=ua)

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
            data='[{"productIds":["30095"]}]'
        )

        texto_resposta = await response.text()
        await browser.close()

        return {'status': response.status, 'data': texto_resposta}