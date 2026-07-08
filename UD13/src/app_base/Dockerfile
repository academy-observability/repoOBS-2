FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/app.py /app/app.py

EXPOSE 8000

ENV PORT=8000
ENV APP_NAME=obsapp-ud13
ENV APP_ENV=container

CMD ["python", "app.py"]
