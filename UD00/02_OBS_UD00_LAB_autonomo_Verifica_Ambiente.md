# OBS_UD00 - Laboratorio autonomo: verifica ambiente e consegna

## 1. Scenario

Dopo il laboratorio guidato dobbiamo dimostrare che l’ambiente è realmente utilizzabile senza seguire meccanicamente i passaggi del docente.

L’obiettivo del laboratorio autonomo è produrre un report tecnico di verifica, eseguire un piccolo test Docker e consegnare tutto tramite Git.

---

## 2. Attività richieste

### Task 1 - Verifica posizione di lavoro

Posizioniamoci nel repository del corso:

```bash
cd ~/corso_obs/NOME-REPOSITORY
pwd
git status
```

Nel report indichiamo:

- percorso corrente;
- nome del branch;
- stato del repository.

---

### Task 2 - Verifica strumenti

Eseguiamo:

```bash
uname -a
lsb_release -a || cat /etc/os-release
git --version
python3 --version
docker version
docker compose version
code --version
```

Se `code --version` non funziona da WSL, annotiamo il problema nel report e verifichiamo l’integrazione di VS Code con WSL.

---

### Task 3 - Test Docker con servizio HTTP

Avviamo un container nginx su una porta diversa da quella usata al mattino:

```bash
docker run --rm -d --name ud00-nginx-autonomo -p 8081:80 nginx:alpine
```

Verifichiamo:

```bash
docker ps
curl -I http://localhost:8081
docker logs ud00-nginx-autonomo
```

Fermiamo il container:

```bash
docker stop ud00-nginx-autonomo
```

---

### Task 4 - Creazione report autonomo

Creiamo il file:

```bash
mkdir -p evidence
nano evidence/ud00_verifica_autonoma.md
```

Il report deve contenere queste sezioni:

```md
# UD00 - Verifica autonoma ambiente

## 1. Percorso di lavoro

## 2. Versioni strumenti

## 3. Test Docker HTTP

## 4. Problemi incontrati

## 5. Cosa ho verificato realmente
```

Non basta copiare i comandi: per ogni sezione scriviamo una breve frase che spiega cosa dimostra l’evidenza.

---

### Task 5 - Commit e push

Eseguiamo:

```bash
git status
git add evidence/ud00_verifica_autonoma.md
git commit -m "[UD00] aggiunge verifica autonoma ambiente"
git push
```

Verifichiamo:

```bash
git log --oneline -3
git status
```

---

## 3. Domande di consolidamento

Rispondiamo nel report o in un file separato indicato dal docente.

1. Perché è preferibile lavorare nella home Linux invece che in `/mnt/c/Users/...`?
2. A cosa serve `git status` prima di un commit?
3. Che differenza c’è tra `git commit` e `git push`?
4. Perché Docker è utile in un percorso Observability?
5. Che cosa rende un’evidenza tecnica più utile di uno screenshot generico?
6. Che cosa dimostra il comando `curl -I http://localhost:8081`?
7. Perché è importante fermare un container di test alla fine del laboratorio?

---

## 4. Criteri di completamento

Il laboratorio autonomo è completato se:

- il report autonomo esiste;
- il test Docker è stato eseguito;
- il container è stato fermato;
- le domande hanno risposta;
- il commit è presente nel repository remoto;
- `git status` non mostra modifiche inattese.
