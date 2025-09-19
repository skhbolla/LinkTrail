from pydantic import BaseModel, HttpUrl

class ShortenRequest(BaseModel):
    long_url: HttpUrl

class ShortenResponse(BaseModel):
    short_code: str
    analytics_secret: str
