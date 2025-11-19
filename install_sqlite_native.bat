@echo off
echo ========================================
echo   Plataforma de Vinculacion UNRC
echo   Version SQLite Nativo (Sin SQLAlchemy)
echo ========================================
echo.

echo [1/6] Activando entorno virtual...
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo Error: No se encontro el entorno virtual
    echo Creando nuevo entorno virtual...
    python -m venv venv
    call venv\Scripts\activate
)

echo.
echo [2/6] Actualizando pip...
python -m pip install --upgrade pip

echo.
echo [3/6] Instalando Flask y dependencias basicas...
pip install Flask==3.0.0
pip install Flask-JWT-Extended==4.6.0
pip install Flask-Mail==0.9.1
pip install Flask-CORS==4.0.0

echo.
echo [4/6] Instalando utilidades...
pip install Werkzeug==3.0.1
pip install bcrypt==4.1.2
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
echo   Verificando instalacion...
echo ========================================
python -c "import flask; print('Flask version:', flask.__version__)"
python -c "import sqlite3; print('SQLite: OK')"
python -c "import jwt; print('JWT: OK')"

echo.
echo ========================================
echo   Instalacion completada!
echo ========================================
echo.
echo Para ejecutar la aplicacion:
echo   python app_sqlite_native.py
echo.
echo Para verificar que funciona:
echo   python -c "import sqlite3, flask; print('Todo OK')"
echo.
echo Caracteristicas disponibles:
echo   ✅ Autenticacion JWT
echo   ✅ Base de datos SQLite nativa
echo   ✅ API REST completa
echo   ✅ Generacion de documentos PDF
echo   ✅ Matching basico con IA
echo   ✅ Dashboard con estadisticas
echo.
pause
