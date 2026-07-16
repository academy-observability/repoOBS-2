# OBS UD20 — Grafana dashboard per il Catalogo prodotti

Questa UD prosegue UD18 e UD19. Lo stack locale rimane lo stesso, ma cambia il modo in cui leggiamo i segnali: in UD19 abbiamo interrogato Prometheus direttamente con PromQL; in UD20 costruiamo una dashboard Grafana che rende quelle metriche più leggibili, confrontabili e utili durante una diagnosi.

## Sequenza consigliata

1. `00_OBS_UD20_Concetti_Grafana_Dashboard_Prodotti_FE_BE_v5_7_1.md`
2. `07_OBS_UD20_GUIDA_ARCHITETTURA_Grafana_Dashboard_Prodotti_FE_BE_v5_7_2.md`
3. `04_OBS_UD20_GUIDA_OPERATIVA_Grafana_Datasource_Dashboard_Panel_v5_7_1.md`
4. `01_OBS_UD20_LAB_guidato_Grafana_Dashboard_Prodotti_Prometheus_v5_7_1.md`
5. `02_OBS_UD20_MINI_ATTIVITA_Dashboard_Pannelli_Metriche_v5_7_1.md`
6. `03_OBS_UD20_LAB_autonomo_Dashboard_Operativa_Prodotti_FE_BE_v5_7_1.md`
7. `05_OBS_UD20_Raccordo_Dashboard_Operativa_Alerting_v5_7_1.md`

## Output atteso

Alla fine della UD il partecipante deve saper mostrare:

- stack locale avviato;
- Grafana raggiungibile su `http://localhost:3000`;
- datasource Prometheus funzionante;
- dashboard `UD20 - Catalogo prodotti - FE/BE metrics` caricata;
- pannelli per disponibilità, traffico, errori e latenza;
- traffico generato sugli endpoint `/products`, `/products/slow`, `/products/error`;
- evidenze salvate in `docs/evidence_ud20.md` o nella cartella `evidence/`.

## Avvio rapido

```bash
cd UD20/src/app_products_grafana
./scripts/start_stack_ud20.sh
./scripts/generate_traffic_ud20.sh
```

Credenziali Grafana:

```text
admin / admin
```

## Cleanup

```bash
./scripts/stop_stack_ud20.sh
```
