# OBS UD17 - Mini-attività
# Mappa dei segnali osservabili per il Catalogo prodotti

## Scopo

Questa mini-attività serve a trasformare ciò che vediamo nel portale in una mappa tecnica. Non basta dire “ho visto dati in Application Insights”: dobbiamo spiegare quale dato rappresenta quale parte del flusso FE → BE.

## Attività 1 - Mappa del flusso

Completa la tabella.

| Passaggio | Dove avviene | Segnale atteso | Tabella/log |
|---|---|---|---|
| Utente chiama `/products` | Frontend ACA | request frontend |  |
| Frontend chiama backend | Frontend verso Backend | dependency |  |
| Backend riceve `/api/products` | Backend ACA | request backend |  |
| Frontend scrive log JSON | stdout container frontend | log container |  |
| Backend scrive log JSON | stdout container backend | log container |  |
| Endpoint lento | backend | durata elevata |  |
| Endpoint errore | backend/frontend | 500 controllato |  |

## Attività 2 - Differenza tra endpoint

Completa.

| Endpoint | Che cosa dimostra | Quando è utile |
|---|---|---|
| `/health` |  |  |
| `/ready` |  |  |
| `/version` |  |  |
| `/products` |  |  |
| `/products/slow` |  |  |
| `/products/error` |  |  |

## Attività 3 - Correlazione

Scegli una richiesta generata con header:

```bash
X-Request-Id: ud17-manual-...
```

Poi trova almeno due evidenze collegate.

| Evidenza | Dove l'ho trovata | Valore osservato |
|---|---|---|
| Request frontend |  |  |
| Dependency FE → BE |  |  |
| Request backend |  |  |
| Log frontend con request_id |  |  |
| Log backend con request_id |  |  |

## Attività 4 - Interpretazione breve

Scrivi una risposta di 5-8 righe:

```text
Ho analizzato la richiesta ...
Nel frontend ho visto ...
Nel backend ho visto ...
La dependency indica ...
I log container confermano ...
La mia conclusione tecnica è ...
```

## Domande di controllo

1. Perché `/ready` è più informativo di `/health`?
2. Perché `/products/slow` non è un errore ma è comunque un segnale importante?
3. Perché `ContainerAppConsoleLogs_CL` non sostituisce `AppRequests`?
4. Che cosa dimostra `AppDependencies` nel nostro scenario?
5. Che cosa succede se nei log vedo `request_id`, ma in Application Insights non vedo request recenti?
6. Perché non dobbiamo usare `latest` per ragionare sulla versione rilasciata?
7. Quale evidenza useresti per dimostrare che il backend è la causa della lentezza?
