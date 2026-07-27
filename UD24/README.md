# OBS UD24 — Incident investigation locale/cloud su app Catalogo prodotti

## Scopo della UD

In UD24 usiamo l'app **Catalogo prodotti** come caso di indagine. Non stiamo introducendo un nuovo strumento: mettiamo in relazione ciò che abbiamo già costruito.

- In locale abbiamo osservato frontend e backend con Prometheus, Grafana, Jaeger e log JSON.
- In Azure abbiamo osservato la stessa app con Azure Container Apps, Application Insights, Log Analytics e KQL.
- Ora simuliamo un comportamento degradato o un errore e costruiamo una spiegazione tecnica difendibile.

L'obiettivo non è trovare “una query giusta”, ma imparare a costruire una catena di evidenze.

```text
Sintomo osservato
  ↓
segnali locali e cloud
  ↓
ipotesi tecniche
  ↓
verifica con metriche, log e trace
  ↓
root cause probabile
  ↓
azione correttiva e limiti dell'analisi
```

## Sequenza consigliata

1. `00_OBS_UD24_Concetti_Incident_Investigation_Locale_Cloud_Products_v5_8.md`
2. `07_OBS_UD24_GUIDA_ARCHITETTURA_Incident_Investigation_Locale_Cloud_Products_v5_8.md`
3. `04_OBS_UD24_GUIDA_OPERATIVA_Query_Diagnosi_Locale_Cloud_v5_8.md`
4. `01_OBS_UD24_LAB_guidato_Incident_Investigation_Locale_Cloud_Products_v5_8.md`
5. `02_OBS_UD24_MINI_ATTIVITA_Timeline_Ipotesi_Evidenze_RCA_v5_8.md`
6. `03_OBS_UD24_LAB_autonomo_Incident_Report_Products_v5_8.md`
7. `05_OBS_UD24_Raccordo_Incident_Baseline_Anomaly_v5_8.md`

## File operativi inclusi

| Cartella | Contenuto |
|---|---|
| `kql/` | Query cloud per Application Insights e log ACA |
| `promql/` | Query locali Prometheus per request rate, error rate e latenza |
| `scripts/` | Script per generare traffico e raccogliere evidenze locali/cloud |
| `docs/` | Template evidence, incident report, timeline e decision record |
| `templates/` | Runbook minimo per scenari prodotti |

## Output attesi

Al termine della UD il partecipante deve produrre:

- una timeline dell'incidente;
- una tabella sintomi/segnali/evidenze;
- query KQL e PromQL usate;
- almeno uno screenshot o estratto da Grafana/Jaeger/App Insights/Log Analytics;
- un incident report finale;
- una decisione tecnica motivata.

## Nota docente

UD24 sostituisce di fatto il project work esteso come momento di sintesi osservabilità. Il project work finale può rimanere solo come attività breve di chiusura e cleanup.
