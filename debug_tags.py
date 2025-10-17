import requests
from bs4 import BeautifulSoup
import re

# Test giochi specifici
games = [
    ("48734", "https://f95zone.to/threads/48734"),
    ("15459", "https://f95zone.to/threads/15459")
]

for game_id, url in games:
    print(f"\n=== GAME {game_id} ===")
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Trova titolo
    title_elem = soup.find('h1', class_='p-title-value')
    if title_elem:
        title = title_elem.get_text().strip()
        print(f"Titolo completo: {title}")
        
        # Test pattern
        if re.search(r'\\[.*?(completed|complete).*?\\]', title, re.IGNORECASE):
            print("✅ COMPLETED trovato")
        if re.search(r'\\[.*?(abandoned|dropped).*?\\]', title, re.IGNORECASE):
            print("❌ ABANDONED trovato")
        
        # Cerca anche senza parentesi quadre
        if re.search(r'\\b(completed|complete)\\b', title, re.IGNORECASE):
            print("✅ COMPLETED (senza tag) trovato")
        if re.search(r'\\b(abandoned|dropped)\\b', title, re.IGNORECASE):
            print("❌ ABANDONED (senza tag) trovato")
            
        # Cerca nel prefix del thread
        prefix_elem = soup.find('span', class_='label-append')
        if prefix_elem:
            prefix = prefix_elem.get_text().strip()
            print(f"Prefix trovato: {prefix}")