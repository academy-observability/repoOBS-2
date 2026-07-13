FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV SERVICE_NAME=backend
ENV APP_VERSION=1.1.0-products
ENV APP_ENV=container
ENV PORT=8000
ENV SLOW_DELAY_SECONDS=2.0

EXPOSE 8000

CMD ["python", "app.py"]
