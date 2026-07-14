# OBS UD17 - Laboratorio guidato
# Observability Azure post-deploy sull'app Catalogo prodotti

## Obiettivo del laboratorio

In questo laboratorio rendiamo osservabile in cloud la release **Catalogo prodotti** distribuita su Azure Container Apps dopo la change request post-UD16.

Alla fine dovremo poter mostrare:

```text
Frontend ACA products osservabile
Backend ACA products osservabile
Application Insights collegato
Log Analytics interrogabile con KQL
Traffico normale / lento / errore
Correlazione FE → BE
Decision record tecnico
```

La UD non crea da zero l'applicazione. Parte da un'app FE/BE già rilasciata o aggiornabile tramite pipeline: backend interno, frontend pubblico, immagini in ACR, Container Apps esistenti.

## Task 1 - Verificare lo stato iniziale

Prima di modificare qualsiasi cosa, annotiamo lo stato reale.

```bash
az account show
az group show --name NOME_RESOURCE_GROUP
az acr show --name NOME_ACR --resource-group NOME_RESOURCE_GROUP
```

Verifichiamo le Container Apps:

```bash
az containerapp show \
  --resource-group NOME_RESOURCE_GROUP \
  --name NOME_BACKEND_CONTAINER_APP \
  --query "{name:name,fqdn:properties.configuration.ingress.fqdn,latestRevision:properties.latestRevisionName,ingress:properties.configuration.ingress.external}" \
  -o json

az containerapp show \
  --resource-group NOME_RESOURCE_GROUP \
  --name NOME_FRONTEND_CONTAINER_APP \
  --query "{name:name,fqdn:properties.configuration.ingress.fqdn,latestRevision:properties.latestRevisionName,ingress:properties.configuration.ingress.external}" \
  -o json
```

Il frontend deve avere ingress esterno. Il backend può avere ingress interno.

## Task 2 - Verificare la release products esistente

Recuperiamo il FQDN frontend:

```bash
FRONTEND_FQDN=$(az containerapp show \
  --resource-group NOME_RESOURCE_GROUP \
  --name NOME_FRONTEND_CONTAINER_APP \
  --query properties.configuration.ingress.fqdn \
  -o tsv)

FRONTEND_URL="https://$FRONTEND_FQDN"
echo "$FRONTEND_URL"
```

Eseguiamo i test applicativi:

```bash
curl -i "$FRONTEND_URL/health"
curl -i "$FRONTEND_URL/ready"
curl -i "$FRONTEND_URL/version"
curl -i "$FRONTEND_URL/products"
curl -i "$FRONTEND_URL/"
```

Risultati attesi:

| Endpoint | Risultato atteso |
|---|---|
| `/health` | HTTP 200, frontend vivo |
| `/ready` | HTTP 200, frontend riesce a parlare con backend |
| `/version` | versione o BuildId della release |
| `/products` | JSON con prodotti |
| `/` | pagina HTML con “Catalogo prodotti” |

Se questi test falliscono, non ha senso passare ad Application Insights. Prima va corretta la release.

## Task 3 - Preparare la cartella UD17 nel repository

Dalla radice del repository:

```bash
mkdir -p work/UD17/src
cp -r UD17/src/app_products_observable work/UD17/src/app_products_observable
cp UD17/templates/azure-pipelines-ud17-observability-products-v5_7_1.yml work/UD17/azure-pipelines.yml
mkdir -p work/UD17/docs work/UD17/evidence work/UD17/logs work/UD17/scripts
cp UD17/docs/template_evidence_ud17_products.md work/UD17/docs/evidence_ud17.md
cp UD17/scripts/generate_traffic_products.sh work/UD17/scripts/generate_traffic_products.sh
chmod +x work/UD17/scripts/generate_traffic_products.sh
```

La struttura attesa è:

```text
work/UD17/
├── src/app_products_observable/
│   ├── backend/
│   └── frontend/
├── azure-pipelines.yml
├── scripts/generate_traffic_products.sh
└── docs/evidence_ud17.md
```

## Task 4 - Verificare sintassi e build locale minima

```bash
python3 -m compileall -q \
  work/UD17/src/app_products_observable/backend \
  work/UD17/src/app_products_observable/frontend
```

Build immagini locali:

```bash
docker build -t obs-ud17-products-backend:local work/UD17/src/app_products_observable/backend
docker build -t obs-ud17-products-frontend:local work/UD17/src/app_products_observable/frontend
```

Questa verifica non sostituisce la pipeline. Serve a intercettare errori banali prima di occupare un run Azure DevOps.

## Task 5 - Creare o verificare Application Insights

Application Insights deve essere workspace-based e collegato al Log Analytics Workspace del corso.

Da portale:

