# UD14 - Laboratorio guidato
## Pipeline multistage con ACR, ACI e smoke test automatico

---

# 1. Obiettivo del laboratorio

In questo laboratorio costruiremo una pipeline Azure DevOps più ordinata rispetto alla UD13.

Il flusso sarà:

```text
GitHub
  -> Azure DevOps Pipeline
      -> ValidateRepository
      -> BuildAndPush
      -> DeployToACI
      -> SmokeTest
  -> ACR
  -> ACI
```

Alla fine dovremo dimostrare che:

- la pipeline valida i file minimi;
- costruisce l'immagine Docker;
- pubblica l'immagine in ACR;
- distribuisce il container su ACI;
- verifica automaticamente gli endpoint principali;
- permette di leggere i log del container cloud.

---

# 2. Prerequisiti

Prima di iniziare devono essere disponibili:

- repository GitHub usato nel percorso;
- progetto Azure DevOps creato;
- service connection Azure Resource Manager funzionante;
- Resource Group Azure;
- Azure Container Registry esistente;
- possibilità di creare un container ACI;
- Azure CLI locale per le verifiche finali;
- conoscenza base di Docker locale dalla UD12;
- primo deploy automatico già sperimentato nella UD13.

Valori da preparare:

```text
NOME_RESOURCE_GROUP=
NOME_ACR=
NOME_SERVICE_CONNECTION=
NOME_ACI=
DNS_LABEL_UNIVOCO=
```

---

# 3. Preparazione cartella di lavoro

Nel repository locale creiamo la cartella della UD14.

```bash
mkdir -p work/UD14/src
mkdir -p work/UD14/docs
cd work/UD14
```

Se vogliamo ripartire dall'app della UD13, copiamo i file:

```bash
cp ../UD13/src/app.py src/app.py
cp ../UD13/requirements.txt .
cp ../UD13/Dockerfile .
cp ../UD13/.dockerignore .
```

In alternativa possiamo usare i file presenti nella cartella `src/app_base` del pacchetto UD14.

La struttura attesa è:

```text
work/UD14/
├── src/
│   └── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── azure-pipelines.yml
└── docs/
```

---

# 4. Verifica locale minima

Prima di passare alla pipeline verifichiamo la sintassi Python:

```bash
python3 -m py_compile src/app.py
```

Se il comando non produce output, la sintassi è corretta.

Facciamo anche una build locale rapida:

```bash
docker build -t obsapp-ud14:local .
```

Test opzionale:

```bash
docker run --rm -p 8000:8000 obsapp-ud14:local
```

Secondo terminale:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/
```

Interrompiamo il container con `CTRL+C`.

---

# 5. Verifica risorse Azure

Eseguiamo:

```bash
az account show
```

Verifichiamo il Resource Group:

```bash
az group show --name NOME_RESOURCE_GROUP
```

Verifichiamo ACR:

```bash
az acr show \
  --name NOME_ACR \
  --resource-group NOME_RESOURCE_GROUP
```

Verifichiamo che l'admin account ACR sia disponibile per il laboratorio:

```bash
az acr credential show --name NOME_ACR
```

Se il comando non restituisce credenziali, abilitiamo l'admin account:

```bash
az acr update \
  --name NOME_ACR \
  --admin-enabled true
```

Nota: questa è una semplificazione didattica. In ambienti più maturi si usano meccanismi di identità più robusti.

---

# 6. Creazione del file pipeline

Creiamo il file:

```bash
code azure-pipelines.yml
```

Inseriamo il contenuto del template:

```text
templates/azure-pipelines-ud14-multistage.yml
```

Poi modifichiamo le variabili iniziali:

```yaml
variables:
  azureServiceConnection: 'sc-obs-azure-rg'
  resourceGroupName: 'INSERIRE_NOME_RESOURCE_GROUP'
  acrName: 'INSERIRE_NOME_ACR'
  imageName: 'obsapp-ud14'
  imageTag: '$(Build.BuildId)'
  aciName: 'aci-obsapp-ud14'
  aciDnsName: 'obsapp-ud14-NOMEUNIVOCO'
  location: 'westeurope'
  containerPort: '8000'
  workDir: 'work/UD14'
