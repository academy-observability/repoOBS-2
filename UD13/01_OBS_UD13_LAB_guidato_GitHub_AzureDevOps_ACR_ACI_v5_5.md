# UD13 - Laboratorio guidato
## GitHub -> Azure DevOps -> ACR -> ACI

---

# 1. Obiettivo del laboratorio

In questo laboratorio realizziamo il primo deploy automatico cloud di una app containerizzata.

Il flusso sarà:

```text
repository GitHub
  -> pipeline Azure DevOps
  -> build immagine Docker
  -> push su Azure Container Registry
  -> deploy su Azure Container Instances
  -> verifica HTTP
  -> lettura log cloud
```

---

# 2. Prerequisiti

Prima di iniziare devono essere disponibili:

- account GitHub e repository personale/fork del corso;
- organizzazione e progetto Azure DevOps creati nella UD dedicata al setup;
- accesso alla subscription Azure del corso;
- Azure CLI funzionante;
- Resource Group già disponibile o indicato dal docente;
- Docker compreso dalla UD precedente;
- VS Code o editor equivalente.

> Nota: se Azure DevOps non mostra il repository GitHub, consultare la guida operativa `04_OBS_UD13_GUIDA_OPERATIVA_Service_Connections_ACR_ACI_v5_5.md`.

---

# 3. Preparazione cartella di lavoro

Nel repository locale del corso creare la cartella della UD:

```bash
mkdir -p work/UD13/src
mkdir -p work/UD13/docs
cd work/UD13
```

La struttura finale sarà:

```text
work/UD13/
├── src/app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── azure-pipelines.yml
└── docs/evidence_ud13.md
```

---

# 4. Creazione applicazione

Creare il file:

```bash
code src/app.py
```

Inserire il codice fornito in `UD13/src/app_base/src/app.py`, oppure copiarlo dalla cartella sorgente.

L'app espone questi endpoint:

| Endpoint | Risultato atteso |
|---|---|
| `GET /` | stato generale app |
| `GET /health` | stato di salute |
| `GET /time` | timestamp corrente |
| `POST /echo` | restituzione payload JSON |
| `GET /error` | errore simulato 500 |
| rotta inesistente | errore 404 reale |

---

# 5. Creazione file dipendenze

Creare `requirements.txt`:

```bash
code requirements.txt
```

Contenuto:

```txt
flask==3.0.0
```

---

# 6. Creazione Dockerfile

Creare `Dockerfile`:

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
ENV APP_NAME=obsapp-ud13
ENV APP_ENV=container

CMD ["python", "app.py"]
```

---

# 7. Creazione `.dockerignore`

Creare `.dockerignore`:

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
evidence/
logs/
img/
```

---

# 8. Verifica locale minima

Prima di creare la pipeline, verificare sintassi e build locale:

```bash
python3 -m py_compile src/app.py

docker build -t obsapp-ud13:local .
```

Avviare il container:

```bash
docker run --rm -p 8000:8000 \
  -e APP_ENV=local-test \
  -e APP_VERSION=local \
  obsapp-ud13:local
```

In un secondo terminale:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/
```

Interrompere il container con `CTRL+C`.

Questa verifica non sostituisce la pipeline: serve solo a evitare errori banali prima di andare su Azure DevOps.

---

# 9. Login Azure e verifica Resource Group

```bash
az login
az account show
```

Verificare il Resource Group indicato dal docente:

```bash
az group show --name NOME_RESOURCE_GROUP
```

Se il Resource Group non esiste, attendere indicazioni del docente prima di crearne uno nuovo.

---

# 10. Creazione o verifica Azure Container Registry

Scegliere un nome ACR univoco, solo lettere minuscole e numeri, ad esempio:

```text
acrobslabnome123
```

Creare ACR se non esiste:

```bash
az acr create \
  --resource-group NOME_RESOURCE_GROUP \
  --name NOME_ACR_UNIVOCO \
  --sku Basic \
  --location westeurope
```

Verificare:

```bash
az acr show \
  --name NOME_ACR_UNIVOCO \
  --resource-group NOME_RESOURCE_GROUP
```

Abilitare admin account per il laboratorio:

```bash
az acr update \
  --name NOME_ACR_UNIVOCO \
  --admin-enabled true
