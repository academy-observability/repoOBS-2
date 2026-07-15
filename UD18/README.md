# OBS UD18 — Stack locale di observability per Catalogo prodotti v5.7_1

## Scopo della UD

In questa UD ricostruiamo in locale un ambiente osservabile completo partendo dallo stesso workload introdotto con la change request post-UD16: l'applicazione **Catalogo prodotti** composta da frontend e backend.

La differenza rispetto a UD17 è sostanziale: in UD17 abbiamo osservato l'applicazione nel cloud, dentro Azure Container Apps, usando Application Insights, Log Analytics e KQL. In UD18 riportiamo il sistema in un ambiente controllato e locale, dove possiamo vedere con maggiore chiarezza i confini tra applicazione osservata e strumenti osservanti.

```text
app-stack
  frontend-products
  backend-products

obs-stack
  prometheus
  grafana
  jaeger
  log JSON su stdout
```

## Prerequisiti

- Docker Desktop in esecuzione con Linux containers.
- WSL2/Ubuntu o terminale Bash equivalente.
- Git repository del corso aggiornato.
- Conoscenza di base dei container FE/BE introdotti in UD15 e del deploy ACA visto in UD16/UD17.

## Sequenza consigliata

1. `00_OBS_UD18_Concetti_AppStack_ObsStack_Prodotti_v5_7_1.md`
2. `07_OBS_UD18_GUIDA_ARCHITETTURA_AppStack_ObsStack_Prodotti_v5_7_1.md`
3. `04_OBS_UD18_GUIDA_OPERATIVA_DockerCompose_Stack_Locale_Prodotti_v5_7_1.md`
4. `01_OBS_UD18_LAB_guidato_Architettura_Stack_Observability_Locale_Prodotti_FE_BE_v5_7_1.md`
5. `02_OBS_UD18_MINI_ATTIVITA_Mappa_AppStack_ObsStack_Prodotti_v5_7_1.md`
6. `03_OBS_UD18_LAB_autonomo_Verifica_Stack_Locale_Prodotti_v5_7_1.md`
7. `05_OBS_UD18_Raccordo_Stack_Locale_Products_Observability_v5_7_1.md`

## Output atteso

Al termine il partecipante deve poter mostrare:

- applicazione frontend prodotti raggiungibile da browser/curl;
- backend prodotti raggiungibile direttamente dal computer host;
- Prometheus attivo e target frontend/backend in stato `UP`;
- Grafana accessibile e collegato a Prometheus;
- Jaeger accessibile e capace di mostrare servizi/tracce dopo traffico applicativo;
- log JSON dei container con `request_id`, path, status e latenza;
- differenza tra traffico normale, lento ed errore controllato.

## Struttura tecnica

```text
UD18/
├── src/app_products_local/
│   ├── docker-compose.yml
│   ├── backend/
│   ├── frontend/
│   ├── prometheus/prometheus.yml
│   ├── grafana/provisioning/datasources/prometheus.yml
│   └── scripts/
├── docs/template_evidence_ud18.md
├── evidence/
├── logs/
└── img/
```

## Nota didattica

UD18 non è ancora la UD dedicata a Prometheus in profondità. Qui costruiamo il laboratorio locale completo e impariamo a riconoscere i componenti. UD19 entrerà nel dettaglio di Prometheus e PromQL; UD20 di Grafana; UD21 dell'alerting; UD22 di Jaeger, log e correlazione.
