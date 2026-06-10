from playwright.async_api import async_playwright

from common.util import MOTORCYCLE_MODELS

async def request_yamaha_data(name):
    async with async_playwright() as playwright:
        browser = None
        context = None
        try:
            browser = await playwright.chromium.launch(
                headless=True,
                args=[
                    '--disable-gpu',
                    '--single-process',
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--no-zygote',
                    '--disable-component-update',
                    '--disable-default-apps',
                    '--js-flags=--max-old-space-size=128'
                ]
            )

            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36 OPR/132.0.0.0',
                extra_http_headers={
                    'Cookie': f'SOFT_LOGIN=eyJraWQiOiJTb2Z0TG9naW5LZXkiLCJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIzOTgyMzc3NDA3IiwiaXNzIjoic3RvcmVmcm9udFVJIiwiZXhwIjoxNzk3OTY2NzIzOTE3LCJpYXQiOjE3NjM4Mzg3MjM5MTd9.VbKqvVknOQ_p7WHhYhHiW5kx0LfG96knAo8bcKo3j6g; carrinho-id=3786ad2c-490e-4ba3-8c62-6854957c6bcd'
                }
            )

            page = await context.new_page()

            await page.route("**/*", lambda route: route.abort() if route.request.resource_type in ["image", "media", "font", "stylesheet"] else route.continue_())
            await page.goto('https://www.yamaha-motor.com.br')

            headers = {
                'accept': 'text/x-component',
                'accept-language': 'pt-BR,pt;q=0.9,en;q=0.8,ko;q=0.7,es;q=0.6,fr;q=0.5',
                'cache-control': 'no-cache',
                'content-type': 'text/plain;charset=UTF-8',
                'dnt': '1',
                'next-action': '40c45b238c8f88d9e47b69c4b53f4dfe78655b653d',
                'next-router-state-tree': '%5B%22%22%2C%7B%22children%22%3A%5B%5B%22slug%22%2C%22servicos%22%2C%22c%22%2Cnull%5D%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%2Cnull%2Cnull%2C0%5D%7D%2Cnull%2Cnull%2C0%5D%7D%2Cnull%2Cnull%2C16%5D',
                'origin': 'https://www.yamaha-motor.com.br',
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
                'https://www.yamaha-motor.com.br/servicos',
                headers=headers,
                data=f'[{{"productIds":["{MOTORCYCLE_MODELS[name]}"]}}]'
            )

            response_text = await response.text()
            await browser.close()

            return response.status, response_text
        finally:
            if context:
                await context.close()
            if browser:
                await browser.close()