"""Database configuration and setup."""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

# Create database engine
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_database():
    """Dependency injection for database session.
    
    Yields:
        Session: SQLAlchemy session instance
    """
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()
