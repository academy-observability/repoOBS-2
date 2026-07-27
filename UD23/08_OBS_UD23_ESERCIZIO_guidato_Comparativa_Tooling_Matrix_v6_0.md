# OBS UD23 - Esercizio guidato
# Tooling matrix comparativa

## Obiettivo

Compilare una matrice decisionale che permetta di scegliere uno stack Observability in modo argomentato.

## Passo 1 - Scegli il contesto

Seleziona uno scenario:

| Scenario | Descrizione |
|---|---|
| A | Team piccolo, app containerizzata su Azure, budget limitato |
| B | Azienda enterprise, molte fonti log, retention lunga |
| C | Ecosistema microservizi, APM e service map importanti |
| D | Infrastruttura tradizionale con host/VM/servizi |

## Passo 2 - Compila criteri

Usa la tabella in `docs/templates/tooling_matrix_template.md`.

Per la riga **Dynatrace**, usa anche ciò che hai osservato direttamente nel Playground; non basarti soltanto sulla scheda teorica. Per Zabbix, Splunk e OpenText la valutazione resta basata sui casi d'uso forniti.

Per ogni strumento assegna:

```text
0 = non adatto / non valutato
1 = debole
2 = adeguato
3 = forte
```

Criteri:

```text
metriche
log search
tracing/APM
alerting
infrastructure monitoring
effort iniziale
retention/costo
integrazione Azure
adatto a team piccolo
adatto a enterprise
```

## Passo 3 - Scrivi una scelta motivata

Non basta il punteggio. Scrivi 8-10 righe di decisione.

Esempio:

```text
Per lo scenario A proporrei Application Insights/Log Analytics insieme a dashboard Azure,
perché l'app è già su Azure e il team può ottenere requests, dependencies e log senza gestire
un nuovo cluster. Prometheus/Grafana resta utile per metriche custom e formazione tecnica,
ma come prima scelta operativa il costo/effort di gestione va considerato.
```

## Passo 4 - Consegna

Salva:

```text
work/UD23/docs/tooling_matrix_ud23.md
```
