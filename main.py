from fastapi import FastAPI
from playwright.async_api import async_playwright

app = FastAPI()

@app.get("/executar-teste")
async def rodar_automacao():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36 OPR/131.0.0.0"
    
    async with async_playwright() as p:
        # Lança o Chromium em modo headless (obrigatório em servidores)
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent=user_agent)

        # Configura os cookies
        await context.add_cookies([{
            "name": "carrinho-id",
            "value": "65fdb0ec-e215-4351-8217-7a00ffab2906",
            "domain": "www3.yamaha-motor.com.br",
            "path": "/"
        }])

        page = await context.new_page()
        
        # Faz o disparo do POST
        headers_curl = {
            'accept': 'text/x-component',
            'content-type': 'text/plain;charset=UTF-8',
            'next-action': '40c45b238c8f88d9e47b69c4b53f4dfe78655b653d',
            'origin': 'https://www3.yamaha-motor.com.br'
        }
        
        response = await page.request.post(
            "https://www3.yamaha-motor.com.br/servicos",
            headers=headers_curl,
            data='[{"productIds":["30095"]}]'
        )
        
        texto_resposta = await response.text()
        await browser.close()
        
        return {"status": response.status, "data": texto_resposta}