# Script UD07

Questa cartella contiene script didattici per UD07.

Eseguire sempre dal repository locale, normalmente da WSL o terminale locale autenticato con Azure CLI.

Prima dell'uso:

```bash
cp config/ud07.env.example config/ud07.env
nano config/ud07.env
set -a
source config/ud07.env
set +a
```

Script principali:

| Script | Scopo |
|---|---|
| `verifica_ud07.sh` | verifica Azure CLI e contesto |
| `ud07_generate_administrative_activity.sh` | genera eventi Activity Log aggiornando tag |
| `ud07_generate_application_traffic.sh` | genera richieste HTTP, operazioni blob e CPU opzionale |
| `az_metric_definitions.sh` | esporta definizioni metriche |
| `az_metrics_snapshot.sh` | esporta valori metrici |
| `az_diagnostic_settings_inventory.sh` | esporta Diagnostic Settings e categorie |


## Nota versione v4.1

I due script automatici `ud07_generate_administrative_activity.sh` e `ud07_generate_application_traffic.sh` sono stati sostituiti dalla guida operativa:

```text
../04_OBS_UD07_GENERAZIONE_CONTROLLATA_SEGNALI_Passo_Passo.md
```

La scelta è didattica: i partecipanti eseguono i comandi passo dopo passo e osservano direttamente la differenza tra segnali amministrativi e segnali applicativi.
