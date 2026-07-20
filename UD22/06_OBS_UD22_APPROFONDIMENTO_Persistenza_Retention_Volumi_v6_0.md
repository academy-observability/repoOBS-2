# OBS UD22 — Approfondimento
# Persistenza delle trace, retention e volumi Docker

## 1. Perché Jaeger necessita di storage

Il collector riceve gli span mentre le richieste vengono eseguite. Per cercarli in seguito, Jaeger deve scriverli in uno storage interrogabile. Nel laboratorio lo storage è Badger.

```text
span ricevuto -> scrittura Badger -> ricerca Jaeger UI
```

Senza storage persistente, il riavvio del processo elimina le trace mantenute soltanto in memoria.

## 2. Database e volume svolgono funzioni diverse

```text
Badger
  organizza, indicizza, legge e scrive i dati

/badger
  directory interna in cui Badger crea i file

obs-ud22-jaeger-data
  named volume che rende durevole la directory
```

Un volume non sostituisce il database. Conserva i file prodotti dal database.

## 3. Persistenza non significa conservazione infinita

- **Persistenza**: i dati sopravvivono al riavvio o alla ricreazione del container.
- **Retention**: regola per quanto tempo i dati devono rimanere disponibili.
- **Capacità**: spazio effettivamente disponibile per i file.
- **Sampling**: decide quali richieste producono trace da conservare.

Queste quattro leve influenzano costo, copertura diagnostica e quantità di dati. Nel laboratorio Badger è configurato con una retention di 72 ore: il volume rende persistenti i file, mentre il TTL stabilisce per quanto tempo le trace rimangono logicamente conservate.

## 4. Mount utilizzati nella UD

```yaml
jaeger:
  volumes:
    - jaeger-data:/badger

prometheus:
  volumes:
    - prometheus-data:/prometheus

grafana:
  volumes:
    - grafana-data:/var/lib/grafana
```

La persistenza è quindi applicata in modo coerente ai dati runtime dello stack. I log applicativi restano su stdout e possono essere salvati con lo script dedicato.

## 5. Prova controllata

```bash
./scripts/generate_persistence_trace_ud22.sh
./scripts/restart_stack_ud22.sh
```

La seconda operazione elimina e ricrea i container con `docker compose down` e `up`, ma non usa `-v`. I named volume rimangono montabili e la trace continua a essere disponibile.

## 6. Reset distruttivo

Solo quando vogliamo ripartire da uno storage vuoto:

```bash
RESET_UD22=yes ./scripts/reset_stack_ud22.sh
```

Il reset usa `docker compose down -v`. La `-v` elimina anche i named volume dichiarati dal Compose. Dopo il reset le trace precedenti non sono più disponibili.

Questa operazione non fa parte del normale arresto del laboratorio.
