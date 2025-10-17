import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///f95checker.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # F95Zone settings
    F95_BASE_URL = 'https://f95zone.to'
    CHECK_INTERVAL = int(os.environ.get('CHECK_INTERVAL', 3600))  # secondi
    
    # Notification settings
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    # App settings
    MAX_GAMES_PER_USER = int(os.environ.get('MAX_GAMES_PER_USER', 50))