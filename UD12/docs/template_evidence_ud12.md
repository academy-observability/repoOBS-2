# Evidence UD12

## 1. Obiettivo compreso
Spiego con parole mie che cosa ho containerizzato e perché.

## 2. Verifica Docker
Incollo output essenziale di:

```bash
docker --version
```

Output:

```text
...
```

Incollo output essenziale di:

```bash
docker info
```

oppure:

```bash
docker version
```

Output:

```text
...
```

## 3. Struttura progetto
Descrivo i file principali:

- `src/app.py`:
- `requirements.txt`:
- `Dockerfile`:
- `.dockerignore`:

## 4. Test app senza Docker
Riporto output degli endpoint principali:

```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/time
curl -X POST http://127.0.0.1:8000/echo -H 'Content-Type: application/json' -d '{"lab":"UD12"}'
curl http://127.0.0.1:8000/error
curl http://127.0.0.1:8000/rotta-inesistente
```

Output/commento:

```text
...
```

## 5. Build immagine
Comando usato:

```bash
...
```

Output essenziale di:

```bash
docker images | grep obsapp-ud12
```

```text
...
```

## 6. Avvio container
Comando usato:

```bash
...
```

Output di:

```bash
docker ps
```

```text
...
```

## 7. Test app nel container
Riporto output di:

- GET `/`
- GET `/health`
- GET `/time`
- POST `/echo`
- GET `/error`
- rotta inesistente

```text
...
```

## 8. Log container
Comando:

```bash
docker logs obsapp-ud12
```

Log:

```text
...
```

Commento i campi principali:

- `path`:
- `status`:
- `latency_ms`:
- `request_id`:

## 9. Differenza immagine/container
Spiego con parole mie la differenza.

```text
...
```

## 10. Problemi incontrati
Descrivo eventuali errori e come li ho risolti.

```text
...
```
