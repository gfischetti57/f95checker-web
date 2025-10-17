from functools import wraps
from flask import request, Response, current_app
import os

def check_auth(username, password):
    """Check if username/password combination is valid."""
    admin_user = os.getenv('ADMIN_USERNAME', 'admin')
    admin_pass = os.getenv('ADMIN_PASSWORD', 'f95checker2024')
    return username == admin_user and password == admin_pass

def authenticate():
    """Send 401 response that enables basic auth."""
    return Response(
        'F95Checker - Accesso Richiesto\n'
        'Inserisci username e password per accedere.', 401,
        {'WWW-Authenticate': 'Basic realm="F95Checker Admin"'})

def requires_auth(f):
    """Decorator for routes that require authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated