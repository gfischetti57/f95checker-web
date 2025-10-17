# Installazione Python

## Passo 1: Installa Python

1. Vai su https://www.python.org/downloads/
2. Scarica Python 3.11 o superiore
3. **IMPORTANTE**: Durante l'installazione, spunta "Add Python to PATH"
4. Installa con privilegi amministratore

## Passo 2: Verifica Installazione

Apri un nuovo prompt dei comandi e digita:
```cmd
python --version
```

Dovresti vedere qualcosa come "Python 3.11.x"

## Passo 3: Continua Setup

Una volta installato Python, torna qui e esegui:

```cmd
cd c:\Python\f95checker-web
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Alternative se Python non funziona

### Opzione 1: Anaconda
1. Scarica Anaconda da https://www.anaconda.com/
2. Installa e usa `conda` invece di `pip`

### Opzione 2: Microsoft Store
1. Apri Microsoft Store
2. Cerca "Python 3.11"
3. Installa

### Opzione 3: Chocolatey
```cmd
# Installa Chocolatey prima (come admin)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Poi installa Python
choco install python
```