# UD08 - Sequenza corretta per lavorare con tabelle Azure reali nel LAW

## Scopo del file

Questo documento chiarisce **quando** e **come** i partecipanti devono usare i file della UD08 per arrivare da un primo esercizio KQL controllato a query KQL su **dati reali Azure**.

Il punto chiave è questo:

> Eseguendo correttamente i task della UD08 è possibile interrogare con KQL dati reali provenienti da risorse Azure, ma solo dopo avere configurato l'invio dei log verso il Log Analytics Workspace.

Il Log Analytics Workspace non legge automaticamente tutte le risorse presenti nello stesso Resource Group. Le risorse devono essere collegate al LAW tramite **Diagnostic settings** oppure, nel caso delle VM, tramite **Azure Monitor Agent + Data Collection Rule**.

---

## 1. Query simulata e query reale

In UD08 ci sono due famiglie di query.

| Tipo di query | Esempio | Cosa dimostra | Cosa non dimostra |
|---|---|---|---|
| Query simulata | `datatable(...)` | Che il partecipante sa usare KQL anche con workspace vuoto | Non dimostra che una risorsa Azure stia inviando log |
| Query reale | `AzureActivity`, `StorageBlobLogs`, `AppServiceHTTPLogs`, `Heartbeat`, `Perf`, `Syslog`, `Event` | Che il LAW contiene dati ricevuti da sorgenti Azure reali | Non funziona se la sorgente non è stata collegata o non ha ancora generato dati |

La catena corretta per le tabelle reali è:

```text
Risorsa Azure reale
-> Diagnostic setting oppure DCR/AMA
-> Log Analytics Workspace
-> Tabella KQL reale
-> Query KQL
```

Quindi la query KQL non interroga direttamente la Web App, lo Storage Account o la VM. Interroga le tabelle presenti nel LAW dopo l'ingestione dei dati.

---

## 2. Risposta sintetica alla domanda didattica

Domanda:

```text
Eseguendo i task della UD08 è possibile estrarre/interrogare dati reali dalle risorse Azure con KQL?
```

Risposta:

```text
Sì, se i partecipanti completano i collegamenti risorsa -> LAW, generano eventi o traffico dopo il collegamento e interrogano la tabella corretta nel Log Analytics Workspace.
```

Più precisamente:

- l'Activity Log della subscription alimenta `AzureActivity`;
- il Blob service dello Storage Account alimenta `StorageBlobLogs`;
- la Web App/App Service alimenta `AppServiceHTTPLogs`;
- la VM, se configurata con AMA + DCR, alimenta `Heartbeat`, `Perf`, `Syslog` oppure `Event`.

Un workspace appena creato può rispondere alle query KQL, ma non per questo contiene già dati applicativi reali.

---

## 3. Sequenza corretta aggiornata dei file UD08

Questa è la sequenza consigliata per i partecipanti.

| Ordine | File | Quando usarlo | Scopo operativo |
|---:|---|---|---|
| 1 | `00_OBS_UD08_Concetti_DETTAGLIATO_v5_3.md` | Prima del laboratorio | Introduce LAW, tabelle, record, colonne, scope, time range, differenza tra query simulata e query reale |
| 2 | `01_OBS_UD08_LAB_guidato_Log_Analytics_KQL_Base_v5_3.md` | Primo laboratorio guidato | Crea o verifica il LAW, recupera `WORKSPACE_ID`, apre Logs nel Portale, esegue query base con `datatable()` e prime prove su tabelle disponibili |
| 3 | `04_OBS_UD08_GUIDA_OPERATIVA_KQL_Passo_Passo_v5_3.md` | Come supporto durante i laboratori | Spiega come eseguire manualmente query da file `.kql`, salvare JSON, leggere errori e produrre evidenze senza script automatici |
| 4 | `06_OBS_UD08_GUIDA_PORTALE_Collegamenti_Risorse_LAW_v5_4.md` | Prima o insieme al laboratorio 05 | Mostra da Portale Azure come collegare Activity Log, Storage Blob, Web App e VM al LAW |
| 5 | `05_OBS_UD08_LAB_guidato_Tabelle_Azure_Reali_v5_4_partecipanti.md` | Dopo il percorso KQL base | Esegue la parte tecnica completa: individua le risorse UD05 del partecipante, crea diagnostic settings, genera traffico, interroga tabelle reali |
| 6 | `03_OBS_UD08_LAB_autonomo_Query_Card_KQL_v5_3.md` | Dopo il guidato, preferibilmente dopo il laboratorio 05 | Produce la Query Card autonoma. A questo punto il partecipante può confrontare query simulate e almeno una tabella reale, se disponibile |
| 7 | `README.md` | Sempre come indice | Riepiloga file, cartelle operative e output atteso della UD08 |

