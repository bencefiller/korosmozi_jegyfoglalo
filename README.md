# Körös Mozi Jegyfoglaló

## Projekt leírása

Ez a projekt egy egyszerű webes mozi jegyfoglaló rendszer. A felhasználók regisztrálhatnak, bejelentkezhetnek, megnézhetik a filmeket és a hozzájuk tartozó vetítéseket, valamint foglalhatnak jegyeket egy kiválasztott vetítésre.

A rendszer tartalmaz egy Python-FastAPI backendet, egy statikus frontend felületet HTML/CSS/JavaScript segítségével, és PostgreSQL adatbázist Docker Compose-ban.

## Főbb jellemzők

- felhasználói regisztráció és bejelentkezés
- session alapú hitelesítés cookie segítségével
- filmek és vetítések listázása
- jegyfoglalás létrehozása és lemondása
- felhasználói foglalások listázása
- alapvető adatvédelem és jelszóhashing bcrypt-tel
- Docker Compose alapú futtatás PostgreSQL adatbázissal

## Projekt szerkezete

- `backend/`
  - `app/` - FastAPI backend kód
  - `tests/` - pytest tesztek
- `frontend/`
  - `index.html` - frontend felület
  - `css/style.css` - stílusok
  - `js/app.js` - frontend logika
- `Dockerfile` - backend Docker image építése
- `docker-compose.yml` - backend és adatbázis szolgáltatás
- `requirements.txt` - Python függőségek

## Telepítés és futtatás

### 1. Docker Compose használata (ajánlott)

```bash
docker-compose up -d
```

A backend a `http://localhost:8000` címen lesz elérhető.

### 2. Docker nélküli futtatás

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:application --host localhost --port 8000
```

A frontend megjelenítéséhez nyissa meg a `frontend/index.html` fájlt, vagy indítson egyszerű statikus szervert:

```bash
cd frontend
python -m http.server 3000
```

Ezután nyissa meg a böngészőt a `http://localhost:3000` címen.

## Környezeti változók

A `docker-compose.yml` fájlban az alábbi változók szerepelnek:

- `DATABASE_URL`
- `SECRET_KEY`
- `DEBUG`
- `POSTGRES_HOST`
- `POSTGRES_PORT`

## Fő API végpontok

### Hitelesítés
- `POST /api/auth/register` – regisztráció
- `POST /api/auth/login` – bejelentkezés
- `GET /api/auth/me` – bejelentkezett felhasználó adatainak lekérése
- `POST /api/auth/logout` – kijelentkezés
- `GET /api/auth/users` – összes felhasználó lekérése (fejlesztői végpont)

### Filmek
- `GET /api/movies` – filmek listázása
- `GET /api/movies/{movie_id}` – film részletei

### Vetítések
- `GET /api/screenings` – vetítések listázása
- `GET /api/screenings?movie_id={id}` – adott film vetítései

### Foglalások
- `POST /api/bookings` – foglalás létrehozása
- `GET /api/bookings/screening/{screening_id}` – foglalt székek lekérése
- `GET /api/bookings` – saját foglalások lekérése
- `DELETE /api/bookings/{booking_id}` – foglalás törlése

## Tesztelés

A tesztek futtatásához használja a következő parancsot:

```bash
cd backend
pytest
```

## Használat

1. Indítsa el a backendet Docker Compose-szal vagy `uvicorn`-nal.
2. Nyissa meg a frontend felületet:
   - `frontend/index.html` fájl megnyitásával, vagy
   - `python -m http.server 3000` használatával.
3. Regisztráljon, majd jelentkezzen be.
4. Válasszon filmet, tekintse meg a vetítéseket, és foglaljon jegyet.

## Megjegyzés

A backend automatikusan létrehozza a szükséges adatbázis táblákat, és első induláskor betölti a mintaadatokat, ha az adatbázis üres.
