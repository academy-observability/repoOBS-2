# 04 - UD09 Guida operativa: KQL troubleshooting passo passo

## 1. Scopo

Questa guida aiuta a eseguire le query UD09, salvare evidenze e interpretare risultati vuoti o errori.

## 2. Dove eseguire le query

Le query KQL si eseguono in:

```text
Azure Portal -> Log Analytics workspaces -> workspace UD08 -> Logs
```

I comandi `cp`, `mkdir`, `git`, `az` vanno invece eseguiti nel terminale locale o in WSL, dentro la cartella `UD09`.

## 3. Come usare un file `.kql`

Procedura manuale consigliata:

1. aprire il file `.kql` in VS Code;
2. copiare tutto il contenuto;
3. incollarlo nel Logs editor;
4. verificare il time range;
5. premere **Run**;
6. salvare screenshot o risultato.

## 4. Time range

Per le query `datatable()` il time range del portale incide poco, perché il dataset usa `now()`. Per le tabelle reali è invece decisivo.

Regola pratica:

```text
se la query reale non restituisce righe, provare prima 24 ore o 48 ore
```

## 5. Risultato vuoto

Un risultato vuoto può essere corretto. Verificare:

| Verifica | Cosa controllare |
|---|---|
| Time range | la finestra temporale è troppo stretta? |
| Diagnostic setting | la risorsa invia dati al LAW? |
| Traffico | è stato generato traffico dopo il collegamento? |
| Tabella | la tabella esiste nello schema? |
| Filtro | il `where` è troppo selettivo? |

## 6. Errore “Failed to resolve table”

Significa che la tabella non è presente nel workspace selezionato.

Azioni:

```text
verificare di essere nel workspace corretto
controllare la configurazione UD08
eseguire src/kql/azure/01_scopri_tabelle_note_workspace.kql
usare le query datatable() per completare il metodo diagnostico
```

## 7. Salvare output JSON con Azure CLI

Valorizzare prima il file ambiente:

```bash
cp config/ud09.env.example config/ud09.env
nano config/ud09.env
source config/ud09.env
```

Eseguire una query da file:

```bash
az monitor log-analytics query   --workspace "$WORKSPACE_ID"   --analytics-query "$(cat src/kql/local/02_error_rate_per_risorsa.kql)"   --output json > evidence/ud09_error_rate.json
```

Verifica:

```bash
ls -lh evidence/ud09_error_rate.json
head -40 evidence/ud09_error_rate.json
```

## 8. Leggere lo schema di una tabella reale

Quando una tabella esiste ma non si conoscono le colonne:

```kql
AppServiceHTTPLogs
| getschema
```

Oppure:

```kql
AppServiceHTTPLogs
| take 5
```

Poi adattare `project`, `where` e `summarize` alle colonne effettive.

## 9. Checklist prima di concludere

Prima di chiudere UD09 verificare:

```text
report guidato compilato
report autonomo compilato, se previsto
evidenze salvate
almeno una query reale verificata o motivazione dell'assenza dati
query candidata per alert scelta
commit finale eseguito
```