Nota: il file `README.md` può essere letto all'inizio come orientamento generale. La sequenza sopra è quella operativa consigliata per evitare che il laboratorio autonomo venga svolto prima di avere tabelle reali disponibili.

---

## 4. Perché il file 03 va preferibilmente dopo il file 05

Il laboratorio autonomo `03_OBS_UD08_LAB_autonomo_Query_Card_KQL_v5_3.md` può essere svolto anche con `datatable()` o `Usage`, ma diventa più coerente se prima i partecipanti hanno configurato almeno una sorgente reale.

Motivo:

```text
Senza il laboratorio 05, il partecipante potrebbe avere solo query simulate o tabelle poco popolate.
Con il laboratorio 05, il partecipante può lavorare su AzureActivity, StorageBlobLogs o AppServiceHTTPLogs.
```

Quindi, per una UD08 più forte didatticamente, la Query Card autonoma va collocata **dopo** il collegamento delle risorse reali, oppure deve indicare chiaramente che l'assenza di tabelle reali è un limite dell'ambiente.

---

## 5. Sequenza tecnica interna del laboratorio 05

Il file `05_OBS_UD08_LAB_guidato_Tabelle_Azure_Reali_v5_4_partecipanti.md` segue una sequenza corretta.

| Task | Cosa fa | Perché è necessario |
|---|---|---|
| Task 1 | Carica `config/ud08.env`, recupera `WORKSPACE_ID` e `LAW_RESOURCE_ID` | `WORKSPACE_ID` serve per interrogare il LAW; `LAW_RESOURCE_ID` serve come destinazione dei diagnostic settings |
| Task 2 | Individua le risorse UD05 del partecipante | Evita di copiare i nomi delle risorse del docente |
| Task 3 | Esegue una query `datatable()` di test | Verifica che la CLI riesca a interrogare il workspace |
| Task 4 | Collega l'Activity Log della subscription al LAW | Abilita la tabella `AzureActivity` |
| Task 5 | Collega il Blob service dello Storage Account al LAW | Abilita la tabella `StorageBlobLogs` dopo traffico Blob |
| Task 6 | Collega la Web App/App Service al LAW | Abilita la tabella `AppServiceHTTPLogs` dopo traffico HTTP |
| Task 7 | Esegue riepilogo sulle tabelle reali | Verifica quali tabelle hanno ricevuto dati |
| Task 8 | Configura VM con AMA + DCR, opzionale | Abilita `Heartbeat`, `Perf`, `Syslog` o `Event` |
| Task 9 | Guida il troubleshooting | Aiuta a distinguere risultato vuoto, tabella assente, errore e ritardo di ingestione |
| Task 10-12 | Salva evidenze, aggiorna report e commit | Rende il lavoro documentabile e verificabile |

---

## 6. Collegamenti risorsa -> LAW da applicare

