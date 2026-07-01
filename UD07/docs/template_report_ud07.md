# Report UD07 - Metriche e segnali generati

## 1. Contesto

- Subscription:
- Resource Group:
- Data/Ora laboratorio:
- Partecipante/Gruppo:

## 2. Risorse osservate

| Risorsa | Nome | Resource ID | Note |
|---|---|---|---|
| App Service |  |  |  |
| Storage Account |  |  |  |
| VM |  |  |  |

## 3. Baseline prima della generazione segnali

### App Service - Requests

- Screenshot:
- Evidenza CLI:
- Interpretazione:

### Storage Account - Transactions

- Screenshot:
- Evidenza CLI:
- Interpretazione:

### VM - Percentage CPU, se applicabile

- Screenshot:
- Evidenza CLI:
- Interpretazione:

## 4. Segnale amministrativo generato

- Script usato:
- Risorse coinvolte:
- Evidenza Activity Log:
- Evidenza tag:
- Interpretazione:

Domanda:

```text
Questo segnale è amministrativo o applicativo?
```

Risposta:

```text

```

## 5. Segnale applicativo/workload generato

- Script usato:
- Attività App Service:
- Attività Storage:
- Attività VM, se applicabile:
- Evidenze:

## 6. Metriche osservate dopo il traffico

| Risorsa | Metrica | Aggregazione | Evidenza | Interpretazione |
|---|---|---|---|---|
| App Service | Requests | Total |  |  |
| Storage Account | Transactions | Total |  |  |
| VM | Percentage CPU | Average / Maximum |  |  |

## 7. Confronto prima/dopo

Descrivere che cosa è cambiato rispetto alla baseline.

```text

```

## 8. Diagnostic Settings

- Risorsa scelta:
- Categorie diagnostiche disponibili:
- Diagnostic Settings esistenti:
- Proposta di destinazione futura:

## 9. Limiti o anomalie osservate

Esempi:

```text
metriche non immediatamente disponibili;
Diagnostic Settings non caricato dal Portale;
VM non running;
permessi Storage insufficienti;
nessun traffico visibile nel time range scelto.
```

## 10. Conclusione tecnica

Scrivere una conclusione nel formato:

```text
Ho osservato <risorsa>.
Ho generato <attività>.
Mi aspettavo <segnale>.
Ho visto <risultato>.
Concludo che <interpretazione>.
Il limite principale è <limite>.
```
