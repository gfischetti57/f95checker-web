@echo off
echo ========================================
echo F95Checker Web - Setup Automatico
echo ========================================

echo.
echo Controllo Python...
python --version
if %errorlevel% neq 0 (
    echo ERRORE: Python non trovato!
    exit /b 1
)

echo Python trovato!
echo.

echo Creazione ambiente virtuale...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERRORE: Impossibile creare ambiente virtuale
    exit /b 1
)

echo.
echo Attivazione ambiente virtuale...
call venv\Scripts\activate.bat

echo.
echo Installazione dipendenze...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERRORE: Installazione dipendenze fallita
    exit /b 1
)

echo.
echo Inizializzazione database...
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('Database inizializzato!')"

echo.
echo ========================================
echo Setup completato con successo!
echo ========================================
echo.
echo Avvio applicazione...
python run.py