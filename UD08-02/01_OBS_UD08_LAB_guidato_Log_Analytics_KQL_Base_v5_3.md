# 01 - Laboratorio guidato UD08
## Log Analytics Workspace, KQL base e preparazione alle tabelle reali

## Obiettivo

In questo laboratorio usiamo un Log Analytics Workspace per eseguire prime query KQL, osservando gli stessi passaggi da Portale Azure e da terminale locale.

Alla fine del laboratorio avremo:

- verificato ambiente locale e contesto Azure;
- individuato o creato un workspace dedicato alla UD08;
- recuperato il `WORKSPACE_ID` usato da Azure CLI;
- aperto Logs dal Portale;
- eseguito query KQL con `datatable`;
- provato query su tabelle reali disponibili;
- preparato l'estensione guidata su risorse Azure reali provenienti dalle UD precedenti;
- salvato evidenze JSON e screenshot;
- compilato un report tecnico.

## Prerequisiti e procedure di ripristino

| Verifica | Comando o azione | Procedura se non soddisfatta |
|---|---|---|
| Repository locale disponibile | aprire la cartella `work/UD08` | clonare o aggiornare il repository del corso prima di iniziare |
| Azure CLI disponibile | `az version` | installare Azure CLI in WSL o usare un terminale locale già configurato |
| Login Azure attivo | `az account show -o table` | eseguire `az login --use-device-code` |
| Subscription corretta | `az account list -o table` | eseguire `az account set --subscription "<subscription-id>"` |
| File configurazione locale | `test -f config/ud08.env` | copiare `config/ud08.env.example` in `config/ud08.env` e valorizzarlo |
| Workspace disponibile | `az monitor log-analytics workspace show -g "$RG" -n "$LAW"` | creare un workspace dedicato UD08 con la procedura del Task 4 |

## Regola locale / Cloud Shell

I comandi che scrivono file in `docs/`, `evidence/`, `logs/` o `img/` si eseguono dal repository locale. Cloud Shell può essere usata per verifiche rapide e screenshot, ma non sostituisce la cartella locale del laboratorio.

---

# Task 1 - Preparazione cartelle e report

Eseguire dal repository locale UD08:

```bash
# Crea le cartelle operative usate nel laboratorio.
mkdir -p docs evidence img logs src/kql/local src/kql/azure

# Crea il report guidato partendo dal template fornito.
cp docs/template_report_ud08_guidato.md docs/report_ud08_guidato.md

# Verifica che il report sia stato creato.
ls -l docs/report_ud08_guidato.md
```

---

# Task 2 - Verifica Azure CLI e login

## Vista da terminale locale

```bash
# Verifica che Azure CLI sia disponibile.
az version --output table

# Mostra il contesto Azure corrente in forma leggibile.
az account show --output table

# Salva il contesto Azure come evidenza JSON nel repository locale.
az account show --output json > evidence/account_context.json
```

Se `az account show` segnala assenza di login:

```bash
# Avvia il login con device code, adatto anche in WSL.
az login --use-device-code

# Dopo il login, verifica di nuovo il contesto.
az account show --output table
```

Se la subscription non è quella del laboratorio:

```bash
# Elenca le subscription visibili all'utente.
az account list --output table

# Imposta la subscription corretta usando nome o ID.
az account set --subscription "<subscription-id>"

# Verifica la subscription attiva.
az account show --query "{name:name,id:id,user:user.name}" --output table
```

## Vista da Portale Azure

Nel Portale verificare profilo, directory e subscription. Salvare uno screenshot se utile:

```text
img/ud08_portale_subscription_context.png
```

---

# Task 3 - Configurazione variabili

Copiare il file esempio e valorizzarlo:

```bash
# Copia la configurazione esempio in un file locale non versionato.
cp config/ud08.env.example config/ud08.env

# Apri il file e inserisci SUB_ID, RG, LOCATION e LAW.
nano config/ud08.env
```

Caricare le variabili:

```bash
# Esporta automaticamente le variabili definite nel file.
set -a
source config/ud08.env
set +a

# Verifica i valori caricati.
printf 'SUB_ID=%s\nRG=%s\nLOCATION=%s\nLAW=%s\nWORKSPACE_ID=%s\n' \
  "$SUB_ID" "$RG" "$LOCATION" "$LAW" "$WORKSPACE_ID"
```

Impostare la subscription indicata nel file:

```bash
# Usa la subscription definita in config/ud08.env.
az account set --subscription "$SUB_ID"

# Verifica che la subscription attiva sia quella prevista.
az account show --query "{name:name,id:id,user:user.name}" --output table
```