| Sorgente reale | Meccanismo | Destinazione | Tabella KQL attesa |
|---|---|---|---|
| Activity Log della subscription | Diagnostic setting a livello subscription | LAW UD08 | `AzureActivity` |
| Storage Account - Blob service | Diagnostic setting sul Blob service | LAW UD08 | `StorageBlobLogs` |
| Web App / App Service | Diagnostic setting sulla Web App | LAW UD08 | `AppServiceHTTPLogs` |
| VM Linux | Azure Monitor Agent + Data Collection Rule | LAW UD08 | `Heartbeat`, `Perf`, `Syslog` |
| VM Windows | Azure Monitor Agent + Data Collection Rule | LAW UD08 | `Heartbeat`, `Perf`, `Event` |

Le risorse infrastrutturali correlate, come App Service Plan, Public IP, Network Interface, VNet, NSG, Disk e NetworkWatcherRG, non sono sorgenti principali nel percorso base UD08.

---

## 7. Esempio di sequenza pratica da eseguire in aula

### Fase A - Preparazione concettuale

Leggere o spiegare:

```text
00_OBS_UD08_Concetti_DETTAGLIATO_v5_3.md
```

Obiettivo della fase:

```text
Capire che un workspace contiene tabelle, che KQL interroga tabelle e che datatable() non rappresenta dati reali Azure.
```

---

### Fase B - Laboratorio guidato KQL base

Eseguire:

```text
01_OBS_UD08_LAB_guidato_Log_Analytics_KQL_Base_v5_3.md
```

Azioni principali:

```text
1. verificare Azure CLI e login;
2. creare o verificare il LAW UD08;
3. recuperare WORKSPACE_ID;
4. aprire Logs nel Portale;
5. eseguire query datatable();
6. salvare evidenze.
```

Supporto operativo:

```text
04_OBS_UD08_GUIDA_OPERATIVA_KQL_Passo_Passo_v5_3.md
```

---

### Fase C - Collegamento da Portale delle risorse reali

Usare:

```text
06_OBS_UD08_GUIDA_PORTALE_Collegamenti_Risorse_LAW_v5_4.md
```

Azioni principali:

```text
1. Activity Log subscription -> LAW;
2. Storage Account / Blob service -> LAW;
3. Web App / App Service -> LAW;
4. VM -> LAW tramite AMA + DCR, se prevista.
```

Questa fase aiuta i partecipanti a vedere graficamente che il collegamento parte dalla sorgente, non dal LAW.

---

### Fase D - Laboratorio guidato sulle tabelle reali

Eseguire:

```text
05_OBS_UD08_LAB_guidato_Tabelle_Azure_Reali_v5_4_partecipanti.md
```

Azioni principali:

```text
1. individuare le risorse UD05 del partecipante;
2. aggiornare config/ud08.env;
3. recuperare LAW_RESOURCE_ID;
4. creare diagnostic settings;
5. generare evento amministrativo, traffico Blob e traffico HTTP;
6. attendere ingestione;
7. interrogare AzureActivity, StorageBlobLogs e AppServiceHTTPLogs;
8. salvare JSON, screenshot e report.
```

---

### Fase E - Laboratorio autonomo Query Card

Eseguire:

```text
03_OBS_UD08_LAB_autonomo_Query_Card_KQL_v5_3.md
```

Scopo:

```text
Produrre una scheda tecnica che collega domanda, query, risultato, limiti e variante migliorativa.
```

Scelta consigliata dopo il laboratorio 05:

```text
Usare almeno una tabella reale disponibile:
- AzureActivity;
- StorageBlobLogs;
- AppServiceHTTPLogs;
- Heartbeat / Perf / Syslog / Event, se VM configurata.
```

Se nessuna tabella reale è popolata, documentare il limite e usare `datatable()` o `Usage`.

---

## 8. Interpretazione corretta dei risultati

