# OBS_UD00 - Concetti: ambiente, repository e workflow del corso

## 1. Perché iniziamo dall’ambiente

Nel percorso Observability lavoreremo con comandi, servizi, container, log, metriche, repository Git e piattaforme cloud. Prima di introdurre strumenti come Azure Monitor, Prometheus, Grafana o pipeline CI/CD, è necessario avere un ambiente locale stabile e ripetibile.

La giornata iniziale serve a costruire una base comune. Non è solo una fase di installazione: è il primo esercizio di metodo tecnico.

Nel corso useremo sempre questa sequenza:

```text
eseguiamo un’azione -> osserviamo l’effetto -> raccogliamo evidenza -> interpretiamo -> documentiamo -> versioniamo
```

Questa sequenza è già una forma elementare di lavoro osservabile.

---

## 2. WSL2 e Ubuntu

WSL2 permette di usare un ambiente Linux dentro Windows. Per questo corso è utile perché molti strumenti DevOps e Observability sono più naturali da usare in ambiente Linux:

- shell Bash;
- comandi di diagnostica;
- gestione file e permessi;
- Docker e container;
- script di automazione;
- strumenti cloud CLI.

Lavoreremo preferibilmente nella home Linux, ad esempio:

```bash
/home/nomeutente/corso_obs
```

Eviteremo di lavorare direttamente in percorsi Windows come:

```text
/mnt/c/Users/...
```

Questo riduce problemi di performance, permessi e path.

---

## 3. Git e repository

Git verrà usato per tracciare il lavoro svolto. Ogni laboratorio produrrà file, report, script o configurazioni che dovranno essere salvati nel repository personale.

I comandi base che useremo spesso sono:

```bash
git status
git add .
git commit -m "messaggio"
git push
```

Il commit non è una formalità: è una fotografia verificabile dello stato del lavoro.

---

## 4. Docker

Docker permette di eseguire applicazioni in container. Un container è un ambiente isolato che contiene tutto ciò che serve per eseguire un servizio.

Nel percorso useremo Docker per:

- eseguire servizi locali;
- simulare ambienti applicativi;
- leggere log container;
- costruire immagini;
- preparare deploy su cloud;
- creare stack di monitoraggio locali.

In questa UD non approfondiamo ancora Docker. Verifichiamo solo che sia disponibile e funzionante.

---

## 5. VS Code e Remote WSL

VS Code sarà usato come editor. È importante aprirlo dal terminale WSL nella cartella corretta:

```bash
code .
```

In questo modo VS Code lavora direttamente sul filesystem Linux, evitando confusione tra Windows e Ubuntu.

---

## 6. Evidenze tecniche

Ogni laboratorio deve produrre evidenze. Un’evidenza è un file, uno screenshot, un output o un report che dimostra che un’attività è stata svolta e compresa.

Esempi di evidenze:

- output di `docker version`;
- output di `git status`;
- report Markdown con comandi e risultati;
- file di log;
- script funzionante;
- screenshot mirato solo quando necessario.

Una buona evidenza non mostra solo “funziona”, ma permette di capire **che cosa è stato verificato**.

---

## 7. Metodo di consegna

Per ogni UD useremo una logica simile:

```text
cartella UD/lab -> file prodotti -> report -> commit -> push
```

Prima di consegnare è necessario controllare:

```bash
git status
```

Dopo il push è utile verificare sul repository remoto che i file siano realmente presenti.

---

## 8. Concetti chiave della giornata

| Concetto | Significato operativo |
|---|---|
| Ambiente ripetibile | Tutti lavorano su una base tecnica simile |
| Repository | Spazio di lavoro versionato |
| Commit | Salvataggio verificabile di una fase del lavoro |
| Push | Pubblicazione del lavoro sul repository remoto |
| Evidenza | Prova tecnica del lavoro svolto |
| Container | Esecuzione isolata di un servizio |
| Workflow | Sequenza ordinata di lavoro tecnico |

---

## 9. Collegamento con la prossima UD

Nella prossima giornata lavoreremo su Linux: filesystem, file, comandi testuali, redirection e pipe. L’ambiente configurato oggi sarà quindi il punto di partenza di tutte le attività successive.