---

# Task 4 - Resource Group e Workspace

## 4.1 Verificare il Resource Group

```bash
# Controlla se il Resource Group esiste.
az group exists --name "$RG"
```

Se il comando restituisce `false`, creare un Resource Group dedicato alla UD08:

```bash
# Crea il Resource Group dedicato al laboratorio UD08.
az group create \
  --name "$RG" \
  --location "$LOCATION" \
  --tags corso=observability ud=08 ambiente=lab \
  --output json > evidence/resource_group_create.json
```

## 4.2 Verificare workspace esistenti

Da Portale:

```text
Azure Portal -> Log Analytics workspaces
Azure Portal -> Resource groups -> <RG> -> risorse
```

Da terminale locale:

```bash
# Elenca i workspace presenti nel Resource Group.
az monitor log-analytics workspace list \
  --resource-group "$RG" \
  --output table

# Salva l'elenco come evidenza JSON.
az monitor log-analytics workspace list \
  --resource-group "$RG" \
  --output json > evidence/workspaces_list.json
```

## 4.3 Creare il workspace se assente

Se il workspace `$LAW` non esiste, crearlo con configurazione minima per il laboratorio:

```bash
# Crea un Log Analytics Workspace dedicato a UD08.
# La creazione non abilita automaticamente nuove raccolte dati applicative.
az monitor log-analytics workspace create \
  --resource-group "$RG" \
  --workspace-name "$LAW" \
  --location "$LOCATION" \
  --tags corso=observability ud=08 ambiente=lab \
  --output json > evidence/workspace_create.json
```

Verificare:

```bash
# Mostra il workspace in forma tabellare.
az monitor log-analytics workspace show \
  --resource-group "$RG" \
  --workspace-name "$LAW" \
  --output table

# Salva il dettaglio completo del workspace.
az monitor log-analytics workspace show \
  --resource-group "$RG" \
  --workspace-name "$LAW" \
  --output json > evidence/workspace_context.json
```

Da Portale salvare uno screenshot della pagina Overview:

```text
img/ud08_portale_workspace_overview.png
```

---

# Task 5 - Recupero del Workspace ID

Il nome del workspace non è il valore usato da CLI per eseguire query. Recuperiamo il `customerId`.

```bash
# Recupera il customerId del workspace.
export WORKSPACE_ID="$(az monitor log-analytics workspace show \
  --resource-group "$RG" \
  --workspace-name "$LAW" \
  --query customerId \
  --output tsv)"

# Salva il valore come evidenza.
printf '%s\n' "$WORKSPACE_ID" | tee evidence/workspace_id.txt

# Verifica che il valore non sia vuoto.
printf 'WORKSPACE_ID=%s\n' "$WORKSPACE_ID"
```

Aggiornare `config/ud08.env` inserendo il valore di `WORKSPACE_ID`, così potrà essere riusato nelle sessioni successive.

---

# Task 6 - Apertura Logs dal Portale

Nel Portale aprire:

```text
Log Analytics workspaces -> <LAW> -> Logs
```

Osservare:

- query editor;
- elenco tabelle;
- schema delle colonne;
- selettore time range;
- area risultati;
- messaggi di errore o avviso.

Evidenza richiesta:

```text
img/ud08_portale_logs_editor.png
```

Nel report annotare quali tabelle sono visibili e quale time range è stato impostato.

---

# Task 7 - Query KQL con `datatable` e `take`

## Portale Azure

Incollare nel pannello Logs la query contenuta in:

```text
src/kql/local/01_datatable_take.kql
```

La query contiene commenti KQL che descrivono ogni passaggio.

## CLI locale

```bash
# Esegue la query da file .kql e salva il risultato in JSON.
az monitor log-analytics query \
  --workspace "$WORKSPACE_ID" \
  --analytics-query "$(cat src/kql/local/01_datatable_take.kql)" \
  --output json > evidence/query_datatable_take.json

# Mostra una versione leggibile del JSON prodotto.
python3 -m json.tool evidence/query_datatable_take.json | head -80
```

Nel report spiegare:

- perché `datatable` funziona anche con workspace vuoto;
- cosa fa `take`;
- che differenza c'è tra screenshot Portale e JSON locale.

---

# Task 8 - Query con `where`, `project`, `sort by`

## Portale Azure

Eseguire la query:

```text
src/kql/local/02_datatable_filter_project.kql
```

## CLI locale

