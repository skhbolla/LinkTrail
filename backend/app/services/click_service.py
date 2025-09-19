from datetime import datetime
import os
from app.core.db import clicks_table
from app.core.settings import settings

def log_click(short_code: str, request) -> None:
    """
    Logs a click in the ClickLogs table.
    Minimal info: timestamp, IP, user-agent.
    """
    # Timestamp
    click_timestamp = datetime.utcnow().isoformat()

    # IP address (X-Forwarded-For if behind a proxy, fallback to client host)
    client_host = request.client.host if request.client else "unknown"

    # User-Agent
    user_agent = request.headers.get("user-agent", "unknown")

    # For simplicity, we store raw user-agent now
    item = {
        "short_code": short_code,
        "click_timestamp": click_timestamp,
        "user_agent": user_agent,
        "client_ip": client_host
    }

    # Write to DynamoDB
    clicks_table.put_item(Item=item)
