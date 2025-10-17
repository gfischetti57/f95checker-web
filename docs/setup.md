# Setup e Installazione

## Prerequisiti

- Python 3.8+
- Git
- Account Render.com (gratuito)

## Installazione Locale

### 1. Clona il Repository
```bash
git clone <repository-url>
cd f95checker-web
```

### 2. Crea Ambiente Virtuale
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Installa Dipendenze
```bash
pip install -r requirements.txt
```

### 4. Configura Variabili d'Ambiente
Crea file `.env`:
```
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///f95checker.db
TELEGRAM_BOT_TOKEN=your-telegram-token
```

### 5. Inizializza Database
```bash
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

### 6. Avvia Applicazione
```bash
python run.py
```

L'applicazione sarà disponibile su `http://localhost:5000`

## Configurazione Notifiche

### Telegram Bot
1. Crea bot con @BotFather su Telegram
2. Ottieni token e inseriscilo in `.env`
3. Avvia bot e ottieni chat_id

### Web Push (Opzionale)
1. Genera VAPID keys
2. Configura service worker
3. Implementa subscription management

## Troubleshooting

### Errori Comuni
- **Port già in uso**: Cambia porta in `run.py`
- **Database locked**: Riavvia applicazione
- **Import errors**: Verifica ambiente virtuale attivo