```

Attenzione al valore `workDir`: deve indicare la posizione della UD14 nel repository.

---

# 7. Lettura della pipeline

Prima di fare commit leggiamo la pipeline.

Dobbiamo riconoscere questi stage:

```text
ValidateRepository
BuildAndPush
DeployToACI
SmokeTest
```

## 7.1 ValidateRepository

Controlla:

```text
src/app.py
requirements.txt
Dockerfile
.dockerignore
```

ed esegue:

```bash
python3 -m py_compile src/app.py
```

## 7.2 BuildAndPush

Costruisce e pubblica l'immagine:

```text
NOME_ACR.azurecr.io/obsapp-ud14:BUILD_ID
```

## 7.3 DeployToACI

Elimina l'eventuale container precedente e crea un nuovo container ACI.

## 7.4 SmokeTest

Recupera il FQDN e testa:

```text
/health
/
/time
/echo
```

---

# 8. Commit e push

Da root del repository o dalla cartella corretta:

```bash
git status
git add work/UD14
git commit -m "UD14 - pipeline multistage con smoke test"
git push
```

La pipeline Azure DevOps leggerà il file YAML dal repository GitHub. Se il file non viene pushato, Azure DevOps non potrà usarlo.

---

# 9. Creazione pipeline Azure DevOps

Nel portale Azure DevOps:

1. apriamo il progetto;
2. andiamo in **Pipelines**;
3. scegliamo **Create Pipeline**;
4. scegliamo **GitHub**;
5. selezioniamo il repository;
6. scegliamo **Existing Azure Pipelines YAML file**;
7. indichiamo il path:

```text
work/UD14/azure-pipelines.yml
```

Nome consigliato:

```text
UD14-obsapp-multistage-aci
```

Poi avviamo la pipeline.

---

# 10. Osservazione degli stage

Durante l'esecuzione apriamo ogni stage.

| Stage | Cosa osservare |
|---|---|
| ValidateRepository | file verificati e sintassi Python |
| BuildAndPush | `docker build`, `docker push`, tag ACR |
| DeployToACI | cancellazione/creazione ACI e FQDN |
| SmokeTest | chiamate HTTP agli endpoint principali |

La pipeline deve terminare con stato `Succeeded` solo se anche lo smoke test passa.

---

# 11. Verifica tag immagine in ACR

Da terminale locale:

```bash
az acr repository show-tags \
  --name NOME_ACR \
  --repository obsapp-ud14 \
  -o table
```

Annotiamo il tag corrispondente al `Build.BuildId` della pipeline.

---

# 12. Verifica ACI

Verifichiamo lo stato del container:

```bash
az container show \
  --resource-group NOME_RESOURCE_GROUP \
  --name NOME_ACI \
  --query "{state:instanceView.state,fqdn:ipAddress.fqdn,ports:ipAddress.ports}" \
  -o json
```

Recuperiamo il FQDN:

```bash
FQDN=$(az container show \
  --resource-group NOME_RESOURCE_GROUP \
  --name NOME_ACI \
  --query ipAddress.fqdn \
  -o tsv)

echo $FQDN
```

---

# 13. Verifica manuale degli endpoint

Anche se lo smoke test è automatico, facciamo una verifica manuale.

```bash
curl http://$FQDN:8000/
curl http://$FQDN:8000/health
curl http://$FQDN:8000/time
curl -X POST http://$FQDN:8000/echo \
  -H 'Content-Type: application/json' \
  -d '{"manual":"true","lab":"UD14"}'
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

# 14. Lettura log cloud

Generiamo alcune richieste:

```bash
curl http://$FQDN:8000/health
curl http://$FQDN:8000/error
```

Poi leggiamo i log:

```bash
az container logs \
  --resource-group NOME_RESOURCE_GROUP \
  --name NOME_ACI
```

Nei log cerchiamo:

```text
path
method
status
latency_ms
request_id
build_id
```

---

# 15. Evidenze richieste

Creiamo il file:

```bash
code docs/evidence_ud14.md
```

Struttura consigliata:

```md
# Evidence UD14

## 1. Obiettivo compreso
Spiego perché una pipeline multistage è migliore di una pipeline monolitica.

## 2. Prerequisiti verificati
Indico Resource Group, ACR, service connection e nome pipeline.

## 3. Struttura repository
Indico i file presenti in work/UD14.

## 4. Pipeline multistage
Descrivo i quattro stage:
- ValidateRepository
- BuildAndPush
- DeployToACI
- SmokeTest

## 5. Build ID e tag immagine
Indico il Build ID e il tag immagine pubblicato in ACR.

## 6. Verifica ACR
Incollo l'output di az acr repository show-tags.

## 7. Verifica ACI
Incollo stato, FQDN e porte del container.

## 8. Smoke test
Descrivo gli endpoint verificati dalla pipeline.

## 9. Test manuali
Incollo l'output degli endpoint principali.

## 10. Log cloud
Incollo alcune righe di az container logs e commento path, status, latency e build_id.

## 11. Problemi incontrati
Descrivo eventuali errori e come li ho risolti.
```

---

# 16. Cleanup

A fine laboratorio possiamo eliminare ACI:

```bash
az container delete \
  --resource-group NOME_RESOURCE_GROUP \
  --name NOME_ACI \
  --yes
```

Non eliminiamo ACR, salvo indicazione del docente, perché conserva le immagini prodotte nel percorso.

---

# 17. Conclusione

Abbiamo migliorato il rilascio automatico:

```text
prima: deploy automatico compatto
ora: pipeline multistage con verifica post-deploy
```

La differenza non è solo estetica. La pipeline UD14 rende il processo più leggibile, più controllabile e più facile da diagnosticare.
