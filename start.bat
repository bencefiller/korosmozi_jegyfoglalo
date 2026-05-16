@echo off
chcp 65001 >nul
echo ===================================================
echo     Körös Mozi Jegyfoglaló - Rendszer Indítása
echo ===================================================
echo.

cd backend

echo [1/3] Python csomagok telepitese (requirements.txt)...
pip install -r requirements.txt >nul 2>&1

echo [2/3] Frontend megnyitasa az alapertelmezett bongeszoben...
start "" "..\frontend\index.html"

echo [3/3] Backend szerver inditasa... (Hagyd nyitva ezt az ablakot!)
echo.
python -m uvicorn app.main:application --host localhost --port 8000