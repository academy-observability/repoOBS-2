# 08 - UD10 Autoverifica partecipante: Alert, Dashboard e Workbook

## 1. Scopo

Questa autoverifica serve a controllare se la UD10 è stata completata in modo operativo.

Compilare il file dopo avere svolto:

```text
01 - Lab guidato principale
05 - Lab su tabelle reali
06 - Creazione reale Log Alert su LAW
07 - Dashboard/Workbook reali nel Portale
```

## 2. Dati generali

| Voce | Valore |
|---|---|
| Partecipante | |
| Data | |
| Resource Group | |
| Log Analytics Workspace | |
| Servizio osservato principale | |

## 3. Verifica Log Analytics Workspace

| Controllo | Risposta |
|---|---|
| Ho aperto il LAW corretto | Sì / No |
| Ho verificato almeno una tabella reale | Sì / No |
| Tabella usata | AppServiceHTTPLogs / StorageBlobLogs / AzureActivity / altro |
| Ho salvato evidenza della query | Sì / No |

Nota sintetica:

```text

```

## 4. Query KQL candidata per alert

| Voce | Risposta |
|---|---|
| Query scelta | |
| Tabella usata | |
| Finestra temporale | |
| Indicatore calcolato | |
| Soglia scelta | |
| La query restituisce righe solo se la soglia è superata? | Sì / No |

Query incollata o riferimento al file:

```kql

```

Motivazione della soglia:

```text

```

## 5. Action Group

| Controllo | Risposta |
|---|---|
| Action Group creato o selezionato | Sì / No |
| Nome Action Group | |
| Tipo notifica | Email / altro |
| Evidenza salvata | Sì / No |

## 6. Alert Rule

| Controllo | Risposta |
|---|---|
| Alert Rule creata o configurazione documentata | Sì / No |
| Nome Alert Rule | |
| Scope | LAW / risorsa specifica |
| Condition | Custom log search |
| Measurement | Table rows |
| Operator | Greater than |
| Threshold | 0 |
| Evaluation period | |
| Frequency | |
| Severity | |

Conclusione:

```text
L'alert segnala ... quando ...
```

## 7. Dashboard o Workbook

| Controllo | Risposta |
|---|---|
| Ho creato o visualizzato una Dashboard | Sì / No |
| Ho creato o visualizzato un Workbook | Sì / No |
| Query principale usata | |
| Visualizzazione usata | Table / Time chart / altro |
| Evidenza salvata | Sì / No |

Spiegazione sintetica:

```text
La Dashboard/Workbook è utile perché ...
```

## 8. Evidenze minime

Barrare le evidenze disponibili:

```text
[ ] evidence query su tabella reale
[ ] evidence traffico o evento generato
[ ] evidence query candidata per alert
[ ] evidence Action Group
[ ] evidence Alert Rule
[ ] evidence Dashboard o Workbook
[ ] report o note finali compilate
```

## 9. Domande di controllo

Rispondere in modo breve.

### 9.1 Perché una query che restituisce righe non è automaticamente un buon alert?

```text

```

### 9.2 Perché in laboratorio può andare bene una soglia più semplice rispetto alla produzione?

```text

```

### 9.3 Che differenza c'è tra Dashboard e Workbook?

```text

```

### 9.4 Quale falso positivo potrebbe produrre il tuo alert?

```text

```

### 9.5 Cosa faresti per rendere l'alert più adatto alla produzione?

```text

```

## 10. Esito personale

| Esito | Selezione |
|---|---|
| Completato senza criticità | |
| Completato con dubbi | |
| Parzialmente completato | |
| Da riprendere | |

Nota finale:

```text

```
