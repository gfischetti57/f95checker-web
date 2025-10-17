# Oracle Cloud Deploy - F95Checker Web

## 🔧 Preparazione Files

### 1. Aggiorna requirements.txt per Oracle
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

### 2. Crea startup script
```bash
#!/bin/bash
# startup.sh
cd /home/ubuntu/f95checker-web
source venv/bin/activate
export FLASK_ENV=production
export SECRET_KEY=your-oracle-secret-key
export DATABASE_URL=sqlite:///f95checker.db
export TELEGRAM_BOT_TOKEN=8306286141:AAHgdSI6ntiQtqlYd_87aKunoWeL7FZIFBE
gunicorn --bind 0.0.0.0:5000 run:app
```

### 3. Systemd service
```ini
# /etc/systemd/system/f95checker.service
[Unit]
Description=F95Checker Web App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/f95checker-web
Environment=PATH=/home/ubuntu/f95checker-web/venv/bin
ExecStart=/home/ubuntu/f95checker-web/venv/bin/gunicorn --bind 0.0.0.0:5000 run:app
Restart=always

[Install]
WantedBy=multi-user.target
```

## 📋 Step-by-Step Oracle Setup

### Fase 1: Account Oracle
1. Vai su [cloud.oracle.com](https://cloud.oracle.com)
2. **Sign Up** → Always Free Account
3. Inserisci dati (serve carta credito ma non viene addebitato)
4. Verifica email e telefono

### Fase 2: Crea VM Instance
1. **Compute** → **Instances** → **Create Instance**
2. Configurazioni:
   - **Name**: f95checker-server
   - **Image**: Ubuntu 22.04 LTS
   - **Shape**: VM.Standard.E2.1.Micro (Always Free)
   - **Network**: Default VCN
   - **SSH Keys**: Generate new key pair (scarica private key)

### Fase 3: Configura Firewall
1. **Networking** → **Virtual Cloud Networks**
2. Clicca sulla VCN default
3. **Security Lists** → Default Security List
4. **Add Ingress Rules**:
   - Source: 0.0.0.0/0
   - Port: 5000
   - Protocol: TCP

### Fase 4: Connetti SSH
```bash
# Windows (PowerShell)
ssh -i path\to\private-key.key ubuntu@YOUR_PUBLIC_IP

# Aggiorna sistema
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv git nginx -y
```

### Fase 5: Deploy App
```bash
# Clone repository
git clone https://github.com/TUO_USERNAME/f95checker-web.git
cd f95checker-web

# Setup Python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configura environment
cp .env.example .env
nano .env  # Modifica con le tue configurazioni

# Inizializza database
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"

# Test locale
python run.py
```

### Fase 6: Nginx Reverse Proxy
```nginx
# /etc/nginx/sites-available/f95checker
server {
    listen 80;
    server_name YOUR_PUBLIC_IP;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

```bash
# Abilita sito
sudo ln -s /etc/nginx/sites-available/f95checker /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Fase 7: Systemd Service
```bash
# Crea service file
sudo nano /etc/systemd/system/f95checker.service
# (copia contenuto da sopra)

# Abilita e avvia
sudo systemctl daemon-reload
sudo systemctl enable f95checker
sudo systemctl start f95checker
sudo systemctl status f95checker
```

## 🌐 Accesso App

- **URL**: http://YOUR_PUBLIC_IP
- **Admin**: SSH con private key
- **Logs**: `sudo journalctl -u f95checker -f`

## 🔧 Manutenzione

### Aggiornamenti
```bash
cd /home/ubuntu/f95checker-web
git pull origin main
sudo systemctl restart f95checker
```

### Backup Database
```bash
# Backup
cp f95checker.db f95checker_backup_$(date +%Y%m%d).db

# Restore
cp f95checker_backup_20240115.db f95checker.db
sudo systemctl restart f95checker
```

## 📊 Monitoraggio

### Status Check
```bash
# App status
sudo systemctl status f95checker

# Nginx status  
sudo systemctl status nginx

# Logs
sudo journalctl -u f95checker --since "1 hour ago"
```

### Resource Usage
```bash
# CPU/Memory
htop

# Disk space
df -h

# Network
netstat -tulpn | grep :5000
```

## 🚨 Troubleshooting

### App non parte
```bash
# Check logs
sudo journalctl -u f95checker -n 50

# Test manuale
cd /home/ubuntu/f95checker-web
source venv/bin/activate
python run.py
```

### Nginx errori
```bash
# Test config
sudo nginx -t

# Restart
sudo systemctl restart nginx
```

### Firewall issues
```bash
# Ubuntu firewall
sudo ufw allow 5000
sudo ufw allow 80
sudo ufw enable
```

## ✅ Checklist Completo

- [ ] Account Oracle creato
- [ ] VM Instance creata
- [ ] SSH key scaricata
- [ ] Firewall configurato (porta 5000)
- [ ] SSH connesso
- [ ] Sistema aggiornato
- [ ] Repository clonato
- [ ] Python environment setup
- [ ] App testata localmente
- [ ] Nginx configurato
- [ ] Systemd service creato
- [ ] App accessibile da internet
- [ ] Telegram bot testato

**Risultato**: App disponibile 24/7 su Oracle Cloud Forever Free! 🚀