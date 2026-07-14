# Immagine base Python leggera per eseguire il backend Flask osservabile.
FROM python:3.12-slim

# Evita file .pyc e rende immediati i log su stdout/stderr.
ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1

WORKDIR /app

# Installiamo prima le dipendenze per sfruttare la cache Docker.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamo il codice applicativo del backend products.
COPY app.py .

EXPOSE 8000
CMD ["python", "app.py"]
