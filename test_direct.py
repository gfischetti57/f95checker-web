import requests
import json

token = "8306286141:AAHgdSI6ntiQtqlYd_87aKunoWeL7FZIFBE"
chat_id = "-4865272838"

print("=== TEST TELEGRAM ===")

# Test 1: Info bot
print("1. Info bot:")
response = requests.get(f"https://api.telegram.org/bot{token}/getMe")
print(json.dumps(response.json(), indent=2))

# Test 2: Info chat
print("\n2. Info chat:")
response = requests.get(f"https://api.telegram.org/bot{token}/getChat", params={"chat_id": chat_id})
print(json.dumps(response.json(), indent=2))

# Test 3: Invio messaggio
print("\n3. Invio messaggio:")
response = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={
    "chat_id": chat_id,
    "text": "🎮 Test F95Checker - Messaggio di prova"
})
print(f"Status: {response.status_code}")
print(json.dumps(response.json(), indent=2))