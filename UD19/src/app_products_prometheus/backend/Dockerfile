# Immagine base Python leggera per il backend Catalogo prodotti locale.
FROM python:3.12-slim

# Log immediati su stdout e nessun file .pyc nel container.
ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1

WORKDIR /app

# Installiamo prima le dipendenze per migliorare la cache Docker.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamo il codice applicativo del backend.
COPY app.py .

EXPOSE 8000
CMD ["python", "app.py"]
