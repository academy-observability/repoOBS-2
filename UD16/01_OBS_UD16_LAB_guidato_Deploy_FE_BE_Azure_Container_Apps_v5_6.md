# UD16 - LAB guidato
## Deploy FE/BE su Azure Container Apps

## 0. Obiettivo

Portare su Azure Container Apps le due immagini prodotte in UD15:

```text
ACR/backend:<tag>
ACR/frontend:<tag>
```

Alla fine avremo:

```text
https://<backend-fqdn>
https://<frontend-fqdn>
```

e il frontend dovrà riuscire a chiamare il backend usando `BACKEND_URL`.

---

## 1. Prerequisiti

Devono essere già disponibili:

- repository GitHub collegato ad Azure DevOps;
- Azure DevOps Project;
- service connection Azure Resource Manager, ad esempio `sc-obs-azure-rg`;
- Resource Group;
- Azure Container Registry;
- immagini `backend` e `frontend` pubblicate in ACR dalla UD15;
- Azure CLI funzionante.

Verifica account:

```bash
az account show --output table
```

---

## 2. Preparazione cartella UD16

Nel repository:

```bash
mkdir -p work/UD16/docs work/UD16/evidence work/UD16/logs
cd work/UD16
```

Copiare il template pipeline:

```bash
cp ../../UD16/templates/azure-pipelines-ud16-deploy-aca.yml ./azure-pipelines.yml
```

Se il materiale è già stato copiato nel repository, usare direttamente:

```bash
code work/UD16/azure-pipelines.yml
```

---

## 3. Identificare i tag immagini prodotti in UD15

Impostare i nomi:

```bash
RG="NOME_RESOURCE_GROUP"
ACR_NAME="NOME_ACR"
```

Mostrare i tag backend:

```bash
az acr repository show-tags   --name "$ACR_NAME"   --repository backend   -o table
```

Mostrare i tag frontend:

```bash
az acr repository show-tags   --name "$ACR_NAME"   --repository frontend   -o table
```

Scegliere un tag coerente, preferibilmente il `Build.BuildId` della pipeline UD15.

Annotarlo:

```text
IMAGE_TAG=<tag>
```

---

## 4. Aggiornare le variabili della pipeline

Aprire:

```text
work/UD16/azure-pipelines.yml
```

Aggiornare almeno:

```yaml
azureServiceConnection: 'sc-obs-azure-rg'
resourceGroupName: 'NOME_RESOURCE_GROUP'
location: 'westeurope'
acrName: 'NOME_ACR'
imageTag: 'INSERIRE_BUILD_ID_UD15'
backendImageName: 'backend'
frontendImageName: 'frontend'
```

Nomi consigliati:

```yaml
acaEnvironmentName: 'acaenv-obs-ud16'
backendContainerAppName: 'ca-obs-ud16-backend'
frontendContainerAppName: 'ca-obs-ud16-frontend'
```

---

## 5. Commit e push

```bash
git status
git add work/UD16
git commit -m "UD16 - deploy FE BE su Azure Container Apps"
git push
```

Punto importante:

```text
Azure DevOps legge il file YAML dal repository GitHub. Se il file non è stato pushato, la pipeline non vede la modifica.
```

---

## 6. Creare la pipeline in Azure DevOps

Nel portale Azure DevOps:

```text
Pipelines
-> Create Pipeline
-> GitHub
-> repository del corso
-> Existing Azure Pipelines YAML file
-> work/UD16/azure-pipelines.yml
-> Run
```

Nome consigliato:

```text
UD16-fe-be-deploy-aca
```

---

## 7. Osservare gli stage

La pipeline deve mostrare:

```text
ValidateInputs
DeployEnvironment
DeployBackend
DeployFrontend
VerifyDeploy
```

| Stage | Cosa controllare |
|---|---|
| ValidateInputs | Resource Group, ACR, tag immagini |
| DeployEnvironment | creazione/verifica ACA Environment |
| DeployBackend | deploy immagine backend e FQDN backend |
| DeployFrontend | deploy immagine frontend con `BACKEND_URL` |
| VerifyDeploy | test HTTP su frontend e ready check |

---

## 8. Verifica da Azure CLI

Impostare variabili:

```bash
RG="NOME_RESOURCE_GROUP"
BACKEND_APP="ca-obs-ud16-backend"
FRONTEND_APP="ca-obs-ud16-frontend"
```

Verificare backend:

```bash
az containerapp show   --resource-group "$RG"   --name "$BACKEND_APP"   --query "{name:name,state:properties.provisioningState,fqdn:properties.configuration.ingress.fqdn,revision:properties.latestRevisionName}"   -o json
```

Verificare frontend:

```bash
az containerapp show   --resource-group "$RG"   --name "$FRONTEND_APP"   --query "{name:name,state:properties.provisioningState,fqdn:properties.configuration.ingress.fqdn,revision:properties.latestRevisionName}"   -o json
```

---

## 9. Test manuale HTTP

Recuperare FQDN frontend:

```bash
FRONTEND_FQDN=$(az containerapp show   --resource-group "$RG"   --name "$FRONTEND_APP"   --query properties.configuration.ingress.fqdn   -o tsv)

echo "https://$FRONTEND_FQDN"
```

Test:

```bash
curl -i "https://$FRONTEND_FQDN/health"
curl -i "https://$FRONTEND_FQDN/ready"
curl -i "https://$FRONTEND_FQDN/"
```

`/ready` è il test più importante perché dimostra che il frontend riesce a parlare con il backend.

---

## 10. Revisioni

Mostrare revisioni backend:

```bash
az containerapp revision list   --resource-group "$RG"   --name "$BACKEND_APP"   -o table
```

Mostrare revisioni frontend:

```bash
az containerapp revision list   --resource-group "$RG"   --name "$FRONTEND_APP"   -o table
```

Da osservare:

- nome revisione;
- stato;
- traffico;
- immagine associata.

---

## 11. Log

Backend:

```bash
az containerapp logs show   --resource-group "$RG"   --name "$BACKEND_APP"   --follow false   --format text
```

Frontend:

```bash
az containerapp logs show   --resource-group "$RG"   --name "$FRONTEND_APP"   --follow false   --format text
```

Se i log sono pochi, generare traffico:

```bash
for i in {1..10}; do
  curl -s "https://$FRONTEND_FQDN/ready" >/dev/null
  sleep 1
done
```

---

## 12. Evidenze

Compilare:

```text
docs/template_evidence_ud16.md
```

E produrre almeno:

- screenshot pipeline con stage verdi;
- output tag ACR;
- FQDN backend;
- FQDN frontend;
- output `/health` e `/ready`;
- lista revisioni;
- log frontend/backend.

---

## 13. Frase finale attesa

> In UD16 abbiamo distribuito su Azure Container Apps le due immagini prodotte in UD15. Il backend e il frontend sono due Container Apps distinte. Il frontend usa la variabile `BACKEND_URL` per raggiungere il backend. La pipeline crea o aggiorna environment, backend, frontend ed esegue una verifica HTTP finale.
