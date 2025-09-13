from fastapi import APIRouter, HTTPException
from app.models.link import ShortenRequest, ShortenResponse
from app.services import url_service

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
