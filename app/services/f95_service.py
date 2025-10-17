import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup
from app import db

class F95Service:
    """Servizio per interagire con F95Zone"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def extract_game_info(self, url):
        """Estrae informazioni del gioco dall'URL F95Zone"""
        try:
            # Estrai ID dal URL - supporta vari formati
            match = re.search(r'threads/(?:[^/]*\.)?(\d+)/?', url)
            if not match:
                return None
            
            f95_id = match.group(1)
            
            # Normalizza URL se necessario
            if not url.endswith('/'):
                url += '/'
            if 'f95zone.to' not in url:
                url = f'https://f95zone.to/threads/{f95_id}/'
            
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Estrai titolo thread
            title_elem = soup.find('h1', class_='p-title-value') or soup.find('h1') or soup.find('title')
            if title_elem:
                title = title_elem.get_text().strip()
                title = re.sub(r'\s+', ' ', title)
            else:
                title = f'Game {f95_id}'
            
            # Estrai titolo del gioco e tag di stato
            game_title = title
            status_tags = []
            
            # Cerca tag di stato importanti (con o senza parentesi)
            if re.search(r'\b(completed|complete)\b', title, re.IGNORECASE):
                status_tags.append('completed')
            if re.search(r'\b(abandoned|dropped)\b', title, re.IGNORECASE):
                status_tags.append('abandoned')

            
            # Cerca anche nei tag tra parentesi quadre
            if re.search(r'\[.*?(completed|complete).*?\]', title, re.IGNORECASE):
                status_tags.append('completed')
            if re.search(r'\[.*?(abandoned|dropped).*?\]', title, re.IGNORECASE):
                status_tags.append('abandoned')

            
            # Rimuovi tutti i tag e parole tecniche dal titolo
            game_title = re.sub(r'\[.*?\]', '', title).strip()
            
            # Rimuovi parole tecniche comuni
            tech_words = ['completed', 'abandoned', 'ren\'py', 'renpy', 'vn', 'visual novel', 
                         'rpg', 'html', 'unity', 'unreal', 'flash', 'java', 'android', 'pc',
                         'mac', 'linux', 'windows', 'final', 'demo', 'beta', 'alpha']
            
            for word in tech_words:
                game_title = re.sub(rf'\b{re.escape(word)}\b', '', game_title, flags=re.IGNORECASE)
            
            # Pulisci spazi multipli e caratteri extra
            game_title = re.sub(r'\s+', ' ', game_title).strip()
            game_title = re.sub(r'^[-\s]+|[-\s]+$', '', game_title)
            
            # Converti tag in stringa per il database
            status_string = ','.join(status_tags) if status_tags else None
            
            # Estrai versione
            version_patterns = [
                r'\[([v\d\.\-\w]+)\]',
                r'v([\d\.\-\w]+)',
                r'Version ([\d\.\-\w]+)',
            ]
            
            version = 'Unknown'
            for pattern in version_patterns:
                version_match = re.search(pattern, title, re.IGNORECASE)
                if version_match:
                    version = version_match.group(1)
                    break
            
            # Estrai immagine - rimuovi thumb per ottenere quella grande
            image_url = None
            
            first_post = soup.find('article', class_='message')
            if first_post:
                for img in first_post.find_all('img'):
                    src = img.get('src')
                    if src and 'attachments.f95zone.to' in src:
                        # Rimuovi /thumb/ per ottenere immagine grande
                        if '/thumb/' in src:
                            image_url = src.replace('/thumb/', '/')
                        else:
                            image_url = src
                        break
            
            print(f"Immagine trovata: {image_url}")
            
            # Estrai data ultimo aggiornamento
            update_date = None
            first_post = soup.find('article', class_='message')
            if first_post:
                time_elem = first_post.find('time')
                if time_elem and time_elem.get('datetime'):
                    try:
                        from datetime import datetime
                        date_str = time_elem.get('datetime')
                        # Converte ISO datetime in oggetto datetime
                        update_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                        print(f"Data aggiornamento trovata: {update_date}")
                    except Exception as e:
                        print(f"Errore parsing data: {e}")
            
            # Estrai descrizione
            description = ''
            desc_elem = soup.find('div', class_='bbWrapper')
            if desc_elem:
                description = desc_elem.get_text()[:500] + '...' if len(desc_elem.get_text()) > 500 else desc_elem.get_text()
            
            # Estrai rating e recensioni - selettori più specifici
            rating = None
            review_count = 0
            weighted_score = None
            
            # Estrai rating - uso selettori trovati nel debug
            print(f"\n=== DEBUG RATING {f95_id} ===")
            
            # Cerca rating con selettori specifici di F95Zone
            rating_elem = soup.find('span', string=re.compile(r'[\d\.]+\s*star\(s\)'))
            if rating_elem:
                try:
                    rating_text = rating_elem.get_text().strip()
                    rating_match = re.search(r'([\d\.]+)', rating_text)
                    if rating_match:
                        rating = float(rating_match.group(1))
                        print(f"Rating trovato: {rating}")
                except Exception as e:
                    print(f"Errore parsing rating: {e}")
            

            
            # Cerca numero recensioni - pattern specifico F95Zone
            vote_elem = soup.find('span', string=re.compile(r'\d+\s*Vote'))
            if vote_elem:
                try:
                    vote_text = vote_elem.get_text().strip()
                    vote_match = re.search(r'(\d+)', vote_text)
                    if vote_match:
                        review_count = int(vote_match.group(1))
                        print(f"Voti trovati: {review_count}")
                except Exception as e:
                    print(f"Errore parsing voti: {e}")
            

            
            # Calcola weighted score
            if rating and review_count > 0:
                weighted_score = rating * (review_count / (review_count + 10))
                print(f"Score: {weighted_score}")
            
            print(f"Finale - Rating: {rating}, Reviews: {review_count}")
            print("=== FINE DEBUG ===")
            
            return {
                'f95_id': f95_id,
                'title': title,
                'game_title': game_title,
                'version': version,
                'status': status_string,
                'url': url,
                'image_url': image_url,
                'description': description,
                'f95_updated_date': update_date,
                'rating': rating,
                'review_count': review_count,
                'weighted_score': weighted_score
            }
            
        except Exception as e:
            print(f"Errore nell'estrazione info gioco da {url}: {e}")
            print(f"Status code: {response.status_code if 'response' in locals() else 'N/A'}")
            return None
    

            
        except Exception as e:
            print(f"Errore nel controllo aggiornamento per {game.title}: {e}")
            return False
    
    def check_for_changes(self, game):
        """Controlla cambiamenti nel gioco (versione, status, ecc.)"""
        try:
            game_info = self.extract_game_info(game.url)
            if not game_info:
                return {'updated': False}
            
            changes = {'updated': False, 'changes': []}
            
            # Aggiorna timestamp controllo
            game.last_checked = datetime.utcnow()
            
            # Controlla versione
            if game_info['version'] != game.version:
                changes['changes'].append({
                    'type': 'version',
                    'old': game.version,
                    'new': game_info['version']
                })
                game.version = game_info['version']
                game.last_updated = datetime.utcnow()
                changes['updated'] = True
            
            # Controlla status
            old_status = game.status or ''
            new_status = game_info.get('status') or ''
            if old_status != new_status:
                changes['changes'].append({
                    'type': 'status',
                    'old': old_status,
                    'new': new_status
                })
                game.status = new_status
                changes['updated'] = True
            
            # Aggiorna altri campi
            game.f95_updated_date = game_info.get('f95_updated_date')
            game.rating = game_info.get('rating')
            game.review_count = game_info.get('review_count', 0)
            game.weighted_score = game_info.get('weighted_score')
            
            db.session.commit()
            return changes
            
        except Exception as e:
            print(f"Errore nel controllo cambiamenti per {game.title}: {e}")
            return {'updated': False}
    
    def get_game_details(self, f95_id):
        """Ottieni dettagli completi del gioco"""
        url = f"https://f95zone.to/threads/{f95_id}/"
        return self.extract_game_info(url)