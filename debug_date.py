import requests
from bs4 import BeautifulSoup
import re

url = "https://f95zone.to/threads/270418"
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(response.content, 'html.parser')

print("=== CERCA DATA AGGIORNAMENTO ===")

# Cerca nel primo post
first_post = soup.find('article', class_='message')
if first_post:
    # Cerca timestamp
    time_elem = first_post.find('time')
    if time_elem:
        print(f"Time elem: {time_elem.get('datetime')} - {time_elem.get_text()}")
    
    # Cerca date nel testo
    date_patterns = [
        r'Updated?:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'Last\s*Update:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'(\d{1,2}\s+\w+\s+\d{4})',
        r'(\w+\s+\d{1,2},?\s+\d{4})'
    ]
    
    text = first_post.get_text()
    for pattern in date_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            print(f"Pattern {pattern}: {matches}")

# Cerca anche nel thread info
thread_info = soup.find('div', class_='p-description')
if thread_info:
    print(f"Thread info: {thread_info.get_text()}")

print("\n=== HTML SAMPLE ===")
print(soup.prettify()[:2000])