# Solución para Error de SQLAlchemy con Python 3.13.3
# Plataforma de Vinculación UNRC

## 🚨 Problema Identificado
```
AssertionError: Class <class 'sqlalchemy.sql.elements.SQLCoreOperations'> 
directly inherits TypingOnly but has additional attributes
```

Este error ocurre porque SQLAlchemy 2.0.23 no es completamente compatible con Python 3.13.3.

## ✅ Soluciones Disponibles

### Solución 1: Actualizar SQLAlchemy (Recomendada)
```bash
# Desinstalar SQLAlchemy actual
pip uninstall SQLAlchemy

# Instalar versión más reciente compatible con Python 3.13
pip install SQLAlchemy>=2.0.25

# O instalar la versión más reciente
pip install SQLAlchemy --upgrade
```

### Solución 2: Usar Python 3.11 (Más Estable)
```bash
# 1. Crear nuevo entorno virtual con Python 3.11
python3.11 -m venv venv311
venv311\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt
```

### Solución 3: Instalación Manual Paso a Paso
```bash
# 1. Limpiar instalación actual
pip uninstall SQLAlchemy Flask-SQLAlchemy

# 2. Instalar SQLAlchemy compatible
pip install SQLAlchemy==2.0.25

# 3. Instalar Flask-SQLAlchemy
pip install Flask-SQLAlchemy==3.1.1

# 4. Verificar instalación
python -c "import sqlalchemy; print(sqlalchemy.__version__)"
```

### Solución 4: Usar Conda (Más Estable)
```bash
# 1. Instalar Anaconda o Miniconda
# 2. Crear entorno con Python 3.11
conda create -n vinculacion python=3.11
conda activate vinculacion

# 3. Instalar dependencias
conda install flask sqlalchemy
pip install Flask-SQLAlchemy Flask-JWT-Extended Flask-Mail Flask-CORS reportlab scikit-learn pandas numpy
```

## 🔧 Comandos de Reparación Rápida

### Opción A: Actualización Completa
```bash
# Activar entorno virtual
venv\Scripts\activate

# Actualizar pip
python -m pip install --upgrade pip

# Desinstalar SQLAlchemy problemático
pip uninstall SQLAlchemy Flask-SQLAlchemy

# Instalar versiones compatibles
pip install SQLAlchemy>=2.0.25
pip install Flask-SQLAlchemy==3.1.1

# Instalar resto de dependencias
pip install Flask==3.0.0 Flask-JWT-Extended==4.6.0 Flask-Mail==0.9.1 Flask-CORS==4.0.0 Werkzeug==3.0.1 bcrypt==4.1.2 python-dotenv==1.0.0 reportlab==4.0.7 scikit-learn pandas numpy requests email-validator python-dateutil
```

### Opción B: Reinstalación Completa
```bash
# Eliminar entorno virtual actual
rmdir /s venv

# Crear nuevo entorno virtual
python -m venv venv
venv\Scripts\activate

# Instalar dependencias actualizadas
pip install -r requirements.txt
```

## ✅ Verificación de Instalación

### Script de Prueba
```python
# Crear archivo test_sqlalchemy.py
try:
    import sqlalchemy
    print("✅ SQLAlchemy version:", sqlalchemy.__version__)
    
    import flask_sqlalchemy
    print("✅ Flask-SQLAlchemy installed")
    
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    
    app = Flask(__name__)
    db = SQLAlchemy(app)
    print("✅ SQLAlchemy integration working")
    
except Exception as e:
    print("❌ Error:", e)
```

### Ejecutar Prueba
```bash
python test_sqlalchemy.py
```

## 🚀 Ejecución Después de la Reparación

```bash
# 1. Verificar que no hay errores
python -c "import sqlalchemy, flask_sqlalchemy; print('OK')"

# 2. Ejecutar aplicación
python app.py

# 3. Abrir navegador
# http://localhost:5000
```

## 🆘 Si el Problema Persiste

### Usar Versión Simplificada Sin SQLAlchemy
```python
# Crear app_simple.py sin SQLAlchemy
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        'message': 'Plataforma de Vinculación UNRC',
        'status': 'running',
        'version': '1.0.0'
    })

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### Ejecutar Versión Simplificada
```bash
python app_simple.py
```

## 📋 Checklist de Solución

- [ ] Actualizar SQLAlchemy a versión >= 2.0.25
- [ ] Verificar compatibilidad con Python 3.13.3
- [ ] Probar importación de SQLAlchemy
- [ ] Ejecutar aplicación sin errores
- [ ] Verificar funcionalidad de base de datos

## 🎯 Alternativas de Desarrollo

### Opción 1: Usar Python 3.11
```bash
# Más estable para desarrollo
python3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Opción 2: Usar Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

### Opción 3: Usar WSL2
```bash
# En Windows Subsystem for Linux
sudo apt update
sudo apt install python3.11 python3.11-venv
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

**¡El problema es conocido y tiene solución!** 🚀

La incompatibilidad entre SQLAlchemy 2.0.23 y Python 3.13.3 se resuelve actualizando SQLAlchemy a una versión más reciente.
