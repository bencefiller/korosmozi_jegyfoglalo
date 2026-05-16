# 🎬 Cinema Booking System - Online Mozi Jegyfoglaló Rendszer

## Projekt Leírása

A **Cinema Booking System** egy teljes körű web alkalmazás filmvetítések jegyfoglalásához. A rendszer lehetővé teszi a felhasználók számára, hogy regisztráljanak, bejelentkezzenek, böngészhessenek a filmek között, és foglalhassanak jegyeket a kiválasztott vetítésekre.

**Funkciók:**
- 📽️ Film listázás és keresés
- 🎫 Interaktív jegyfoglalás (szék kiválasztás)
- 👤 Felhasználó regisztráció és bejelentkezés
- 📋 Saját foglalások megtekintése és lemondása
- 🔐 Session-based hitelesítés
- 📱 Teljes reszponzív design (360px - 1366px+)
- 🐳 Docker containerizáció

---

## Technológia Stack

### Backend
- **Framework:** FastAPI (Python 3.11)
- **ORM:** SQLAlchemy 2.0
- **Adatbázis:** PostgreSQL 15
- **Hitelesítés:** Session-based (cookies)
- **Password Hashing:** bcrypt

### Frontend
- **HTML5**, **CSS3** (Grid + Flexbox), **Vanilla JavaScript**
- **Reszponzív Design:** Mobile-first (360px), Tablet (768px), Desktop (1366px+)

### DevOps
- **Containerizáció:** Docker & Docker Compose
- **Testing:** pytest (Unit & Integration tesztek)

---

## Telepítés & Futtatás

### Előfeltételek
- **Docker & Docker Compose** (javasolt)
- Vagy: **Python 3.11+**, **PostgreSQL 15**, **pip**

### Módszer 1: Docker Compose (JAVASOLT)

```bash
# 1. Klónozd a repositoryt
cd cinema-booking-system

# 2. Indítsd a containereket
docker-compose up -d

# 3. Ellenőrizd az indítást
docker-compose logs -f api

# 4. Nyisd meg a böngészőt
http://localhost:8000
```

**API docs:** http://localhost:8000/docs (Swagger UI)

### Módszer 2: Legegyszerűbb lokális futtatás (Oktatói / Tesztelési mód)
Ezzel a módszerrel sem Docker, sem különálló adatbázis-szerver nem szükséges. A rendszer automatikusan egy lokális SQLite adatbázist (`cinema.db`) hoz létre és tölt fel tesztadatokkal.

```bash
# 1. Lépj be a backend mappába
cd backend

# 2. Telepítsd a függőségeket
pip install -r requirements.txt

# 3. Indítsd el az API-t (Az adatbázis automatikusan létrejön és feltöltődik)
uvicorn app.main:application --host localhost --port 8000
```
**Frontend:** Nyisd meg a `frontend/index.html` fájlt egyszerűen dupla kattintással a böngészőben! (A CORS engedélyezi a lokális fájlmegnyitást is).

### Módszer 3: Hagyományos Local Development Setup (PostgreSQL)

```bash
# 1. Python virtuális env létrehozása
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Függőségek telepítése
pip install -r requirements.txt

# 3. .env fájl létrehozása
cp .env.example .env
# Szerkeszd a .env fájlt a PostgreSQL adatokkal

# 4. Backend indítása
cd backend
uvicorn app.main:application --reload --host 0.0.0.0 --port 8000

# 5. Frontend megnyitása (külön ablakban)
# Nyisd meg a frontend/index.html fájlt böngészőben vagy
# Használj egy egyszerű HTTP szervert: python -m http.server 3000 --directory frontend
```

---

## Adatbázis Séma

### Táblák és Kapcsolatok

```
┌─────────────┐
│   users     │
├─────────────┤
│ id (PK)     │
│ email (UQ)  │
│ password    │
│ full_name   │
└─────────────┘
      │ 1
      │
      ├──→ (1:N) bookings
      └──→ (1:N) sessions

┌─────────────┐
│   movies    │
├─────────────┤
│ id (PK)     │
│ title       │
│ description │
│ duration    │
│ genre       │
└─────────────┘
      │ 1
      │
      └──→ (1:N) screenings

┌──────────────┐
│  screenings  │
├──────────────┤
│ id (PK)      │
│ movie_id (FK)│
│ screen_num   │
│ datetime     │ (UQ: screen_num, datetime)
│ available    │
│ total_seats  │
│ price        │
└──────────────┘
      │ 1
      │
      └──→ (1:N) bookings

┌──────────────┐
│   bookings   │
├──────────────┤
│ id (PK)      │
│ user_id (FK) │
│ screening(FK)│
│ seat_number  │ (UQ: screening_id, seat_number)
│ status       │
│ created_at   │
└──────────────┘

┌──────────────┐
│   sessions   │
├──────────────┤
│ session_id(PK)
│ user_id (FK) │
│ session_data │
│ expires_at   │
└──────────────┘
```

