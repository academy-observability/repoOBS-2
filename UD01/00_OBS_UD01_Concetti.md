# OBS_UD01 - Concetti

## 1. Perché partiamo da Linux, file e testo

Nel percorso Observability lavoreremo spesso con strumenti più complessi: container, pipeline, Azure Monitor, Log Analytics, Prometheus, Grafana, ELK e sistemi di alerting.

Prima di arrivare a questi strumenti dobbiamo essere in grado di fare una cosa molto semplice, ma fondamentale: **osservare un sistema attraverso file, output e log**.

Un log, prima di essere visualizzato in una dashboard, è spesso una sequenza di righe testuali. Una metrica, prima di essere tracciata in un grafico, può essere estratta da un output. Un problema operativo, prima di essere spiegato, deve essere documentato con evidenze.

In questa giornata lavoriamo quindi su:

- orientamento nel filesystem Linux;
- gestione di file e directory;
- lettura di file testuali;
- stream standard di input/output;
- redirection;
- pipe;
- filtri su log;
- produzione di report tecnici.

---

## 2. Filesystem Linux: cartelle, path e posizione corrente

In Linux tutto viene rappresentato all’interno di un albero di directory. La radice dell’albero è:

```text
/
```

Da lì si sviluppano directory di sistema, directory utente, directory temporanee e mount point.

Esempi comuni:

| Percorso | Significato |
|---|---|
| `/home` | contiene le home directory degli utenti |
| `/home/nomeutente` | home directory di un utente |
| `/etc` | configurazioni di sistema |
| `/var/log` | log di sistema e servizi |
| `/tmp` | file temporanei |
| `/mnt/c` | disco Windows `C:` visto da WSL |

Nel corso lavoriamo preferibilmente nella home Linux, per esempio:

```bash
~/corso_obs/NOME-REPOSITORY
```

Il simbolo `~` indica la home directory dell’utente corrente.

---

## 3. Path assoluti e path relativi

Un **path assoluto** parte dalla radice `/`.

Esempio:

```bash
/home/studente/corso_obs/repo/labs/ud01
```

Un **path relativo** parte dalla directory corrente.

Esempio:

```bash
logs/work
```

Se ci troviamo in:

```bash
~/corso_obs/repo/labs/ud01
```

allora `logs/work` indica:

```bash
~/corso_obs/repo/labs/ud01/logs/work
```

Questa distinzione è importante perché molti errori nei laboratori derivano dal fatto che un comando viene eseguito nella cartella sbagliata.

---

## 4. File, directory e operazioni di base

I comandi minimi che usiamo sono:

| Comando | Uso principale |
|---|---|
| `pwd` | mostra la directory corrente |
| `ls` | elenca file e directory |
| `ls -la` | elenca anche file nascosti e dettagli |
| `mkdir` | crea directory |
| `mkdir -p` | crea directory anche annidate |
| `touch` | crea un file vuoto o aggiorna la data di modifica |
| `cp` | copia file o directory |
| `mv` | sposta o rinomina |
| `rm` | elimina file |
| `cat` | visualizza o concatena contenuti |
| `less` | legge file lunghi in modo navigabile |
| `find` | cerca file e directory secondo criteri |

📌 **Nota didattica**

Nel percorso useremo spesso `mkdir -p` perché permette di creare strutture annidate in modo ripetibile. Se una directory esiste già, il comando non genera errore.

---

## 5. Output, input e stream standard

Quando un comando Linux viene eseguito, normalmente lavora con tre stream:

| Stream | Nome | Funzione |
|---|---|---|
| `stdin` | standard input | input del comando |
| `stdout` | standard output | output normale |
| `stderr` | standard error | errori e messaggi diagnostici |

Esempio:

```bash
ls -la
```

Il risultato viene scritto su `stdout`, quindi appare nel terminale.

Se proviamo a leggere un file inesistente:

```bash
cat file_inesistente.txt
```

il messaggio di errore viene scritto su `stderr`.

Questa distinzione diventerà importante quando lavoreremo con script, container e pipeline.

---

## 6. Redirection: salvare output in file

La redirection permette di mandare l’output di un comando in un file.

