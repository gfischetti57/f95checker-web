import requests
import json
from datetime import datetime
from app import db
from app.models import Notification, User

class GitHubService:
    """Servizio per monitorare repository GitHub"""
    
    def __init__(self):
        self.api_base = "https://api.github.com"
        self.repo_url = "https://github.com/WillyJL/F95Checker"
        self.repo_api = f"{self.api_base}/repos/WillyJL/F95Checker"
        self.last_check_file = "github_last_check.json"
    
    def get_latest_release(self):
        """Ottieni ultima release"""
        try:
            response = requests.get(f"{self.repo_api}/releases/latest")
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Errore nel controllo release: {e}")
        return None
    
    def get_latest_commits(self, limit=10):
        """Ottieni ultimi commit"""
        try:
            response = requests.get(f"{self.repo_api}/commits?per_page={limit}")
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Errore nel controllo commit: {e}")
        return []
    
    def load_last_check(self):
        """Carica ultimo controllo"""
        try:
            with open(self.last_check_file, 'r') as f:
                return json.load(f)
        except:
            return {"last_release": None, "last_commit": None}
    
    def save_last_check(self, data):
        """Salva ultimo controllo"""
        try:
            with open(self.last_check_file, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Errore nel salvare controllo: {e}")
    
    def check_for_updates(self):
        """Controlla aggiornamenti GitHub"""
        last_check = self.load_last_check()
        updates_found = []
        
        # Controlla release
        latest_release = self.get_latest_release()
        if latest_release and latest_release['tag_name'] != last_check.get('last_release'):
            updates_found.append({
                'type': 'release',
                'title': f"Nuova Release: {latest_release['tag_name']}",
                'description': latest_release['body'][:500],
                'url': latest_release['html_url'],
                'date': latest_release['published_at']
            })
            last_check['last_release'] = latest_release['tag_name']
        
        # Controlla commit
        commits = self.get_latest_commits(5)
        if commits:
            latest_commit = commits[0]['sha']
            if latest_commit != last_check.get('last_commit'):
                for commit in commits:
                    if commit['sha'] == last_check.get('last_commit'):
                        break
                    updates_found.append({
                        'type': 'commit',
                        'title': f"Nuovo Commit: {commit['commit']['message'][:50]}...",
                        'description': commit['commit']['message'],
                        'url': commit['html_url'],
                        'date': commit['commit']['author']['date']
                    })
                last_check['last_commit'] = latest_commit
        
        # Salva controllo
        if updates_found:
            self.save_last_check(last_check)
            self.create_notifications(updates_found)
        
        return updates_found
    
    def create_notifications(self, updates):
        """Crea notifiche per aggiornamenti GitHub"""
        users = User.query.filter_by(is_active=True).all()
        
        for update in updates:
            message = f"🔄 F95Checker GitHub Update!\n\n" \
                     f"{update['title']}\n" \
                     f"{update['description']}\n\n" \
                     f"Link: {update['url']}"
            
            for user in users:
                notification = Notification(
                    user_id=user.id,
                    game_id=None,
                    message=message,
                    notification_type='github_update'
                )
                db.session.add(notification)
        
        db.session.commit()
    
    def get_repo_info(self):
        """Ottieni info repository"""
        try:
            response = requests.get(self.repo_api)
            if response.status_code == 200:
                repo = response.json()
                return {
                    'name': repo['name'],
                    'description': repo['description'],
                    'stars': repo['stargazers_count'],
                    'forks': repo['forks_count'],
                    'language': repo['language'],
                    'updated_at': repo['updated_at'],
                    'url': repo['html_url']
                }
        except Exception as e:
            print(f"Errore nel recupero info repo: {e}")
        return None