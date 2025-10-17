import requests

# Test bot Telegram
token = "8306286141:AAHgdSI6ntiQtqlYd_87aKunoWeL7FZIFBE"

# Test 1: Info bot
response = requests.get(f"https://api.telegram.org/bot{token}/getMe")
print("Bot info:", response.json())

# Test 2: Invia messaggio di test (sostituisci con il tuo chat_id)
# Per ottenere chat_id: avvia conversazione con @giorgiof95bot e invia /start
chat_id = "YOUR_CHAT_ID"  # Sostituisci con il tuo chat_id

test_message = """🎮 F95Checker Test!

Questo è un messaggio di test per verificare le notifiche.

✅ Bot configurato correttamente!"""

# Decommentare quando hai il chat_id:
# response = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", {
#     'chat_id': chat_id,
#     'text': test_message,
#     'parse_mode': 'HTML'
# })
# print("Messaggio inviato:", response.json())