# OBS UD20 — Raccordo
# Dalla dashboard all'alerting operativo

In UD20 abbiamo costruito una vista visuale sulle metriche del Catalogo prodotti. Questa vista è importante perché rende leggibili segnali che in Prometheus sono disponibili come serie temporali, ma non sempre sono immediati da interpretare durante una diagnosi.

La progressione del blocco locale ora è:

```text
UD18 = stack locale app + observability
UD19 = Prometheus raccoglie e interroga metriche
UD20 = Grafana visualizza metriche in dashboard
UD21 = le metriche diventano condizioni di alert
UD22 = metriche, log e trace vengono correlate
```

Il passaggio successivo è naturale: alcuni pannelli della dashboard descrivono condizioni che, se persistono, devono diventare alert.

Esempi:

```text
Target backend DOWN        → possibile alert disponibilità
Error rate /products/error → possibile alert errore applicativo
P95 /products/slow alto    → possibile alert degrado prestazionale
/ready non 200             → possibile alert integrazione FE → BE
```

In UD21 non ripartiremo da zero. Useremo proprio le metriche e i pannelli della UD20 per ragionare su soglie, finestre temporali, severità e runbook.
