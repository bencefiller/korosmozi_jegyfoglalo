"""Main FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routes import movies
from app.routes import screenings, bookings, auth

# Betöltjük a modelleket, hogy az SQLAlchemy tudja, milyen táblákat kell létrehoznia
from app.models.movie import Movie

# Adatbázis táblák automatikus létrehozása (ha még nem léteznek)
Base.metadata.create_all(bind=engine)

# ===== AUTOMATIKUS ADATFELTÖLTÉS (SEEDING) =====
from app.database import SessionLocal
db = SessionLocal()
try:
    if not db.query(Movie).first():
        print("🎬 Üres az adatbázis! Automatikus tesztadatok betöltése...")
        import seed_data
        seed_data.seed_db()
finally:
    db.close()

application = FastAPI(
    title="Cinema Booking System API",
    description="Backend API for the cinema reservation system.",
    version="1.0.0"
)

# ===== CORS BEÁLLÍTÁS (Kritikus!) =====
# Ez engedi meg a frontendnek (ami pl. file:// vagy localhost:3000 alatt fut), 
# hogy kéréseket küldjön a 8000-es porton futó backendnek.
application.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000", 
        "http://localhost:8000", 
        "http://127.0.0.1:8000",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "null" # Ha simán dupla kattintással nyitod meg a HTML fájlt
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== ÚTVONALAK (ROUTEREK) BEKÖTÉSE =====
application.include_router(movies.router)
application.include_router(screenings.router)
application.include_router(bookings.router)
application.include_router(auth.router)

@application.get("/api/health")
def health_check():
    """Health check endpoint to verify API is running."""
    return {
        "status": "healthy",
        "service": "Cinema Booking API"
    }