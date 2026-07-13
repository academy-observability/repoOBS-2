# UD16 - Guida operativa
## Azure Container Apps, revisioni, log e BACKEND_URL

## 1. Verifica provider Azure

Se il comando `az containerapp` non funziona:

```bash
az extension add --name containerapp --upgrade
```

Se la subscription non ha provider registrati:

```bash
az provider register --namespace Microsoft.App
az provider register --namespace Microsoft.OperationalInsights
```

Attendere la registrazione se necessario.

## 2. Verifica immagini ACR

```bash
az acr repository list --name <ACR> -o table
az acr repository show-tags --name <ACR> --repository backend -o table
az acr repository show-tags --name <ACR> --repository frontend -o table
```

Errore tipico:

```text
repository not found
```

Possibili cause:

- pipeline UD15 non eseguita;
- nomi repository diversi da `backend`/`frontend`;
- ACR sbagliato;
- tag immagine inesistente.

## 3. Verifica Container Apps Environment

```bash
az containerapp env show   --resource-group <RG>   --name acaenv-obs-ud16   -o table
```

Se non esiste, la pipeline lo crea.

## 4. Verifica ingress e FQDN

```bash
az containerapp show   --resource-group <RG>   --name ca-obs-ud16-frontend   --query properties.configuration.ingress   -o json
```

Il FQDN si legge con:

```bash
az containerapp show   --resource-group <RG>   --name ca-obs-ud16-frontend   --query properties.configuration.ingress.fqdn   -o tsv
```

## 5. Verifica BACKEND_URL

```bash
az containerapp show   --resource-group <RG>   --name ca-obs-ud16-frontend   --query properties.template.containers[0].env   -o json
```

Cercare:

```text
BACKEND_URL=https://<backend-fqdn>
```

## 6. Revisioni

```bash
az containerapp revision list   --resource-group <RG>   --name ca-obs-ud16-frontend   -o table
```

Una nuova revisione può essere creata quando cambiano:

- immagine;
- variabili ambiente;
- configurazione del container;
- ingress o parametri rilevanti.

## 7. Log

```bash
az containerapp logs show   --resource-group <RG>   --name ca-obs-ud16-frontend   --follow false   --format text
```

Per stream live:

```bash
az containerapp logs show   --resource-group <RG>   --name ca-obs-ud16-frontend   --follow true   --format text
```

## 8. Errori frequenti

| Sintomo | Causa probabile | Azione |
|---|---|---|
| Pipeline non trova immagine | tag errato | verificare tag ACR |
| Container App non parte | porta target sbagliata | controllare `PORT` e `target-port` |
| `/health` ok ma `/ready` ko | frontend non raggiunge backend | controllare `BACKEND_URL` |
| FQDN vuoto | ingress non abilitato | controllare `--ingress external` |
| Log vuoti | traffico assente | generare curl |
| Nuova revisione non chiara | immagine/tag invariato | cambiare tag o env var |

## 9. Regola pratica

Quando qualcosa fallisce, seguire sempre questa sequenza:

```text
ACR tag -> ACA environment -> backend -> backend FQDN -> frontend BACKEND_URL -> frontend /ready -> revisioni -> log
```
