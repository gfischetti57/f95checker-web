#!/bin/bash
# F95Checker Web - Startup Script per Oracle Cloud

echo "🚀 Avvio F95Checker Web..."

# Vai nella directory app
cd /home/ubuntu/f95checker-web

# Attiva ambiente virtuale
source venv/bin/activate

# Imposta variabili d'ambiente
export FLASK_ENV=production
export SECRET_KEY=oracle-f95checker-secret-key-2024
export DATABASE_URL=sqlite:///f95checker.db
export TELEGRAM_BOT_TOKEN=8306286141:AAHgdSI6ntiQtqlYd_87aKunoWeL7FZIFBE

echo "✅ Ambiente configurato"

# Avvia con Gunicorn
echo "🌐 Avvio server su porta 5000..."
gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 120 run:app