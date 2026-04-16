@echo off
title Qontint — Semantic Authority OS
color 0B

echo.
echo  ╔═══════════════════════════════════════════════════╗
echo  ║   QONTINT — Semantic Authority Operating System   ║
echo  ║   Starting Backend + Frontend...                   ║
echo  ╚═══════════════════════════════════════════════════╝
echo.

:: Start Backend (FastAPI) in a new window
echo [*] Starting Backend (FastAPI) on http://localhost:8000 ...
start "Qontint Backend" cmd /k "cd /d %~dp0backend && python -m uvicorn app.main:app --reload --port 8000"

:: Wait a moment for backend to initialize
timeout /t 3 /nobreak >nul

:: Start Frontend (Vite + React) in a new window
echo [*] Starting Frontend (Vite) on http://localhost:5173 ...
start "Qontint Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

:: Wait a moment then open browser
timeout /t 3 /nobreak >nul
echo.
echo [✓] Backend:  http://localhost:8000
echo [✓] API Docs: http://localhost:8000/docs
echo [✓] Frontend: http://localhost:5173
echo.
echo Opening browser...
start http://localhost:5173

echo.
echo Press any key to stop both servers...
pause >nul

:: Kill the servers
taskkill /FI "WINDOWTITLE eq Qontint Backend" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Qontint Frontend" /F >nul 2>&1
echo Servers stopped.
