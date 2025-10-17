import requests
from bs4 import BeautifulSoup
import re

url = "https://f95zone.to/threads/270418"
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(response.content, 'html.parser')

print("=== CERCA IMMAGINE ===")
# Cerca tutte le immagini
for img in soup.find_all('img'):
    src = img.get('src')
    if src and 'attachments' in src:
        print(f"IMG: {src}")

print("\n=== CERCA RATING ===")
# Cerca elementi con stelle o rating
for elem in soup.find_all(['span', 'div'], class_=re.compile(r'rating|star')):
    print(f"RATING ELEM: {elem.get('class')} - {elem.get_text()}")

# Cerca nel testo
text = soup.get_text()
if '5 stelle' in text.lower() or '5 star' in text.lower():
    print("Trovato riferimento a 5 stelle nel testo")

print("\n=== CERCA RECENSIONI ===")
# Cerca link o testo recensioni
for elem in soup.find_all(['a', 'span'], string=re.compile(r'review|recensio', re.I)):
    print(f"REVIEW: {elem.get_text()} - {elem.get('href', 'no-href')}")

print("\n=== HTML SAMPLE ===")
# Stampa un pezzo di HTML per vedere la struttura
first_post = soup.find('article', class_='message')
if first_post:
    print(first_post.prettify()[:1000])