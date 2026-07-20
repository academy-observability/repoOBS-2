# OBS UD22 — Tracing distribuito con Jaeger

## Domanda guida

**Come ricostruiamo il percorso completo di una richiesta tra frontend e backend e individuiamo il punto in cui nasce una lentezza o un errore?**

La UD22 usa Jaeger come strumento principale. Prometheus, Grafana e i log rimangono disponibili come fonti di contesto, ma il lavoro centrale consiste nel leggere trace e span, comprendere la propagazione del contesto e sostenere una diagnosi con evidenze.

## Sequenza consigliata

1. `00_OBS_UD22_Concetti_Tracing_Distribuito_Jaeger_v6_0.md`
2. `07_OBS_UD22_GUIDA_ARCHITETTURA_Jaeger_Storage_Volumi_v6_0.md`
3. `04_OBS_UD22_GUIDA_OPERATIVA_Jaeger_Correlazione_v6_0.md`
4. `01_OBS_UD22_LAB_guidato_Analisi_Trace_FE_BE_v6_0.md`
5. `02_OBS_UD22_MINI_ATTIVITA_Lettura_Trace_v6_0.md`
6. `06_OBS_UD22_APPROFONDIMENTO_Persistenza_Retention_Volumi_v6_0.md`
7. `03_OBS_UD22_LAB_autonomo_Incident_Investigation_v6_0.md`
8. `05_OBS_UD22_Raccordo_Metriche_Log_Trace_v6_0.md`
9. `08_OBS_UD22_APPROFONDIMENTO_Dal_Lab_alla_Produzione_v6_0.md`
10. `09_OBS_UD22_RIFERIMENTI_TECNICI_v6_0.md`

## URL

| Servizio | URL |
|---|---|
| Frontend | `http://localhost:8122` |
| Backend | `http://localhost:8022/health` |
| Jaeger | `http://localhost:16686` |
| Prometheus | `http://localhost:9090` |
| Grafana | `http://localhost:3000` — `admin/admin` |

## Risultato atteso

Il partecipante deve saper leggere una trace frontend→backend, individuare lo span dominante, riconoscere un errore, correlare `request_id` e `trace_id` con i log e spiegare a cosa servono lo storage Badger e il volume Docker montato da Jaeger.
