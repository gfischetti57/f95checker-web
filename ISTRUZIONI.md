# 🎮 F95Checker Web - Istruzioni Complete

## ⚡ Setup Rapido

### 1. Installa Python
- Vai su https://www.python.org/downloads/
- Scarica Python 3.11+
- **IMPORTANTE**: Spunta "Add Python to PATH" durante l'installazione

### 2. Setup Automatico
```cmd
# Doppio click su setup.bat OPPURE:
cd c:\Python\f95checker-web
setup.bat
```

### 3. Avvio Applicazione
```cmd
# Doppio click su start.bat OPPURE:
start.bat
```

L'app sarà disponibile su: **http://localhost:5000**

## 🔧 Setup Manuale (se gli script non funzionano)

```cmd
cd c:\Python\f95checker-web
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

## 📱 Configurazione Telegram (Opzionale)

### 1. Crea Bot Telegram
1. Apri Telegram e cerca **@BotFather**
2. Invia `/newbot`
3. Scegli nome e username per il bot
4. Copia il **token** che ti viene dato

### 2. Configura Token
1. Apri il file `.env`
2. Incolla il token: `TELEGRAM_BOT_TOKEN=il-tuo-token-qui`
3. Riavvia l'app

### 3. Ottieni Chat ID
1. Avvia conversazione con il tuo bot
2. Invia `/start`
3. Il bot ti dirà il tuo chat_id
4. Usa questo ID per registrarti nell'app web

## 🌐 Come Usare l'App

### Aggiungere Giochi
1. Vai su F95Zone e trova il gioco
2. Copia l'URL (es: `https://f95zone.to/threads/game-name.12345/`)
3. Nell'app web clicca "Aggiungi Gioco"
4. Incolla l'URL e conferma

### Controlli Automatici
- L'app controlla automaticamente ogni ora
- Puoi forzare un controllo manuale dal dashboard

### Notifiche
- Le notifiche appaiono nella sezione "Notifiche"
- Se hai configurato Telegram, riceverai messaggi automatici

## 🚀 Deploy Online (Hosting Gratuito)

### Render.com
1. Carica il progetto su GitHub
2. Vai su render.com e registrati
3. "New Web Service" → Connetti GitHub repo
4. Configura:
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn run:app`
5. Aggiungi variabili d'ambiente nel dashboard

### Railway.app
1. Vai su railway.app
2. "Deploy from GitHub"
3. Seleziona il repo
4. Deploy automatico

## 📱 Accesso da Android/Mobile

### Browser Mobile
- Apri il browser e vai all'URL dell'app
- L'interfaccia è responsive

### App Android (Futura)
- L'API è pronta per integrazioni native
- Endpoint disponibili in `docs/api.md`

## 🔍 Risoluzione Problemi

### Python non trovato
```cmd
# Verifica installazione
python --version

# Se non funziona, reinstalla Python con "Add to PATH"
```

### Errori dipendenze
```cmd
# Aggiorna pip
python -m pip install --upgrade pip

# Reinstalla dipendenze
pip install -r requirements.txt --force-reinstall
```

### Porta occupata
- Cambia porta in `run.py`: `app.run(port=5001)`

### Database errori
```cmd
# Ricrea database
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.drop_all(); db.create_all()"
```

## 📞 Supporto

- Controlla `docs/` per documentazione dettagliata
- API documentation: `docs/api.md`
- Deployment guide: `docs/deployment.md`

## 🎯 Prossimi Passi

1. **Setup locale** ✅
2. **Configurazione Telegram** (opzionale)
3. **Deploy online** per accesso remoto
4. **App Android** (sviluppo futuro)