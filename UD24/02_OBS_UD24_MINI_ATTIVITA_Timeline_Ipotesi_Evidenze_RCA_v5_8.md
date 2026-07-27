# OBS UD24 — Mini-attività
# Timeline, ipotesi, evidenze e RCA

## Obiettivo

Questa mini-attività serve a distinguere quattro elementi che spesso vengono confusi:

```text
sintomo ≠ ipotesi ≠ evidenza ≠ root cause
```

## Parte 1 — Classificazione

Per ogni frase indica se è: **Sintomo**, **Ipotesi**, **Evidenza**, **Root cause probabile**, **Azione correttiva**.

| Frase | Classificazione |
|---|---|
| Gli utenti vedono errore sulla pagina prodotti | |
| Il backend potrebbe restituire 500 | |
| La query AppRequests mostra ResultCode 500 su `/products/error` | |
| Il problema è localizzato nell'endpoint backend `/api/products/error` | |
| Riattivare la revisione precedente | |
| Grafana mostra p95 elevato su `/products/slow` | |
| Jaeger mostra uno span backend più lungo del frontend | |
| Il frontend non raggiunge il backend | |

## Parte 2 — Timeline

Completa la timeline con almeno sei eventi.

| Ora | Evento | Fonte | Nota |
|---|---|---|---|
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |

## Parte 3 — Ipotesi

Scegli due ipotesi e indica quali segnali useresti.

| Ipotesi | Segnale locale | Segnale cloud | Cosa la confermerebbe | Cosa la smentirebbe |
|---|---|---|---|---|
| | | | | |
| | | | | |

## Parte 4 — Frase finale

Scrivi una frase tecnica di massimo 8 righe:

```text
Il problema osservato è ...
Le evidenze principali sono ...
La root cause probabile è ...
L'azione correttiva proposta è ...
Il limite dell'analisi è ...
```

## Criteri di qualità

Una buona risposta:

- non salta subito alla causa;
- cita almeno un segnale locale e uno cloud;
- usa endpoint precisi;
- distingue errore da lentezza;
- indica limiti o incertezze.
