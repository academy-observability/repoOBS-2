# OBS UD19 — Prometheus osserva l'app Catalogo prodotti

Questa UD prosegue direttamente la UD18. Lo stack locale è già composto da due blocchi:

```text
app-stack = frontend-products + backend-products
obs-stack = Prometheus + Grafana + Jaeger + log JSON
```

In UD19 il centro dell'attività diventa **Prometheus**. Non ci limitiamo a verificare che i container siano accesi: impariamo a leggere il comportamento dell'applicazione attraverso metriche raccolte periodicamente.

## Sequenza consigliata

1. `00_OBS_UD19_Concetti_Prometheus_Metriche_Prodotti_FE_BE_v5_7_1.md`
2. `07_OBS_UD19_GUIDA_ARCHITETTURA_Prometheus_App_Prodotti_FE_BE_v5_7_1.md`
3. `04_OBS_UD19_GUIDA_OPERATIVA_Prometheus_Config_Target_PromQL_v5_7_1.md`
4. `01_OBS_UD19_LAB_guidato_Prometheus_Osserva_Prodotti_FE_BE_Container_v5_7_1.md`
5. `02_OBS_UD19_MINI_ATTIVITA_Target_Scrape_PromQL_Prodotti_v5_7_1.md`
6. `03_OBS_UD19_LAB_autonomo_Query_PromQL_Prodotti_FE_BE_v5_7_1.md`
7. `05_OBS_UD19_Raccordo_Metriche_Locali_Prodotti_v5_7_1.md`

## Output atteso

Alla fine della UD il partecipante deve saper mostrare:

- stack locale avviato;
- Prometheus raggiungibile su `http://localhost:9090`;
- target `products-frontend` e `products-backend` in stato `UP`;
- endpoint `/metrics` funzionanti su frontend e backend;
- query PromQL per richieste, errori e latenza;
- evidenze salvate in `docs/evidence_ud19.md` o nella cartella `evidence/`.

## Pulizia

Dalla cartella `src/app_products_prometheus`:

```bash
./scripts/stop_stack_ud19.sh
```
