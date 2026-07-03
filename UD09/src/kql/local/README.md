# Query KQL locali UD09

Le query in questa cartella usano `datatable()` e sono autosufficienti. Servono a consolidare il ragionamento diagnostico senza dipendere dalla presenza di dati reali nel Log Analytics Workspace.

Sequenza consigliata:

1. `01_dataset_operazioni.kql`
2. `02_error_rate_per_risorsa.kql`
3. `03_trend_temporale_errori_bin_15m.kql`
4. `04_latenza_percentili_p95_p99.kql`
5. `05_top_operazioni_lente.kql`
6. `06_finestra_incidente_candidata.kql`
7. `07_query_alert_candidata.kql`
