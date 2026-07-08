# UD13 - Guida operativa
## Service connection, GitHub, ACR, ACI e troubleshooting

---

# 1. Scopo della guida

Questa guida supporta il laboratorio UD13 nei passaggi più delicati:

- autorizzazione GitHub in Azure DevOps;
- creazione Azure Resource Manager service connection;
- creazione/verifica ACR;
- deploy su ACI;
- lettura log;
- troubleshooting.

---

# 2. Repository GitHub non visibile in Azure DevOps

Possibili cause:

| Problema | Verifica / azione |
|---|---|
| GitHub App non autorizzata | Riautorizzare Azure Pipelines su GitHub |
| Fork personale non incluso | Installare/autorizzare Azure Pipelines sull'account personale |
| Repository in organizzazione docente | Verificare permessi del partecipante sul repository |
| Repository appena creato | Refresh della connessione o nuova service connection |
| Account GitHub sbagliato | Logout/login nel browser e controllo account attivo |

Indicazione pratica: se il repository è un fork personale, Azure DevOps deve essere autorizzato a leggere quel fork, non solo il repository sorgente dell'organizzazione docente.

---

# 3. Creazione service connection Azure

Nel progetto Azure DevOps:

```text
Project settings
-> Service connections
-> New service connection
-> Azure Resource Manager
```

Valori consigliati:

| Campo | Valore suggerito |
|---|---|
| Nome | `sc-obs-azure-rg` |
| Scope | Subscription o Resource Group indicato dal docente |
| Descrizione | Connessione Azure per lab Observability |

Controllo fondamentale: il nome nel file YAML deve coincidere con il nome della service connection.

---

# 4. Verifiche ACR

Verificare ACR:

```bash
az acr show \
  --name NOME_ACR_UNIVOCO \
  --resource-group NOME_RESOURCE_GROUP
```

Login manuale per controllo:

```bash
az acr login --name NOME_ACR_UNIVOCO
```

Lista repository:

```bash
az acr repository list \
  --name NOME_ACR_UNIVOCO \
  -o table
```

Lista tag:

```bash
az acr repository show-tags \
  --name NOME_ACR_UNIVOCO \
  --repository obsapp-ud13 \
  -o table
```

---

# 5. Admin account ACR

Nel laboratorio si abilita l'admin account ACR:

```bash
az acr update \
  --name NOME_ACR_UNIVOCO \
  --admin-enabled true
```

Verifica credenziali:

```bash
az acr credential show --name NOME_ACR_UNIVOCO
```

Nota docente/partecipante: è una semplificazione di laboratorio, non una best practice di produzione.

---

# 6. Verifiche ACI

Stato container:

```bash
az container show \
  --resource-group NOME_RESOURCE_GROUP \
  --name aci-obsapp-ud13 \
  --query "{state:instanceView.state,fqdn:ipAddress.fqdn,ports:ipAddress.ports}" \
  -o json
```

Log:

```bash
az container logs \
  --resource-group NOME_RESOURCE_GROUP \
  --name aci-obsapp-ud13
```

Eliminazione container:

```bash
az container delete \
  --resource-group NOME_RESOURCE_GROUP \
  --name aci-obsapp-ud13 \
  --yes
```

---

# 7. Troubleshooting rapido

## Pipeline fallisce su service connection

Possibili cause:

- nome service connection diverso da quello nel YAML;
- service connection non autorizzata per la pipeline;
- permessi insufficienti sulla subscription o sul Resource Group.

Controllare:

```yaml
azureServiceConnection: 'sc-obs-azure-rg'
```

## Pipeline fallisce su `az acr login`

Possibili cause:

- nome ACR errato;
- ACR non esistente;
- permessi insufficienti della service connection.

Controllare:

```bash
az acr show --name NOME_ACR_UNIVOCO --resource-group NOME_RESOURCE_GROUP
```

## Pipeline fallisce su `docker build`

Possibili cause:

- path sbagliato nel repository;
- file `Dockerfile` mancante;
- file `requirements.txt` mancante;
- errore sintattico in `src/app.py`.

Nel template UD13 la build usa:

```bash
docker build -t ${FULL_IMAGE_NAME} work/UD13
```

Quindi i file devono trovarsi realmente in `work/UD13`.

## Deploy ACI fallisce per DNS name

Possibile causa: il valore `aciDnsName` è già usato da qualcun altro nella region.

Soluzione: cambiare nel YAML:

```yaml
aciDnsName: 'obsapp-ud13-nomeunivoco'
```

Usare un valore personale e univoco.

## App deployata ma `curl` non risponde

Possibili cause:

- container ancora in avvio;
- porta errata;
- container terminato;
- FQDN errato;
- errore runtime.

Verificare:

```bash
az container show \
  --resource-group NOME_RESOURCE_GROUP \
  --name aci-obsapp-ud13 \
  --query "{state:instanceView.state,events:instanceView.events}" \
  -o json

az container logs \
  --resource-group NOME_RESOURCE_GROUP \
  --name aci-obsapp-ud13
```

## `az container logs` non mostra richieste recenti

Possibili cause:

- non hai generato traffico dopo il deploy;
- stai interrogando il container sbagliato;
- l'app non è partita.

Genera traffico:

```bash
curl http://FQDN:8000/health
curl http://FQDN:8000/error
```

Poi ripeti `az container logs`.

---

# 8. Checklist prima di chiedere supporto

Prima di chiedere supporto al docente, verificare:

- repository GitHub aggiornato;
- file `work/UD13/azure-pipelines.yml` presente su GitHub;
- nome service connection corretto;
- Resource Group corretto;
- nome ACR corretto;
- admin account ACR abilitato;
- DNS label ACI univoca;
- log della pipeline letti almeno fino al punto di errore.
