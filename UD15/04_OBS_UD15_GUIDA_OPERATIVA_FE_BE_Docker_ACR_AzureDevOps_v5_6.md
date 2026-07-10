# UD15 - Guida operativa
## FE/BE, Docker, ACR e Azure DevOps

## 1. Comandi Docker principali

Build backend:

```bash
docker build -t backend:ud15 ./backend
```

Build frontend:

```bash
docker build -t frontend:ud15 ./frontend
```

Rete locale:

```bash
docker network create ud15-net || true
```

Run backend:

```bash
docker run -d --name be-ud15 --network ud15-net -p 8001:8000 backend:ud15
```

Run frontend:

```bash
docker run -d --name fe-ud15 --network ud15-net -p 8000:8000 -e BACKEND_URL=http://be-ud15:8000 frontend:ud15
```

Log:

```bash
docker logs be-ud15
docker logs fe-ud15
```

Cleanup:

```bash
docker rm -f fe-ud15 be-ud15
docker network rm ud15-net
```

## 2. Comandi ACR

Verifica ACR:

```bash
az acr show --name NOME_ACR --resource-group NOME_RESOURCE_GROUP
```

Repository immagini:

```bash
az acr repository list --name NOME_ACR -o table
```

Tag backend:

```bash
az acr repository show-tags --name NOME_ACR --repository backend -o table
```

Tag frontend:

```bash
az acr repository show-tags --name NOME_ACR --repository frontend -o table
```

## 3. Errori frequenti

| Problema | Causa probabile | Verifica |
|---|---|---|
| Il frontend non raggiunge il backend | `BACKEND_URL` errata | `docker logs fe-ud15` |
| `/ready` restituisce errore | backend non avviato o rete errata | `docker ps`, `docker network inspect ud15-net` |
| Build frontend fallisce | `requirements.txt` o Dockerfile errato | `docker build -t frontend:ud15 ./frontend` |
| Pipeline fallisce in Validate | path YAML o workingDirectory errati | controllare `work/UD15` |
| Push ACR fallisce | service connection o nome ACR errato | `az acr show` |
| Non vedo repository in ACR | pipeline non arrivata al push | log job BuildBackend/BuildFrontend |

## 4. Nota su GitHub e Azure DevOps

Il repository del codice resta GitHub. La pipeline gira su Azure DevOps. ACR conserva solo immagini container.

```text
GitHub != ACR
GitHub = codice
ACR = immagini
```
