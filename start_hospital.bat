@echo off
title Smart Hospital - Startup
color 0A
echo ==========================================
echo   SMART HOSPITAL - Starting Services...
echo ==========================================
echo.

:: Step 1: Verify MySQL is running
echo [*] Ensure your standalone MySQL Server is running!
timeout /t 2 /nobreak >nul

:: Step 2: Start Flask Backend
echo [1/2] Starting Flask Backend Server...
cd /d "%~dp0backend"
start "Flask Server" cmd /k "python server.py"
timeout /t 3 /nobreak >nul

:: Step 3: Open Browser
echo.
echo [*] Opening Website in Browser...
timeout /t 2 /nobreak >nul
start http://127.0.0.1:5000

echo.
echo ==========================================
echo   Website : http://127.0.0.1:5000
echo   Database: Manage via MySQL Workbench
echo ==========================================
echo.
echo Press any key to close this window...
pause >nul
