@echo off
title Installer Otomatis SKP & MPH AI
color 0A

echo ============================================================
echo   MENYIAPKAN LINGKUNGAN APLIKASI SKP & MPH AI
echo ============================================================
echo.

:: 1. Cek Apakah Python Terinstall
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Python belum terinstall atau belum di-centang "Add to PATH"!
    echo Silakan install Python 3.11/3.12 terlebih dahulu dari python.org
    echo.
    pause
    exit
)

echo [1/3] Memeriksa dan menginstall library Python yang dibutuhkan...
pip install flask requests
echo.

:: 2. Cek Apakah Ollama Terinstall
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0E
    echo [WARNING] Ollama belum terinstall di komputer ini!
    echo Silakan download dan install Ollama dari https://ollama.com/download
    echo Setelah selesai diinstall, jalankan ulang file batch ini.
    echo.
    pause
    exit
)

:: 3. Mengunduh Model AI Qwen2.5:7b secara Otomatis
echo [2/3] Mengunduh Model AI (qwen2.5:7b)...
echo Catatan: Ukuran file +- 4.7 GB. Harap tunggu hingga 100%%.
echo.
ollama pull qwen2.5:7b

echo.
echo ============================================================
echo [3/3] SELESAI! Seluruh komponen telah berhasil disiapakan.
echo Silakan jalankan file "2-Jalankan-Aplikasi.bat" untuk memulai.
echo ============================================================
echo.
pause