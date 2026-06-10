FROM python:3.10-slim

# 1. Instala as dependências básicas do Linux necessárias para baixar arquivos
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Copia os arquivos de dependências do Python e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Instala os binários do Chromium e as dependências de sistema do próprio Playwright
RUN playwright install chromium
RUN playwright install-deps chromium

# 4. Copia o restante do código do projeto para dentro do contêiner
COPY . .

# 5. Comando de inicialização da sua API (FastAPI/Uvicorn lê a porta dinâmica do Render)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]