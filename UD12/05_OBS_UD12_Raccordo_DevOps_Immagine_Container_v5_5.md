# UD12 - Raccordo finale
## Dall'immagine locale al ciclo DevOps automatizzato

---

# 1. Che cosa abbiamo imparato

In questa UD abbiamo costruito una piccola applicazione, l'abbiamo trasformata in una immagine Docker e l'abbiamo eseguita come container locale.

Il flusso realizzato è stato:

```text
codice sorgente
   -> Dockerfile
   -> docker build
   -> immagine locale
   -> docker run
   -> container locale
   -> test HTTP
   -> log
```

---

# 2. Perché questo è importante per DevOps

Una pipeline DevOps non dovrebbe improvvisare il deployment partendo da file copiati manualmente.

Deve invece lavorare su unità tecniche ripetibili e versionabili.

Nel nostro caso, questa unità è l'immagine container.

La pipeline potrà, in un passaggio successivo del percorso:

```text
leggere il codice
   -> costruire l'immagine
   -> assegnare un tag
   -> pubblicarla in un registry
   -> distribuirla in un ambiente
   -> verificare che risponda
```

Quindi la UD12 prepara il pezzo tecnico fondamentale: la costruzione corretta dell'immagine.

---

# 3. Che cosa deve restare chiaro

## 3.1 Il repository contiene codice

Il repository contiene:

- codice sorgente;
- Dockerfile;
- requirements;
- documentazione;
- evidenze.

## 3.2 L'immagine contiene un'app eseguibile

L'immagine contiene:

- runtime;
- dipendenze;
- codice;
- configurazione base;
- comando di avvio.

## 3.3 Il container è l'esecuzione dell'immagine

Il container è il processo applicativo in esecuzione a partire dall'immagine.

---

# 4. Perché i log restano centrali

Containerizzare l'app non significa perdere visibilità.

Anzi, una app containerizzata deve continuare a produrre log leggibili.

Nel nostro caso i log JSON contengono:

- richiesta;
- percorso;
- stato;
- latenza;
- identificativo richiesta;
- versione applicativa.

Questi segnali sono la base per ragionare poi su osservabilità, diagnosi e verifica post-rilascio.

---

# 5. Cosa non abbiamo ancora fatto

Non abbiamo ancora:

- pubblicato l'immagine in un registry remoto;
- creato una pipeline automatica;
- fatto deploy cloud;
- collegato più servizi;
- introdotto uno stack di observability.

Questi aspetti non mancano per errore. Sono esclusi volutamente per mantenere chiaro il passaggio locale.

---

# 6. Frase finale da ricordare

```text
In locale impariamo che cos'è un container e come si comporta.
Nel ciclo DevOps useremo poi l'immagine container come unità tecnica di build, rilascio e deploy.
```
