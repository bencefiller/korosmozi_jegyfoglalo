"""Main FastAPI application setup."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from app.database import engine, Base
from app.config import settings
from app.routes import auth, movies, screenings, bookings

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
application = FastAPI(
    title="Cinema Booking System",
    description="A complete online cinema ticket booking system with user authentication, movie listings, and booking management.",
    version="1.0.0"
)

# Add CORS middleware
application.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
application.include_router(auth.router)
application.include_router(movies.router)
application.include_router(screenings.router)
application.include_router(bookings.router)

# Mount static files (frontend)
frontend_path = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")
if os.path.exists(frontend_path):
    application.mount("/static", StaticFiles(directory=frontend_path), name="static")


@application.get("/", include_in_schema=False)
async def root():
    """Redirect to frontend or serve index.html."""
    frontend_index = os.path.join(frontend_path, "index.html")
    if os.path.exists(frontend_index):
        return FileResponse(frontend_index)
    return {"message": "Cinema Booking System API. Visit /docs for API documentation."}


@application.get("/health", status_code=200)
async def health_check() -> dict:
    """Health check endpoint.
    
    Returns:
        Dictionary indicating API health status
    """
    return {
        "status": "healthy",
        "service": "Cinema Booking System API",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:application",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
