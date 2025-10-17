# API Documentation

## Endpoint Disponibili

### Games

#### GET /api/games
Ottieni lista di tutti i giochi monitorati.

**Response:**
```json
[
  {
    "id": 1,
    "f95_id": "12345",
    "title": "Game Title [v1.0]",
    "version": "v1.0",
    "url": "https://f95zone.to/threads/game.12345/",
    "last_updated": "2024-01-01T12:00:00",
    "last_checked": "2024-01-01T12:00:00",
    "is_active": true
  }
]
```

#### POST /api/games
Aggiungi nuovo gioco da monitorare.

**Request:**
```json
{
  "url": "https://f95zone.to/threads/game-name.12345/"
}
```

**Response:**
```json
{
  "id": 1,
  "f95_id": "12345",
  "title": "Game Title [v1.0]",
  "version": "v1.0",
  "url": "https://f95zone.to/threads/game.12345/",
  "last_updated": "2024-01-01T12:00:00",
  "last_checked": "2024-01-01T12:00:00",
  "is_active": true
}
```

**Errori:**
- `400`: URL richiesto
- `409`: Gioco già monitorato

#### DELETE /api/games/{id}
Rimuovi gioco dal monitoraggio.

**Response:** `204 No Content`

### Updates

#### POST /api/check-updates
Forza controllo aggiornamenti per tutti i giochi.

**Response:**
```json
{
  "message": "Controllo completato. 2 aggiornamenti trovati.",
  "updates_found": 2
}
```

### Users

#### POST /api/users
Registra nuovo utente per le notifiche.

**Request:**
```json
{
  "username": "user123",
  "telegram_chat_id": "123456789",
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "id": 1,
  "username": "user123",
  "telegram_chat_id": "123456789",
  "email": "user@example.com",
  "is_active": true,
  "created_at": "2024-01-01T12:00:00"
}
```

**Errori:**
- `400`: Username richiesto
- `409`: Username già esistente

## Codici di Stato HTTP

- `200`: Successo
- `201`: Creato
- `204`: Nessun contenuto
- `400`: Richiesta non valida
- `404`: Non trovato
- `409`: Conflitto
- `500`: Errore server

## Esempi di Utilizzo

### JavaScript/Fetch
```javascript
// Aggiungi gioco
const response = await fetch('/api/games', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    url: 'https://f95zone.to/threads/game.12345/'
  })
});

const game = await response.json();
```

### Python/Requests
```python
import requests

# Ottieni giochi
response = requests.get('http://localhost:5000/api/games')
games = response.json()

# Aggiungi gioco
data = {'url': 'https://f95zone.to/threads/game.12345/'}
response = requests.post('http://localhost:5000/api/games', json=data)
```

### cURL
```bash
# Ottieni giochi
curl -X GET http://localhost:5000/api/games

# Aggiungi gioco
curl -X POST http://localhost:5000/api/games \
  -H "Content-Type: application/json" \
  -d '{"url":"https://f95zone.to/threads/game.12345/"}'

# Controlla aggiornamenti
curl -X POST http://localhost:5000/api/check-updates
```

## Rate Limiting

Attualmente non implementato, ma raccomandato per produzione:
- Max 100 richieste per IP per ora
- Max 10 richieste per minuto per endpoint di controllo

## Autenticazione

Attualmente non implementata. Per produzione considerare:
- API Key
- JWT Token
- OAuth 2.0