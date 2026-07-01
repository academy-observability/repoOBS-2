# OBS_UD07 - Concetti aggiuntivi
# Granularità nelle metriche Azure Monitor

## 1. Obiettivo del documento

Questo documento integra i concetti della UD07 e chiarisce il significato di **granularità** quando osserviamo metriche in Azure Monitor.

Nel laboratorio UD07 generiamo segnali controllati su risorse Azure e poi osserviamo le metriche prima e dopo l’attività. Per interpretare correttamente i grafici è necessario distinguere tre concetti:

| Concetto | Significato sintetico |
|---|---|
| Intervallo osservato | quanto tempo complessivo stiamo guardando |
| Granularità | quanto è grande ogni blocco temporale del grafico |
| Aggregazione | come Azure riassume i valori dentro ogni blocco temporale |

La granularità non dice “quanto tempo guardo”. Dice **ogni quanto voglio un punto sul grafico**.

---

## 2. Definizione pratica di granularità

Nel contesto di Azure Monitor, la **granularità** è la dimensione dei blocchi temporali con cui Azure raggruppa i dati di una metrica.

Detto in modo pratico:

```text
Granularità = ogni quanto voglio vedere un punto sul grafico.
```

Detto in modo più tecnico:

```text
La granularità stabilisce l’ampiezza temporale di ogni intervallo di aggregazione della metrica.
```

Esempio:

```text
Se osservo le ultime 3 ore con granularità 1 minuto, ottengo molti punti.
Se osservo le ultime 3 ore con granularità 1 ora, ottengo pochi punti.
```

La metrica è la stessa, ma il dettaglio temporale cambia molto.

---

## 3. Intervallo osservato e granularità non sono la stessa cosa

Supponiamo di osservare le metriche dell’App Service nell’ultima ora.

```text
Intervallo osservato: ultime 1 ora
```

Ora dobbiamo decidere con quale dettaglio temporale vogliamo visualizzare quell’ora.

| Granularità | Numero indicativo di punti sul grafico |
|---|---:|
| 1 minuto | 60 punti |
| 5 minuti | 12 punti |
| 15 minuti | 4 punti |
| 1 ora | 1 punto |

Quindi:

```text
Ultima ora = quanto tempo guardo.
Granularità 1 minuto = quanto è fine il dettaglio.
```

Nel Portale Azure questa impostazione si trova normalmente in:

```text
Risorsa
→ Monitoring
→ Metrics
→ Time range
→ Time granularity
```

Nella CLI Azure la granularità viene indicata con `--interval`.

Esempio:

```bash
# Esempio su App Service.
# Il parametro --interval PT1M indica che ogni punto rappresenta 1 minuto.
# Non significa che stiamo osservando solo l’ultimo minuto.
az monitor metrics list \
  --resource "$APP_ID" \
  --metric "Requests" \
  --interval PT1M \
  --aggregation Total \
  --output table
```

Il valore:

```text
PT1M
```

significa:

```text
raggruppa i dati in blocchi da 1 minuto.
```

Non significa:

```text
guarda solo 1 minuto di dati.
```

---

## 4. Formato dei valori di granularità nella CLI

Azure CLI usa durate in formato ISO 8601.

| Valore CLI | Significato |
|---|---|
| `PT1M` | 1 minuto |
| `PT5M` | 5 minuti |
| `PT15M` | 15 minuti |
| `PT1H` | 1 ora |
| `P1D` | 1 giorno |

Esempio:

```bash
# Ogni punto della metrica rappresenta un intervallo di 5 minuti.
az monitor metrics list \
  --resource "$VM_ID" \
  --metric "Percentage CPU" \
  --interval PT5M \
  --aggregation Average Maximum \
  --output table
```

In questo comando:

| Parte del comando | Significato |
|---|---|
| `--metric "Percentage CPU"` | metrica osservata |
| `--interval PT5M` | granularità di 5 minuti |
| `--aggregation Average Maximum` | calcolo della media e del massimo per ogni blocco |

---

## 5. Granularità e aggregazione

La granularità e l’aggregazione lavorano insieme, ma non sono la stessa cosa.

```text
Granularità = quanto dura ogni blocco temporale.
Aggregazione = come riassumo i valori dentro quel blocco.
```

Esempio su una VM con metrica `Percentage CPU`.

Supponiamo che in un blocco di 5 minuti i valori siano questi:

| Minuto | CPU |
|---|---:|
| 10:00 | 5% |
| 10:01 | 5% |
| 10:02 | 90% |
| 10:03 | 5% |
| 10:04 | 5% |

Con granularità 5 minuti, Azure può restituire valori diversi a seconda dell’aggregazione scelta.

| Aggregazione | Valore risultante |
|---|---:|
| Average | 22% |
| Maximum | 90% |
| Minimum | 5% |

Interpretazione:

```text
Average mostra il carico medio.
Maximum evidenzia il picco.
Minimum mostra il valore minimo osservato.
```

