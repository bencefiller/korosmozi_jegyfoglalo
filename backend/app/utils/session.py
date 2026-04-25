"""Session management utilities."""
import secrets
from datetime import datetime, timedelta


def generate_session_id() -> str:
    """Generate a secure random session ID.
    
    Returns:
        Random 32-byte hex string
    """
    return secrets.token_hex(32)


def get_session_expiry() -> datetime:
    """Get session expiry time (24 hours from now).
    
    Returns:
        Datetime object for session expiry
    """
    return datetime.utcnow() + timedelta(hours=24)
