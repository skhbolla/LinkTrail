from datetime import datetime
from collections import Counter, defaultdict
from app.core.db import links_table, clicks_table

def get_analytics(short_id: str, secret_key: str) -> dict:
    """
    Fetch analytics for a short URL if secret_key is valid.
    Returns total clicks and clicks per day/hour.
    """
    # 1️⃣ Validate secret key
    resp = links_table.get_item(Key={"short_id": short_id})
    link_item = resp.get("Item")
    if not link_item:
        raise ValueError("Short URL not found")
    
    if link_item["secret_key"] != secret_key:
        raise ValueError("Invalid secret key")

    # 2️⃣ Fetch click logs
    resp = clicks_table.query(
        KeyConditionExpression="short_id = :sid",
        ExpressionAttributeValues={":sid": short_id}
    )
    clicks = resp.get("Items", [])

    total_clicks = len(clicks)

    # 3️⃣ Aggregate clicks by day
    clicks_by_day = defaultdict(int)
    clicks_by_hour = defaultdict(int)

    for click in clicks:
        ts = click["click_timestamp"]
        dt = datetime.fromisoformat(ts)
        day = dt.date().isoformat()
        hour = dt.strftime("%Y-%m-%d %H:00")
        clicks_by_day[day] += 1
        clicks_by_hour[hour] += 1

    return {
        "short_id": short_id,
        "total_clicks": total_clicks,
        "clicks_by_day": dict(clicks_by_day),
        "clicks_by_hour": dict(clicks_by_hour)
    }