Domanda docente:

```text
Quale aggregazione useresti per vedere se ci sono stati picchi brevi?
```

Risposta attesa:

```text
Maximum.
```

Domanda docente:

```text
Quale aggregazione useresti per capire il carico medio?
```

Risposta attesa:

```text
Average.
```

---

## 6. Esempio App Service: metrica Requests

Nel laboratorio UD07 generiamo richieste HTTP verso l’App Service. La metrica da osservare è spesso:

```text
Requests
```

Scenario di esempio:

```text
10:00 - 10:10   nessuna richiesta
10:11 - 10:12   40 richieste
10:13 - 11:00   nessuna richiesta
```

### 6.1 Lettura con granularità 1 minuto

| Minuto | Requests |
|---|---:|
| 10:10 | 0 |
| 10:11 | 20 |
| 10:12 | 20 |
| 10:13 | 0 |

Interpretazione:

```text
Il traffico è concentrato in due minuti.
```

Con granularità fine riusciamo a vedere quando è avvenuto il traffico.

### 6.2 Lettura con granularità 15 minuti

| Intervallo | Requests |
|---|---:|
| 10:00-10:15 | 40 |
| 10:15-10:30 | 0 |
| 10:30-10:45 | 0 |
| 10:45-11:00 | 0 |

Interpretazione:

```text
Sappiamo che ci sono state 40 richieste tra le 10:00 e le 10:15,
ma perdiamo il dettaglio sui minuti esatti.
```

Conclusione:

```text
Granularità più fine = più dettaglio.
Granularità più larga = vista più sintetica.
```

---

## 7. Esempio VM: Percentage CPU

La granularità è particolarmente importante quando cerchiamo picchi brevi.

Scenario:

```text
10:00-10:14   CPU 0%
10:15         CPU 100%
10:16-10:30   CPU 0%
```

### 7.1 Granularità 1 minuto, aggregazione Maximum

| Minuto | Maximum CPU |
|---|---:|
| 10:14 | 0% |
| 10:15 | 100% |
| 10:16 | 0% |

Interpretazione:

```text
Il picco è visibile.
```

### 7.2 Granularità 15 minuti, aggregazione Average

| Intervallo | Average CPU |
|---|---:|
| 10:00-10:15 | circa 6,7% |
| 10:15-10:30 | circa 0% |

Interpretazione:

```text
Il picco quasi sparisce perché viene mediato con molti valori bassi.
```

Frase chiave:

```text
Una granularità larga può nascondere picchi brevi.
```

Per cercare picchi:

```text
Granularità fine + aggregazione Maximum.
```

Per leggere un comportamento medio:

```text
Granularità più ampia + aggregazione Average.
```

---

## 8. Esempio Storage Account: Transactions

Nel laboratorio UD07 generiamo operazioni Blob, per esempio upload, list, download e delete.

La metrica da osservare è spesso:

```text
Transactions
```

Scenario:

```text
Il partecipante genera traffico Storage per circa 2 minuti.
```

### 8.1 Granularità 1 minuto

| Minuto | Transactions |
|---|---:|
| 11:00 | 40 |
| 11:01 | 45 |
| 11:02 | 0 |

Interpretazione:

```text
Vediamo chiaramente quando è stato eseguito il test.
```

### 8.2 Granularità 1 ora

| Ora | Transactions |
|---|---:|
| 11:00-12:00 | 85 |

Interpretazione:

```text
Sappiamo che nell’ora ci sono state 85 transazioni,
ma non vediamo più in quali minuti si sono concentrate.
```

Conclusione:

```text
Se sto facendo un laboratorio breve, uso granularità fine.
Se sto osservando un trend giornaliero, posso usare granularità più ampia.
```

---

## 9. Granularità durante il laboratorio UD07

Durante la generazione controllata dei segnali, le attività durano pochi minuti. Per questo motivo conviene usare granularità fine.

Scelte consigliate:

| Scenario UD07 | Granularità consigliata | Aggregazione consigliata |
|---|---|---|
| App Service, Requests | `PT1M` | `Total` |
| Storage Account, Transactions | `PT1M` | `Total` |
| VM, Percentage CPU | `PT1M` o `PT5M` | `Average` e `Maximum` |
| Analisi veloce di traffico breve | `PT1M` | dipende dalla metrica |
| Analisi di tendenza più lunga | `PT15M`, `PT1H` | `Average`, `Total` o `Maximum` |

Esempio App Service:

```bash
# Lettura delle richieste HTTP con granularità 1 minuto.
# Total è adatto perché vogliamo contare quante richieste sono arrivate in ogni minuto.
az monitor metrics list \
  --resource "$APP_ID" \
  --metric "Requests" \
  --interval PT1M \
  --aggregation Total \
  --output table
```

Esempio Storage Account:

```bash
# Lettura delle transazioni Storage con granularità 1 minuto.
# Total mostra quante transazioni sono state registrate in ogni blocco temporale.
az monitor metrics list \
  --resource "$STORAGE_ID" \
  --metric "Transactions" \
  --interval PT1M \
  --aggregation Total \
  --output table
```

