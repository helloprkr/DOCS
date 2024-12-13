from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from datetime import datetime

from app.database.db import init_db
from app.api import notes, gamification

import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events for the FastAPI application."""
    # Startup
    logger.info("Initializing database...")
    await init_db()
    logger.info("Database initialized successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")

# Create FastAPI app
app = FastAPI(
    title="2025 API",
    description="Backend API for 2025 project",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(notes.router, prefix="/api", tags=["notes"])
app.include_router(gamification.router, prefix="/api", tags=["gamification"])

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
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