"""Pytest konfiguráció és fixture-ek."""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import os
from app.database import Base, get_database
from app.main import application


# Teszteléshez in-memory SQLite használata
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_database():
    """Adatbázis-függőség felülírása teszteléshez."""
    database = TestingSessionLocal()
    try:
        yield database
    finally:
        database.close()


# Táblák létrehozása teszteléshez
Base.metadata.create_all(bind=engine)

# Függőség felülírása
application.dependency_overrides[get_database] = override_get_database


@pytest.fixture
def database():
    """Fixture, amely tesztadatbázis-sessiont biztosít."""
    # Táblák létrehozása
    Base.metadata.create_all(bind=engine)
    
    database = TestingSessionLocal()
    yield database
    
    database.close()
    # Takarítás
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    """Fixture, amely FastAPI tesztklienst biztosít."""
    return TestClient(application)


@pytest.fixture
def sample_user(database, client):
    """Fixture mintafelhasználó létrehozásához teszteléshez."""
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    
    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 201
    
    return user_data


@pytest.fixture
def authenticated_client(client, sample_user):
    """Fixture hitelesített tesztklienst biztosít."""
    # Bejelentkezés
    login_data = {
        "email": sample_user["email"],
        "password": sample_user["password"]
    }
    
    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200
    
    return client
