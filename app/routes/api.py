from flask import Blueprint, request, jsonify
from app import db
from app.models import Game, User, Notification
from app.services.f95_service import F95Service
from app.services.notification_service import NotificationService
from app.services.github_service import GitHubService
from app.auth import requires_auth

api_bp = Blueprint('api', __name__)

@api_bp.route('/games', methods=['GET'])
def get_games():
    """Ottieni lista giochi"""
    games = Game.query.all()
    return jsonify([game.to_dict() for game in games])

@api_bp.route('/games', methods=['POST'])
@requires_auth
def add_game():
    """Aggiungi uno o più giochi da monitorare"""
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': 'URL richiesto'}), 400
    
    urls = data['url'].strip().split('\n') if '\n' in data['url'] else [data['url']]
    f95_service = F95Service()
    results = []
    errors = []
    
    for url in urls:
        url = url.strip()
        if not url:
            continue
            
        game_info = f95_service.extract_game_info(url)
        if not game_info:
            errors.append(f'Impossibile estrarre info da: {url}')
            continue
        
        # Controlla se esiste già
        existing = Game.query.filter_by(f95_id=game_info['f95_id']).first()
        if existing:
            errors.append(f'Gioco già monitorato: {game_info["title"]}')
            continue
        
        game = Game(
            f95_id=game_info['f95_id'],
            title=game_info['title'],
            game_title=game_info['game_title'],
            version=game_info['version'],
            status=game_info.get('status'),
            url=url,
            image_url=game_info.get('image_url'),
            description=game_info.get('description'),
            f95_updated_date=game_info.get('f95_updated_date'),
            rating=game_info.get('rating'),
            review_count=game_info.get('review_count', 0),
            weighted_score=game_info.get('weighted_score')
        )
        
        db.session.add(game)
        results.append(game_info)
    
    db.session.commit()
    
    response = {'added': len(results), 'games': results}
    if errors:
        response['errors'] = errors
    
    return jsonify(response), 201 if results else 400

@api_bp.route('/games/<int:game_id>', methods=['DELETE'])
@requires_auth
def delete_game(game_id):
    """Rimuovi gioco dal monitoraggio"""
    game = Game.query.get_or_404(game_id)
    db.session.delete(game)
    db.session.commit()
    return '', 204

@api_bp.route('/check-updates', methods=['POST'])
@requires_auth
def check_updates():
    """Forza controllo aggiornamenti"""
    f95_service = F95Service()
    notification_service = NotificationService()
    
    games = Game.query.filter_by(is_active=True).all()
    updates_found = 0
    
    for game in games:
        changes = f95_service.check_for_changes(game)
        if changes['updated']:
            updates_found += 1
            notification_service.create_change_notification(game, changes)
    
    return jsonify({
        'message': f'Controllo completato. {updates_found} aggiornamenti trovati.',
        'updates_found': updates_found
    })

@api_bp.route('/users', methods=['POST'])
def register_user():
    """Registra nuovo utente"""
    data = request.get_json()
    
    if not data or 'username' not in data:
        return jsonify({'error': 'Username richiesto'}), 400
    
    existing = User.query.filter_by(username=data['username']).first()
    if existing:
        return jsonify({'error': 'Username già esistente'}), 409
    
    user = User(
        username=data['username'],
        telegram_chat_id=data.get('telegram_chat_id'),
        email=data.get('email')
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user.to_dict()), 201

@api_bp.route('/register-telegram', methods=['POST'])
def register_telegram():
    """Registra utente Telegram per notifiche"""
    data = request.get_json()
    
    if not data or 'chat_id' not in data:
        return jsonify({'error': 'chat_id richiesto'}), 400
    
    chat_id = str(data['chat_id'])
    username = data.get('username', f'user_{chat_id}')
    
    # Controlla se esiste già
    existing = User.query.filter_by(telegram_chat_id=chat_id).first()
    if existing:
        return jsonify({'message': 'Utente già registrato', 'user': existing.to_dict()}), 200
    
    user = User(
        username=username,
        telegram_chat_id=chat_id
    )
    
    db.session.add(user)
    db.session.commit()
    
    # Invia messaggio di benvenuto
    notification_service = NotificationService()
    welcome_msg = f"🎉 <b>Benvenuto in F95Checker!</b>\n\n" \
                 f"✅ Registrazione completata\n" \
                 f"🔔 Riceverai notifiche per aggiornamenti giochi\n" \
                 f"🎮 Buon gaming!"
    
    notification_service.send_telegram_message(chat_id, welcome_msg)
    
    return jsonify({
        'message': 'Utente registrato con successo!',
        'user': user.to_dict()
    }), 201

@api_bp.route('/check-github', methods=['POST'])
def check_github():
    """Controlla aggiornamenti GitHub F95Checker"""
    github_service = GitHubService()
    updates = github_service.check_for_updates()
    
    if updates:
        notification_service = NotificationService()
        notification_service.send_pending_notifications()
    
    return jsonify({
        'message': f'Controllo GitHub completato. {len(updates)} aggiornamenti trovati.',
        'updates_found': len(updates),
        'updates': updates
    })

@api_bp.route('/github-info', methods=['GET'])
def github_info():
    """Ottieni informazioni repository GitHub"""
    github_service = GitHubService()
    info = github_service.get_repo_info()
    
    return jsonify(info or {'error': 'Impossibile recuperare info repository'})

@api_bp.route('/refresh-all-games', methods=['POST'])
@requires_auth
def refresh_all_games():
    """Ricarica dati per tutti i giochi esistenti"""
    f95_service = F95Service()
    games = Game.query.all()
    updated_count = 0
    
    for game in games:
        try:
            game_info = f95_service.extract_game_info(game.url)
            if game_info:
                game.game_title = game_info.get('game_title')
                game.status = game_info.get('status')
                game.image_url = game_info.get('image_url')
                game.description = game_info.get('description')
                game.f95_updated_date = game_info.get('f95_updated_date')
                game.rating = game_info.get('rating')
                game.review_count = game_info.get('review_count', 0)
                game.weighted_score = game_info.get('weighted_score')
                updated_count += 1
        except Exception as e:
            print(f"Errore aggiornamento {game.title}: {e}")
    
    db.session.commit()
    
    return jsonify({
        'message': f'Aggiornati {updated_count} giochi su {len(games)} totali.',
        'updated_count': updated_count,
        'total_games': len(games)
    })