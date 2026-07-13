# UD16 - LAB autonomo
## Nuova revisione FE/BE su Azure Container Apps

## Scenario

La pipeline UD16 funziona. Ora dobbiamo dimostrare che sappiamo produrre una nuova revisione applicativa usando un nuovo tag immagine.

## Obiettivo

Usare un tag immagine diverso, aggiornare almeno una delle due Container Apps e dimostrare che ACA ha creato una nuova revisione.

## Attività

1. Identificare un altro tag disponibile in ACR, oppure generarlo rilanciando la pipeline UD15.
2. Aggiornare `imageTag` nella pipeline UD16.
3. Eseguire la pipeline UD16.
4. Verificare che backend e frontend siano ancora raggiungibili.
5. Verificare le revisioni.
6. Leggere i log.
7. Compilare evidenze.

## Comandi utili

```bash
az acr repository show-tags --name <ACR> --repository backend -o table
az acr repository show-tags --name <ACR> --repository frontend -o table
```

Revisioni:

```bash
az containerapp revision list   --resource-group <RG>   --name ca-obs-ud16-frontend   -o table
```

## Evidenza richiesta

| Evidenza | Obbligatoria |
|---|---|
| Vecchio tag | sì |
| Nuovo tag | sì |
| Run pipeline UD16 | sì |
| Nuova revisione frontend o backend | sì |
| Test `/ready` | sì |
| Log runtime | sì |
| Spiegazione tecnica | sì |

## Risposta finale attesa

> Ho aggiornato il tag immagine usato da Azure Container Apps. L'aggiornamento ha generato una nuova revisione. Ho verificato che il frontend risponda e che `/ready` confermi la comunicazione con il backend.
