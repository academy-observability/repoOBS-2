# UD15 - Laboratorio guidato
## FE/BE Docker locale, due immagini e pipeline multi-image verso ACR

## Obiettivo del laboratorio

In questo laboratorio costruiremo un piccolo sistema composto da:

- backend;
- frontend;
- due Dockerfile;
- due immagini Docker;
- una pipeline Azure DevOps che pubblica entrambe le immagini su ACR.

Non faremo ancora il deploy FE/BE su Azure Container Apps.

---

## 1. Preparazione cartella di lavoro

Dal repository del corso apriamo il terminale WSL:

```bash
mkdir -p work/UD15
cd work/UD15
mkdir -p frontend backend docs
```

Se il docente ha fornito la cartella `src/app_base`, possiamo copiare i file base:

```bash
cp -r ../../UD15/src/app_base/frontend ./frontend
cp -r ../../UD15/src/app_base/backend ./backend
```

In alternativa creiamo manualmente i file seguendo le sezioni successive.

Struttura attesa:

```text
work/UD15/
├── frontend/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
└── docs/
```

---

## 2. Verifica sintattica dei due servizi

Eseguiamo:

```bash
python3 -m py_compile backend/app.py
python3 -m py_compile frontend/app.py
```

Se non compare output, la sintassi è valida.

---

## 3. Build locale delle immagini

Costruiamo l'immagine del backend:

```bash
docker build -t backend:ud15 ./backend
```

Costruiamo l'immagine del frontend:

```bash
docker build -t frontend:ud15 ./frontend
```

Verifichiamo:

```bash
docker images | grep -E 'backend|frontend'
```

---

## 4. Test locale FE/BE con rete Docker

Creiamo una rete dedicata:

```bash
docker network create ud15-net || true
```

Avviamo il backend:

```bash
docker rm -f be-ud15 2>/dev/null || true

docker run -d   --name be-ud15   --network ud15-net   -p 8001:8000   -e SERVICE_NAME=backend   -e APP_ENV=local-container   -e APP_VERSION=1.0.0-ud15   backend:ud15
```

Avviamo il frontend collegandolo al backend tramite il nome del container:

```bash
docker rm -f fe-ud15 2>/dev/null || true

docker run -d   --name fe-ud15   --network ud15-net   -p 8000:8000   -e SERVICE_NAME=frontend   -e APP_ENV=local-container   -e APP_VERSION=1.0.0-ud15   -e BACKEND_URL=http://be-ud15:8000   frontend:ud15
```

Verifichiamo i container:

```bash
docker ps
```

---

## 5. Test HTTP locale

Testiamo il backend dalla macchina host:

```bash
curl http://127.0.0.1:8001/health
curl http://127.0.0.1:8001/version
curl http://127.0.0.1:8001/work
```

Testiamo il frontend:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/version
curl http://127.0.0.1:8000/ready
curl http://127.0.0.1:8000/demo
```

Generiamo anche un errore controllato:

```bash
curl http://127.0.0.1:8000/demo-error
```

Risultati attesi:

| Endpoint | Risultato atteso |
|---|---|
| backend `/health` | 200 |
| backend `/work` | 200 |
| frontend `/health` | 200 |
| frontend `/ready` | 200 se il backend è raggiungibile |
| frontend `/demo` | 200 e risposta del backend inclusa |
| frontend `/demo-error` | 500 controllato |

---

## 6. Lettura log separati

Leggiamo i log del backend:

```bash
docker logs be-ud15
```

Leggiamo i log del frontend:

```bash
docker logs fe-ud15
```

Nei log dobbiamo riconoscere:

- `service`;
- `request_id`;
- `method`;
- `path`;
- `status`;
- `latency_ms`.

Questa separazione è importante: il frontend e il backend sono due servizi distinti e producono segnali distinti.

---

## 7. Verifica ACR

Verifichiamo di avere accesso ad Azure e ad ACR:

```bash
az login
az account show
az acr show --name NOME_ACR --resource-group NOME_RESOURCE_GROUP
```

Se ACR non esiste ancora, crearne uno solo se il docente lo prevede:

```bash
az acr create   --resource-group NOME_RESOURCE_GROUP   --name NOME_ACR_UNIVOCO   --sku Basic   --location westeurope
```

---

## 8. Creazione del file pipeline

Creiamo il file:

```bash
code azure-pipelines.yml
```

Usiamo il template `templates/azure-pipelines-ud15-multiimage.yml` e adattiamo almeno:

```yaml
variables:
  azureServiceConnection: 'sc-obs-azure-rg'
  acrName: 'NOME_ACR'
```

La pipeline esegue:

```text
ValidateRepository
-> BuildBackend
-> BuildFrontend
-> push immagini su ACR
```

---

## 9. Commit e push su GitHub

```bash
git status
git add work/UD15
git commit -m "UD15 - FE BE multi-image pipeline to ACR"
git push
```

Il file deve essere su GitHub, perché Azure DevOps lo leggerà dal repository remoto.

---

## 10. Creazione pipeline Azure DevOps

Nel progetto Azure DevOps:

```text
Pipelines
-> Create Pipeline
-> GitHub
-> seleziona repository
-> Existing Azure Pipelines YAML file
-> work/UD15/azure-pipelines.yml
-> Run
```

Nome consigliato:

```text
UD15-fe-be-multiimage-acr
```

---

## 11. Osservazione della pipeline

Durante l'esecuzione apriamo i log e verifichiamo:

| Stage/job | Cosa osservare |
|---|---|
| ValidateRepository | file presenti e sintassi Python valida |
| BuildBackend | build e push immagine backend |
| BuildFrontend | build e push immagine frontend |

---

## 12. Verifica immagini in ACR

Dopo la pipeline:

```bash
az acr repository list --name NOME_ACR -o table
```

Dovremmo vedere almeno:

```text
backend
frontend
```

Verifichiamo i tag:

```bash
az acr repository show-tags --name NOME_ACR --repository backend -o table
az acr repository show-tags --name NOME_ACR --repository frontend -o table
```

I tag devono includere il valore del run della pipeline, cioè `Build.BuildId`.

---

## 13. Evidenze

Creiamo il file:

```bash
code docs/evidence_ud15.md
```

Usiamo il template fornito in `docs/template_evidence_ud15.md`.

---

## 14. Cleanup locale

A fine laboratorio possiamo fermare i container locali:

```bash
docker rm -f fe-ud15 be-ud15
```

La rete può essere rimossa se non serve più:

```bash
docker network rm ud15-net
```

Non eliminare ACR, salvo indicazione esplicita del docente.
