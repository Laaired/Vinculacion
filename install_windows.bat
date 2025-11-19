@echo off
echo ========================================
echo   Plataforma de Vinculacion UNRC
echo   Instalacion Automatica para Windows
echo ========================================
echo.

echo [1/6] Actualizando pip...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo Error actualizando pip. Continuando...
)

echo.
echo [2/6] Instalando dependencias basicas...
pip install Flask==3.0.0
pip install Flask-SQLAlchemy==3.1.1
pip install Flask-JWT-Extended==4.6.0
pip install Flask-Mail==0.9.1
pip install Flask-CORS==4.0.0
pip install Flask-Migrate==4.0.5

echo.
echo [3/6] Instalando dependencias de base de datos...
pip install SQLAlchemy==2.0.23
pip install Werkzeug==3.0.1
pip install bcrypt==4.1.2

echo.
echo [4/6] Instalando utilidades...
pip install python-dotenv==1.0.0
pip install requests>=2.30.0
pip install email-validator>=2.0.0
pip install python-dateutil>=2.8.0

echo.
echo [5/6] Instalando generacion de documentos...
pip install reportlab==4.0.7

echo.
echo [6/6] Instalando dependencias de IA (opcional)...
pip install scikit-learn>=1.3.0
pip install pandas>=2.0.0
pip install numpy>=1.24.0

echo.
echo ========================================
echo   Instalacion completada!
echo ========================================
echo.
echo Para ejecutar la aplicacion:
echo   python app.py
echo.
echo Para abrir en el navegador:
echo   http://localhost:5000
echo.
echo Cuentas de demostracion:
echo   Admin: admin@unrc.edu.mx / Admin123
echo   Estudiante: estudiante1@unrc.edu.mx / Estudiante123
echo   Empresa: empresa1@empresa.com / Empresa123
echo.
pause