| Operatore | Significato |
|---|---|
| `>` | scrive in un file sovrascrivendo il contenuto esistente |
| `>>` | aggiunge in fondo al file |
| `<` | usa un file come input |
| `2>` | salva lo stream degli errori |
| `&>` | salva output normale ed errori nello stesso file |

Esempio:

```bash
echo "Prima riga" > report.md
echo "Seconda riga" >> report.md
```

Dopo questi comandi, `report.md` contiene due righe.

⚠️ **Attenzione**

`>` sovrascrive il file. Se il file contiene già dati importanti, vengono persi.

---

## 7. Pipe: collegare più comandi

La pipe `|` prende l’output di un comando e lo passa come input al comando successivo.

Esempio:

```bash
cat access.log | grep " 500 "
```

Il comando legge `access.log`, poi passa le righe a `grep`, che mostra solo quelle contenenti `500`.

In molti casi possiamo scrivere anche:

```bash
grep " 500 " access.log
```

La pipe diventa utile quando vogliamo concatenare più trasformazioni:

```bash
awk '{print $3}' access.log | sort | uniq -c | sort -nr
```

Questa sequenza:

1. estrae il terzo campo;
2. ordina i valori;
3. conta le occorrenze duplicate consecutive;
4. ordina il risultato dal più frequente al meno frequente.

---

## 8. Log testuali e analisi minima

Un log applicativo può contenere righe simili a questa:

```text
2026-06-17T10:01:02Z GET /api/users 200 45ms
```

Possiamo leggere la riga come:

| Campo | Valore | Significato |
|---|---|---|
| timestamp | `2026-06-17T10:01:02Z` | quando è avvenuto l’evento |
| metodo | `GET` | metodo HTTP |
| endpoint | `/api/users` | risorsa richiesta |
| status | `200` | esito HTTP |
| durata | `45ms` | tempo di risposta |

Già con comandi semplici possiamo ottenere informazioni operative:

| Domanda | Comando utile |
|---|---|
| Quante righe contiene il log? | `wc -l access.log` |
| Quanti errori 5xx sono presenti? | `grep -E ' 5[0-9]{2} ' access.log` |
| Quali endpoint sono più chiamati? | `awk '{print $3}' access.log \| sort \| uniq -c \| sort -nr` |
| Quali richieste sono lente? | `awk` filtrando la durata |

Questo è un primo livello di Observability: non stiamo ancora usando dashboard o strumenti avanzati, ma stiamo già trasformando eventi grezzi in evidenze.

---

## 9. Report tecnico ed evidenza

Nel corso non basta dire “funziona” o “non funziona”. Dobbiamo produrre evidenze.

Una buona evidenza contiene:

- comando eseguito;
- output rilevante;
- breve interpretazione;
- eventuale problema incontrato;
- conclusione tecnica.

Esempio:

````md
## Conteggio errori HTTP

Comando eseguito:

```bash
grep -E ' (4|5)[0-9]{2} ' access.log | wc -l
```

Risultato:

```text
5
```

Interpretazione:

Sono presenti 5 richieste con status HTTP di errore client o server.
````

---

## 10. Collegamento con le prossime UD

Questa UD prepara direttamente:

| Prossima area | Collegamento |
|---|---|
| UD02 - permessi/processi | useremo comandi per verificare file, permessi, processi e script |
| UD03 - rete | useremo output di comandi come evidenza diagnostica |
| UD04 - servizio osservabile | analizzeremo log generati da una piccola applicazione |
| Azure/KQL | la logica di filtro e selezione sarà simile, ma su piattaforma cloud |
| Prometheus/Grafana/ELK | i dati verranno visualizzati da strumenti, ma il ragionamento parte sempre dalle evidenze |

---

## 11. Domande di consolidamento

1. Che differenza c’è tra path assoluto e path relativo?
2. Perché nel corso lavoriamo nella home Linux e non direttamente in `/mnt/c`?
3. Che differenza c’è tra `>` e `>>`?
4. Che differenza c’è tra redirection e pipe?
5. Perché `sort | uniq -c` richiede che i dati siano ordinati?
6. Perché un file di log è una fonte di osservabilità?
7. Quali elementi minimi dovrebbe contenere un report tecnico?
8. Perché è utile salvare le evidenze nel repository?
