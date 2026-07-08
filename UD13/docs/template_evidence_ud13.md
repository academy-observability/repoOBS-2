# Evidence UD13

## 1. Obiettivo compreso
Spiego con parole mie il flusso:
GitHub -> Azure DevOps -> ACR -> ACI.

## 2. Repository GitHub
Indico:
- nome repository;
- branch usato;
- path del file YAML.

## 3. Risorse Azure
Indico:
- Resource Group;
- nome ACR;
- nome ACI;
- DNS label/FQDN.

## 4. Service connection
Indico:
- nome della Azure Resource Manager service connection;
- eventuali problemi di autorizzazione risolti.

## 5. Pipeline
Riporto:
- nome pipeline;
- numero run;
- stato finale;
- passaggi principali osservati nei log.

## 6. Build e push immagine
Indico:
- nome immagine;
- tag generato;
- output essenziale di `az acr repository show-tags`.

## 7. Deploy su ACI
Riporto output essenziale di:

```bash
az container show
```

## 8. Test HTTP cloud
Incollo output di:
- GET `/`;
- GET `/health`;
- GET `/time`;
- POST `/echo`;
- GET `/error`;
- rotta inesistente.

## 9. Log cloud
Incollo alcune righe di:

```bash
az container logs
```

Commento almeno:
- `path`;
- `status`;
- `latency_ms`;
- `version`;
- `environment`.

## 10. Mini-attività
Riporto la mappa GitHub -> Azure DevOps -> ACR -> ACI e le risposte alle domande.

## 11. Laboratorio autonomo
Documento:
- modifica versione;
- nuovo commit;
- nuovo run pipeline;
- nuovo tag immagine;
- verifica endpoint;
- log cloud.

## 12. Problemi incontrati
Descrivo eventuali errori e come li ho risolti.
