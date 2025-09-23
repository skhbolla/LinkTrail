from fastapi import FastAPI
from mangum import Mangum
from app.routes import link_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="LinkTrail API", version="0.1")

origins = [
    "https://skhbolla.github.io",
    "http://localhost:3000",  # if you later use custom domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # Don't use "*" in PRD
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

