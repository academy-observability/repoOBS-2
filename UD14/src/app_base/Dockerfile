FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/app.py /app/app.py

EXPOSE 8000

ENV PORT=8000
ENV APP_NAME=obsapp
ENV APP_ENV=container
ENV APP_VERSION=1.0
ENV BUILD_ID=local

CMD ["python", "app.py"]
