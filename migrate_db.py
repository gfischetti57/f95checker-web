from app import create_app, db
from app.models import Game

app = create_app()

with app.app_context():
    # Aggiungi le nuove colonne al database esistente
    try:
        db.engine.execute('ALTER TABLE game ADD COLUMN game_title VARCHAR(200)')
        print("Aggiunta colonna game_title")
    except:
        print("Colonna game_title già esistente")
    
    try:
        db.engine.execute('ALTER TABLE game ADD COLUMN image_url VARCHAR(500)')
        print("Aggiunta colonna image_url")
    except:
        print("Colonna image_url già esistente")
    
    try:
        db.engine.execute('ALTER TABLE game ADD COLUMN description TEXT')
        print("Aggiunta colonna description")
    except:
        print("Colonna description già esistente")
    
    try:
        db.engine.execute('ALTER TABLE game ADD COLUMN changelog TEXT')
        print("Aggiunta colonna changelog")
    except:
        print("Colonna changelog già esistente")
    
    try:
        db.engine.execute('ALTER TABLE game ADD COLUMN rating FLOAT')
        print("Aggiunta colonna rating")
    except:
        print("Colonna rating già esistente")
    
    try:
        db.engine.execute('ALTER TABLE game ADD COLUMN review_count INTEGER DEFAULT 0')
        print("Aggiunta colonna review_count")
    except:
        print("Colonna review_count già esistente")
    
    try:
        db.engine.execute('ALTER TABLE game ADD COLUMN weighted_score FLOAT')
        print("Aggiunta colonna weighted_score")
    except:
        print("Colonna weighted_score già esistente")
    
    print("Migrazione completata!")