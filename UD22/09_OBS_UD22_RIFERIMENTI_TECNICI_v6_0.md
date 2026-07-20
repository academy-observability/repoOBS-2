# OBS UD22 — Riferimenti tecnici

I materiali della UD utilizzano come riferimenti principali la documentazione ufficiale dei progetti impiegati.

## Jaeger

- Deployment, componenti, porte e storage backend:  
  https://www.jaegertracing.io/docs/1.76/deployment/
- Configurazione Badger e permessi del volume con utente non privilegiato:  
  https://github.com/jaegertracing/jaeger/blob/v1.76.0/internal/storage/v1/badger/docs/storage-file-non-root-permission.md
- Sampling:  
  https://www.jaegertracing.io/docs/1.76/architecture/sampling/

## OpenTelemetry Python

- Strumentazione Flask:  
  https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/flask/flask.html
- Strumentazione della libreria `requests`:  
  https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/requests/requests.html
- Propagazione del contesto:  
  https://opentelemetry.io/docs/languages/python/propagation/

## Docker

- Volumi:  
  https://docs.docker.com/engine/storage/volumes/
- Volumi nel Compose:  
  https://docs.docker.com/reference/compose-file/volumes/
- Comportamento di `docker compose down`:  
  https://docs.docker.com/reference/cli/docker/compose/down/
