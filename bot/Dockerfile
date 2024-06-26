FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

WORKDIR /app/

ENV PYTHONPATH=/app

RUN  pip install --no-cache-dir -r bot/requirements.txt
CMD ["python", "bot/main.py"]