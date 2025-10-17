from app import create_app, db

app = create_app()

with app.app_context():
    # Elimina e ricrea tutte le tabelle
    db.drop_all()
    db.create_all()
    print("Database ricreato con successo!")
    print("Tutte le tabelle sono state aggiornate con i nuovi campi.")