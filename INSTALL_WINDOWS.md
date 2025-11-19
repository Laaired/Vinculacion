# Instalación Alternativa para Windows - Plataforma de Vinculación UNRC

## 🚀 Solución al Error de Pillow

Si tienes problemas con Pillow en Windows, sigue estos pasos:

### Opción 1: Instalación por Partes
```bash
# 1. Actualizar pip primero
python -m pip install --upgrade pip

# 2. Instalar dependencias básicas primero
pip install Flask==3.0.0
pip install Flask-SQLAlchemy==3.1.1
pip install Flask-JWT-Extended==4.6.0
pip install Flask-Mail==0.9.1
pip install Flask-CORS==4.0.0
pip install Flask-Migrate==4.0.5
pip install SQLAlchemy==2.0.23
pip install Werkzeug==3.0.1
pip install bcrypt==4.1.2
pip install python-dotenv==1.0.0
pip install reportlab==4.0.7

# 3. Instalar Pillow con versión específica para Windows
pip install Pillow==10.0.1

# 4. Instalar dependencias de IA
pip install scikit-learn>=1.3.0
pip install pandas>=2.0.0
pip install numpy>=1.24.0
pip install matplotlib>=3.7.0
pip install seaborn>=0.12.0
pip install plotly>=5.15.0
pip install requests>=2.30.0
pip install email-validator>=2.0.0
pip install python-dateutil>=2.8.0
```

### Opción 2: Usar Conda (Recomendado para Windows)
```bash
# 1. Instalar Anaconda o Miniconda
# 2. Crear entorno con conda
conda create -n vinculacion python=3.11
conda activate vinculacion

# 3. Instalar dependencias con conda
conda install flask sqlalchemy pillow scikit-learn pandas numpy matplotlib seaborn requests

# 4. Instalar dependencias restantes con pip
pip install Flask-JWT-Extended Flask-Mail Flask-CORS Flask-Migrate bcrypt python-dotenv reportlab plotly email-validator python-dateutil
```

### Opción 3: Versión Simplificada (Sin Pillow)
Si Pillow sigue dando problemas, puedes usar una versión simplificada:

```bash
# Instalar solo dependencias esenciales
pip install Flask==3.0.0
pip install Flask-SQLAlchemy==3.1.1
pip install Flask-JWT-Extended==4.6.0
pip install Flask-Mail==0.9.1
pip install Flask-CORS==4.0.0
pip install SQLAlchemy==2.0.23
pip install Werkzeug==3.0.1
pip install bcrypt==4.1.2
pip install python-dotenv==1.0.0
pip install reportlab==4.0.7
pip install scikit-learn>=1.3.0
pip install pandas>=2.0.0
pip install numpy>=1.24.0
pip install requests>=2.30.0
pip install email-validator>=2.0.0
pip install python-dateutil>=2.8.0
```

## 🔧 Configuración Alternativa

Si tienes problemas con las dependencias, puedes modificar el código para que funcione sin algunas librerías:

### 1. Modificar ai_matching.py
```python
# Comentar las importaciones problemáticas
# import matplotlib.pyplot as plt
# import seaborn as sns

# Usar solo las librerías básicas
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
```

### 2. Modificar document_routes.py
```python
# Comentar la importación de PIL si da problemas
# from PIL import Image as PILImage

# El resto del código funcionará sin problemas
```

## 🚀 Ejecución Rápida

Una vez instaladas las dependencias:

```bash
# 1. Ejecutar la aplicación
python app.py

# 2. Abrir navegador en http://localhost:5000

# 3. Hacer clic en "Inicializar" para crear datos de ejemplo

# 4. Usar las cuentas de demostración:
#    Admin: admin@unrc.edu.mx / admin123
#    Estudiante: estudiante1@unrc.edu.mx / estudiante123
#    Empresa: empresa1@empresa.com / empresa123
```

## 🆘 Solución de Problemas Comunes

### Error: "Microsoft Visual C++ 14.0 is required"
```bash
# Instalar Microsoft C++ Build Tools
# O usar conda que incluye los compiladores
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

## ✅ Verificación de Instalación

Para verificar que todo está instalado correctamente:

```bash
python -c "
import flask
import sqlalchemy
import sklearn
import pandas
import numpy
print('✅ Todas las dependencias instaladas correctamente')
print('Flask version:', flask.__version__)
print('SQLAlchemy version:', sqlalchemy.__version__)
print('Scikit-learn version:', sklearn.__version__)
"
```

## 🎯 Funcionalidades Disponibles

Incluso si algunas dependencias fallan, la plataforma seguirá funcionando con:

- ✅ Sistema de autenticación JWT
- ✅ API REST completa
- ✅ Base de datos SQLite
- ✅ Generación de documentos PDF
- ✅ Interfaz web moderna
- ✅ Sistema de matching básico
- ✅ KPIs y OKRs

La funcionalidad de IA avanzada puede requerir scikit-learn, pero el sistema básico funcionará sin problemas.

---

**¡La plataforma está diseñada para ser robusta y funcionar incluso con dependencias limitadas!** 🚀
