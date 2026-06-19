# OBS_UD02 - Concetti

## 1. Perché permessi e processi sono importanti per l'Observability

Nella UD01 abbiamo lavorato su filesystem, file testuali, redirection, pipe e report tecnici. In questa UD facciamo un passo successivo: osserviamo il comportamento locale del sistema quando qualcosa non funziona.

Nel lavoro operativo reale molti problemi iniziano con sintomi molto semplici:

- un file non è leggibile;
- uno script non parte;
- un processo resta attivo;
- una porta risulta già occupata;
- un servizio non accetta connessioni;
- il processo giusto non è quello che pensavamo.

Prima di usare piattaforme di monitoraggio, dobbiamo saper rispondere a domande di base:

```text
Chi sta eseguendo il comando?
Con quali permessi?
Quale processo è attivo?
Quale PID lo identifica?
Quale porta sta usando?
Come lo fermiamo senza fare danni?
```

Questa UD non è una lezione generica di amministrazione Linux. È una preparazione diretta alle attività successive su servizi HTTP, container, log applicativi, metriche, alert e troubleshooting.

---

## 2. Utenti, gruppi e identità di esecuzione

Ogni processo Linux viene eseguito con un'identità. Questa identità determina quali file può leggere, quali file può modificare e quali risorse può usare.

I comandi principali sono:

```bash
whoami
id
groups
```

`whoami` mostra il nome dell'utente corrente.

`id` mostra UID, GID e gruppi associati all'utente.

`groups` mostra i gruppi di appartenenza.

Esempio:

```bash
whoami
id
groups
```

Output indicativo:

```text
student
uid=1000(student) gid=1000(student) groups=1000(student),27(sudo)
student sudo
```

Questo output ci dice che l'utente corrente è `student`, che ha un identificativo numerico e che appartiene ad almeno un gruppo principale.

In Observability questa informazione diventa importante quando un servizio non riesce a leggere un file di configurazione, scrivere un log o aprire una risorsa.

---

## 3. Permessi Unix: lettura, scrittura, esecuzione

In Linux i permessi base sono tre:

| Permesso | Simbolo | Su file | Su directory |
|---|---|---|---|
| lettura | `r` | permette di leggere il contenuto | permette di elencare i nomi, se combinato correttamente |
| scrittura | `w` | permette di modificare il file | permette di creare, rinominare o cancellare elementi nella directory |
| esecuzione | `x` | permette di eseguire uno script/binario | permette di attraversare la directory |

Il significato di `x` sulle directory è spesso la parte meno intuitiva. Su una directory, `x` non significa "eseguire la directory". Significa poterla attraversare, cioè poter entrare nel percorso.

Esempio:

```bash
ls -l file.txt
```

Output indicativo:

```text
-rw-r--r-- 1 student student 120 Jun 17 10:00 file.txt
```

La prima colonna va letta così:

```text
- rw- r-- r--
| |   |   |
| |   |   altri utenti
| |   gruppo
| proprietario
file normale
```

---

## 4. Permessi simbolici e permessi ottali

I permessi possono essere modificati in forma simbolica o ottale.

Esempi simbolici:

```bash
chmod u+x script.sh
chmod g-w file.txt
chmod o-r file.txt
chmod a+r file.txt
```

Significato:

| Comando | Significato |
|---|---|
| `u+x` | aggiunge esecuzione al proprietario |
| `g-w` | rimuove scrittura al gruppo |
| `o-r` | rimuove lettura agli altri |
| `a+r` | aggiunge lettura a tutti |

Esempi ottali:

```bash
chmod 600 secret.txt
chmod 644 report.txt
chmod 755 script.sh
```

Significato:

| Valore | Permessi | Uso tipico |
|---:|---|---|
| `600` | `rw-------` | file privato leggibile/scrivibile solo dal proprietario |
| `644` | `rw-r--r--` | file leggibile da tutti, modificabile dal proprietario |
| `755` | `rwxr-xr-x` | script eseguibile dal proprietario e leggibile/eseguibile dagli altri |

---

## 5. `umask`: i permessi predefiniti non nascono dal nulla

Quando creiamo un file o una directory, Linux applica una maschera chiamata `umask`. Questa maschera limita i permessi predefiniti.