### Adatbázis Inicializálása

SQL séma: [app/schema.py](backend/app/schema.py)

A séma automatikusan létrehozódik az első alkalmazás indításakor (`Base.metadata.create_all()`).

**Manuális inicializálás PostgreSQL CLI-vel:**

```sql
psql -U cinema_user -d cinema_db -f backend/app/schema.py
```

---

## API Dokumentáció

Teljes API dokumentáció: **http://localhost:8000/docs** (Swagger UI)

### 1. Hitelesítés (Authentication)

#### POST `/api/auth/register`
Új felhasználó regisztrálása.

**Request:**
```json
{
    "email": "user@example.com",
    "password": "securepassword123",
    "full_name": "János Kovács"
}
```

**Response (201 Created):**
```json
{
    "success": true,
    "message": "User registered successfully.",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "full_name": "János Kovács"
    }
}
```

**Hibák:**
- `400 Bad Request` - Email már regisztrált
- `422 Unprocessable Entity` - Validációs hiba

---

#### POST `/api/auth/login`
Felhasználó bejelentkezése (session cookie beállítása).

**Request:**
```json
{
    "email": "user@example.com",
    "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Login successful.",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "full_name": "János Kovács"
    }
}
```

**Cookie:** `session_id=<secure_token>` (24 óra)

**Hibák:**
- `401 Unauthorized` - Hibás email vagy jelszó

---

#### GET `/api/auth/me`
Bejelentkezett felhasználó információi.

**Autentikáció szükséges:** `session_id` cookie

**Response (200 OK):**
```json
{
    "success": true,
    "user": {
        "id": 1,
        "email": "user@example.com",
        "full_name": "János Kovács",
        "created_at": "2026-04-25T10:30:00+00:00"
    }
}
```

**Hibák:**
- `401 Unauthorized` - Nincs session vagy lejárt

---

#### POST `/api/auth/logout`
Felhasználó kijelentkezése (session cookie törlése).

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Logout successful."
}
```

---

### 2. Filmek (Movies)

#### GET `/api/movies?skip=0&limit=20&genre=Action`
Filmek listázása pagináció és szűrés alapján.

**Query Parameters:**
- `skip` (int, default: 0) - Kihagyandó rekordok száma
- `limit` (int, default: 20) - Maximum megjelenítendő filmek
- `genre` (string, optional) - Szűrés műfaj alapján

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "movies": [
            {
                "id": 1,
                "title": "Interstellar",
                "description": "Egy csapat...",
                "duration_minutes": 169,
                "genre": "Science Fiction",
                "release_date": "2014-11-07",
                "poster_url": "https://example.com/poster.jpg"
            }
        ],
        "total": 5,
        "skip": 0,
        "limit": 20
    }
}
```

---

#### GET `/api/movies/{movie_id}`
Egy film részletei.

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "title": "Interstellar",
        "description": "...",
        "duration_minutes": 169,
        "genre": "Science Fiction",
        "release_date": "2014-11-07",
        "poster_url": "...",
        "screenings_count": 3
    }
}
```

**Hibák:**
- `404 Not Found` - Film nem található

---

### 3. Vetítések (Screenings)

#### GET `/api/screenings?movie_id=1&skip=0&limit=20`
Vetítések listázása (szűrhető film szerint).

**Query Parameters:**
- `movie_id` (int, optional) - Szűrés film alapján
- `skip` (int, default: 0)
- `limit` (int, default: 20)

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "screenings": [
            {
                "id": 1,
                "movie_id": 1,
                "screen_number": 1,
                "screening_datetime": "2026-04-26T14:00:00+00:00",
                "available_seats": 80,
                "total_seats": 100,
                "price_per_ticket": 1500.00
            }
        ],
        "total": 3,
        "skip": 0,
        "limit": 20
    }
}
```

