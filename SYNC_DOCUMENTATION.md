# Documentazione Sincronizzazione F95Checker

## Database Identificati

### 1. F95Checker Windows (Desktop)
- **Percorso**: `c:\Users\gfisc\AppData\Roaming\f95checker\db.sqlite3`
- **Tabella principale**: `games`
- **Campi rilevanti**:
  - `id`: ID interno
  - `name`: Nome del gioco
  - `url`: URL completo del thread F95Zone
  - `version`: Versione del gioco
  - `developer`: Sviluppatore
  - **Thread ID**: Estratto dall'URL con regex `f95zone\.to/threads/(\d+)`

### 2. F95Checker Web (Online)
- **Percorso**: `c:\Python\f95checker-web\instance\f95checker.db`
- **Tabella principale**: `game`
- **Campi rilevanti**:
  - `id`: ID interno
  - `f95_id`: Thread ID di F95Zone (campo diretto)
  - `title`: Titolo del gioco
  - `url`: URL completo del thread
  - `version`: Versione del gioco

## Statistiche Database

### F95Checker Windows
- **Thread totali**: 154
- **Range thread ID**: 4815 - 271592
- **File estratti**:
  - `f95checker_thread_ids.txt`: Lista thread ID
  - `f95checker_threads_detailed.json`: Dettagli completi

### F95Checker Web
- **Thread totali**: 154
- **Range thread ID**: 4815 - 271592
- **Stato**: Tutti thread attivi

## Funzione di Sincronizzazione

La funzione `sync_threads_from_desktop()` implementata:

1. **Legge** il database desktop F95Checker Windows
2. **Estrae** thread ID dagli URL
3. **Confronta** con il database web
4. **Aggiunge** thread mancanti al database web
5. **Aggiorna** thread esistenti se necessario

### Endpoint API
- **URL**: `/api/sync-threads`
- **Metodo**: POST
- **Risposta**: JSON con statistiche di sincronizzazione

### Utilizzo

#### 1. Via API REST
```bash
curl -X POST http://localhost:5000/api/sync-threads
```

#### 2. Via Interfaccia Web
- Accedi alla Dashboard
- Clicca su "Sincronizza da Desktop"

#### 3. Via Comando CLI
```bash
cd f95checker-web
python sync_command.py
```

## Note Tecniche

- La sincronizzazione è **unidirezionale**: Desktop → Web
- I thread esistenti nel web vengono **preservati**
- Solo i thread **mancanti** vengono aggiunti
- I thread esistenti vengono **aggiornati** se la versione è diversa
- La funzione è **sicura** e non elimina dati esistenti
- Richiede che l'applicazione desktop F95Checker sia installata

## File Implementati

- `app/services/sync_service.py` - Servizio di sincronizzazione
- `sync_command.py` - Comando CLI
- `test_sync.py` - Script di test
- Endpoint API: `/api/sync-threads`
- Pulsante nella Dashboard web