Verifica:

```bash
umask
```

Esempio comune:

```text
0022
```

Questo significa che i nuovi file e le nuove directory avranno permessi meno permissivi rispetto al massimo teorico.

In questa UD non modifichiamo stabilmente la `umask`. Ci basta sapere che i permessi iniziali dei file possono variare leggermente tra ambienti diversi.

---

## 6. Processi e PID

Un processo è un programma in esecuzione. Ogni processo ha un identificativo numerico chiamato PID.

Comandi principali:

```bash
ps
ps -ef
ps -eo pid,ppid,comm,%cpu,%mem --sort=-%cpu | head
pgrep nomeprocesso
```

Esempio:

```bash
sleep 300 &
pgrep sleep
```

Il simbolo `&` avvia il processo in background. Il processo continua a girare mentre il terminale resta disponibile.

Per vedere un processo specifico:

```bash
ps -p <PID> -o pid,ppid,comm,etime,%cpu,%mem
```

Questa forma è utile perché restituisce solo le informazioni rilevanti.

---

## 7. Segnali: chiedere a un processo di terminare o forzarlo

Per terminare un processo usiamo il comando `kill`, che in realtà invia un segnale.

I segnali più usati in questa UD sono:

| Segnale | Numero | Significato |
|---|---:|---|
| `SIGTERM` | 15 | richiesta ordinata di terminazione |
| `SIGKILL` | 9 | terminazione forzata, non intercettabile |

Esempi:

```bash
kill -15 <PID>
kill -9 <PID>
```

`SIGTERM` è preferibile perché consente al processo di chiudersi in modo ordinato. `SIGKILL` va usato solo quando il processo non risponde, perché non gli lascia modo di completare operazioni di cleanup.

Nel troubleshooting reale, la differenza è importante. Terminare brutalmente un processo può lasciare file temporanei, connessioni interrotte o stati incoerenti.

---

## 8. Porte occupate e servizi in ascolto

Molti servizi espongono una porta TCP. Se una porta è già occupata, un secondo processo non può usarla.

Sintomo tipico:

```text
Address already in use
```

Su Linux possiamo usare:

```bash
ss -ltnp | grep 8080
```

Significato delle opzioni:

| Opzione | Significato |
|---|---|
| `-l` | mostra socket in ascolto |
| `-t` | mostra TCP |
| `-n` | mostra numeri invece di nomi risolti |
| `-p` | mostra processo associato, quando possibile |

Su macOS possiamo usare:

```bash
lsof -iTCP:8080 -sTCP:LISTEN
```

L'obiettivo non è imparare un comando a memoria. L'obiettivo è rispondere alla domanda operativa:

```text
Quale processo sta occupando la porta?
```

---

## 9. Metodo di troubleshooting della UD02

Durante la giornata usiamo sempre la stessa sequenza:

```text
sintomo -> ipotesi -> comando di verifica -> interpretazione -> azione correttiva -> evidenza
```

Esempio su permessi:

| Passo | Esempio |
|---|---|
| Sintomo | `Permission denied` |
| Ipotesi | manca un permesso su file o directory |
| Verifica | `ls -l`, `stat`, `id` |
| Interpretazione | l'utente corrente non ha lettura/esecuzione |
| Azione | `chmod` mirato |
| Evidenza | comando eseguito, output prima/dopo, spiegazione |

Esempio su porta occupata:

| Passo | Esempio |
|---|---|
| Sintomo | `Address already in use` |
| Ipotesi | un altro processo ascolta sulla stessa porta |
| Verifica | `ss -ltnp` oppure `lsof` |
| Interpretazione | individuazione del PID |
| Azione | terminazione controllata del PID corretto |
| Evidenza | output prima/dopo |

---

## 10. Collegamento con le prossime UD

Nella UD03 useremo queste competenze per diagnosticare rete, DNS, HTTP e raggiungibilità.

Nella UD04 le useremo per gestire un primo servizio osservabile locale.

Più avanti, quando lavoreremo con Docker, Azure, pipeline e sistemi di monitoraggio, questi concetti torneranno con nomi diversi ma con la stessa logica:

```text
chi esegue?
con quali permessi?
quale processo?
quale porta?
quale log?
quale evidenza?
```
