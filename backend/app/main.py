"""A FastAPI alkalmazĂˇs belĂ©pĂ©si pontja."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routes import movies
from app.routes import screenings, bookings, auth

# BetĂ¶ltjĂĽk a modelleket, hogy az SQLAlchemy tudja, milyen tĂˇblĂˇkat kell lĂ©trehoznia
from app.models.movie import Movie

# AdatbĂˇzis tĂˇblĂˇk automatikus lĂ©trehozĂˇsa (ha mĂ©g nem lĂ©teznek)
Base.metadata.create_all(bind=engine)

# ===== AUTOMATIKUS ADATFELTĂ–LTĂ‰S (SEEDING) =====
from app.database import SessionLocal
db = SessionLocal()
try:
    if not db.query(Movie).first():
        print("đźŽ¬ Ăśres az adatbĂˇzis! Automatikus tesztadatok betĂ¶ltĂ©se...")
        import seed_data
        seed_data.seed_db()
finally:
    db.close()

application = FastAPI(
    title="Mozi JegyfoglalĂł Rendszer API",
    description="A mozi jegyfoglalĂł rendszer backend API-ja.",
    version="1.0.0"
)

# ===== CORS BEĂLLĂŤTĂS (Kritikus!) =====
# Ez engedi meg a frontendnek (ami pl. file:// vagy localhost:3000 alatt fut), 
# hogy kĂ©rĂ©seket kĂĽldjĂ¶n a 8000-es porton futĂł backendnek.
application.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000", 
        "http://localhost:8000", 
        "http://127.0.0.1:8000",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "null" # Ha simĂˇn dupla kattintĂˇssal nyitod meg a HTML fĂˇjlt
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== ĂšTVONALAK (ROUTEREK) BEKĂ–TĂ‰SE =====
application.include_router(movies.router)
application.include_router(screenings.router)
application.include_router(bookings.router)
application.include_router(auth.router)

@application.get("/api/health")
def health_check():
    """Egészségügyi ellenőrző végpont, amely megerősíti, hogy az API fut."""
    return {
        "status": "healthy",
        "service": "Mozi Foglaló API"
    }
