# UD12 - Laboratorio guidato
## Docker locale: singola applicazione containerizzata

---

# 1. Obiettivo del laboratorio

In questo laboratorio costruiremo una piccola applicazione HTTP, la testeremo localmente, la containerizzeremo con Docker e ne verificheremo il comportamento tramite endpoint e log.

Alla fine dovremo essere in grado di dimostrare:

- app funzionante senza Docker;
- Dockerfile corretto;
- immagine costruita localmente;
- container avviato;
- porta esposta correttamente;
- endpoint verificati con `curl`;
- log letti con `docker logs`;
- differenza tra immagine e container.

---

# 2. Verifica iniziale Docker

Apriamo il terminale WSL o il terminale indicato dal docente.

Verifichiamo Docker:

```bash
docker --version
docker version
docker info
```

Se Docker risponde correttamente, possiamo proseguire.

Test opzionale:

```bash
docker run hello-world
```

Se questo comando funziona, Docker riesce a scaricare ed eseguire una immagine di test.

---

# 3. Creazione cartella di lavoro

Creiamo la cartella della UD12:

```bash
mkdir -p ~/corso_obs/work/UD12/src
mkdir -p ~/corso_obs/work/UD12/docs
cd ~/corso_obs/work/UD12
```

Verifichiamo:

```bash
pwd
find . -maxdepth 2 -type d | sort
```

Struttura attesa:

```text
.
./docs
./src
```

---

# 4. Creazione applicazione Flask

Creiamo il file:

```bash
code src/app.py
```

Inseriamo il seguente contenuto:

```python
import json
import os
import time
import uuid
from datetime import datetime, timezone

from flask import Flask, g, jsonify, request
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
APP_VERSION = os.getenv("APP_VERSION", "1.0")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_log(status_code: int, message: str = "request_completed") -> None:
    latency_ms = round((time.perf_counter() - g.start_time) * 1000, 2)

    record = {
        "timestamp": utc_now_iso(),
        "level": "INFO" if status_code < 400 else "ERROR",
        "message": message,
        "request_id": g.request_id,
        "method": request.method,
        "path": request.path,
        "status": int(status_code),
        "latency_ms": latency_ms,
        "client_ip": request.headers.get("X-Forwarded-For", request.remote_addr),
        "user_agent": request.headers.get("User-Agent"),
        "version": APP_VERSION,
    }

    print(json.dumps(record), flush=True)


@app.before_request
def before_request() -> None:
    g.start_time = time.perf_counter()
    g.request_id = request.headers.get("X-Request-Id", str(uuid.uuid4()))


@app.after_request
def after_request(response):
    write_log(response.status_code)
    response.headers["X-Request-Id"] = g.request_id
    return response


@app.errorhandler(HTTPException)
def handle_http_exception(exc: HTTPException):
    response = jsonify(
        {
            "error": exc.name.lower().replace(" ", "_"),
            "status": exc.code,
            "path": request.path,
            "version": APP_VERSION,
        }
    )
    response.status_code = exc.code
    return response


@app.errorhandler(Exception)
def handle_generic_exception(exc: Exception):
    response = jsonify(
        {
            "error": "internal_server_error",
            "status": 500,
            "path": request.path,
            "version": APP_VERSION,
        }
    )
    response.status_code = 500
    return response


@app.get("/")
def home():
    return jsonify(
        {
            "app": "obsapp-ud12",
            "version": APP_VERSION,
            "status": "running",
            "timestamp": utc_now_iso(),
        }
    ), 200


@app.get("/health")
def health():
    return jsonify({"status": "ok", "version": APP_VERSION, "timestamp": utc_now_iso()}), 200


@app.get("/time")
def current_time():
    return jsonify({"time": utc_now_iso(), "version": APP_VERSION}), 200


@app.post("/echo")
def echo():
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "invalid_json", "status": 400, "version": APP_VERSION}), 400
    return jsonify({"received": payload, "status": 200, "version": APP_VERSION}), 200


@app.get("/error")
def simulated_error():
    return jsonify({"error": "simulated_error", "status": 500, "version": APP_VERSION}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    app.run(host="0.0.0.0", port=port)
```

---

# 5. Creazione requirements

Creiamo:

```bash
code requirements.txt
```

Contenuto:

```txt
flask==3.0.0
```

---

# 6. Test dell'app senza Docker

Creiamo l'ambiente virtuale:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Verifichiamo la sintassi:

```bash
python3 -m py_compile src/app.py
```

Avviamo l'app:

```bash
python src/app.py
```

Apriamo un secondo terminale ed eseguiamo:

```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/time
curl -X POST http://127.0.0.1:8000/echo \
  -H 'Content-Type: application/json' \
  -d '{"lab":"UD12","mode":"no-docker"}'
curl http://127.0.0.1:8000/error
curl http://127.0.0.1:8000/rotta-inesistente
```

Risultati attesi:

| Endpoint | Risultato atteso |
|---|---|
| `/` | risposta `200` con nome app |
| `/health` | risposta `200` con `status: ok` |
| `/time` | risposta `200` con timestamp |
| `/echo` | risposta `200` con payload ricevuto |
| `/error` | risposta `500` simulata |
| rotta inesistente | risposta `404` |

Fermiamo l'app nel primo terminale con `CTRL+C`.

---

# 7. Creazione Dockerfile

Creiamo:

```bash
code Dockerfile
```

