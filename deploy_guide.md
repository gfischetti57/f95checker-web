# Deploy Gratuito - Guida Completa

## 🚀 Opzione 1: Render.com (Raccomandato)

### Preparazione
```bash
# 1. Inizializza Git
git init
git add .
git commit -m "F95Checker Web App"

# 2. Carica su GitHub
# Crea repository su github.com
git remote add origin https://github.com/TUO_USERNAME/f95checker-web.git
git push -u origin main
```

### Deploy su Render
1. Vai su [render.com](https://render.com)
2. Registrati con GitHub
3. **New** → **Web Service**
4. Connetti repository GitHub
5. Configurazioni:
   - **Name**: `f95checker-web`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn run:app`
   - **Instance Type**: `Free`

### Variabili d'Ambiente Render
```
SECRET_KEY=your-production-secret-key-here
DATABASE_URL=postgresql://render-internal-hostname:5432/database
TELEGRAM_BOT_TOKEN=8306286141:AAHgdSI6ntiQtqlYd_87aKunoWeL7FZIFBE
FLASK_ENV=production
```

### Database PostgreSQL
1. **New** → **PostgreSQL**
2. **Name**: `f95checker-db`
3. **Plan**: `Free`
4. Copia **Internal Database URL**
5. Incolla in `DATABASE_URL` del Web Service

## 🚀 Opzione 2: Railway.app

### Deploy Railway
1. Vai su [railway.app](https://railway.app)
2. **Deploy from GitHub repo**
3. Seleziona repository
4. Aggiungi variabili d'ambiente
5. Deploy automatico

### Variabili Railway
```
SECRET_KEY=your-secret-key
TELEGRAM_BOT_TOKEN=8306286141:AAHgdSI6ntiQtqlYd_87aKunoWeL7FZIFBE
DATABASE_URL=${{Postgres.DATABASE_URL}}
```

## 🚀 Opzione 3: Fly.io

### Setup Fly
```bash
# Installa Fly CLI
# Windows: scoop install flyctl
# Mac: brew install flyctl

# Login
flyctl auth login

# Deploy
flyctl launch
```

## 📝 File Necessari per Deploy

### Procfile (già presente)
```
web: gunicorn run:app
```

### runtime.txt (già presente)
```
python-3.11.0
```

### requirements.txt (aggiornato per produzione)
```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-CORS==4.0.0
requests==2.31.0
beautifulsoup4==4.12.2
schedule==1.2.0
python-dotenv==1.0.0
gunicorn==21.2.0
psycopg2-binary==2.9.7
```

## 🔧 Configurazione Produzione

### Aggiorna config.py
```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fallback-key'
    
    # Database
    if os.environ.get('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://')
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///f95checker.db'
    
    # Telegram
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
```

## 🌐 Dominio Personalizzato

### Render Custom Domain
1. Dashboard → Settings → Custom Domains
2. Aggiungi dominio
3. Configura DNS CNAME

### Cloudflare (Opzionale)
1. Aggiungi sito a Cloudflare
2. Configura DNS
3. SSL automatico

## 📊 Monitoraggio

### UptimeRobot (Gratuito)
1. [uptimerobot.com](https://uptimerobot.com)
2. Aggiungi monitor HTTP
3. URL: `https://your-app.onrender.com`
4. Notifiche email gratuite

## 🔍 Troubleshooting

### Errori Comuni
- **Build failed**: Controlla `requirements.txt`
- **App crash**: Verifica logs
- **Database error**: Controlla `DATABASE_URL`
- **502 Error**: App non risponde

### Debug Logs
```bash
# Render
# Dashboard → Logs

# Railway  
# Dashboard → Deployments → View Logs
```

## ✅ Checklist Deploy

- [ ] Repository GitHub creato
- [ ] Render account creato
- [ ] Web Service configurato
- [ ] Database PostgreSQL creato
- [ ] Variabili d'ambiente impostate
- [ ] Deploy completato
- [ ] App funzionante
- [ ] Telegram bot testato
- [ ] Monitoraggio configurato

**URL finale**: `https://f95checker-web.onrender.com`