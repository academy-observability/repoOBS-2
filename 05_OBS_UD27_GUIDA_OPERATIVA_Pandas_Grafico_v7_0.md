# UD27 — Laboratorio autonomo
# Confrontare due gruppi

## Scenario

Dobbiamo confrontare il comportamento osservato di due gruppi correlati al Catalogo prodotti:

```text
frontend /products
backend  /api/products
```

Non dobbiamo stabilire quale sia “anomalo”.

Dobbiamo soltanto descrivere e confrontare i dati disponibili.

## Starter

Copiare:

```bash
cp src/starter/compare_two_groups_TODO.py src/compare_two_groups.py
```

PowerShell:

```powershell
Copy-Item src/starter/compare_two_groups_TODO.py src/compare_two_groups.py
```

## Come si comporta lo starter

Se viene eseguito senza completare i primi due TODO, termina con il messaggio:

```text
Completare TODO 1 e TODO 2 prima di proseguire.
```

Questo comportamento è intenzionale: evita di scambiare un output parziale per un risultato completo.

## Obiettivi

Completare i TODO per ottenere, per entrambi i gruppi:

- count;
- minimo;
- massimo;
- media;
- mediana;
- p95.

## Tabella da compilare nell'evidenza

| Gruppo | Count | Min | Max | Media | Mediana | P95 |
|---|---:|---:|---:|---:|---:|---:|
| frontend `/products` | | | | | | |
| backend `/api/products` | | | | | | |

## Interpretazione richiesta

Scrivere quattro frasi:

1. quale gruppo ha media maggiore;
2. quale gruppo ha mediana maggiore;
3. quale gruppo ha p95 maggiore;
4. perché questi risultati non bastano ancora per dichiarare un'anomalia.

## Vincoli

Non usare:

- baseline;
- soglie;
- ground truth;
- modelli ML.

Non aggiungere nuove librerie.

## Verifica

```bash
python src/compare_two_groups.py
```

Il programma deve terminare senza errori e mostrare entrambi i gruppi.

## Competenza verificata

> So applicare a un caso nuovo le stesse statistiche già esercitate e confrontare i risultati senza trasformare automaticamente una differenza in una diagnosi.
