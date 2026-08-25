@echo off
title Server Aplikasi SKP & MPH AI
color 0B

echo Menjalankan Aplikasi SKP & MPH AI...
echo Harap jangan menutup jendela terminal ini selama aplikasi digunakan.
echo.

:: Membuka Browser Otomatis setelah delay 3 detik
start /b "" cmd /c "timeout /t 3 /nobreak >nul && start http://localhost:5000"

:: Menjalankan Server Python Flask
python app.py

pause