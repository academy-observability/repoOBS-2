# 04 - UD08 Guida operativa passo passo
## Esecuzione KQL e salvataggio evidenze senza script automatici

Questa guida sostituisce l'uso di script Bash automatici. Ogni comando viene eseguito manualmente, così è chiaro che cosa viene letto, dove viene salvato il risultato e quale evidenza viene prodotta.

## 1. Caricare la configurazione

```bash
# Carica le variabili definite nel file locale config/ud08.env.
set -a
source config/ud08.env
set +a

# Verifica che i valori principali siano presenti.
printf 'RG=%s\nLAW=%s\nWORKSPACE_ID=%s\n' "$RG" "$LAW" "$WORKSPACE_ID"
```

Se `WORKSPACE_ID` è vuoto:

```bash
# Recupera il customerId del workspace e lo salva in variabile.
export WORKSPACE_ID="$(az monitor log-analytics workspace show \
  --resource-group "$RG" \
  --workspace-name "$LAW" \
  --query customerId \
  --output tsv)"

# Salva il customerId come evidenza locale.
printf '%s\n' "$WORKSPACE_ID" > evidence/workspace_id.txt
```

## 2. Controllare una query prima di eseguirla

```bash
# Mostra il contenuto della query KQL con numeri di riga.
nl -ba src/kql/local/01_datatable_take.kql
```

Controllare sempre:

- tabella o dataset usato;
- operatori principali;
- eventuale time range;
- commenti presenti nella query.

## 3. Eseguire una query da file `.kql`

```bash
# Esegue una query KQL letta da file e salva il risultato JSON.
az monitor log-analytics query \
  --workspace "$WORKSPACE_ID" \
  --analytics-query "$(cat src/kql/local/01_datatable_take.kql)" \
  --output json > evidence/query_datatable_take.json
```

## 4. Leggere il risultato JSON

```bash
# Format JSON usando Python, disponibile nella maggior parte degli ambienti Linux.
python3 -m json.tool evidence/query_datatable_take.json | head -80
```

Se `jq` è disponibile:

```bash
# jq permette di ispezionare rapidamente chiavi e struttura JSON.
jq 'keys' evidence/query_datatable_take.json
```

## 5. Salvare una nota quando una tabella è assente

Per una tabella reale non sempre disponibile, come `AzureActivity`, usare una nota tecnica quando l'esecuzione non produce risultato utilizzabile.

```bash
# Registra nel repository l'esito tecnico della prova su AzureActivity.
printf 'AzureActivity non disponibile o non popolata nel workspace/time range selezionato.\n' \
  > evidence/azureactivity_note.txt
```

## 6. Query `Usage`: lettura controllata

```bash
# Esegue la query Usage da file.
az monitor log-analytics query \
  --workspace "$WORKSPACE_ID" \
  --analytics-query "$(cat src/kql/azure/02_usage_summary.kql)" \
  --output json > evidence/query_usage_summary.json

# Mostra una preview del risultato formattato.
python3 -m json.tool evidence/query_usage_summary.json | head -80
```

Interpretazione minima da scrivere nel report:

```text
La query Usage indica quali tipi di dati risultano presenti nel workspace nel time range scelto. Se non restituisce righe, il workspace può non avere dati raccolti in quell'intervallo.
```

## 7. Query `AzureActivity`: prova controllata

```bash
# Esegue la query AzureActivity e salva l'output se la tabella è disponibile.
az monitor log-analytics query \
  --workspace "$WORKSPACE_ID" \
  --analytics-query "$(cat src/kql/azure/03_azureactivity_attivita_recenti.kql)" \
  --output json > evidence/query_azureactivity_recent.json
```

Se il comando restituisce errore per tabella assente:

```bash
# Salva una nota tecnica invece di lasciare il caso non documentato.
printf 'La tabella AzureActivity non è disponibile nel workspace o non contiene dati nel time range.\n' \
  > evidence/query_azureactivity_recent_note.txt
```

## 8. Verifica finale delle evidenze del percorso base

```bash
# Elenca i file prodotti in modo ordinato.
find docs evidence img logs src/kql -maxdepth 3 -type f | sort

# Controlla lo stato Git prima del commit.
git status
```

## 9. Errori comuni e azione correttiva nel percorso base

| Errore | Possibile causa | Azione |
|---|---|---|
| `WORKSPACE_ID` vuoto | variabile non recuperata | rieseguire il comando di recupero `customerId` |
| `Table not found` | tabella non raccolta nel workspace | usare `datatable` o altra tabella disponibile e documentare l'assenza |
| risultato JSON senza righe | nessun dato nel time range | cambiare time range o documentare risultato vuoto |
| `az: command not found` | Azure CLI assente | installare Azure CLI o usare terminale locale già configurato |
| `Please run az login` | sessione Azure non attiva | eseguire `az login --use-device-code` |


---

## 10. Query su tabelle Azure reali

Per lavorare sui dati reali del workspace aprire i file in:

```text
src/kql/azure/
```

Ordine consigliato:

```text
01_scopri_tabelle_note_workspace.kql
02_usage_summary.kql
03_azureactivity_attivita_recenti.kql
04_azureactivity_operazioni_per_stato.kql
05_azuremetrics_metriche_disponibili.kql
06_appservice_http_status.kql
07_vm_ama_dcr_tabelle_disponibili.kql
10_azureactivity_ud05_recent.kql
11_storagebloblogs_ud05_recent.kql
12_appservicehttplogs_ud05_recent.kql
13_realtables_summary_ud08.kql
```

Eseguire le query nel Logs editor del portale Azure. Salvare screenshot o esportazioni in `evidence/` usando la repository locale, non Cloud Shell.


## 11. Quando usare il laboratorio 05

Il file `05_OBS_UD08_LAB_guidato_Tabelle_Azure_Reali_v5_3.md` va usato dopo il percorso base. Il percorso base insegna gli operatori KQL in modo controllato; il laboratorio 05 configura e interroga segnali reali prodotti da risorse Azure create nelle UD precedenti.
