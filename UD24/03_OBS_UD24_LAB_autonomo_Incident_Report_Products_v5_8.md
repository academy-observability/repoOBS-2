# OBS UD24 — Laboratorio autonomo
# Incident report su app Catalogo prodotti

## Scenario

Il docente assegna uno dei tre scenari:

| Scenario | Endpoint | Comportamento |
|---|---|---|
| A | `/products` | comportamento normale da usare come baseline |
| B | `/products/slow` | lentezza controllata |
| C | `/products/error` | errore controllato |

Il partecipante deve produrre un mini incident report, anche se lo scenario è simulato.

## Consegna

1. Genera traffico locale e cloud per lo scenario assegnato.
2. Raccogli almeno due evidenze locali.
3. Raccogli almeno due evidenze cloud.
4. Costruisci una timeline.
5. Formula almeno due ipotesi.
6. Scegli la root cause probabile.
7. Proponi un'azione correttiva o preventiva.
8. Indica i limiti dell'analisi.

## Evidenze minime

| Tipo evidenza | Richiesta |
|---|---|
| curl/output HTTP | almeno uno |
| PromQL o screenshot Grafana | almeno uno |
| Jaeger/log locale | almeno uno |
| KQL AppRequests/AppDependencies/AppExceptions | almeno uno |
| ContainerAppConsoleLogs_CL | almeno uno se disponibile |
| incident report | obbligatorio |

## Template

Usa:

```text
UD24/docs/template_incident_report_ud24.md
UD24/docs/template_decision_record_ud24.md
```

## Criteri di valutazione

| Criterio | Peso |
|---|---:|
| timeline chiara | 20% |
| uso corretto segnali locali | 20% |
| uso corretto segnali cloud | 20% |
| ipotesi e root cause coerenti | 25% |
| azione correttiva e limiti | 15% |

## Nota

Non è richiesto “risolvere davvero” il bug simulato. È richiesto dimostrare un metodo di indagine.
