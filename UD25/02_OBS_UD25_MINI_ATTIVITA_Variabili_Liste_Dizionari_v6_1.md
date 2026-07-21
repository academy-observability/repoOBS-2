# UD25 — Mini-attività
# Variabili, liste, dizionari e funzioni

Svolgere le attività senza consultare subito le soluzioni docente.

## Attività 1 — Conversione esplicita

Dato:

```python
status_text = "503"
```

1. convertirlo in intero;
2. verificare se è uno status 5xx;
3. stampare il risultato.

**Criterio:** nessun confronto diretto tra stringa e intero.

## Attività 2 — Contare valori lenti

Dato:

```python
durations = [120.0, 980.0, 1400.0, 250.0]
```

Contare quante durate superano `1000.0` ms usando `for` e `if`.

## Attività 3 — Arricchire un dizionario

Aggiungere a una richiesta:

```text
request_id
trace_id
environment
```

poi stampare una frase leggibile che li utilizzi.

## Attività 4 — Filtrare una lista di dizionari

Creare almeno tre richieste e stampare soltanto quelle con status 4xx o 5xx.

## Attività 5 — Funzione `is_slow`

Scrivere:

```python
def is_slow(duration_ms, threshold_ms):
    ...
```

Provare la funzione con almeno tre coppie di valori.

## Attività 6 — Previsione di errore

Spiegare, prima di eseguire, che cosa accade:

```python
status_code = "500"
print(status_code >= 500)
```

Correggere poi il codice.

## Evidenza

Riportare nel file evidence:

- una soluzione scelta;
- il risultato;
- un errore incontrato;
- la correzione applicata.
