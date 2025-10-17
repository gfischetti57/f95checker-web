import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///f95checker.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Telegram Bot Configuration
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    # GitHub Configuration
    GITHUB_REPO = os.environ.get('GITHUB_REPO') or 'Willy-JL/F95Checker'
    
    # Desktop Database Path (configurabile)
    DESKTOP_DB_PATH = os.environ.get('DESKTOP_DB_PATH') or r'c:\Users\gfisc\AppData\Roaming\f95checker\db.sqlite3'
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size