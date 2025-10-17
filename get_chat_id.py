import requests

token = "8306286141:AAHgdSI6ntiQtqlYd_87aKunoWeL7FZIFBE"

# Ottieni gli ultimi messaggi per trovare il chat_id
response = requests.get(f"https://api.telegram.org/bot{token}/getUpdates")
result = response.json()

print("=== ULTIMI MESSAGGI ===")
if result.get('ok') and result.get('result'):
    for update in result['result']:
        if 'message' in update:
            msg = update['message']
            chat = msg['chat']
            print(f"Chat ID: {chat['id']}")
            print(f"Tipo: {chat['type']}")
            print(f"Nome: {chat.get('title', chat.get('first_name', 'N/A'))}")
            print(f"Messaggio: {msg.get('text', 'N/A')}")
            print("---")
else:
    print("Nessun messaggio trovato o errore:", result)

print("\nUsa uno dei Chat ID sopra per registrarti!")