---

#### GET `/api/screenings/{screening_id}`
Egy vetítés részletei filmmel.

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "movie_id": 1,
        "movie": {
            "id": 1,
            "title": "Interstellar",
            "genre": "Science Fiction",
            "duration_minutes": 169
        },
        "screen_number": 1,
        "screening_datetime": "2026-04-26T14:00:00+00:00",
        "available_seats": 80,
        "total_seats": 100,
        "price_per_ticket": 1500.00
    }
}
```

---

### 4. Foglalások (Bookings) - CORE LOGIC

#### POST `/api/bookings`
**Új jegyfoglalás létrehozása.**

**Autentikáció szükséges:** `session_id` cookie

**KRITIKUS ÜZLETI LOGIKA:**
1. Validáció: szék szám 1-100 között kell legyen
2. Szék-ellenőrzés: már foglalt-e (UNIQUE constraint)
3. Verfifikáció: van-e szabad hely
4. Available seats dekrementálása
5. Atomikus tranzakció (all-or-nothing)

**Request:**
```json
{
    "screening_id": 1,
    "seat_number": 15
}
```

**Response (201 Created):**
```json
{
    "success": true,
    "message": "Booking created successfully.",
    "data": {
        "id": 42,
        "user_id": 1,
        "screening_id": 1,
        "seat_number": 15,
        "status": "active",
        "booking_datetime": "2026-04-25T12:30:00+00:00",
        "price": 1500.00
    }
}
```

**Hibák:**
- `400 Bad Request` - Szék szám érvénytelen (nem 1-100)
- `400 Bad Request` - Nincs szabad hely
- `404 Not Found` - Vetítés nem létezik
- `409 Conflict` - Szék már foglalt
- `401 Unauthorized` - Bejelentkezés szükséges

---

#### GET `/api/bookings`
Bejelentkezett felhasználó foglalásai.

**Autentikáció szükséges:** `session_id` cookie

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "bookings": [
            {
                "id": 42,
                "screening_id": 1,
                "seat_number": 15,
                "status": "active",
                "booking_datetime": "2026-04-25T12:30:00+00:00",
                "movie_title": "Interstellar",
                "screening_datetime": "2026-04-26T14:00:00+00:00",
                "price": 1500.00
            }
        ],
        "total": 1
    }
}
```

---

#### DELETE `/api/bookings/{booking_id}`
Foglalás lemondása (szék felszabadítása).

**Autentikáció szükséges:** `session_id` cookie

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Booking cancelled successfully.",
    "data": {
        "id": 42,
        "status": "cancelled"
    }
}
```

**Logika:**
- Foglalás státusza "cancelled"-re módosul
- Available seats megnövekedik (+1)
- Csak a saját foglalások lemondhatók (403 Forbidden másé)

**Hibák:**
- `403 Forbidden` - Nem saját foglalás
- `404 Not Found` - Foglalás nem létezik
- `401 Unauthorized` - Bejelentkezés szükséges

---

#### GET `/api/bookings/{booking_id}`
Egy foglalás részletei.

**Autentikáció szükséges:** `session_id` cookie

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "id": 42,
        "user_id": 1,
        "screening_id": 1,
        "seat_number": 15,
        "status": "active",
        "booking_datetime": "2026-04-25T12:30:00+00:00",
        "movie_title": "Interstellar",
        "screening_datetime": "2026-04-26T14:00:00+00:00",
        "price": 1500.00
    }
}
```

---

### 5. Health Check

#### GET `/api/health`
API egészségügyi státusza.

**Response (200 OK):**
```json
{
    "status": "healthy",
    "service": "Cinema Booking System API",
    "version": "1.0.0"
}
```

---

## Frontend Funkciók

### Oldalak

1. **Filmek Főoldala** (/)
   - Film lista Grid layoutban
   - Keresés/szűrés műfaj alapján
   - Film kattintva → Részletoldal

2. **Film Részletoldal** (/movie/:id)
   - Film plakát, leírás, műfaj, hossz
   - Elérhető vetítések listája
   - "Foglalás" gomb (csak bejelentkezett felhasználók)

3. **Szék Kiválasztás** (modal/inline)
   - 10x10-es székrács (100 szék)
   - Kattintható székek (szabad)
   - Szürke székek (foglalt)
   - Kiemelt szék (kiválasztott)
   - Megerősítés gomb

