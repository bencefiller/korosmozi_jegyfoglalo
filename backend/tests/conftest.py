"""Pytest configuration and fixtures."""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import os
from app.database import Base, get_database
from app.main import application


# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_database():
    """Override database dependency for testing."""
    database = TestingSessionLocal()
    try:
        yield database
    finally:
        database.close()


# Create tables for testing
Base.metadata.create_all(bind=engine)

# Override dependency
application.dependency_overrides[get_database] = override_get_database


@pytest.fixture
def database():
    """Fixture providing test database session."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    database = TestingSessionLocal()
    yield database
    
    database.close()
    # Cleanup
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    """Fixture providing FastAPI test client."""
    return TestClient(application)


@pytest.fixture
def sample_user(database, client):
    """Fixture creating a sample user for testing."""
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
    """Fixture providing an authenticated test client."""
    # Login
    login_data = {
        "email": sample_user["email"],
        "password": sample_user["password"]
    }
    
    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200
    
    return client
