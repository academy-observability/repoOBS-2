# UD25 — Raccordo
# Dal Python elementare al dataset della UD26

## Che cosa abbiamo costruito

Sappiamo ora rappresentare:

```text
una richiesta       -> dizionario
più richieste       -> lista di dizionari
un file tabellare   -> sequenza di dizionari letti da DictReader
```

Sappiamo inoltre:

- convertire testo in numero;
- applicare condizioni;
- mantenere contatori;
- trovare un massimo;
- scrivere un output testuale.

## Il limite dell'approccio elementare

Per venti righe il ciclo esplicito è utile e leggibile. Con centinaia di righe e molte domande diventano frequenti operazioni come:

- controllare valori mancanti;
- raggruppare per servizio ed endpoint;
- calcolare media, mediana e percentili;
- produrre tabelle e grafici.

Potremmo implementare tutto manualmente, ma il codice diventerebbe lungo prima di aver chiarito il problema. In UD26 introdurremo `pandas`, una libreria esterna progettata per dati tabellari.

## Continuità

La logica non cambia:

```text
colonna CSV        -> colonna del DataFrame
riga CSV           -> osservazione
conversione tipo   -> tipo della colonna
ciclo manuale      -> operazioni di selezione e raggruppamento
```

`pandas` non sostituisce la comprensione acquisita. La rende applicabile a dataset più grandi.

## Competenze richieste in ingresso a UD26

Prima di procedere dobbiamo saper spiegare:

1. differenza tra stringa, intero e float;
2. lista e dizionario;
3. ciclo `for`;
4. condizione `if`;
5. funzione con parametri;
6. comportamento di `csv.DictReader`.
