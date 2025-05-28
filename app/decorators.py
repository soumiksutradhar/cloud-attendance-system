from functools import wraps
from flask import abort
from flask_login import current_user

def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(403)  # Forbidden if not logged in
            if current_user.role not in roles:
                abort(403)  # Forbidden if role not allowed
            return f(*args, **kwargs)
        return decorated_function
    return decorator
