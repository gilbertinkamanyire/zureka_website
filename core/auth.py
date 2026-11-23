"""
Authentication and Session Management
"""
import hashlib
import secrets
from typing import Optional, Dict

SALT = "_zureka_salt"

# In-memory session store: session_token -> user dict
ACTIVE_SESSIONS: Dict[str, dict] = {}

def hash_password(password: str) -> str:
    """Hash password using SHA-256 with Zureka standard salt."""
    return hashlib.sha256((password + SALT).encode('utf-8')).hexdigest()

def create_session(user: dict) -> str:
    """Create a new session token for authenticated user."""
    token = secrets.token_hex(32)
    ACTIVE_SESSIONS[token] = user
    return token

def get_session_user(token: str) -> Optional[dict]:
    """Retrieve user for an active session token."""
    return ACTIVE_SESSIONS.get(token)

def update_session_user(email: str, updated_user: dict) -> None:
    """Refresh active session objects when user updates their profile."""
    for token, u in list(ACTIVE_SESSIONS.items()):
        if u.get('email', '').strip().lower() == email.strip().lower():
            ACTIVE_SESSIONS[token] = dict(updated_user)

def destroy_session(token: str) -> None:
    """Remove session token upon logout."""
    ACTIVE_SESSIONS.pop(token, None)
