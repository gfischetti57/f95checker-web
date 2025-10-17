@echo off
echo ========================================
echo F95Checker Web - Avvio Applicazione
echo ========================================

if not exist "venv\Scripts\activate.bat" (
    echo ERRORE: Ambiente virtuale non trovato!
    echo Esegui prima setup.bat
    exit /b 1
)

echo Attivazione ambiente virtuale...
call venv\Scripts\activate.bat

echo.
echo Avvio applicazione...
echo L'app sarà disponibile su: http://localhost:5000
echo Premi Ctrl+C per fermare
echo.

python run.py