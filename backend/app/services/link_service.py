import string
import random
import uuid
from datetime import datetime
from app.core.db import links_table
from app.core.settings import settings

def generate_short_id(length: int = 6) -> str:
    """Generate a random alphanumeric short ID"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def generate_secret_key() -> str:
    """Generate a UUID-based secret key for analytics"""
    return str(uuid.uuid4())

def create_short_code(long_url: str) -> tuple[str, str]:
    """
    Creates a new short code and analytics secret entry in DynamoDB.

    Returns:
        short_code, analytics_secret
    """
    short_code = generate_short_id()
    analytics_secret = generate_secret_key()
    created_at = datetime.utcnow().isoformat()

    # Store in DynamoDB
    links_table.put_item(
        Item={
            "short_code": short_code,
            "long_url": long_url,
            "analytics_secret": analytics_secret,
            "created_at": created_at,
        }
    )

    return short_code, analytics_secret
