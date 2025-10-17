from datetime import datetime
from app import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    f95_id = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    game_title = db.Column(db.String(200))
    version = db.Column(db.String(50))
    status = db.Column(db.String(100))
    url = db.Column(db.String(500), nullable=False)
    image_url = db.Column(db.String(500))
    description = db.Column(db.Text)
    changelog = db.Column(db.Text)
    f95_updated_date = db.Column(db.DateTime)
    rating = db.Column(db.Float)
    review_count = db.Column(db.Integer, default=0)
    weighted_score = db.Column(db.Float)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    last_checked = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relazioni
    notifications = db.relationship('Notification', backref='game', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Game {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'f95_id': self.f95_id,
            'title': self.title,
            'game_title': self.game_title,
            'version': self.version,
            'status': self.status,
            'url': self.url,
            'image_url': self.image_url,
            'description': self.description,
            'changelog': self.changelog,
            'rating': self.rating,
            'review_count': self.review_count,
            'weighted_score': self.weighted_score,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'last_checked': self.last_checked.isoformat() if self.last_checked else None,
            'is_active': self.is_active
        }