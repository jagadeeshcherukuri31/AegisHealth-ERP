from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request


def roles_required(*roles):
    """Require a valid JWT whose role is in `roles` (admin always passes)."""
    def deco(fn):
        @wraps(fn)
        def wrapper(*a, **kw):
            verify_jwt_in_request()
            role = get_jwt().get("role")
            if role != "admin" and role not in roles:
                return jsonify(error="Forbidden for role: %s" % role), 403
            return fn(*a, **kw)
        return wrapper
    return deco
