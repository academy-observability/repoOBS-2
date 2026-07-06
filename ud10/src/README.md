# Sorgenti tecniche UD10

Questa cartella contiene query KQL divise per uso.

| Cartella | Uso |
|---|---|
| `kql/alert/` | query candidate per alert e confronto soglie |
| `kql/workbook/` | query per dashboard e workbook |
| `kql/azure/` | query su tabelle reali del Log Analytics Workspace |

Le query con `datatable()` sono autosufficienti e servono a esercitare la logica. Le query in `kql/azure/` dipendono dalle tabelle realmente disponibili nel workspace.
