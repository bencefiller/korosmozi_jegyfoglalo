"""SQL schema creation script for Cinema Booking System."""

CREATE_TABLES_SQL = """
-- Drop existing tables if needed (only for development)
-- DROP TABLE IF EXISTS bookings CASCADE;
-- DROP TABLE IF EXISTS sessions CASCADE;
-- DROP TABLE IF EXISTS screenings CASCADE;
-- DROP TABLE IF EXISTS movies CASCADE;
-- DROP TABLE IF EXISTS users CASCADE;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create movies table
CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    duration_minutes INTEGER NOT NULL,
    genre VARCHAR(100),
    release_date DATE,
    poster_url VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create screenings table (vetítések)
CREATE TABLE IF NOT EXISTS screenings (
    id SERIAL PRIMARY KEY,
    movie_id INTEGER NOT NULL REFERENCES movies(id) ON DELETE CASCADE,
    screen_number INTEGER NOT NULL,
    screening_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
    available_seats INTEGER NOT NULL,
    total_seats INTEGER NOT NULL DEFAULT 100,
    price_per_ticket NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(screen_number, screening_datetime)
);

-- Create bookings table (foglalások)
CREATE TABLE IF NOT EXISTS bookings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    screening_id INTEGER NOT NULL REFERENCES screenings(id) ON DELETE CASCADE,
    seat_number INTEGER NOT NULL,
    booking_datetime TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'active' CHECK(status IN ('active', 'cancelled')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(screening_id, seat_number)
);

-- Create sessions table for web session management
CREATE TABLE IF NOT EXISTS sessions (
    session_id VARCHAR(255) PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    session_data JSONB,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_bookings_user_id ON bookings(user_id);
CREATE INDEX IF NOT EXISTS idx_bookings_screening_id ON bookings(screening_id);
CREATE INDEX IF NOT EXISTS idx_screenings_movie_id ON screenings(movie_id);
CREATE INDEX IF NOT EXISTS idx_screenings_datetime ON screenings(screening_datetime);
CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_expires_at ON sessions(expires_at);

-- Create sample data for testing

-- Insert sample users
INSERT INTO users (email, password_hash, full_name) VALUES
    ('user1@example.com', '$2b$12$6q2CZ0gKmk.yANfBH6JUr.8SRuKnXY1bPyV8g6Nj7h6Z3Y3Zx3T.e', 'János Kovács'),
    ('user2@example.com', '$2b$12$6q2CZ0gKmk.yANfBH6JUr.8SRuKnXY1bPyV8g6Nj7h6Z3Y3Zx3T.e', 'Márta Szabó'),
    ('user3@example.com', '$2b$12$6q2CZ0gKmk.yANfBH6JUr.8SRuKnXY1bPyV8g6Nj7h6Z3Y3Zx3T.e', 'Péter Nagy')
ON CONFLICT DO NOTHING;

-- Insert sample movies
INSERT INTO movies (title, description, duration_minutes, genre, release_date, poster_url) VALUES
    ('Interstellar', 'Egy csapat utazik a fekete lyukon keresztül más bolygók felfedezésére.', 169, 'Science Fiction', '2014-11-07', 'https://via.placeholder.com/300x450?text=Interstellar'),
    ('The Dark Knight', 'Batman megcsapja a Joker-t Gotham városért való küzdelemben.', 152, 'Action', '2008-07-18', 'https://via.placeholder.com/300x450?text=The+Dark+Knight'),
    ('Inception', 'A tetszhalál állapotában egy betörő pedig képességeket nyer.', 148, 'Science Fiction', '2010-07-16', 'https://via.placeholder.com/300x450?text=Inception'),
    ('The Shawshank Redemption', 'Egy élettartam börtönben eltöltött egy férfi és barátsága.', 142, 'Drama', '1994-10-14', 'https://via.placeholder.com/300x450?text=Shawshank'),
    ('Avatar', 'Egy paralizált katona egy hatalmas humanoid test vezérlésére képes.', 162, 'Science Fiction', '2009-12-18', 'https://via.placeholder.com/300x450?text=Avatar')
ON CONFLICT DO NOTHING;

-- Insert sample screenings
INSERT INTO screenings (movie_id, screen_number, screening_datetime, available_seats, total_seats, price_per_ticket) VALUES
    (1, 1, '2026-04-26 14:00:00+02:00', 80, 100, 1200.00),
    (1, 1, '2026-04-26 18:00:00+02:00', 45, 100, 1500.00),
    (1, 2, '2026-04-27 14:00:00+02:00', 100, 100, 1200.00),
    (2, 1, '2026-04-26 16:00:00+02:00', 60, 100, 1500.00),
    (3, 2, '2026-04-26 20:00:00+02:00', 90, 100, 1500.00),
    (4, 3, '2026-04-27 18:00:00+02:00', 70, 100, 1000.00),
    (5, 1, '2026-04-28 14:00:00+02:00', 50, 100, 1500.00)
ON CONFLICT DO NOTHING;

-- Insert sample bookings
INSERT INTO bookings (user_id, screening_id, seat_number, status) VALUES
    (1, 1, 5, 'active'),
    (1, 1, 6, 'active'),
    (2, 1, 15, 'active'),
    (2, 2, 1, 'active'),
    (3, 4, 42, 'active')
ON CONFLICT DO NOTHING;
"""


def init_database(database_connection) -> None:
    """Initialize database with schema and sample data.
    
    Args:
        database_connection: Database connection object
    """
    with database_connection.cursor() as cursor:
        cursor.execute(CREATE_TABLES_SQL)
        database_connection.commit()
