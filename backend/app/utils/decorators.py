from functools import wraps
from flask import session, jsonify
from app.models.user import User


def login_required(f):
    """Decorator that checks if a user is logged in via session."""
    @wraps(f)
    def decorated(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        user = User.query.get(user_id)
        if not user:
            session.clear()
            return jsonify({'error': 'User not found'}), 401
        kwargs['current_user'] = user
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    """Decorator that checks if the logged-in user is an admin."""
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        current_user = kwargs.get('current_user')
        if current_user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated
