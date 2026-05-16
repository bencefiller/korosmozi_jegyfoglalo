# Körös Mozi Jegyfoglaló

## Projekt
Egy Dockerrel futtatható mozi jegyfoglaló rendszer FastAPI backenddel és PostgreSQL adatbázissal.

## Követelmény
- Docker Desktop telepítve
- `docker compose` parancs elérhető

## Indítás
A projekt gyökeréből futtassa:

```bash
docker compose up --build
```

Ez a parancs felépíti a backend Docker image-et, elindítja a PostgreSQL adatbázist és a FastAPI szolgáltatást.

## Jegyfoglaló megtekintése
- frontend\index.html indítása


## Elérés
- API: `http://localhost:8000`
- Dokumentáció: `http://localhost:8000/docs`

## Leállítás

```bash
docker compose down
```

## Teljes adatbázis törlése

```bash
docker compose down -v
```

## Tartalom
- `docker-compose.yml` – PostgreSQL és FastAPI szolgáltatások
- `Dockerfile` – backend image építése
- `requirements.txt` – Python függőségek
- `backend/app/` – FastAPI alkalmazás
- `frontend/` – statikus frontend fájlok

## Megjegyzés
A projekt bármilyen mappába kicsomagolható, és a `docker compose up --build` parancs után futnia kell további kézi konfiguráció nélkül.
