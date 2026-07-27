# OBS UD24 — Raccordo finale
# Dall'incident investigation alla baseline e anomaly detection

UD24 chiude la parte più operativa del percorso Observability. Abbiamo usato strumenti diversi, ma soprattutto abbiamo costruito un metodo:

```text
osservare → formulare ipotesi → verificare → decidere → documentare
```

## 1. Perché UD24 prepara UD25

UD25 parlerà di baseline e anomaly detection. Però non ha senso cercare anomalie se non sappiamo prima:

- quale comportamento è normale;
- quale endpoint stiamo misurando;
- quale finestra temporale usiamo;
- quale metrica è affidabile;
- quali segnali sono rumorosi;
- quale anomalia è davvero rilevante.

UD24 ha introdotto questa disciplina.

## 2. Cosa portiamo avanti

Da UD24 portiamo in UD25:

| Elemento | Uso in UD25 |
|---|---|
| timeline | costruzione serie temporale |
| latenza `/products/slow` | esempio di deviazione dalla baseline |
| errori `/products/error` | esempio di evento anomalo |
| request rate | volume e stagionalità semplice |
| falsi positivi | valutazione soglie |
| incident report | interpretazione tecnica dei risultati |

## 3. Project work ridotto

UD24 svolge già una funzione di sintesi pratica. Per questo il project work finale può essere ridotto a una breve attività autonoma, cleanup e consegna evidenze.

## 4. Frase di chiusura

Al termine di UD24 il partecipante dovrebbe poter dire:

> Non mi limito a guardare dashboard. So usare metriche, log e trace per formulare un'ipotesi, verificarla, indicare una root cause probabile e documentare una decisione tecnica.
