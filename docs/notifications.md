# Sistema Notifiche

## Panoramica

Il sistema di notifiche supporta multiple piattaforme per informare gli utenti degli aggiornamenti dei giochi.

## Telegram Bot

### Setup
1. Crea bot con @BotFather su Telegram
2. Ottieni il token del bot
3. Aggiungi token alle variabili d'ambiente: `TELEGRAM_BOT_TOKEN`

### Configurazione Bot
```python
# Comandi bot supportati
/start - Avvia bot e ottieni chat_id
/help - Mostra aiuto
/status - Stato monitoraggio
```

### Ottenere Chat ID
1. Avvia conversazione con il bot
2. Invia `/start`
3. Il bot risponderà con il tuo chat_id
4. Usa questo ID per registrare l'utente

### Esempio Messaggio
```
🎮 Aggiornamento disponibile!

Gioco: Game Title
Nuova versione: v1.2
Link: https://f95zone.to/threads/game.12345/
```

## Web Push Notifications

### Setup Service Worker
```javascript
// sw.js
self.addEventListener('push', function(event) {
  const options = {
    body: event.data.text(),
    icon: '/static/icon-192.png',
    badge: '/static/badge-72.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: 'Vai al gioco',
        icon: '/static/checkmark.png'
      },
      {
        action: 'close',
        title: 'Chiudi',
        icon: '/static/xmark.png'
      }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification('F95Checker', options)
  );
});
```

### Subscription Management
```javascript
// Richiedi permesso notifiche
async function requestNotificationPermission() {
  const permission = await Notification.requestPermission();
  if (permission === 'granted') {
    await subscribeUser();
  }
}

// Sottoscrivi utente
async function subscribeUser() {
  const registration = await navigator.serviceWorker.ready;
  const subscription = await registration.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: urlBase64ToUint8Array(vapidPublicKey)
  });
  
  // Invia subscription al server
  await fetch('/api/subscribe', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(subscription)
  });
}
```

## Email Notifications

### Setup SMTP
```python
# config.py
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
```

### Invio Email
```python
from flask_mail import Mail, Message

def send_email(to, subject, body):
    msg = Message(
        subject=subject,
        recipients=[to],
        body=body,
        sender=app.config['MAIL_USERNAME']
    )
    mail.send(msg)
```

## Android App Integration

### API Polling
```java
// Polling service per Android
public class F95CheckerService extends Service {
    private static final int POLL_INTERVAL = 300000; // 5 minuti
    
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        startPolling();
        return START_STICKY;
    }
    
    private void startPolling() {
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                checkForUpdates();
                handler.postDelayed(this, POLL_INTERVAL);
            }
        }, POLL_INTERVAL);
    }
    
    private void checkForUpdates() {
        // Chiamata API per controllo aggiornamenti
        ApiClient.checkUpdates(new Callback<UpdateResponse>() {
            @Override
            public void onResponse(UpdateResponse response) {
                if (response.getUpdatesFound() > 0) {
                    showNotification(response.getMessage());
                }
            }
        });
    }
}
```

### Notifiche Android
```java
private void showNotification(String message) {
    NotificationCompat.Builder builder = new NotificationCompat.Builder(this, CHANNEL_ID)
        .setSmallIcon(R.drawable.ic_notification)
        .setContentTitle("F95Checker")
        .setContentText(message)
        .setPriority(NotificationCompat.PRIORITY_DEFAULT)
        .setAutoCancel(true);
    
    NotificationManagerCompat.from(this).notify(NOTIFICATION_ID, builder.build());
}
```

## Windows Desktop Notifications

### PowerShell Script
```powershell
# notify.ps1
param([string]$Title, [string]$Message)

Add-Type -AssemblyName System.Windows.Forms
$notification = New-Object System.Windows.Forms.NotifyIcon
$notification.Icon = [System.Drawing.SystemIcons]::Information
$notification.BalloonTipTitle = $Title
$notification.BalloonTipText = $Message
$notification.Visible = $True
$notification.ShowBalloonTip(5000)
```

### Python Windows Toast
```python
from win10toast import ToastNotifier

def show_windows_notification(title, message):
    toaster = ToastNotifier()
    toaster.show_toast(
        title,
        message,
        icon_path="icon.ico",
        duration=10,
        threaded=True
    )
```

## Configurazione Notifiche

### Tipi di Notifica
- `update`: Aggiornamento gioco disponibile
- `new`: Nuovo gioco aggiunto
- `error`: Errore nel controllo

### Personalizzazione
```python
# Modello notifica personalizzabile
class NotificationTemplate:
    def __init__(self, type, game, user):
        self.type = type
        self.game = game
        self.user = user
    
    def render(self):
        templates = {
            'update': f"🎮 {self.game.title} aggiornato a {self.game.version}!",
            'new': f"🆕 Nuovo gioco monitorato: {self.game.title}",
            'error': f"❌ Errore nel controllo di {self.game.title}"
        }
        return templates.get(self.type, "Notifica F95Checker")
```

## Testing

### Test Telegram
```bash
curl -X POST "https://api.telegram.org/bot<TOKEN>/sendMessage" \
  -d "chat_id=<CHAT_ID>&text=Test message"
```

### Test Web Push
```javascript
// Console browser
navigator.serviceWorker.ready.then(registration => {
  registration.showNotification('Test', {
    body: 'Test notification',
    icon: '/icon.png'
  });
});
```