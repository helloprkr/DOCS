from fastapi import FastAPI
from datetime import datetime

app = FastAPI(
    title="2025 API",
    description="Backend API for 2025 project",
    version="1.0.0",
    debug=True  # Enable debug mode to see detailed errors
)

@app.get("/", status_code=200)
async def root():
    return {
        "status": "online",
        "message": "API is running"
    }

@app.get("/health", status_code=200)
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }
