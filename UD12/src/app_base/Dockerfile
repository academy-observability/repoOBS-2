FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/app.py /app/app.py

EXPOSE 8000

ENV PORT=8000
ENV APP_VERSION=1.0

CMD ["python", "app.py"]
