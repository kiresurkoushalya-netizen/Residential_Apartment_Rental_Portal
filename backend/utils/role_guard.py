from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def role_required(required_role: str):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # ✅ ensures JWT exists
            verify_jwt_in_request()

            claims = get_jwt()
            role = claims.get("role")

            if role != required_role:
                return jsonify({"message": "Access denied"}), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator


# ✅ Optional: allow multiple roles
def roles_required(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            role = claims.get("role")

            if role not in allowed_roles:
                return jsonify({"message": "Access denied"}), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator
