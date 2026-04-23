"""
Auth Service — JWT-based user authentication.
Handles registration, login, token generation, and token verification.
"""
import logging
import hashlib
import os
import json
from typing import Optional, Dict
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Simple file-based user store (no external DB required for MVP)
_USERS_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "users.json")


def _load_users() -> Dict:
    """Load users from JSON file."""
    try:
        if os.path.exists(_USERS_FILE):
            with open(_USERS_FILE) as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def _save_users(users: Dict):
    """Save users to JSON file."""
    try:
        os.makedirs(os.path.dirname(_USERS_FILE), exist_ok=True)
        with open(_USERS_FILE, "w") as f:
            json.dump(users, f, indent=2)
    except Exception as e:
        logger.error(f"Failed to save users: {e}")


def _hash_password(password: str) -> str:
    """Hash password with SHA-256 + salt."""
    salt = "qontint_salt_2025"
    return hashlib.sha256(f"{salt}{password}".encode()).hexdigest()


def _create_token(email: str, secret: str) -> str:
    """Create a simple JWT-like token."""
    try:
        from jose import jwt
        payload = {
            "sub": email,
            "exp": datetime.utcnow() + timedelta(days=7),
            "iat": datetime.utcnow(),
        }
        return jwt.encode(payload, secret, algorithm="HS256")
    except ImportError:
        # Fallback: simple base64 token
        import base64
        import time
        data = f"{email}:{time.time() + 604800}"
        return base64.urlsafe_b64encode(data.encode()).decode()


def _verify_token(token: str, secret: str) -> Optional[str]:
    """Verify token and return email if valid."""
    try:
        from jose import jwt, JWTError
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        return payload.get("sub")
    except Exception:
        pass
    # Fallback base64 decode
    try:
        import base64
        import time
        data = base64.urlsafe_b64decode(token.encode()).decode()
        email, expires_at = data.rsplit(":", 1)
        if float(expires_at) > time.time():
            return email
    except Exception:
        pass
    return None


class AuthService:
    """
    JWT-based user authentication service.
    Uses file-based storage for MVP (can be swapped for DB).
    """

    def __init__(self):
        self._secret = os.environ.get("JWT_SECRET", "qontint_jwt_secret_2025_change_in_production")

    def register(self, email: str, password: str, name: str = "", plan: str = "starter") -> Dict:
        """Register a new user. Returns success status."""
        users = _load_users()

        if email in users:
            return {"success": False, "error": "Email already registered"}

        users[email] = {
            "email": email,
            "name": name or email.split("@")[0],
            "password_hash": _hash_password(password),
            "plan": plan,
            "created_at": datetime.utcnow().isoformat(),
            "analyses_count": 0,
            "verticals": ["saas"],
        }
        _save_users(users)

        token = _create_token(email, self._secret)
        return {
            "success": True,
            "token": token,
            "user": {
                "email": email,
                "name": users[email]["name"],
                "plan": plan,
                "analyses_count": 0,
            },
        }

    def login(self, email: str, password: str) -> Dict:
        """Authenticate user. Returns JWT token on success."""
        users = _load_users()
        user = users.get(email)

        if not user:
            return {"success": False, "error": "Invalid email or password"}

        if user["password_hash"] != _hash_password(password):
            return {"success": False, "error": "Invalid email or password"}

        token = _create_token(email, self._secret)
        return {
            "success": True,
            "token": token,
            "user": {
                "email": email,
                "name": user.get("name", email.split("@")[0]),
                "plan": user.get("plan", "starter"),
                "analyses_count": user.get("analyses_count", 0),
            },
        }

    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify JWT token. Returns user info if valid."""
        email = _verify_token(token, self._secret)
        if not email:
            return None

        users = _load_users()
        user = users.get(email)
        if not user:
            return None

        return {
            "email": email,
            "name": user.get("name", email.split("@")[0]),
            "plan": user.get("plan", "starter"),
            "analyses_count": user.get("analyses_count", 0),
        }

    def get_user(self, email: str) -> Optional[Dict]:
        """Get user by email."""
        users = _load_users()
        user = users.get(email)
        if not user:
            return None
        return {
            "email": email,
            "name": user.get("name"),
            "plan": user.get("plan", "starter"),
            "analyses_count": user.get("analyses_count", 0),
            "created_at": user.get("created_at"),
            "verticals": user.get("verticals", ["saas"]),
        }

    def increment_analysis_count(self, email: str):
        """Increment the analysis counter for a user."""
        users = _load_users()
        if email in users:
            users[email]["analyses_count"] = users[email].get("analyses_count", 0) + 1
            _save_users(users)

    def update_plan(self, email: str, plan: str) -> bool:
        """Update user plan."""
        users = _load_users()
        if email not in users:
            return False
        users[email]["plan"] = plan
        _save_users(users)
        return True


# Singleton instance
auth_service = AuthService()
