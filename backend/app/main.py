from fastapi import FastAPI
from mangum import Mangum

app = FastAPI(title="LinkTrail API", version="0.1")

@app.get("/")
def root():
    return {"message": "Welcome to LinkTrail"}

# Test route (for container checks)
@app.get("/health")
def health():
    return {"status": "ok"}

handler = Mangum(app)  # For AWS Lambda

