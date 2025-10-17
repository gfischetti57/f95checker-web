# Guida Deployment

## Deployment su Render.com (Gratuito)

### 1. Preparazione Repository
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo>
git push -u origin main
```

### 2. Configurazione Render
1. Vai su [render.com](https://render.com) e registrati
2. Clicca "New +" → "Web Service"
3. Connetti il tuo repository GitHub
4. Configura:
   - **Name**: f95checker-web
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn run:app`

### 3. Variabili d'Ambiente
Aggiungi in Render Dashboard → Environment:
```
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:pass@host:port/db
TELEGRAM_BOT_TOKEN=your-telegram-token
FLASK_ENV=production
```

### 4. Database PostgreSQL
1. In Render: "New +" → "PostgreSQL"
2. Copia l'URL del database
3. Aggiorna `DATABASE_URL` nelle variabili d'ambiente

### 5. Deploy
- Render farà il deploy automaticamente
- L'app sarà disponibile su `https://your-app-name.onrender.com`

## Alternative Hosting Gratuito

### Railway.app
1. Vai su [railway.app](https://railway.app)
2. "Deploy from GitHub repo"
3. Configura variabili d'ambiente
4. Deploy automatico

### Heroku (Limitato)
1. Installa Heroku CLI
2. `heroku create your-app-name`
3. `heroku config:set SECRET_KEY=your-key`
4. `git push heroku main`

## Configurazione Dominio Personalizzato

### Render
1. Dashboard → Settings → Custom Domains
2. Aggiungi il tuo dominio
3. Configura DNS CNAME

### Cloudflare (Opzionale)
1. Aggiungi sito a Cloudflare
2. Configura DNS
3. Abilita SSL/TLS

## Monitoraggio

### Uptime Monitoring
- [UptimeRobot](https://uptimerobot.com) (gratuito)
- [Pingdom](https://pingdom.com)

### Logs
- Render: Dashboard → Logs
- Railway: Dashboard → Deployments → Logs

## Backup Database

### Script Backup
```python
# backup.py
import os
import subprocess
from datetime import datetime

def backup_db():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'backup_{timestamp}.sql'
    
    subprocess.run([
        'pg_dump', 
        os.environ['DATABASE_URL'], 
        '-f', filename
    ])
    
    print(f'Backup creato: {filename}')

if __name__ == '__main__':
    backup_db()
```

## Troubleshooting

### Errori Comuni
- **Build failed**: Controlla `requirements.txt`
- **App crash**: Verifica logs per errori Python
- **Database error**: Controlla `DATABASE_URL`
- **502 Bad Gateway**: App non risponde, controlla `Procfile`

### Debug
```bash
# Logs in tempo reale
heroku logs --tail

# Restart app
heroku restart
```