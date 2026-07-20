# OBS UD22 — Mini-attività
# Leggere una trace senza fermarsi alla schermata

## Attività 1 — Gerarchia

Per la trace normale rappresentare la gerarchia con un albero:

```text
operazione radice
└── ...
```

Per ogni span indicare:

- servizio;
- tipo: SERVER, CLIENT o INTERNAL;
- durata approssimativa.

## Attività 2 — Critical path

Nella trace lenta individuare il percorso che determina la durata percepita dall'utente.

Rispondere:

1. quale span domina la timeline;
2. quale servizio lo possiede;
3. quale evidenza esclude che il frontend stia eseguendo lavoro locale equivalente;
4. perché non bisogna sommare tutte le durate degli span.

## Attività 3 — Errore

Nella trace di errore distinguere:

```text
origine dell'errore
propagazione dell'errore
manifestazione dell'errore all'utente
```

## Attività 4 — Identificatori

Completare:

| Affermazione | Identificatore |
|---|---|
| collega tutti gli span della richiesta | |
| distingue una singola operazione | |
| viene passato come `X-Request-Id` | |
| resta uguale nei log FE e BE | |
| cambia tra log FE e BE | |
