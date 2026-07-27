# OBS UD23 - Raccordo finale
# Dalla comparativa strumenti al Modern SRE

Con UD23 abbiamo chiuso un passaggio che spesso nei corsi tecnici viene saltato. Non abbiamo semplicemente aggiunto altri nomi di prodotto. Abbiamo provato a ragionare su come un tecnico sceglie, combina e giustifica strumenti di osservabilità.

Il risultato più importante non è il report in sé, ma la capacità di distinguere:

```text
metriche
log
trace
APM
monitoraggio infrastrutturale
strumenti cloud-native
strumenti enterprise
```

## Cosa abbiamo imparato

Prometheus e Grafana sono efficaci quando vogliamo metriche, dashboard e alerting controllabili. Application Insights e Log Analytics sono molto forti quando l'applicazione gira su Azure e vogliamo correlare richieste, dipendenze, tracce e log cloud. Uno stack log o una vista Kibana-like aiuta quando il problema è dentro gli eventi applicativi e serve cercare pattern o campi. Zabbix, Splunk, Dynatrace e OpenText entrano in contesti diversi: infrastruttura tradizionale, log search enterprise, APM avanzato, ITOM/AIOps e governance aziendale.

## Ponte verso UD24

UD24 userà questa competenza per fare il passo SRE:

```text
Non basta sapere quale strumento mostra un segnale.
Dobbiamo decidere quali segnali diventano SLI,
quali obiettivi diventano SLO,
e come si gestisce un incidente rispetto a un error budget.
```

In altre parole, UD23 chiude il blocco “strumenti”. UD24 apre il blocco “affidabilità”.