4. **Bejelentkezés** (/login)
   - Email + Jelszó form
   - Regisztrálási linkk
   - Hiba üzenetek

5. **Regisztráció** (/register)
   - Teljes név + Email + Jelszó (8+ kar)
   - Bejelentkezési link
   - Validációs üzenetek

6. **Saját Foglalások** (/bookings)
   - Aktív foglalások kártya layout
   - Film cím, dátum, szék, ár
   - "Foglalás lemondása" gomb
   - Üres állapot üzenet

### Reszponzivitás

| Méret | Breakpoint | Grid | Szék Grid |
|-------|-----------|------|-----------|
| **Desktop** | 1366px+ | 4 oszlop | 10x10 |
| **Tablet** | 768px | 3 oszlop | 10x10 |
| **Mobil** | 480px | 2 oszlop | 5x20 |

---

## Tesztelés

### Unit & Integration Tesztek

Pytest teszteket futtass:

```bash
# Összes teszt futtatása
pytest

# Konkrét teszt fájl
pytest backend/tests/test_bookings.py -v

# Coverage report
pytest --cov=app backend/tests/
```

### Tesztelt Üzleti Logika

1. **test_create_booking_success** - Sikeres foglalás, available seats csökkentés
2. **test_create_booking_duplicate_seat_conflict** - 409 Conflict duplikátum szék
3. **test_cancel_booking_frees_seat** - Lemondás után szék felszabadul
4. **test_booking_invalid_seat_number** - 400 Bad Request érvénytelen szék
5. **test_user_registration_success** - Felhasználó regisztrálása
6. **test_user_registration_duplicate_email** - 400 duplikátum email
7. **test_user_login_success** - Sikeres bejelentkezés, session cookie
8. **test_user_login_invalid_credentials** - 401 hibás jelszó
9. **test_get_current_user_info** - GET /auth/me működik
10. **test_get_current_user_without_auth** - 401 bejelentkezés nélkül

---

## Projekstruktúra

```
cinema-booking-system/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app entry point
│   │   ├── config.py              # Konfigurációs beállítások
│   │   ├── database.py            # SQLAlchemy ORM setup
│   │   ├── schema.py              # SQL séma + init script
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py           # User ORM modell
│   │   │   ├── movie.py          # Movie ORM modell
│   │   │   ├── screening.py      # Screening ORM modell
│   │   │   ├── booking.py        # Booking ORM modell (mag logika)
│   │   │   └── session.py        # Session ORM modell
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py           # Pydantic schemas
│   │   │   ├── movie.py
│   │   │   ├── screening.py
│   │   │   └── booking.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py           # /api/auth/* endpoints
│   │   │   ├── movies.py         # /api/movies/* endpoints
│   │   │   ├── screenings.py     # /api/screenings/* endpoints
│   │   │   └── bookings.py       # /api/bookings/* endpoints (kritikus logika!)
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── password.py       # bcrypt hash/verify
│   │   │   ├── session.py        # Session ID generátor
│   │   │   └── deps.py           # get_current_user dependency
│   │   └── middleware/
│   │       └── [middleware files]
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py           # pytest fixtures, test database
│   │   ├── test_bookings.py      # 5 booking teszt
│   │   └── test_auth.py          # 6 auth teszt
│   ├── requirements.txt
│   ├── .env.example
│   └── docker-entrypoint.sh
├── frontend/
│   ├── index.html               # Single page app
│   ├── css/
│   │   └── style.css            # Reszponzív CSS (360-1366px)
│   └── js/
│       └── app.js               # API hívások, DOM manipuláció
├── Dockerfile                    # Python 3.11-slim backend container
├── docker-compose.yml            # PostgreSQL + API services
├── README.md                      # Ez a fájl
└── .gitignore
```

---

## Git Commit Történet

Javasolt commit üzenetek (5+ konkrét, jól strukturált):

