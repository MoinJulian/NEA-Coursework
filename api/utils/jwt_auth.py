"""
JWT token utilities for authentication
"""
import jwt
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify


JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24


def generate_token(user_id: str, email: str) -> str:
    """
    Generate JWT token for a user
    
    Args:
        user_id: User's UUID
        email: User's email
        
    Returns:
        JWT token string
    """
    payload = {
        "user_id": user_id,
        "email": email,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    """
    Decode and verify JWT token
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded token payload
        
    Raises:
        jwt.ExpiredSignatureError: If token is expired
        jwt.InvalidTokenError: If token is invalid
    """
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])


def require_auth(f):
    """
    Decorator to require JWT authentication for Flask routes
    
    Usage:
        @app.route('/protected')
        @require_auth
        def protected_route(current_user):
            # current_user contains decoded token payload
            return jsonify({"message": "Success"})
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            return jsonify({"error": "No authorization header"}), 401
        
        try:
            # Extract token from "Bearer <token>"
            token = auth_header.split(" ")[1] if " " in auth_header else auth_header
            current_user = decode_token(token)
            return f(current_user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        except Exception as e:
            return jsonify({"error": str(e)}), 401
    
    return decorated