```text
Azure Portal
→ Application Insights
→ Create
→ Resource Group del corso
→ Workspace-based
→ Log Analytics Workspace del corso
```

Da CLI, se preferiamo:

```bash
LAW_ID=$(az monitor log-analytics workspace show \
  --resource-group NOME_RESOURCE_GROUP \
  --workspace-name NOME_LOG_ANALYTICS_WORKSPACE \
  --query id \
  -o tsv)

az monitor app-insights component create \
  --app NOME_APPINSIGHTS \
  --location westeurope \
  --resource-group NOME_RESOURCE_GROUP \
  --application-type web \
  --workspace "$LAW_ID"
```

Recuperiamo la connection string:

```bash
az monitor app-insights component show \
  --app NOME_APPINSIGHTS \
  --resource-group NOME_RESOURCE_GROUP \
  --query connectionString \
  -o tsv
```

Questa stringa non va committata nel repository.

## Task 6 - Configurare la variabile segreta in Azure DevOps

Nella pipeline Azure DevOps UD17 aggiungiamo una variabile segreta:

```text
APPLICATIONINSIGHTS_CONNECTION_STRING
```

Valore: connection string di Application Insights.

La pipeline YAML usa poi:

```yaml
appInsightsConnectionString: '$(APPLICATIONINSIGHTS_CONNECTION_STRING)'
```

## Task 7 - Personalizzare il file YAML

Apriamo:

```text
work/UD17/azure-pipelines.yml
```

Aggiorniamo i valori reali:

```yaml
azureServiceConnection: 'NOME_SERVICE_CONNECTION'
resourceGroupName: 'NOME_RESOURCE_GROUP'
acrName: 'NOME_ACR'
backendContainerAppName: 'NOME_ACA_BACKEND'
frontendContainerAppName: 'NOME_ACA_FRONTEND'
```

I repository immagini restano:

```yaml
backendRepository: 'obsapp-products-backend'
frontendRepository: 'obsapp-products-frontend'
```

La pipeline userà:

```yaml
imageTag: '$(Build.BuildId)'
```

Quindi backend e frontend avranno lo stesso tag numerico, ma in repository distinti.

## Task 8 - Commit e push

```bash
git status
git add work/UD17
git commit -m "UD17 - observability cloud catalogo prodotti"
git push
```

## Task 9 - Creare o aggiornare la pipeline Azure DevOps

Dal portale Azure DevOps:

```text
Pipelines
→ New pipeline
→ GitHub
→ repository del partecipante
→ Existing Azure Pipelines YAML file
→ Branch main
→ Path /work/UD17/azure-pipelines.yml
→ Save
```

Nome consigliato:

```text
UD17 - Observability cloud products ACA
```

La pipeline ha `trigger: none`, quindi l'avvio è manuale.

## Task 10 - Eseguire la pipeline e leggere gli stage

La pipeline contiene quattro stage:

```text
1. Validate
2. BuildAndPush
3. DeployBackend
4. DeployFrontendAndVerify
```

Durante la run annotiamo:

| Dato | Dove lo troviamo |
|---|---|
| BuildId | intestazione run pipeline |
| tag backend | log BuildAndPush / ACR |
| tag frontend | log BuildAndPush / ACR |
| revisione backend | stage DeployBackend |
| revisione frontend | stage DeployFrontendAndVerify |
| frontend URL | log stage 4 |
| backend URL | log stage 4 |

## Task 11 - Verificare ACR e revisioni ACA

ACR:

```bash
az acr repository show-tags \
  --name NOME_ACR \
  --repository obsapp-products-backend \
  --orderby time_desc \
  --top 5 \
  -o table

az acr repository show-tags \
  --name NOME_ACR \
  --repository obsapp-products-frontend \
  --orderby time_desc \
  --top 5 \
  -o table
```

Revisioni ACA:

```bash
az containerapp revision list \
  --resource-group NOME_RESOURCE_GROUP \
  --name NOME_BACKEND_CONTAINER_APP \
  --query '[].{revision:name,active:properties.active,health:properties.healthState,image:properties.template.containers[0].image}' \
  -o table

az containerapp revision list \
  --resource-group NOME_RESOURCE_GROUP \
  --name NOME_FRONTEND_CONTAINER_APP \
  --query '[].{revision:name,active:properties.active,health:properties.healthState,image:properties.template.containers[0].image}' \
  -o table
```

## Task 12 - Generare traffico osservabile

Recuperiamo il frontend URL e lanciamo traffico:

```bash
FRONTEND_URL="https://$(az containerapp show \
  --resource-group NOME_RESOURCE_GROUP \
  --name NOME_FRONTEND_CONTAINER_APP \
  --query properties.configuration.ingress.fqdn \
  -o tsv)"

bash work/UD17/scripts/generate_traffic_products.sh "$FRONTEND_URL"
```