```
1. "feat(backend): Initialize FastAPI project with PostgreSQL ORM models

   - Set up FastAPI app with CORS middleware
   - Created SQLAlchemy ORM models: User, Movie, Screening, Booking, Session
   - Defined database connection and session management
   - Added configuration management from .env"

2. "feat(auth): Implement session-based authentication system

   - POST /api/auth/register: User registration with bcrypt password hashing
   - POST /api/auth/login: Login with session cookie (24 hours)
   - POST /api/auth/logout: Clear session
   - GET /api/auth/me: Get current user info
   - Added password utility functions and session dependency injection"

3. "feat(api): Implement core API endpoints with validation

   - GET /api/movies: List movies with pagination and genre filter
   - GET /api/movies/{id}: Movie details
   - GET /api/screenings: List screenings with movie filter
   - GET /api/screenings/{id}: Screening details with movie info
   - Added Pydantic schemas for request/response validation"

4. "feat(bookings): Implement ticket booking business logic

   - POST /api/bookings: Create booking with seat selection
   - Business logic: seat validation, duplicate check (409 Conflict), 
     available seats decrement, atomic transaction
   - GET /api/bookings: User bookings list
   - DELETE /api/bookings/{id}: Cancel booking and free seat
   - GET /api/bookings/{id}: Booking details
   - Includes comprehensive error handling and input validation"

5. "feat(frontend): Build responsive HTML/CSS/JS SPA

   - Single page app with pages: home, login, register, movie detail, bookings
   - Fully responsive Grid layout: 360px (2 col) → 1366px (4 col)
   - CSS Flexbox + Grid, Vanilla JS for API calls
   - Seat selection grid (10x10) with visual feedback
   - Real-time booking status and cancellation"

6. "test: Add unit and integration tests for critical business logic

   - test_bookings.py: 5 tests for booking creation, conflicts, cancellation
   - test_auth.py: 6 tests for registration, login, auth checks
   - Pytest fixtures for test database and authenticated client
   - Tests cover: validation, constraints, HTTP status codes, error messages"

7. "devops(docker): Add containerization and deployment config

   - Dockerfile: Python 3.11-slim with FastAPI + PostgreSQL client
   - docker-compose.yml: PostgreSQL 15 + FastAPI services
   - Health checks for both services
   - Persistent volumes for database
   - Network isolation with cinema-network"

8. "docs: Complete README with architecture, API docs, setup guide

   - Database schema diagram with relationships
   - Complete API endpoint documentation with examples
   - Frontend features and responsiveness guide
   - Installation instructions (Docker + Local)
   - Testing and git commit history"
```

---

## Fejlesztői Útmutató

### Új végpont hozzáadása

1. **Modell** → `app/models/model_name.py`
2. **Schema** → `app/schemas/model_name.py`
3. **Route** → `app/routes/model_name.py`
4. **Include** → `app/main.py` router includeálása
5. **Test** → `tests/test_model_name.py`

### Adatbázis migráció (dev mód)

```python
# app/models/new_model.py fájlt szerkesztesz
from sqlalchemy import Column, ...
class NewModel(Base):
    ...

# Automatikus: Base.metadata.create_all(bind=engine)
# vagy manual Alembic: alembic revision --autogenerate -m "Add new model"
```

### Environment Variables

```
DATABASE_URL=postgresql://user:password@localhost:5432/cinema_db
SECRET_KEY=your-secret-key (min. 32 char)
DEBUG=True (development), False (production)
POSTGRES_HOST=postgres (Docker network name)
POSTGRES_PORT=5432
```

---

## Hibaelhárítás

### "Connection refused" PostgreSQL-hez

```bash
# Docker Compose-ban
docker-compose ps  # Ellenőrizd, hogy a postgres service fut-e
docker-compose logs postgres  # Postgres naplók
```

### "Port 8000 already in use"

```bash
# Keresd meg a folyamatot
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows
```

### Tesztek sikertelenek

```bash
# SQLite test database
rm test.db  # Töröld az előző test DB-t
pytest --tb=short -v  # Részletes output
```

---

## Jövőbeli Fejlesztések (v1.1+)

- [ ] Payment integration (Stripe/PayPal)
- [ ] Email notifications (confirmation, reminder)
- [ ] Admin panel (film management, analytics)
- [ ] Advanced search (title, date range, price range)
- [ ] User profile page
- [ ] Wishlist functionality
- [ ] Reviews and ratings
- [ ] Multi-language support
- [ ] Real-time booking availability updates (WebSocket)
- [ ] Mobile app (React Native)

---

## Licenc

MIT License - Szabad felhasználás, módosítás, terjesztés.

---

## Támogatás

Problémákkal vagy kérdésekkel kapcsolatban nyiss egy GitHub Issue-t vagy vedd fel a kapcsolatot.

---

**Készült: 2026. április | Cinema Booking System v1.0**
