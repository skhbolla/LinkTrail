from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi import Query

from app.models.link import ShortenRequest, ShortenResponse
from app.services import url_service, click_service, analytics_service
from app.core.db import links_table

router = APIRouter()

@router.post("/shorten", response_model=ShortenResponse)
def shorten_url(request: ShortenRequest):
    """
    Endpoint to create a short URL and corresponding analytics URL.
    """
    try:
        short_url, analytics_url = url_service.create_short_url(str(request.long_url))
        return ShortenResponse(short_url=short_url, analytics_url=analytics_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        

@router.get("/l/{short_id}")
def redirect_short_url(short_id: str, request: Request):
    """
    Redirects to the original URL and logs the click.
    """
    # Fetch the original URL from DynamoDB
    resp = links_table.get_item(Key={"short_id": short_id})
    item = resp.get("Item")

    if not item:
        raise HTTPException(status_code=404, detail="Short URL not found")

    long_url = item["long_url"]

    # Log the click asynchronously if you want later; for now sync
    click_service.log_click(short_id, request)

    # Redirect user
    return RedirectResponse(url=long_url)


@router.get("/analytics/{short_id}")
def analytics(short_id: str, key: str = Query(...)):
    """
    Returns analytics for a short URL if key is valid.
    """
    try:
        data = analytics_service.get_analytics(short_id, key)
        return JSONResponse(content=data)
    except ValueError as e:
        return JSONResponse(status_code=403, content={"error": str(e)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
