"""Session kezeléséhez szükséges segédfüggvények."""
import secrets
from datetime import datetime, timedelta


def generate_session_id() -> str:
    """Biztonságos, véletlenszerű session azonosító előállítása.
    
    Returns:
        Véletlenszerű 32 bájtos hex string
    """
    return secrets.token_hex(32)


def get_session_expiry() -> datetime:
    """A session lejárati idejének lekérése (24 órával később).
    
    Returns:
        Datetime objektum a session lejáratához
    """
    return datetime.utcnow() + timedelta(hours=24)
