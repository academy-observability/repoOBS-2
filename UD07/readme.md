# OBS_UD07 - Azure Monitor, metriche e Diagnostic Settings

## Versione v4

Questa versione integra la lettura delle metriche con la **generazione controllata di segnali osservabili**.

La differenza didattica rispetto a UD06 è netta:

```text
UD06 = riconoscere quali segnali diagnostici espone una risorsa.
UD07 = generare un segnale controllato, osservare prima/dopo e interpretare metriche e Activity Log.
```

In UD07 non creiamo nuove risorse Azure. Usiamo le risorse preparate in UD05 e osservate in UD06.

## Ordine consigliato

1. Leggere `00_OBS_UD07_Concetti_DETTAGLIATO_v4.md`.
2. Configurare `config/ud07.env` partendo da `config/ud07.env.example`.
3. Eseguire `01_OBS_UD07_LAB_guidato_Azure_Monitor_Metriche_Diagnostic_Settings_v4.md`.
4. Usare gli script in `src/` per generare segnali amministrativi e traffico applicativo.
5. Salvare evidenze in `evidence/` e log locali in `logs/`.
6. Compilare il report in `docs/`.
7. Svolgere `03_OBS_UD07_LAB_autonomo_Azure_Monitor_Metriche_Diagnostic_Settings_v4.md`.

## Regola fondamentale su WSL, terminale locale e Cloud Shell

I comandi che scrivono file in `docs/`, `evidence/`, `logs/` o `img/` devono essere eseguiti dal repository locale, normalmente in WSL o in un terminale locale con Azure CLI autenticata.

Cloud Shell può essere usata per controlli rapidi, viste tabellari, query da copiare o screenshot dal Portale, ma non per produrre i file locali del repository.

## File principali

| File | Uso |
|---|---|
| `00_OBS_UD07_Concetti_DETTAGLIATO_v4.md` | teoria dettagliata |
| `01_OBS_UD07_LAB_guidato_Azure_Monitor_Metriche_Diagnostic_Settings_v4.md` | laboratorio guidato |
| `03_OBS_UD07_LAB_autonomo_Azure_Monitor_Metriche_Diagnostic_Settings_v4.md` | laboratorio autonomo |

## Script operativi

| Script | Scopo |
|---|---|
| `src/verifica_ud07.sh` | verifica ambiente, Azure CLI e contesto |
| `04_OBS_UD07_GENERAZIONE_CONTROLLATA_SEGNALI_Passo_Passo.md` | guida passo dopo passo per generare attività amministrativa e traffico applicativo senza script automatici |
| `src/az_metric_definitions.sh` | esporta definizioni metriche di una risorsa |
| `src/az_metrics_snapshot.sh` | esporta valori metrici recenti |
| `src/az_diagnostic_settings_inventory.sh` | esporta categorie diagnostiche e Diagnostic Settings |

## Output attesi

Alla fine del guidato, dovrebbero esistere file simili a:

```text
docs/report_ud07_metriche_segnali_generati.md
evidence/ud07_account_context.json
evidence/ud07_admin_activity_log_after_core_tag_updates.json
evidence/ud07_appservice_requests_after_application_traffic.json
evidence/ud07_storage_transactions_after_application_traffic.json
logs/ud07_admin_activity.log
logs/ud07_application_traffic.log
```

I nomi possono variare leggermente se il docente modifica gli script o i parametri. L'importante è che il report colleghi ogni conclusione a un'evidenza.

## Riferimenti ufficiali

- Azure Monitor Metrics overview: https://learn.microsoft.com/en-us/azure/azure-monitor/metrics/data-platform-metrics
- Activity Log in Azure Monitor: https://learn.microsoft.com/en-us/azure/azure-monitor/platform/activity-log
- Diagnostic Settings in Azure Monitor: https://learn.microsoft.com/en-us/azure/azure-monitor/platform/diagnostic-settings

