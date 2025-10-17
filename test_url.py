from app.services.f95_service import F95Service

# Test rapido
service = F95Service()
url = "https://f95zone.to/threads/4907"
result = service.extract_game_info(url)
print(f"Risultato: {result}")

# Test con URL completo
url2 = "https://f95zone.to/threads/4907/"
result2 = service.extract_game_info(url2)
print(f"Risultato 2: {result2}")