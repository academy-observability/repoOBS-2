# UD23 - Comparativa stack e strumenti Observability

## Scopo della UD

Questa unità chiude il blocco dedicato agli strumenti di monitoraggio. Nelle UD18-UD22 abbiamo costruito e usato uno stack locale completo: Prometheus per raccogliere metriche, Grafana per leggerle, Grafana Alerting per trasformarle in segnali operativi, Jaeger per vedere le trace e log JSON per seguire `request_id`, `trace_id` e comportamento dei servizi.

In UD17 e UD23 rientriamo nel cloud Azure, ma questa volta non per ripetere Application Insights. Il punto è più professionale: osservare la stessa applicazione da più prospettive e capire quale strumento risponde meglio a quale domanda.

La domanda guida è:

```text
Quando userei Prometheus/Grafana, quando Azure Monitor/Application Insights,
quando uno stack log/Kibana-like, e quando avrebbe senso valutare strumenti enterprise?
```

## Baseline applicativa

La baseline rimane l'app **Catalogo prodotti**:

```text
Browser
  -> Frontend products
      -> Backend products
          -> catalogo
```

Endpoint principali:

```text
/products
/products/slow
/products/error
/ready
/version
```

## Sequenza consigliata

1. Leggere `00_OBS_UD23_Concetti_Comparativa_Stack_Strumenti_Observability_v6_0.md`.
2. Tenere aperta la guida operativa `04_...` durante il laboratorio.
3. Eseguire il laboratorio guidato `01_...`.
4. Completare la mini-attività `02_...`.
5. Eseguire `10_OBS_UD23_DEMO_GUIDATA_Dynatrace_Playground_v6_0.md`: è la demo pratica enterprise obbligatoria della UD.
6. Usare `06_...` per le altre schede strumenti enterprise e per consolidare Dynatrace.
7. Consultare `07_...` per chiarire l'architettura comparativa.
8. Svolgere `08_...` sulla matrice decisionale.
9. Usare `09_...` e il dataset log per l'esercizio Kibana-like.
10. Svolgere il laboratorio autonomo `03_...`.
11. Chiudere con `05_...`, che prepara UD24.

## Output attesi

Al termine della UD23 il partecipante deve consegnare:

```text
docs/report_comparativo_observability_ud23.md
docs/tooling_matrix_ud23.md
docs/evidence_ud23.md
```

Tra le evidenze deve comparire anche una breve osservazione pratica del Dynatrace Playground.

Il report non deve essere una preferenza personale. Deve essere una scelta motivata con criteri tecnici: tipo di segnale, profondità APM, effort, costi, retention, integrazione, scalabilità e uso operativo.
