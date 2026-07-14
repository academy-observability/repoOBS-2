# OBS UD17 v5.7_1
# Observability cloud Catalogo prodotti su Azure Container Apps

## Scopo della UD

UD17 osserva in cloud la release **Catalogo prodotti** introdotta dopo UD16. Il workload è composto da frontend e backend Flask su Azure Container Apps, immagini in ACR e collegamento FE → BE tramite `BACKEND_URL`.

Questa versione sostituisce la precedente UD17 v5.7 perché conserva la profondità della v5.6 e integra il nuovo scenario products senza comprimere i contenuti.

## Sequenza consigliata di studio

1. `00_OBS_UD17_Concetti_Observability_Azure_Products_v5_7_1.md`
2. `07_OBS_UD17_GUIDA_ARCHITETTURA_Observability_Cloud_Products_ACA_v5_7_1.md`
3. `04_OBS_UD17_GUIDA_OPERATIVA_AppInsights_LogAnalytics_KQL_Products_v5_7_1.md`
4. `01_OBS_UD17_LAB_guidato_Observability_Azure_Post_Deploy_Products_v5_7_1.md`
5. `02_OBS_UD17_MINI_ATTIVITA_AppInsights_KQL_Correlazione_Products_v5_7_1.md`
6. `03_OBS_UD17_LAB_autonomo_Analisi_Errori_Latenza_Catalogo_Prodotti_v5_7_1.md`
7. `05_OBS_UD17_Raccordo_Cloud_Observability_Stack_Locale_v5_7_1.md`

## Cartelle principali

```text
UD17/
├── src/app_products_observable/
├── templates/
├── kql/
├── scripts/
├── docs/
├── evidence/
├── logs/
└── img/
```

## Output atteso

Al termine il partecipante deve poter mostrare:

- frontend e backend ACA aggiornati con immagini products osservabili;
- Application Insights collegato;
- traffico su `/products`, `/products/slow`, `/products/error`;
- query KQL su request, dependency e log container;
- correlazione tramite `request_id`, `OperationId` o `trace_id`;
- decision record tecnico.

## Nota sui tempi

Dopo la generazione del traffico, Application Insights e Log Analytics possono richiedere alcuni minuti prima di mostrare tutti i dati.
