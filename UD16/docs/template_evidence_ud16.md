# Evidence UD16 - Deploy FE/BE su Azure Container Apps

## 1. Dati ambiente

| Campo | Valore |
|---|---|
| Resource Group | |
| ACR | |
| ACA Environment | |
| Backend Container App | |
| Frontend Container App | |
| Tag immagini UD15 | |

## 2. Immagini usate

```bash
az acr repository show-tags --name <ACR> --repository backend -o table
az acr repository show-tags --name <ACR> --repository frontend -o table
```

Annotare il tag usato:

```text
<tag>
```

## 3. Pipeline UD16

| Stage | Esito | Evidenza |
|---|---|---|
| ValidateInputs | | |
| DeployEnvironment | | |
| DeployBackend | | |
| DeployFrontend | | |
| VerifyDeploy | | |

## 4. URL finali

| Servizio | URL |
|---|---|
| Backend | |
| Frontend | |

## 5. Test HTTP

```bash
curl -i https://<frontend-fqdn>/health
curl -i https://<frontend-fqdn>/ready
curl -i https://<frontend-fqdn>/
```

## 6. Revisioni

```bash
az containerapp revision list --resource-group <RG> --name <APP> -o table
```

## 7. Log

```bash
az containerapp logs show --resource-group <RG> --name <APP> --follow false --format text
```

## 8. Spiegazione finale

Scrivere 5-8 righe:

- dove sono le immagini;
- dove vengono eseguiti i container;
- come il frontend raggiunge il backend;
- perché ACA crea revisioni;
- cosa dimostra lo smoke test.
