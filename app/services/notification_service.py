import requests
from datetime import datetime
from app import db
from app.models import Notification, User
from app.config import Config

class NotificationService:
    """Servizio per gestire le notifiche"""
    
    def __init__(self):
        self.telegram_token = Config.TELEGRAM_BOT_TOKEN
    
    def create_change_notification(self, game, changes):
        """Crea notifica per cambiamenti nel gioco"""
        users = User.query.filter_by(is_active=True).all()
        
        game_name = game.game_title or game.title
        
        # Intestazione con immagine
        message = f"\ud83c\udfae <b>F95Checker - Aggiornamento!</b>\n\n"
        
        if game.image_url:
            # Invia prima l'immagine, poi il testo
            for user in users:
                self.send_telegram_photo(user.telegram_chat_id, game.image_url, f"\ud83c\udfaf {game_name}")
        
        # Status icon
        status_icon = ""
        if game.status:
            if 'completed' in game.status:
                status_icon = "\u2705 "
            elif 'abandoned' in game.status:
                status_icon = "\u274c "
        
        message += f"\ud83c\udfaf <b>Gioco:</b> {status_icon}{game_name}\n"
        
        # Dettagli cambiamenti
        for change in changes.get('changes', []):
            if change['type'] == 'version':
                message += f"\ud83d\udce6 <b>Versione:</b> {change['old']} \u2192 <b>{change['new']}</b>\n"
            elif change['type'] == 'status':
                old_status = self.format_status(change['old'])
                new_status = self.format_status(change['new'])
                message += f"\ud83d\udcca <b>Status:</b> {old_status} \u2192 <b>{new_status}</b>\n"
        
        if game.rating:
            stars = "\u2b50" * int(game.rating)
            message += f"\u2b50 <b>Rating:</b> {game.rating}/5 {stars}\n"
        
        if game.f95_updated_date:
            date_str = game.f95_updated_date.strftime('%d/%m/%Y')
            message += f"\ud83d\udcc5 <b>Aggiornato:</b> {date_str}\n"
        
        message += f"\n\ud83d\udd17 <a href='{game.url}'>Vai al gioco su F95Zone</a>"
        
        for user in users:
            notification = Notification(
                user_id=user.id,
                game_id=game.id,
                message=message,
                notification_type='update'
            )
            db.session.add(notification)
        
        db.session.commit()
        self.send_pending_notifications()
    
    def format_status(self, status):
        """Formatta status per visualizzazione"""
        if not status:
            return "In Development"
        if 'completed' in status:
            return "\u2705 Completed"
        if 'abandoned' in status:
            return "\u274c Abandoned"
        return status.title()
    
    def send_telegram_photo(self, chat_id, photo_url, caption):
        """Invia foto Telegram"""
        if not self.telegram_token:
            return False
        
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendPhoto"
            data = {
                'chat_id': chat_id,
                'photo': photo_url,
                'caption': caption,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, data=data)
            return response.status_code == 200
        except Exception as e:
            print(f"Errore invio foto Telegram: {e}")
            return False
    
    def create_update_notification(self, game):
        """Crea notifica per aggiornamento gioco"""
        users = User.query.filter_by(is_active=True).all()
        
        # Crea messaggio più ricco
        status_icon = ""
        if game.status:
            if 'completed' in game.status:
                status_icon = "✅ "
            elif 'abandoned' in game.status:
                status_icon = "❌ "
        
        game_name = game.game_title or game.title
        
        message = f"🎮 <b>Aggiornamento F95Checker!</b>\n\n" \
                 f"🎯 <b>Gioco:</b> {status_icon}{game_name}\n" \
                 f"📦 <b>Versione:</b> {game.version}\n"
        
        if game.rating:
            stars = "⭐" * int(game.rating)
            message += f"⭐ <b>Rating:</b> {game.rating}/5 {stars}\n"
        
        if game.f95_updated_date:
            date_str = game.f95_updated_date.strftime('%d/%m/%Y')
            message += f"📅 <b>Aggiornato:</b> {date_str}\n"
        
        message += f"\n🔗 <a href='{game.url}'>Vai al gioco su F95Zone</a>"
        
        for user in users:
            notification = Notification(
                user_id=user.id,
                game_id=game.id,
                message=message,
                notification_type='update'
            )
            
            db.session.add(notification)
        
        db.session.commit()
        self.send_pending_notifications()
    
    def send_pending_notifications(self):
        """Invia tutte le notifiche in sospeso"""
        notifications = Notification.query.filter_by(is_sent=False).all()
        
        for notification in notifications:
            if self.send_notification(notification):
                notification.is_sent = True
                notification.sent_at = datetime.utcnow()
        
        db.session.commit()
    
    def send_notification(self, notification):
        """Invia singola notifica"""
        user = notification.user
        
        # Telegram
        if user.telegram_chat_id and self.telegram_token:
            return self.send_telegram_message(user.telegram_chat_id, notification.message)
        
        # Email (da implementare)
        if user.email:
            return self.send_email(user.email, notification.message)
        
        return False
    
    def send_telegram_message(self, chat_id, message):
        """Invia messaggio Telegram"""
        if not self.telegram_token:
            print("Token Telegram non configurato")
            return False
        
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            data = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'HTML',
                'disable_web_page_preview': True
            }
            
            response = requests.post(url, data=data)
            result = response.json()
            
            if response.status_code == 200 and result.get('ok'):
                print(f"Messaggio Telegram inviato a {chat_id}")
                return True
            else:
                print(f"Errore Telegram: {result}")
                return False
            
        except Exception as e:
            print(f"Errore invio Telegram: {e}")
            return False
    
    def send_email(self, email, message):
        """Invia email (placeholder)"""
        # TODO: Implementare invio email
        print(f"Email da inviare a {email}: {message}")
        return True