Contenuto:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/app.py /app/app.py

EXPOSE 8000

ENV PORT=8000
ENV APP_VERSION=1.0

CMD ["python", "app.py"]
```

---

# 8. Creazione .dockerignore

Creiamo:

```bash
code .dockerignore
```

Contenuto:

```txt
.git
.gitignore
__pycache__/
*.pyc
*.pyo
*.pyd
.venv/
venv/
.env
docs/
logs/
```

---

# 9. Build immagine Docker

Dalla cartella `UD12`:

```bash
docker build -t obsapp-ud12:1.0 .
```

Verifichiamo:

```bash
docker images | grep obsapp-ud12
```

Dovremmo vedere l'immagine:

```text
obsapp-ud12   1.0
```

---

# 10. Avvio container in foreground

Avviamo il container:

```bash
docker run --name obsapp-ud12 -p 8000:8000 obsapp-ud12:1.0
```

Il terminale resta occupato perché il container è in foreground.

In un secondo terminale:

```bash
docker ps
```

Verifichiamo che il container sia in esecuzione.

---

# 11. Test dell'app containerizzata

Nel secondo terminale:

```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/time
curl -X POST http://127.0.0.1:8000/echo \
  -H 'Content-Type: application/json' \
  -d '{"lab":"UD12","container":"true"}'
curl http://127.0.0.1:8000/error
curl http://127.0.0.1:8000/rotta-inesistente
```

Il comportamento deve essere equivalente a quello visto senza Docker.

Nel primo terminale dovremmo vedere log prodotti dall'applicazione.

Fermiamo il container con `CTRL+C`.

---

# 12. Avvio container in background

Rimuoviamo l'eventuale container precedente:

```bash
docker rm -f obsapp-ud12
```

Avviamo in detached mode:

```bash
docker run -d --name obsapp-ud12 -p 8000:8000 obsapp-ud12:1.0
```

Verifichiamo:

```bash
docker ps
```

---

# 13. Lettura log del container

Generiamo traffico:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/error
curl http://127.0.0.1:8000/rotta-inesistente
```

Leggiamo i log:

```bash
docker logs obsapp-ud12
```

Nei log dobbiamo riconoscere:

- `path`;
- `method`;
- `status`;
- `latency_ms`;
- `request_id`;
- `version`.

---

# 14. Gestione ciclo di vita del container

Eseguiamo:

```bash
docker stop obsapp-ud12
docker ps
docker ps -a
```

Riavviamo:

```bash
docker start obsapp-ud12
docker ps
```

Riavvio completo:

```bash
docker restart obsapp-ud12
```

Rimozione:

```bash
docker rm -f obsapp-ud12
```

Verifica finale:

```bash
docker ps -a
docker images | grep obsapp-ud12
```

Il container è stato rimosso, ma l'immagine resta disponibile.

---

# 15. Modifica versione e rebuild

Modifichiamo il Dockerfile:

```dockerfile
ENV APP_VERSION=1.1
```

Ricostruiamo l'immagine:

```bash
docker build -t obsapp-ud12:1.1 .
```

Avviamo la nuova versione:

```bash
docker run -d --name obsapp-ud12 -p 8000:8000 obsapp-ud12:1.1
```

Verifichiamo:

```bash
curl http://127.0.0.1:8000/
docker logs obsapp-ud12
```

Dovremmo vedere `version: 1.1` nella risposta e nei log.

Messaggio tecnico: se cambiamo il contenuto che deve stare nell'immagine, dobbiamo ricostruire l'immagine e avviare un nuovo container.

---

# 16. Evidenza da produrre

Creiamo:

```bash
code docs/evidence_ud12.md
```

Struttura richiesta:

```md
# Evidence UD12

## 1. Obiettivo compreso
Spiego con parole mie che cosa ho containerizzato e perché.

## 2. Verifica Docker
Incollo output essenziale di:
- docker --version
- docker info oppure docker version

## 3. Struttura progetto
Descrivo i file principali:
- src/app.py
- requirements.txt
- Dockerfile
- .dockerignore

## 4. Test app senza Docker
Riporto output degli endpoint principali.

## 5. Build immagine
Riporto comando usato e output essenziale di docker images.

## 6. Avvio container
Riporto comando docker run e output di docker ps.

## 7. Test app nel container
Riporto output di:
- GET /
- GET /health
- GET /time
- POST /echo
- GET /error
- rotta inesistente

## 8. Log container
Incollo alcune righe di docker logs e commento path, status e latency.

## 9. Differenza immagine/container
Spiego con parole mie la differenza.

## 10. Problemi incontrati
Descrivo eventuali errori e come li ho risolti.
```

---

# 17. Cleanup finale

A fine laboratorio, se richiesto dal docente:

```bash
docker rm -f obsapp-ud12
```

Le immagini possono essere lasciate disponibili per confronto oppure rimosse:

```bash
docker rmi obsapp-ud12:1.0 obsapp-ud12:1.1
```

Rimuovere le immagini solo se il docente lo richiede.

---

# 18. Conclusione

Abbiamo trasformato una piccola applicazione locale in una immagine Docker e l'abbiamo eseguita come container.

Il risultato importante non è solo tecnico. È concettuale:

```text
codice -> immagine -> container -> endpoint -> log -> evidenza
```

Questa è la base necessaria per comprendere il deploy automatizzato nei passaggi successivi del percorso.