```

Verificare che le credenziali siano leggibili:

```bash
az acr credential show --name NOME_ACR_UNIVOCO
```

> Nota: questa è una semplificazione didattica. Non va presentata come modello di produzione.

---

# 11. Creazione Azure Resource Manager service connection

Nel progetto Azure DevOps:

```text
Project settings
-> Service connections
-> New service connection
-> Azure Resource Manager
```

Creare una connessione verso la subscription o il Resource Group corretto.

Nome consigliato:

```text
sc-obs-azure-rg
```

Annotare il nome: deve coincidere con quello usato nel file YAML.

---

# 12. Creazione pipeline YAML

Creare il file:

```bash
code azure-pipelines.yml
```

Copiare il contenuto del template:

```text
UD13/templates/azure-pipelines-ud13.yml
```

Poi modificare almeno questi valori:

```yaml
resourceGroupName: 'NOME_RESOURCE_GROUP'
acrName: 'NOME_ACR_UNIVOCO'
aciDnsName: 'obsapp-ud13-nomeunivoco'
```

Il nome DNS deve essere univoco nella region Azure. Usare solo minuscole, numeri e trattini.

Controllare anche il nome della service connection:

```yaml
azureServiceConnection: 'sc-obs-azure-rg'
```

---

# 13. Commit e push su GitHub

Dal repository locale:

```bash
git status
git add work/UD13
git commit -m "UD13 - primo deploy automatico Azure DevOps ACR ACI"
git push
```

Verificare su GitHub che sia presente:

```text
work/UD13/azure-pipelines.yml
```

---

# 14. Creazione pipeline in Azure DevOps

Nel portale Azure DevOps:

```text
Pipelines
-> Create Pipeline
-> GitHub
-> selezionare il repository
-> Existing Azure Pipelines YAML file
-> selezionare work/UD13/azure-pipelines.yml
-> Run
```

Se il repository GitHub non compare, consultare la guida operativa.

---

# 15. Verifica esecuzione pipeline

Durante il run devono comparire passaggi simili a:

```text
checkout
az account show
az acr login
docker build
docker push
az container delete
az container create
FQDN finale
```

La pipeline deve terminare con stato `Succeeded`.

---

# 16. Verifica immagine pubblicata in ACR

Da terminale locale:

```bash
az acr repository list \
  --name NOME_ACR_UNIVOCO \
  -o table
```

Verificare i tag dell'immagine:

```bash
az acr repository show-tags \
  --name NOME_ACR_UNIVOCO \
  --repository obsapp-ud13 \
  -o table
```

Dovrebbe comparire almeno un tag numerico, corrispondente al run della pipeline.

---

# 17. Verifica container ACI

```bash
az container show \
  --resource-group NOME_RESOURCE_GROUP \
  --name aci-obsapp-ud13 \
  --query "{state:instanceView.state,fqdn:ipAddress.fqdn,ports:ipAddress.ports}" \
  -o json
```

Annotare il FQDN.

---

# 18. Test HTTP dell'app cloud

Recuperare il FQDN:

```bash
FQDN=$(az container show \
  --resource-group NOME_RESOURCE_GROUP \
  --name aci-obsapp-ud13 \
  --query ipAddress.fqdn \
  -o tsv)

echo $FQDN
```

Eseguire i test:

```bash
curl http://$FQDN:8000/
curl http://$FQDN:8000/health
curl http://$FQDN:8000/time
curl -X POST http://$FQDN:8000/echo \
  -H 'Content-Type: application/json' \
  -d '{"lab":"UD13","deploy":"aci"}'
curl http://$FQDN:8000/error
curl http://$FQDN:8000/rotta-inesistente
```

Risultati attesi:

| Endpoint | Esito atteso |
|---|---|
| `/` | 200 |
| `/health` | 200 |
| `/time` | 200 |
| `/echo` | 200 |
| `/error` | 500 simulato |
| rotta inesistente | 404 |

---

# 19. Lettura log cloud

```bash
az container logs \
  --resource-group NOME_RESOURCE_GROUP \
  --name aci-obsapp-ud13
```

Nei log devono comparire record JSON con campi come:

```text
timestamp
level
request_id
method
path
status
latency_ms
app
version
environment
```

---

# 20. Evidenze da produrre

Creare:

```bash
code docs/evidence_ud13.md
```

Usare il template disponibile in:

```text
UD13/docs/template_evidence_ud13.md
```

---

# 21. Cleanup minimo

A fine laboratorio, se indicato dal docente, eliminare ACI:

```bash
az container delete \
  --resource-group NOME_RESOURCE_GROUP \
  --name aci-obsapp-ud13 \
  --yes
```

Non eliminare ACR salvo indicazione esplicita del docente.
