@echo off
echo ========================================
echo HuggingFace Deployment Script
echo ========================================
echo.

REM Check if HF CLI is installed
huggingface-cli --version >nul 2>&1
if %errorlevel% neq 0 (
    echo HuggingFace CLI belum terinstall!
    echo Menjalankan: pip install huggingface_hub
    pip install huggingface_hub
)

echo.
echo Langkah 1: Login ke HuggingFace
echo Anda akan diminta memasukkan HF Token.
echo Dapatkan token di: https://huggingface.co/settings/tokens
echo.
huggingface-cli login

echo.
echo Langkah 2: Upload ke Space
echo.
cd hf_deploy
huggingface-cli upload Zainajabroh/retail-analytics-api . . --repo-type=space

echo.
echo ========================================
echo SUKSES! Backend sudah ter-deploy!
echo URL: https://huggingface.co/spaces/Zainajabroh/retail-analytics-api
echo ========================================
pause
