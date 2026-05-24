FROM python:3.11-slim

WORKDIR /app

# Instala as dependências
RUN pip install --no-cache-dir pandas

# Copia o código do pipeline
COPY pipeline.py .

# Comando padrão ao iniciar o container
CMD ["python", "pipeline.py"]