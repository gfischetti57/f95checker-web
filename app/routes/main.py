from flask import Blueprint, render_template, request, jsonify
from app.models import Game, User, Notification
from app.services.f95_service import F95Service
from app.auth import requires_auth

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@requires_auth
def index():
    """Pagina principale con dashboard"""
    stats = {
        'total_games': Game.query.count(),
        'active_games': Game.query.filter_by(is_active=True).count(),
        'total_users': User.query.count(),
        'pending_notifications': Notification.query.filter_by(is_sent=False).count()
    }
    return render_template('home.html', stats=stats)



@main_bp.route('/games')
@requires_auth
def games():
    """Lista giochi monitorati"""
    sort_by = request.args.get('sort', 'id')
    
    if hasattr(Game, sort_by):
        games = Game.query.order_by(getattr(Game, sort_by).desc()).all()
    else:
        games = Game.query.all()
    
    return render_template('games.html', games=games)

@main_bp.route('/notifications')
@requires_auth
def notifications():
    """Lista notifiche"""
    notifications = Notification.query.order_by(Notification.created_at.desc()).limit(50).all()
    return render_template('notifications.html', notifications=notifications)

@main_bp.route('/game/<int:game_id>')
@requires_auth
def game_detail(game_id):
    """Scheda dettaglio gioco"""
    game = Game.query.get_or_404(game_id)
    return render_template('game_detail.html', game=game)