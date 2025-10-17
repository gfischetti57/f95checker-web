# F95Checker Web

Interfaccia web per monitorare aggiornamenti dei giochi su F95Zone con notifiche Telegram.

## Caratteristiche

- 🎮 Monitoraggio automatico aggiornamenti giochi F95Zone
- 📱 Notifiche Telegram in tempo reale
- 🔄 Sincronizzazione con F95Checker desktop
- 🌐 Interfaccia web responsive
- 📊 Dashboard con statistiche
- 🔍 Controllo aggiornamenti GitHub F95Checker

## Installazione

1. **Clona il repository**
```bash
git clone https://github.com/your-username/f95checker-web.git
cd f95checker-web
```

2. **Installa dipendenze**
```bash
pip install -r requirements.txt
```

3. **Configura variabili d'ambiente**
```bash
cp .env.example .env
# Modifica .env con le tue configurazioni
```

4. **Inizializza database**
```bash
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

5. **Avvia applicazione**
```bash
python run.py
```

## Configurazione

### Variabili d'ambiente (.env)

- `SECRET_KEY`: Chiave segreta Flask
- `TELEGRAM_BOT_TOKEN`: Token bot Telegram
- `DESKTOP_DB_PATH`: Percorso database F95Checker desktop
- `DATABASE_URL`: URL database (default: SQLite)

### Percorsi Database Desktop

- **Windows**: `c:\Users\USERNAME\AppData\Roaming\f95checker\db.sqlite3`
- **Linux**: `~/.local/share/f95checker/db.sqlite3`
- **macOS**: `~/Library/Application Support/f95checker/db.sqlite3`

## Utilizzo

### Registrazione Telegram

1. Avvia il bot Telegram
2. Invia `/start` per registrarti
3. Riceverai notifiche automatiche

### Sincronizzazione Desktop

1. Installa F95Checker desktop
2. Aggiungi giochi da monitorare
3. Nella web app, clicca "Sincronizza da Desktop"
4. I thread verranno importati automaticamente

### API Endpoints

- `GET /api/games` - Lista giochi
- `POST /api/games` - Aggiungi gioco
- `POST /api/sync-threads` - Sincronizza da desktop
- `POST /api/check-updates` - Controlla aggiornamenti

## Deployment

### Systemd Service

```bash
sudo cp systemd_service /etc/systemd/system/f95checker-web.service
sudo systemctl enable f95checker-web
sudo systemctl start f95checker-web
```

### Nginx

```bash
sudo cp nginx_config /etc/nginx/sites-available/f95checker-web
sudo ln -s /etc/nginx/sites-available/f95checker-web /etc/nginx/sites-enabled/
sudo systemctl reload nginx
```

## Contribuire

1. Fork del repository
2. Crea branch feature (`git checkout -b feature/nuova-funzione`)
3. Commit modifiche (`git commit -am 'Aggiungi nuova funzione'`)
4. Push branch (`git push origin feature/nuova-funzione`)
5. Crea Pull Request

## Licenza

MIT License - vedi file LICENSE per dettagli.