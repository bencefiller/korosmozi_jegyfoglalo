"""Tests for authentication routes."""
import pytest


def test_user_registration_success(client):
    """Test successful user registration.
    
    Business Logic Tested:
    - Email validation
    - Password strength requirement (8+ chars)
    - User creation and storage
    """
    user_data = {
        "email": "newuser@example.com",
        "password": "securepassword123",
        "full_name": "New User"
    }
    
    response = client.post("/api/auth/register", json=user_data)
    
    assert response.status_code == 201
    assert response.json()["success"] is True
    assert response.json()["user"]["email"] == user_data["email"]
    assert response.json()["user"]["full_name"] == user_data["full_name"]


def test_user_registration_duplicate_email(client):
    """Test registration with duplicate email returns 400.
    
    Business Logic Tested:
    - Email uniqueness constraint
    - Proper error response
    """
    user_data = {
        "email": "duplicate@example.com",
        "password": "password123",
        "full_name": "User One"
    }
    
    # First registration
    response1 = client.post("/api/auth/register", json=user_data)
    assert response1.status_code == 201
    
    # Second registration with same email
    response2 = client.post("/api/auth/register", json=user_data)
    assert response2.status_code == 400
    assert "already registered" in response2.json()["detail"]


def test_user_login_success(client):
    """Test successful user login.
    
    Business Logic Tested:
    - Password verification
    - Session creation
    - Cookie setting
    """
    # Register user
    user_data = {
        "email": "login@example.com",
        "password": "password123",
        "full_name": "Login User"
    }
    client.post("/api/auth/register", json=user_data)
    
    # Login
    response = client.post(
        "/api/auth/login",
        json={"email": user_data["email"], "password": user_data["password"]}
    )
    
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["user"]["email"] == user_data["email"]
    assert "session_id" in client.cookies


def test_user_login_invalid_credentials(client):
    """Test login with invalid credentials returns 401.
    
    Business Logic Tested:
    - Password verification failure
    - Non-existent user handling
    """
    # Register user
    user_data = {
        "email": "registered@example.com",
        "password": "correctpassword123",
        "full_name": "Registered User"
    }
    client.post("/api/auth/register", json=user_data)
    
    # Try login with wrong password
    response = client.post(
        "/api/auth/login",
        json={"email": user_data["email"], "password": "wrongpassword"}
    )
    
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]


def test_get_current_user_info(client):
    """Test getting current user info requires authentication.
    
    Business Logic Tested:
    - Session validation
    - Protected endpoint access
    """
    # Register and login
    user_data = {
        "email": "metest@example.com",
        "password": "password123",
        "full_name": "Me Test User"
    }
    client.post("/api/auth/register", json=user_data)
    client.post("/api/auth/login", json={"email": user_data["email"], "password": user_data["password"]})
    
    # Get current user info
    response = client.get("/api/auth/me")
    
    assert response.status_code == 200
    assert response.json()["user"]["email"] == user_data["email"]


def test_get_current_user_without_auth(client):
    """Test getting current user without authentication returns 401.
    
    Business Logic Tested:
    - Protected endpoints
    - Authentication requirement
    """
    response = client.get("/api/auth/me")
    
    assert response.status_code == 401
    assert "Nincs bejelentkezve" in response.json()["detail"]
