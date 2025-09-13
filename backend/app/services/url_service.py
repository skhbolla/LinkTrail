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

def create_short_url(long_url: str) -> tuple[str, str]:
    """
    Creates a new short URL entry in DynamoDB.

    Returns:
        short_url, analytics_url
    """
    short_id = generate_short_id()
    secret_key = generate_secret_key()
    created_at = datetime.utcnow().isoformat()

    # Store in DynamoDB
    links_table.put_item(
        Item={
            "short_id": short_id,
            "long_url": long_url,
            "secret_key": secret_key,
            "created_at": created_at,
        }
    )

    # Construct URLs
    short_url = f"{settings.BASE_URL}/l/{short_id}"
    analytics_url = f"{settings.BASE_URL}/analytics/{short_id}?key={secret_key}"

    return short_url, analytics_url