Lo script genera richieste normali, lente e in errore. Dopo la generazione traffico, attendere alcuni minuti prima di interrogare Application Insights e Log Analytics.

## Task 13 - Verifiche manuali con request id esplicito

Creiamo un request id leggibile:

```bash
RID="ud17-manual-$(date +%s)"
echo "$RID"
```

Eseguiamo:

```bash
curl -i -H "X-Request-Id: $RID" "$FRONTEND_URL/products"
curl -i -H "X-Request-Id: $RID-slow" "$FRONTEND_URL/products/slow"
curl -i -H "X-Request-Id: $RID-error" "$FRONTEND_URL/products/error"
```

Salviamo il request id nell'evidence. Ci servirà nelle query su `ContainerAppConsoleLogs_CL`.

## Task 14 - Leggere i log runtime ACA

```bash
az containerapp logs show \
  --resource-group NOME_RESOURCE_GROUP \
  --name NOME_FRONTEND_CONTAINER_APP \
  --tail 100

az containerapp logs show \
  --resource-group NOME_RESOURCE_GROUP \
  --name NOME_BACKEND_CONTAINER_APP \
  --tail 100
```

Cerchiamo:

- `products-frontend`;
- `products-backend`;
- `request_id`;
- path `/products` e `/api/products`;
- status 200 e 500;
- latenza su `/products/slow`.

## Task 15 - Eseguire query KQL

Apriamo:

```text
Application Insights → Logs
```

oppure:

```text
Log Analytics Workspace → Logs
```

Usiamo il file:

```text
UD17/kql/ud17_products_observability_queries.kql
```

Le prime tre query da eseguire sono:

```kql
AppRequests
| where TimeGenerated > ago(2h)
| where Url has "/products" or Name has "/products"
| project TimeGenerated, AppRoleName, Name, Url, ResultCode, Success, DurationMs, OperationId
| order by TimeGenerated desc
```

```kql
AppDependencies
| where TimeGenerated > ago(2h)
| where Name has "/api/products" or Data has "/api/products" or Target has "backend"
| project TimeGenerated, AppRoleName, Target, Name, Data, ResultCode, Success, DurationMs, OperationId
| order by TimeGenerated desc
```

```kql
ContainerAppConsoleLogs_CL
| where TimeGenerated > ago(2h)
| where Log_s has "request_id"
| extend j=parse_json(Log_s)
| project TimeGenerated, ContainerAppName_s, service=tostring(j.service), path=tostring(j.path), status=toint(j.status), latency_ms=todouble(j.latency_ms), request_id=tostring(j.request_id), trace_id=tostring(j.trace_id)
| order by TimeGenerated desc
```

## Task 16 - Analisi guidata di tre casi

### Caso A - Richiesta normale

Usare `/products`.

Annotare:

- request frontend;
- dependency FE → BE;
- request backend;
- log frontend;
- log backend;
- durata normale.

### Caso B - Richiesta lenta

Usare `/products/slow`.

Domande:

- la request è riuscita?
- quanto dura?
- la lentezza si vede come dependency?
- il backend conferma latenza maggiore?

### Caso C - Errore controllato

Usare `/products/error`.

Domande:

- quale status code vediamo?
- l'errore compare in AppRequests?
- compare nei log container?
- riesco a collegare frontend e backend con request_id o OperationId?

## Task 17 - Compilare evidence e decision record

Nel file:

```text
work/UD17/docs/evidence_ud17.md
```

compiliamo:

- dati ambiente;
- BuildId;
- endpoint testati;
- query KQL;
- evidenze per richiesta normale;
- evidenze per richiesta lenta;
- evidenze per errore controllato;
- decision record.

Esempio decision record:

```text
Osservazione: /products/slow risponde 200 ma impiega più di 2 secondi.
Evidenza: AppDependencies mostra dependency verso /api/products/slow con DurationMs elevato.
Ipotesi: la latenza nasce nel backend.
Verifica: ContainerAppConsoleLogs_CL sul backend mostra path /api/products/slow con latency_ms elevata.
Decisione: proporre alert su p95 latency o ottimizzazione endpoint.
Limite: test svolto con traffico artificiale e finestra breve.
```

## Task 18 - Frase finale da saper dire

> Ho osservato in Azure una release FE/BE del Catalogo prodotti. Ho generato traffico normale, lento e in errore. Ho usato Application Insights per leggere request e dependency, Log Analytics per leggere i log container, e KQL per correlare frontend, backend, request id, durata e status code. Posso spiegare dove nasce una lentezza o un errore usando evidenze tecniche.
