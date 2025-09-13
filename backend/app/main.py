from fastapi import FastAPI
from mangum import Mangum
from app.routes import url_routes

app = FastAPI(title="LinkTrail API", version="0.1")

app.include_router(url_routes.router)

@app.get("/")
def root():
    return {"message": "Welcome to LinkTrail"}

# Test route (for container checks)
@app.get("/health")
def health():
    return {"status": "ok"}

handler = Mangum(app)  # For AWS Lambda

