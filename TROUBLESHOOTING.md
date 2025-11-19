# 🚨 Solución de Problemas - Plataforma de Vinculación UNRC

## ❌ Error: Pillow Installation Failed

### Problema
```
error: subprocess-exited-with-error
× Getting requirements to build wheel did not run successfully.
KeyError: '__version__'
```

### ✅ Soluciones

#### Solución 1: Instalación Manual por Partes
```bash
# 1. Actualizar pip
python -m pip install --upgrade pip

# 2. Instalar dependencias básicas
pip install Flask==3.0.0 Flask-SQLAlchemy==3.1.1 Flask-JWT-Extended==4.6.0

# 3. Instalar Pillow con versión específica
pip install Pillow==10.0.1

# 4. Continuar con el resto
pip install reportlab==4.0.7 scikit-learn pandas numpy
```

#### Solución 2: Usar Conda (Recomendado)
```bash
# Instalar Anaconda o Miniconda
# Crear entorno
conda create -n vinculacion python=3.11
conda activate vinculacion

# Instalar con conda
conda install flask sqlalchemy pillow scikit-learn pandas numpy matplotlib
pip install Flask-JWT-Extended Flask-Mail Flask-CORS reportlab
```

#### Solución 3: Versión Sin Pillow
```bash
# Instalar solo dependencias esenciales
pip install Flask==3.0.0 Flask-SQLAlchemy==3.1.1 Flask-JWT-Extended==4.6.0 Flask-Mail==0.9.1 Flask-CORS==4.0.0 SQLAlchemy==2.0.23 Werkzeug==3.0.1 bcrypt==4.1.2 python-dotenv==1.0.0 reportlab==4.0.7 scikit-learn pandas numpy requests email-validator python-dateutil
```

## 🔧 Modificaciones de Código para Windows

### 1. Reemplazar ai_matching.py
```bash
# Copiar la versión simplificada
copy ai_matching_simple.py ai_matching.py
```

### 2. Modificar app.py (opcional)
```python
# Comentar importaciones problemáticas
# from PIL import Image as PILImage

# El resto del código funcionará sin problemas
```

### 3. Usar requirements_windows.txt
```bash
pip install -r requirements_windows.txt
```

## 🚀 Instalación Automática

### Usar el Script de Windows
```bash
# Ejecutar el archivo .bat
install_windows.bat
```

### Instalación Manual Paso a Paso
```bash
# 1. Crear entorno virtual
python -m venv venv
venv\Scripts\activate

# 2. Actualizar pip
python -m pip install --upgrade pip

# 3. Instalar Flask y dependencias básicas
pip install Flask==3.0.0
pip install Flask-SQLAlchemy==3.1.1
pip install Flask-JWT-Extended==4.6.0
pip install Flask-Mail==0.9.1
pip install Flask-CORS==4.0.0
pip install SQLAlchemy==2.0.23
pip install Werkzeug==3.0.1
pip install bcrypt==4.1.2
pip install python-dotenv==1.0.0

# 4. Instalar generación de documentos
pip install reportlab==4.0.7

# 5. Instalar IA (opcional)
pip install scikit-learn
pip install pandas
pip install numpy

# 6. Instalar utilidades
pip install requests
pip install email-validator
pip install python-dateutil
```

## ✅ Verificación de Instalación

### Script de Verificación
```python
# Crear archivo test_install.py
import sys

def test_imports():
    try:
        import flask
        print("✅ Flask:", flask.__version__)
    except ImportError as e:
        print("❌ Flask:", e)
    
    try:
        import sqlalchemy
        print("✅ SQLAlchemy:", sqlalchemy.__version__)
    except ImportError as e:
        print("❌ SQLAlchemy:", e)
    
    try:
        import sklearn
        print("✅ Scikit-learn:", sklearn.__version__)
    except ImportError as e:
        print("❌ Scikit-learn:", e)
    
    try:
        import pandas
        print("✅ Pandas:", pandas.__version__)
    except ImportError as e:
        print("❌ Pandas:", e)
    
    try:
        import numpy
        print("✅ NumPy:", numpy.__version__)
    except ImportError as e:
        print("❌ NumPy:", e)
    
    try:
        import reportlab
        print("✅ ReportLab:", reportlab.Version)
    except ImportError as e:
        print("❌ ReportLab:", e)

if __name__ == "__main__":
    print("Verificando instalación de dependencias...")
    test_imports()
```

### Ejecutar Verificación
```bash
python test_install.py
```

## 🎯 Funcionalidades Disponibles por Nivel

### Nivel 1: Básico (Solo Flask)
- ✅ Sistema de autenticación
- ✅ API REST
- ✅ Base de datos SQLite
- ✅ Interfaz web

### Nivel 2: Intermedio (+ ReportLab)
- ✅ Todo lo anterior
- ✅ Generación de documentos PDF
- ✅ Constancias y cartas

### Nivel 3: Avanzado (+ Scikit-learn)
- ✅ Todo lo anterior
- ✅ Matching inteligente con IA
- ✅ Recomendaciones automáticas
- ✅ KPIs y OKRs

## 🆘 Problemas Comunes y Soluciones

### Error: "Microsoft Visual C++ 14.0 is required"
```bash
# Solución: Instalar Visual Studio Build Tools
# O usar conda que incluye compiladores
conda install libpython m2w64-toolchain
```

### Error: "Failed building wheel"
```bash
# Usar versiones pre-compiladas
pip install --only-binary=all Pillow
pip install --only-binary=all scikit-learn
```

### Error: "No module named 'sklearn'"
```bash
# Instalar scikit-learn específicamente
pip install scikit-learn==1.3.2
```

### Error: "Permission denied"
```bash
# Ejecutar como administrador
# O usar --user flag
pip install --user package_name
```

## 🚀 Ejecución Final

Una vez resueltos los problemas:

```bash
# 1. Ejecutar aplicación
python app.py

# 2. Abrir navegador
# http://localhost:5000

# 3. Inicializar sistema
# Hacer clic en "Inicializar" en la página de login

# 4. Usar cuentas de demo
# Admin: admin@unrc.edu.mx / admin123
# Estudiante: estudiante1@unrc.edu.mx / estudiante123
# Empresa: empresa1@empresa.com / empresa123
```

## 📞 Soporte Adicional

Si sigues teniendo problemas:

1. **Verificar versión de Python**: `python --version`
2. **Verificar pip**: `pip --version`
3. **Limpiar caché**: `pip cache purge`
4. **Reinstalar pip**: `python -m ensurepip --upgrade`
5. **Usar entorno virtual**: Siempre usar venv o conda

---

**¡La plataforma está diseñada para ser robusta y funcionar incluso con dependencias limitadas!** 🚀