| Situazione | Interpretazione corretta | Azione |
|---|---|---|
| Query `datatable()` funziona | Il motore KQL risponde | Non dimostra ancora dati reali Azure |
| `AzureActivity`, `StorageBlobLogs` o `AppServiceHTTPLogs` restituiscono righe | Il collegamento risorsa -> LAW è riuscito e ci sono dati nel time range | Salvare evidenza e commentare il risultato |
| Query valida ma risultato vuoto | La tabella può essere interrogabile ma non contiene righe nel time range | Aumentare time range, attendere ingestione, generare traffico |
| Errore `Failed to resolve table or column expression` | La tabella non esiste ancora nel LAW o non è stata mai popolata | Verificare diagnostic setting, sorgente e modalità tabella |
| File JSON a 0 byte | Il comando è probabilmente fallito e l'errore è finito su `stderr` | Usare redirezione robusta con file `.err` |
| `Usage | count` restituisce 0 | Il workspace può essere valido ma povero di dati | Documentare il caso, non trattarlo automaticamente come errore |

---

## 9. Cosa deve risultare chiaro ai partecipanti

Alla fine della UD08 ogni partecipante deve saper dire:

1. Un LAW è il contenitore interrogabile, non il generatore automatico di tutti i log.
2. `datatable()` serve per imparare KQL anche senza dati reali.
3. Una tabella reale compare solo se una sorgente invia dati al LAW.
4. I diagnostic settings collegano Activity Log, Storage Blob e Web App al LAW.
5. Per la VM si usa AMA + DCR, non la vecchia diagnostica legacy come percorso standard.
6. Dopo il collegamento bisogna generare eventi o traffico.
7. L'ingestione può richiedere alcuni minuti.
8. Un risultato vuoto è diverso da un errore.
9. Le evidenze devono essere salvate nel repository locale.

---

## 10. Checklist finale partecipante

| Verifica | Stato |
|---|---|
| Ho letto i concetti UD08 | ☐ |
| Ho creato/verificato il LAW UD08 | ☐ |
| Ho recuperato `WORKSPACE_ID` | ☐ |
| Ho eseguito query `datatable()` | ☐ |
| Ho individuato le mie risorse UD05 | ☐ |
| Ho aggiornato `config/ud08.env` con risorse mie, non del docente | ☐ |
| Ho recuperato `LAW_RESOURCE_ID` | ☐ |
| Ho collegato Activity Log al LAW | ☐ |
| Ho generato un evento amministrativo | ☐ |
| Ho interrogato `AzureActivity` | ☐ |
| Ho collegato Blob service al LAW | ☐ |
| Ho generato traffico Blob | ☐ |
| Ho interrogato `StorageBlobLogs` | ☐ |
| Ho collegato Web App al LAW | ☐ |
| Ho generato traffico HTTP | ☐ |
| Ho interrogato `AppServiceHTTPLogs` | ☐ |
| Ho documentato eventuali risultati vuoti | ☐ |
| Ho salvato evidenze JSON e screenshot | ☐ |
| Ho compilato il report | ☐ |
| Ho svolto la Query Card autonoma | ☐ |

---

## 11. Formula didattica da usare in aula

```text
Il LAW non osserva automaticamente tutto.
Prima colleghiamo la sorgente.
Poi generiamo eventi.
Poi interroghiamo la tabella KQL prodotta.
```

Esempi:

```text
Web App -> diagnostic setting -> richieste HTTP -> AppServiceHTTPLogs
```

```text
Storage Blob -> diagnostic setting -> upload/list/download/delete -> StorageBlobLogs
```

```text
Activity Log subscription -> diagnostic setting -> modifica amministrativa -> AzureActivity
```

```text
VM -> AMA + DCR -> segnali guest OS -> Heartbeat / Perf / Syslog / Event
```

---

## 12. Conclusione

Il percorso UD08 è coerente se viene letto in due livelli:

1. **livello base**: usare `datatable()` per imparare KQL in modo controllato;
2. **livello reale**: collegare risorse Azure al LAW e interrogare le tabelle effettivamente popolate.

La UD08 non deve essere presentata come un laboratorio in cui il LAW contiene dati automaticamente. Deve essere presentata come un percorso in cui i partecipanti imparano prima il linguaggio KQL e poi configurano la raccolta dei segnali reali verso il workspace.