Esempio VM:

```bash
# Lettura della CPU della VM con granularità 1 minuto.
# Average mostra il carico medio, Maximum aiuta a individuare picchi.
az monitor metrics list \
  --resource "$VM_ID" \
  --metric "Percentage CPU" \
  --interval PT1M \
  --aggregation Average Maximum \
  --output table
```

---

## 10. Errori comuni da evitare

### Errore 1: confondere `PT1M` con il time range

Errore:

```text
Ho messo PT1M, quindi sto guardando solo un minuto.
```

Correzione:

```text
No. PT1M indica la granularità dei punti.
L’intervallo temporale osservato è un’altra impostazione.
```

### Errore 2: concludere troppo presto che una risorsa non ha traffico

Errore:

```text
Non vedo valori, quindi la risorsa non funziona.
```

Correzione:

```text
Potrebbe non esserci traffico nel periodo osservato.
Potrebbe esserci un ritardo di popolamento della metrica.
Potrebbe essere stato scelto un time range sbagliato.
Potrebbe essere stata scelta una granularità poco adatta.
```

### Errore 3: cercare picchi usando solo Average

Errore:

```text
La CPU media è bassa, quindi non ci sono stati picchi.
```

Correzione:

```text
Average può nascondere picchi brevi.
Per cercare picchi bisogna confrontare anche Maximum.
```

### Errore 4: usare granularità troppo larga durante un test breve

Errore:

```text
Ho generato traffico per 2 minuti e guardo il grafico con granularità 1 ora.
```

Correzione:

```text
Con granularità 1 ora il test breve viene schiacciato dentro un solo punto.
Durante UD07 è meglio usare PT1M o PT5M.
```

---

## 11. Metafora didattica

La granularità è lo **zoom temporale** del grafico.

| Granularità | Metafora | Cosa permette di vedere |
|---|---|---|
| 1 minuto | microscopio | dettagli fini, picchi brevi, test di laboratorio |
| 15 minuti | vista intermedia | andamento sintetico senza troppo rumore |
| 1 ora | binocolo | tendenza generale |
| 1 giorno | vista storica | andamento di lungo periodo |

Sintesi:

```text
Granularità fine = più dettaglio, più punti, più rumore.
Granularità larga = meno dettaglio, meno punti, più sintesi.
```

---

## 12. Mini-checkpoint docente

### Domanda 1

```text
Che differenza c’è tra osservare Requests con granularità 1 minuto e granularità 15 minuti?
```

Risposta attesa:

```text
Con 1 minuto vedo meglio quando sono arrivate le richieste.
Con 15 minuti vedo un dato più aggregato e perdo dettaglio temporale.
```

### Domanda 2

```text
Perché un picco CPU può sparire guardando Average su una granularità larga?
```

Risposta attesa:

```text
Perché il valore alto viene mediato insieme a molti valori bassi.
```

### Domanda 3

```text
Quale combinazione useresti per cercare picchi brevi?
```

Risposta attesa:

```text
Granularità fine e aggregazione Maximum.
```

### Domanda 4

```text
Quale combinazione useresti per leggere un andamento generale?
```

Risposta attesa:

```text
Granularità più ampia e aggregazione Average o Total, a seconda della metrica.
```

### Domanda 5

```text
Nel comando az monitor metrics list, cosa indica --interval PT1M?
```

Risposta attesa:

```text
Indica che ogni punto della metrica rappresenta un blocco temporale di 1 minuto.
Non indica che stiamo osservando solo 1 minuto complessivo.
```

---

## 13. Frase da inserire nel report UD07

Nel report del laboratorio, il partecipante può scrivere:

```text
Durante la generazione controllata dei segnali è stata usata una granularità fine, ad esempio PT1M, perché le attività di test duravano pochi minuti.

La granularità fine ha permesso di osservare meglio quando si sono concentrati richieste HTTP, transazioni Storage o eventuali picchi CPU.

Per la metrica Percentage CPU è stato utile confrontare Average e Maximum, perché la media può nascondere picchi brevi.
```

---

## 14. Sintesi finale

```text
Granularità = quanto è grande ogni finestra temporale.
Aggregazione = come riassumo i dati dentro quella finestra.
Intervallo osservato = quanto tempo complessivo sto guardando.
```

Esempio finale:

| Configurazione | Risultato |
|---|---|
| ultime 3 ore con granularità 1 minuto | 180 punti, molto dettaglio |
| ultime 3 ore con granularità 15 minuti | 12 punti, meno dettaglio |
| ultime 3 ore con granularità 1 ora | 3 punti, vista sintetica |

Per UD07, durante i test controllati:

```text
PT1M o PT5M sono spesso le scelte più adatte.
```

Per analisi storiche:

```text
PT15M, PT1H o granularità superiori sono più adatte a leggere la tendenza generale.
```
