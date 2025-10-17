# F95Checker Web Service

Un servizio web per monitorare aggiornamenti di giochi e ricevere notifiche su dispositivi Android e PC Windows.

## Descrizione Generale

Questo progetto trasforma F95Checker in un servizio web accessibile da qualsiasi dispositivo, fornendo:
- Monitoraggio automatico degli aggiornamenti
- Notifiche push per Android e PC
- Interfaccia web responsive
- API REST per integrazioni

## Struttura del Progetto

```
f95checker-web/
├── README.md                 # Documentazione principale
├── docs/                     # Documentazione dettagliata
│   ├── setup.md             # Guida installazione
│   ├── api.md               # Documentazione API
│   ├── deployment.md        # Guida deployment
│   └── notifications.md     # Sistema notifiche
├── app/                      # Applicazione principale
│   ├── __init__.py
│   ├── config.py            # Configurazioni
│   ├── models/              # Modelli dati
│   ├── routes/              # Endpoint API
│   ├── services/            # Logica business
│   └── utils/               # Utilità
├── web/                      # Frontend
│   ├── static/              # CSS, JS, immagini
│   └── templates/           # Template HTML
├── requirements.txt          # Dipendenze Python
├── Procfile                 # Per deployment Heroku/Render
└── runtime.txt              # Versione Python
```

## Tecnologie Utilizzate

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite (locale) / PostgreSQL (produzione)
- **Notifiche**: Web Push API, Telegram Bot
- **Hosting**: Render.com (gratuito)

## Quick Start

1. Clona il repository
2. Installa le dipendenze: `pip install -r requirements.txt`
3. Configura le variabili d'ambiente
4. Avvia l'applicazione: `python run.py`

## Link Documentazione

- [Setup e Installazione](docs/setup.md)
- [API Documentation](docs/api.md)
- [Deployment Guide](docs/deployment.md)
- [Sistema Notifiche](docs/notifications.md)