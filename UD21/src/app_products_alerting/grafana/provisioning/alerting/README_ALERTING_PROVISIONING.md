# Provisioning alerting — nota didattica UD21 v6.0

Il percorso obbligatorio è GUI-first. I partecipanti creano manualmente:

- contact point webhook;
- folder;
- evaluation group;
- alert rule;
- labels e annotations.

Questi oggetti sono salvati nel database Grafana presente nel volume:

```text
obs-ud21-grafana-data → /var/lib/grafana
```

La cartella non contiene YAML attivi per evitare che l'esercizio venga già svolto dal provisioning. Gli esempi non attivi sono in:

```text
grafana/examples/alerting
```
