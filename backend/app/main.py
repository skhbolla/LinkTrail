import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from app.routes import link_routes

app = FastAPI(title="LinkTrail API", version="0.1")

#CORS middleware
origins = os.getenv("ALLOWED_ORIGINS", "")
allowed_origins = [origin.strip() for origin in origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(link_routes.router)

@app.get("/")
def root():
    return {"message": "Welcome to LinkTrail"}

# Test route (for container checks)
@app.get("/health")
def health():
    return {"status": "ok"}

handler = Mangum(app)  # For AWS Lambda

