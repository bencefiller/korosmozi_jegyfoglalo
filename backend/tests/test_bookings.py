"""Tests for booking business logic."""
import pytest
from app.models.user import User
from app.models.movie import Movie
from app.models.screening import Screening
from app.models.booking import Booking
from app.utils.password import hash_password
from datetime import datetime, timedelta
from decimal import Decimal


def test_create_booking_success(database, client):
    """Test successful booking creation.
    
    Business Logic Tested:
    - User registration
    - Movie and screening creation
    - Booking creation with validation
    - Available seats decrement
    """
    # Setup: Create user
    user_data = {
        "email": "bookingtest@example.com",
        "password": "password123",
        "full_name": "Booking Test User"
    }
    register_response = client.post("/api/auth/register", json=user_data)
    assert register_response.status_code == 201
    
    # Setup: Create movie
    movie = Movie(
        title="Test Movie",
        description="Test Description",
        duration_minutes=120,
        genre="Drama",
        release_date=datetime.now().date()
    )
    database.add(movie)
    database.commit()
    database.refresh(movie)
    
    # Setup: Create screening
    screening = Screening(
        movie_id=movie.id,
        screen_number=1,
        screening_datetime=datetime.now() + timedelta(days=1),
        available_seats=100,
        total_seats=100,
        price_per_ticket=Decimal("1500.00")
    )
    database.add(screening)
    database.commit()
    database.refresh(screening)
    
    # Login user
    login_response = client.post(
        "/api/auth/login",
        json={"email": user_data["email"], "password": user_data["password"]}
    )
    assert login_response.status_code == 200
    
    # Test: Create booking
    booking_data = {
        "screening_id": screening.id,
        "seat_number": 5
    }
    booking_response = client.post("/api/bookings", json=booking_data)
    
    # Assert: Booking created successfully
    assert booking_response.status_code == 201
    assert booking_response.json()["success"] is True
    assert booking_response.json()["data"]["seat_number"] == 5
    assert booking_response.json()["data"]["status"] == "active"
    
    # Assert: Available seats decremented
    database.refresh(screening)
    assert screening.available_seats == 99


def test_create_booking_duplicate_seat_conflict(database, client):
    """Test that booking same seat twice returns 409 Conflict.
    
    Business Logic Tested:
    - UNIQUE constraint enforcement (screening_id, seat_number)
    - Proper HTTP 409 Conflict response
    - Transaction rollback on conflict
    """
    # Setup: Create two users
    user1_data = {
        "email": "user1@example.com",
        "password": "password123",
        "full_name": "User One"
    }
    user2_data = {
        "email": "user2@example.com",
        "password": "password123",
        "full_name": "User Two"
    }
    
    client.post("/api/auth/register", json=user1_data)
    client.post("/api/auth/register", json=user2_data)
    
    # Setup: Create movie and screening
    movie = Movie(
        title="Popular Movie",
        description="Test",
        duration_minutes=120,
        genre="Action"
    )
    database.add(movie)
    database.commit()
    database.refresh(movie)
    
    screening = Screening(
        movie_id=movie.id,
        screen_number=1,
        screening_datetime=datetime.now() + timedelta(days=1),
        available_seats=100,
        total_seats=100,
        price_per_ticket=Decimal("1500.00")
    )
    database.add(screening)
    database.commit()
    database.refresh(screening)
    
    # User 1: Login and book seat 10
    client.post("/api/auth/login", json={"email": user1_data["email"], "password": user1_data["password"]})
    booking_data = {"screening_id": screening.id, "seat_number": 10}
    response1 = client.post("/api/bookings", json=booking_data)
    assert response1.status_code == 201
    
    # Setup: New client for user 2 (separate session)
    client2 = client
    client2.cookies.clear()
    
    # User 2: Login and try to book same seat
    client2.post("/api/auth/login", json={"email": user2_data["email"], "password": user2_data["password"]})
    response2 = client2.post("/api/bookings", json=booking_data)
    
    # Assert: 409 Conflict returned
    assert response2.status_code == 409
    assert response2.json()["detail"] == "Seat already booked for this screening."
    
    # Assert: Available seats count unchanged (transaction rolled back)
    database.refresh(screening)
    assert screening.available_seats == 99


def test_cancel_booking_frees_seat(database, client):
    """Test that cancelling booking frees up the seat.
    
    Business Logic Tested:
    - Booking cancellation
    - Seat availability restoration
    - Booking status update
    """
    # Setup: Create user, movie, screening
    user_data = {
        "email": "canceltest@example.com",
        "password": "password123",
        "full_name": "Cancel Test User"
    }
    client.post("/api/auth/register", json=user_data)
    
    movie = Movie(
        title="Cancellable Movie",
        description="Test",
        duration_minutes=120,
        genre="Comedy"
    )
    database.add(movie)
    database.commit()
    database.refresh(movie)
    
    screening = Screening(
        movie_id=movie.id,
        screen_number=2,
        screening_datetime=datetime.now() + timedelta(days=1),
        available_seats=100,
        total_seats=100,
        price_per_ticket=Decimal("1500.00")
    )
    database.add(screening)
    database.commit()
    database.refresh(screening)
    
    # Login and create booking
    client.post("/api/auth/login", json={"email": user_data["email"], "password": user_data["password"]})
    booking_response = client.post(
        "/api/bookings",
        json={"screening_id": screening.id, "seat_number": 15}
    )
    assert booking_response.status_code == 201
    booking_id = booking_response.json()["data"]["id"]
    
    # Assert: Available seats decremented
    database.refresh(screening)
    assert screening.available_seats == 99
    
    # Cancel booking
    cancel_response = client.delete(f"/api/bookings/{booking_id}")
    assert cancel_response.status_code == 200
    assert cancel_response.json()["data"]["status"] == "cancelled"
    
    # Assert: Available seats restored
    database.refresh(screening)
    assert screening.available_seats == 100


def test_booking_invalid_seat_number(database, client):
    """Test booking with invalid seat number returns 400.
    
    Business Logic Tested:
    - Input validation (seat number 1-100)
    - Proper 400 Bad Request response
    """
    # Setup: Create user, movie, screening
    user_data = {
        "email": "seattest@example.com",
        "password": "password123",
        "full_name": "Seat Test User"
    }
    client.post("/api/auth/register", json=user_data)
    
    movie = Movie(
        title="Seat Test Movie",
        description="Test",
        duration_minutes=120,
        genre="Drama"
    )
    database.add(movie)
    database.commit()
    database.refresh(movie)
    
    screening = Screening(
        movie_id=movie.id,
        screen_number=3,
        screening_datetime=datetime.now() + timedelta(days=1),
        available_seats=100,
        total_seats=100,
        price_per_ticket=Decimal("1500.00")
    )
    database.add(screening)
    database.commit()
    database.refresh(screening)
    
    # Login
    client.post("/api/auth/login", json={"email": user_data["email"], "password": user_data["password"]})
    
    # Test invalid seat numbers
    invalid_seats = [0, -1, 101, 150, -50]
    for invalid_seat in invalid_seats:
        response = client.post(
            "/api/bookings",
            json={"screening_id": screening.id, "seat_number": invalid_seat}
        )
        assert response.status_code == 400
        assert "Seat number must be between 1 and 100" in response.json()["detail"]
