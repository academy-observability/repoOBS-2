# 03 - Laboratorio autonomo UD08
## Query Card KQL: progettare, spiegare e migliorare una query

## Obiettivo

Il laboratorio autonomo non ripete il guidato. Nel guidato abbiamo eseguito query base. Nell'autonomo costruiamo una **Query Card**: una scheda tecnica che collega domanda, query, risultato, limiti e variante migliorativa.

Il prodotto finale è:

```text
docs/report_ud08_autonomo_query_card.md
```

## Regola di lavoro

Usare le evidenze e il workspace già preparati nel guidato. Eseguire nuovi comandi solo per completare la Query Card scelta.

## Scelta dello scenario

Scegliere **uno** scenario.

| Scenario | Descrizione | Valore aggiunto |
|---|---|---|
| A | Analisi su dataset simulato `datatable` | dimostra controllo sugli operatori KQL anche con workspace vuoto |
| B | Analisi della tabella `Usage` | interpreta quali dati sono presenti nel workspace |
| C | Analisi di `AzureActivity`, se disponibile | distingue eventi amministrativi da log applicativi |
| D | Confronto tra due versioni della stessa query | mostra come filtro, proiezione o aggregazione cambiano il significato |

## Parte 1 - Preparazione report

```bash
# Crea il report autonomo dal template.
cp docs/template_report_ud08_autonomo_query_card.md docs/report_ud08_autonomo_query_card.md

# Verifica che il file sia presente.
ls -l docs/report_ud08_autonomo_query_card.md
```

## Parte 2 - Scelta della domanda tecnica

La domanda deve essere concreta. Esempi:

| Scenario | Domanda tecnica valida |
|---|---|
| A | Quale servizio simulato presenta più errori o durata maggiore? |
| B | Quali tipi di dati risultano presenti nel workspace negli ultimi sette giorni? |
| C | Quali operazioni amministrative recenti risultano visibili? |
| D | Cosa cambia tra mostrare righe grezze e aggregare per servizio? |

## Parte 3 - Creazione della query personale

Creare una nuova query nella cartella corretta: `src/kql/local/` per dataset didattici oppure `src/kql/azure/` per tabelle reali.

Esempio per scenario A:

```bash
# Crea una query autonoma commentata basata su datatable.
cat > src/kql/local/autonomo_query_card_datatable.kql <<'EOF'
// UD08 autonomo - Query Card su dataset simulato
// Domanda tecnica:
//   Quale servizio simulato presenta più errori e durata media maggiore?
// Nota:
//   I dati sono simulati con datatable e non rappresentano log reali del workspace.

let BaseTime = now();

datatable(OffsetMin:int, Service:string, Status:int, DurationMs:int)
[
  8, "catalog", 200, 120,
  7, "catalog", 500, 700,
  6, "orders", 200, 180,
  5, "orders", 503, 950,
  4, "orders", 200, 210,
  3, "payments", 429, 300,
  2, "payments", 200, 240,
  1, "payments", 500, 820
]
| extend TimeGenerated = BaseTime - OffsetMin * 1m
// Raggruppa per servizio per ottenere indicatori sintetici.
| summarize
    Requests=count(),
    ServerErrors=countif(Status >= 500),
    ClientOrThrottle=countif(Status between (400 .. 499)),
    AvgDurationMs=avg(DurationMs),
    MaxDurationMs=max(DurationMs)
  by Service
// Ordina i servizi più critici in alto.
| sort by ServerErrors desc, AvgDurationMs desc
EOF
```

Esempio per scenario B:

```bash
# Crea una query autonoma sulla tabella Usage.
cat > src/kql/azure/autonomo_query_card_usage.kql <<'EOF'
// UD08 autonomo - Query Card su Usage
// Domanda tecnica:
//   Quali tipi di dati sono presenti nel workspace negli ultimi sette giorni?
// Nota:
//   Il risultato può essere vuoto se il workspace non ha dati nel time range.

Usage
| where TimeGenerated > ago(7d)
// Aggrega quantità e numero di record per DataType.
| summarize
    Record=count(),
    QuantitaTotale=sum(Quantity)
  by DataType
| sort by QuantitaTotale desc
EOF
```

## Parte 4 - Esecuzione query

Caricare le variabili se necessario:

```bash
# Carica la configurazione locale.
set -a
source config/ud08.env
set +a

# Verifica che WORKSPACE_ID sia valorizzato.
printf 'WORKSPACE_ID=%s\n' "$WORKSPACE_ID"
```

Eseguire la query scelta. Sostituire il nome file se si usa una query diversa.

```bash
# Esegue la query autonoma e salva il risultato.
az monitor log-analytics query \
  --workspace "$WORKSPACE_ID" \
  --analytics-query "$(cat src/kql/local/autonomo_query_card_datatable.kql)" \
  --output json > evidence/autonomo_query_card_result.json

# Mostra una preview leggibile del risultato.
python3 -m json.tool evidence/autonomo_query_card_result.json | head -100
```

## Parte 5 - Evidenza dal Portale

Aprire nel Portale:

```text
Log Analytics workspaces -> <LAW> -> Logs
```

Incollare la stessa query e salvare uno screenshot significativo:

```text
img/ud08_autonomo_query_card_result.png
```

## Parte 6 - Variante migliorativa

Produrre una piccola variante della query. Esempi:

| Variante | Esempio |
|---|---|
| filtro | aggiungere `where Status >= 400` |
| proiezione | mostrare solo colonne utili con `project` |
| aggregazione | raggruppare con `summarize` |
| ordinamento | cambiare criterio di `sort by` |
| time range | usare `ago(24h)` invece di `ago(7d)` per una tabella reale |

Scrivere nel report perché la variante migliora la lettura.

## Parte 7 - Conclusione

Nel report devono comparire:

- domanda tecnica scelta;
- query commentata;
- risultato osservato;
- interpretazione;
- limite dell'analisi;
- variante migliorativa;
- evidenza Portale;
- evidenza JSON.

## Criteri di completamento

| Criterio | Stato |
|---|---|
| uno scenario scelto | ☐ |
| domanda tecnica esplicita | ☐ |
| query autonoma commentata in `src/kql/local/` o `src/kql/azure/` | ☐ |
| esecuzione da Portale | ☐ |
| screenshot prodotto | ☐ |
| JSON prodotto in `evidence/` | ☐ |
| report compilato | ☐ |
| variante migliorativa descritta | ☐ |
| commit/push eseguito | ☐ |


---

## Integrazione richiesta su dati reali

La query card autonoma deve contenere anche una breve sezione di confronto con almeno una tabella reale, se disponibile nel workspace.

Esempi ammessi:

- `AzureActivity` per attività amministrative;
- `StorageBlobLogs` per operazioni sul servizio Blob, se configurato;
- `AppServiceHTTPLogs` per traffico applicativo App Service;
- `Heartbeat` per VM monitorate con Azure Monitor Agent e Data Collection Rules;
- `Usage` se non sono presenti altre tabelle significative.

Se nessuna tabella applicativa è popolata, documentare l'esito come limite dell'ambiente e mantenere la query `datatable()` come palestra KQL.
