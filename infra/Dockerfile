FROM python:3.11.9-slim

RUN apt-get update && \
    apt-get install -y gcc libpq-dev git build-essential && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

# COPY /alembic.ini .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8010

CMD ["uvicorn", "src.core.app.main:app", "--host", "0.0.0.0", "--port", "8010"]