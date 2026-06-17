# OBS_UD00 - Laboratorio guidato: Setup Ambiente

## 1. Obiettivo del laboratorio guidato

In questo laboratorio configuriamo e verifichiamo l’ambiente necessario per il percorso Observability.

Al termine del laboratorio dobbiamo poter usare:

- Ubuntu su WSL2;
- Git;
- GitHub Classroom o repository personale;
- Docker Desktop integrato con WSL2;
- VS Code aperto da WSL;
- primo workflow commit/push.

---

## 2. Verifica iniziale del sistema

Apriamo PowerShell come amministratore e verifichiamo la disponibilità di WSL:

```powershell
wsl --status
```

Se WSL non è installato:

```powershell
wsl --install
wsl --set-default-version 2
wsl --install -d Ubuntu
```

Dopo l’installazione può essere necessario riavviare Windows.

---

## 3. Primo avvio di Ubuntu

Apriamo Ubuntu dal menu Start. Alla prima apertura vengono richiesti:

- nome utente Linux;
- password Linux.

Verifichiamo che il terminale sia operativo:

```bash
uname -a
whoami
pwd
```

Aggiorniamo i pacchetti base:

```bash
sudo apt update
sudo apt upgrade -y
```

---

## 4. Installazione e configurazione Git

Installiamo Git:

```bash
sudo apt install -y git
git --version
```

Configuriamo nome e email:

```bash
git config --global user.name "Nome Cognome"
git config --global user.email "email@example.com"
```

Verifichiamo:

```bash
git config --global --list
```

---

## 5. Preparazione cartella corso

Creiamo una cartella di lavoro nella home Linux:

```bash
mkdir -p ~/corso_obs
cd ~/corso_obs
pwd
```

Il percorso deve essere simile a:

```text
/home/nomeutente/corso_obs
```

Non lavoriamo dentro `/mnt/c/Users/...` salvo indicazioni specifiche del docente.

---

## 6. Configurazione accesso GitHub via SSH

Generiamo una chiave SSH:

```bash
ssh-keygen -t ed25519 -C "email@example.com"
```

Avviamo l’agent e aggiungiamo la chiave:

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

Visualizziamo la chiave pubblica:

```bash
cat ~/.ssh/id_ed25519.pub
```

Copiamo il contenuto in GitHub, nella sezione dedicata alle SSH keys.

Verifichiamo la connessione:

```bash
ssh -T git@github.com
```

Un messaggio di autenticazione riuscita è sufficiente anche se GitHub specifica che non fornisce accesso shell.

---

## 7. Clone del repository

Cloniamo il repository assegnato dal docente o da GitHub Classroom:

```bash
cd ~/corso_obs
git clone git@github.com:ORG/NOME-REPOSITORY.git
cd NOME-REPOSITORY
```

Verifichiamo:

```bash
pwd
ls -la
git status
```

---

## 8. Apertura con VS Code da WSL

Dalla cartella del repository:

```bash
code .
```

VS Code deve aprirsi nel contesto WSL. Verifichiamo nella barra inferiore o nel terminale integrato che l’ambiente sia Linux/WSL.

---

## 9. Installazione e verifica Docker Desktop

Docker Desktop va installato in Windows e configurato con backend WSL2.

Dopo l’installazione, da Ubuntu verifichiamo:

```bash
docker version
docker compose version
```

Eseguiamo un container di test:

```bash
docker run --rm hello-world
```

Eseguiamo un servizio temporaneo:

```bash
docker run --rm -d --name obs-nginx-test -p 8080:80 nginx:alpine
```

Verifichiamo:

```bash
docker ps
curl -I http://localhost:8080
docker logs obs-nginx-test
```

Puliamo:

```bash
docker stop obs-nginx-test
```

---

## 10. Primo report di verifica

Creiamo una cartella per le evidenze:

```bash
mkdir -p evidence
```

Creiamo il report:

```bash
cat > evidence/ud00_setup_report.md << 'EOF'
# UD00 - Report setup ambiente

## Sistema

```bash
uname -a
```

## Utente

```bash
whoami
```

## Git

```bash
git --version
git config --global --list
```

## Docker

```bash
docker version
docker compose version
```

## Test HTTP container

```bash
curl -I http://localhost:8080
```

## Note personali

Scrivere qui eventuali problemi incontrati e come sono stati risolti.
EOF
```

Apriamo il file e completiamolo con gli output effettivi.

---

## 11. Primo commit e push

Verifichiamo lo stato:

```bash
git status
```

Aggiungiamo il report:

```bash
git add evidence/ud00_setup_report.md
git commit -m "[UD00] aggiunge report setup ambiente"
git push
```

Verifichiamo di nuovo:

```bash
git status
```

---

## 12. Controllo finale

Il laboratorio guidato è completato se sono vere queste condizioni:

- Ubuntu WSL2 funziona;
- Git è configurato;
- il repository è clonato nella home Linux;
- VS Code si apre con `code .`;
- Docker risponde da WSL;
- il container nginx è stato avviato e testato;
- il report è stato creato;
- il commit e il push sono stati eseguiti.
