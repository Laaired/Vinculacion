@echo off
echo ========================================
echo   Reparacion SQLAlchemy - Python 3.13
echo   Plataforma de Vinculacion UNRC
echo ========================================
echo.

echo [1/5] Activando entorno virtual...
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo Error: No se encontro el entorno virtual
    echo Creando nuevo entorno virtual...
    python -m venv venv
    call venv\Scripts\activate
)

echo.
echo [2/5] Actualizando pip...
python -m pip install --upgrade pip

echo.
echo [3/5] Desinstalando SQLAlchemy problemático...
pip uninstall SQLAlchemy Flask-SQLAlchemy -y

echo.
echo [4/5] Instalando SQLAlchemy compatible...
pip install SQLAlchemy>=2.0.25
pip install Flask-SQLAlchemy==3.1.1

echo.
echo [5/5] Instalando dependencias restantes...
pip install Flask==3.0.0 Flask-JWT-Extended==4.6.0 Flask-Mail==0.9.1 Flask-CORS==4.0.0 Flask-Migrate==4.0.5 Werkzeug==3.0.1 bcrypt==4.1.2 python-dotenv==1.0.0 reportlab==4.0.7 scikit-learn pandas numpy requests email-validator python-dateutil

echo.
echo ========================================
echo   Verificando instalacion...
echo ========================================
python -c "import sqlalchemy; print('SQLAlchemy version:', sqlalchemy.__version__)"
python -c "import flask_sqlalchemy; print('Flask-SQLAlchemy: OK')"

echo.
echo ========================================
echo   Reparacion completada!
echo ========================================
echo.
echo Para ejecutar la aplicacion:
echo   python app.py
echo.
echo Para verificar que funciona:
echo   python -c "from flask import Flask; from flask_sqlalchemy import SQLAlchemy; print('Todo OK')"
echo.
pause
