# Query KQL su tabelle Azure reali UD09

Le query in questa cartella applicano il metodo UD09 alle tabelle reali configurate durante UD08.

Le tabelle possono essere assenti o vuote. In quel caso non va forzata una conclusione: documentare quale tabella manca, quale diagnostic setting è stato verificato e se è stato generato traffico dopo il collegamento al LAW.

Sequenza consigliata:

1. `01_scopri_tabelle_note_workspace.kql`
2. `02_azureactivity_operazioni_fallite.kql`
3. `03_azureactivity_trend_orario.kql`
4. `04_appservice_errori_http.kql`
5. `05_storageblob_operazioni_errori.kql`
6. `06_azuremetrics_risorse_trend.kql`
7. `07_vm_heartbeat_perf.kql`
8. `08_azurediagnostics_errori_fallback.kql`
