import schedule
import time
import threading
from app.services.f95_service import F95Service
from app.services.notification_service import NotificationService
from app.services.github_service import GitHubService
from app.models import Game

class UpdateScheduler:
    """Scheduler per controlli automatici"""
    
    def __init__(self, app):
        self.app = app
        self.f95_service = F95Service()
        self.notification_service = NotificationService()
        self.github_service = GitHubService()
        self.running = False
    
    def check_all_games(self):
        """Controlla tutti i giochi attivi"""
        with self.app.app_context():
            games = Game.query.filter_by(is_active=True).all()
            updates_found = 0
            
            for game in games:
                changes = self.f95_service.check_for_changes(game)
                if changes['updated']:
                    updates_found += 1
                    self.notification_service.create_change_notification(game, changes)
            
            print(f"Controllo automatico completato. {updates_found} aggiornamenti trovati.")
    
    def check_github_updates(self):
        """Controlla aggiornamenti repository GitHub"""
        with self.app.app_context():
            updates = self.github_service.check_for_updates()
            if updates:
                print(f"Trovati {len(updates)} aggiornamenti GitHub F95Checker")
                self.notification_service.send_pending_notifications()
            else:
                print("Nessun aggiornamento GitHub trovato")
    
    def start(self):
        """Avvia lo scheduler"""
        if self.running:
            return
        
        # Programma controlli ogni ora
        schedule.every().hour.do(self.check_all_games)
        schedule.every(6).hours.do(self.check_github_updates)
        
        self.running = True
        
        def run_scheduler():
            while self.running:
                schedule.run_pending()
                time.sleep(60)  # Controlla ogni minuto
        
        thread = threading.Thread(target=run_scheduler, daemon=True)
        thread.start()
        print("Scheduler avviato - controlli ogni ora")
    
    def stop(self):
        """Ferma lo scheduler"""
        self.running = False
        schedule.clear()
        print("Scheduler fermato")