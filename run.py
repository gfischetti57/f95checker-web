from app import create_app, db
from app.utils.scheduler import UpdateScheduler

app = create_app()

# Inizializza database
with app.app_context():
    db.create_all()

# Avvia scheduler
scheduler = UpdateScheduler(app)
scheduler.start()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)