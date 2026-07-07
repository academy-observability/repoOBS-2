# App base UD12

Questa cartella contiene una versione completa dell'applicazione usata nella UD12.

Il laboratorio guidato prevede la creazione passo passo degli stessi file.

Per eseguire rapidamente:

```bash
cd src/app_base
docker build -t obsapp-ud12:1.0 .
docker run -d --name obsapp-ud12 -p 8000:8000 obsapp-ud12:1.0
curl http://127.0.0.1:8000/health
docker logs obsapp-ud12
```
