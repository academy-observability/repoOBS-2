# Evidence UD15

## 1. Obiettivo compreso
Spiego con parole mie perché in UD15 passiamo da app singola a FE/BE.

## 2. Struttura progetto
Incollo o descrivo la struttura:

```text
frontend/
backend/
azure-pipelines.yml
```

## 3. Build locale
Riporto i comandi:

```bash
docker build -t backend:ud15 ./backend
docker build -t frontend:ud15 ./frontend
```

## 4. Test locale backend
Incollo output di:

- `GET /health`
- `GET /version`
- `GET /work`

## 5. Test locale frontend
Incollo output di:

- `GET /health`
- `GET /ready`
- `GET /version`
- `GET /demo`

## 6. Log separati
Incollo alcune righe di:

```bash
docker logs be-ud15
docker logs fe-ud15
```

## 7. Pipeline Azure DevOps
Indico:

- nome pipeline;
- run ID / Build ID;
- stage eseguiti;
- esito finale.

## 8. ACR
Incollo output di:

```bash
az acr repository list --name NOME_ACR -o table
az acr repository show-tags --name NOME_ACR --repository backend -o table
az acr repository show-tags --name NOME_ACR --repository frontend -o table
```

## 9. Differenza frontend/backend
Spiego perché le due immagini non sono intercambiabili.

## 10. Problemi incontrati
Descrivo eventuali errori e come li ho risolti.