```bash
# Esegue la query di filtro e salva il risultato.
az monitor log-analytics query \
  --workspace "$WORKSPACE_ID" \
  --analytics-query "$(cat src/kql/local/02_datatable_filter_project.kql)" \
  --output json > evidence/query_datatable_filter_project.json

# Mostra le prime righe del risultato JSON formattato.
python3 -m json.tool evidence/query_datatable_filter_project.json | head -80
```

Nel report spiegare:

- quale condizione filtra le righe;
- perché `project` riduce le colonne mostrate;
- perché l'ordinamento temporale aiuta la lettura operativa.

---

# Task 9 - Query con `summarize`

## Portale Azure

Eseguire la query:

```text
src/kql/local/03_datatable_summarize.kql
```

## CLI locale

```bash
# Esegue la query di aggregazione e salva il risultato.
az monitor log-analytics query \
  --workspace "$WORKSPACE_ID" \
  --analytics-query "$(cat src/kql/local/03_datatable_summarize.kql)" \
  --output json > evidence/query_datatable_summarize.json

# Mostra una preview del risultato.
python3 -m json.tool evidence/query_datatable_summarize.json | head -80
```

Nel report spiegare:

- cosa significa aggregare per `Service`;
- differenza tra `count()` e `countif()`;
- perché media e massimo raccontano aspetti diversi della durata.

---

# Task 10 - Esplorazione della tabella `Usage`

La tabella `Usage` può essere disponibile anche in workspace con pochi dati. Eseguire prima dal Portale, poi da CLI.

```bash
# Esegue una query reale su Usage, se la tabella è disponibile nel workspace.
az monitor log-analytics query \
  --workspace "$WORKSPACE_ID" \
  --analytics-query "$(cat src/kql/azure/02_usage_summary.kql)" \
  --output json > evidence/query_usage_summary.json

# Mostra una preview del risultato.
python3 -m json.tool evidence/query_usage_summary.json | head -80
```

Se il risultato è vuoto, documentare il caso nel report. Un risultato vuoto è un'informazione tecnica: indica assenza di record nel time range o workspace non ancora popolato.

---

# Task 11 - Esplorazione della tabella `AzureActivity`

Eseguire solo se la tabella è visibile nel Portale o se si vuole documentare l'eventuale assenza.

```bash
# Prova a interrogare AzureActivity e salva l'esito.
# Se la tabella non esiste, il comando può restituire errore: l'errore va documentato.
az monitor log-analytics query \
  --workspace "$WORKSPACE_ID" \
  --analytics-query "$(cat src/kql/azure/03_azureactivity_attivita_recenti.kql)" \
  --output json > evidence/query_azureactivity_recent.json
```

Se il comando fallisce perché la tabella non esiste:

```bash
# Salva una nota tecnica nel repository locale.
printf 'AzureActivity non disponibile nel workspace o non popolata nel time range.\n' \
  > evidence/query_azureactivity_recent_note.txt
```

Nel report distinguere chiaramente tra:

- tabella non disponibile;
- tabella disponibile ma senza righe;
- query con errore di sintassi.

---

# Task 12 - Verifica file prodotti e commit

```bash
# Elenca le evidenze prodotte durante UD08.
find docs evidence img logs src/kql -maxdepth 3 -type f | sort

# Verifica lo stato Git.
git status
```

Commit consigliato:

```bash
# Aggiunge i file della UD08.
git add docs evidence img logs src/kql config/ud08.env.example README.md *.md

# Registra il lavoro svolto.
git commit -m "UD08 Log Analytics Workspace e KQL base"

# Pubblica sul repository remoto.
git push
```

## Criteri di completamento

| Criterio | Stato |
|---|---|
| Azure CLI verificata | ☐ |
| Workspace individuato o creato | ☐ |
| `WORKSPACE_ID` recuperato | ☐ |
| Logs aperto dal Portale | ☐ |
| Query `datatable` eseguite | ☐ |
| Almeno una query reale provata | ☐ |
| Evidenze JSON prodotte | ☐ |
| Screenshot salvati | ☐ |
| Report compilato | ☐ |
| Commit/push eseguito | ☐ |


---

# Estensione guidata - Tabelle Azure reali

Dopo i task basati su `datatable()`, eseguire il file aggiuntivo:

```text
05_OBS_UD08_LAB_guidato_Tabelle_Azure_Reali_v5_3.md
```

Questa estensione serve a configurare e interrogare tabelle effettivamente presenti nel workspace, distinguendo dati didattici controllati e dati Azure reali. La parte lavora su Activity Log, Storage Blob, App Service e, come estensione opzionale, VM con AMA/DCR. Per le VM usare come riferimento Azure Monitor Agent e Data Collection Rules, non la vecchia diagnostica VM legacy.
