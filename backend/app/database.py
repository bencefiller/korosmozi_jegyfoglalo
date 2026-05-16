"""Adatbázis-kapcsolat és session kezelés."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from sqlalchemy import event
from datetime import datetime, timezone

# Alapértelmezetten SQLite adatbázist használunk a helyi fejlesztéshez (cinema.db fájl)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cinema.db")

# SQLite esetén szükséges ez a beállítás a többszálú végrehajtás miatt
connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=connect_args
)

# Kijavítjuk az SQLite hiányzó utcnow() függvényét a Session táblához
@event.listens_for(engine, "connect")
def sqlite_engine_connect(dbapi_connection, connection_record):
    if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
        dbapi_connection.create_function("utcnow", 0, lambda: datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_database():
    """Dependency function to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()