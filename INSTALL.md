# Plataforma de Vinculación UNRC - Guía de Instalación Rápida

## 🚀 Instalación en 5 Pasos

### 1. Preparar el Entorno
```bash
# Crear directorio del proyecto
mkdir vinculacion-unrc
cd vinculacion-unrc

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

### 2. Instalar Dependencias
```bash
# Instalar todas las dependencias
pip install -r requirements.txt
```

### 3. Configurar la Aplicación
```bash
# Crear directorios necesarios
mkdir uploads uploads\cvs uploads\photos documents models

# El archivo config.py ya está configurado con valores por defecto
```

### 4. Ejecutar la Aplicación
```bash
# Ejecutar la aplicación
python app.py
```

### 5. Inicializar con Datos de Ejemplo
1. Abrir navegador en `http://localhost:5000`
2. Ir a la página de login
3. Hacer clic en "Inicializar" para crear datos de ejemplo
4. Usar las cuentas de demostración:
   - **Admin**: admin@unrc.edu.mx / Admin123
   - **Estudiante**: estudiante1@unrc.edu.mx / Estudiante123
   - **Empresa**: empresa1@empresa.com / Empresa123

## 🎯 Funcionalidades Principales

### Para Estudiantes
- ✅ Registro y perfil completo
- ✅ Recomendaciones inteligentes con IA
- ✅ Aplicación a oportunidades
- ✅ Seguimiento de solicitudes
- ✅ Generación de documentos PDF

### Para Empresas
- ✅ Registro y gestión de perfil
- ✅ Creación de oportunidades
- ✅ Evaluación de candidatos
- ✅ Respuesta a solicitudes
- ✅ Estadísticas de la empresa

### Para Administradores
- ✅ Dashboard completo con KPIs
- ✅ Gestión de usuarios
- ✅ Supervisión de solicitudes
- ✅ Generación de reportes
- ✅ Analytics avanzados

## 🤖 Inteligencia Artificial

La plataforma incluye un motor de matching inteligente que:
- Analiza perfiles usando TF-IDF
- Calcula compatibilidad con Random Forest
- Genera recomendaciones personalizadas
- Predice probabilidad de éxito

## 📊 KPIs y OKRs

### KPIs Implementados
- Total de estudiantes registrados
- Total de empresas participantes
- Tasa de aceptación de aplicaciones
- Score promedio de matching

### OKRs Implementados
- Objetivo de colocación de estudiantes
- Meta de satisfacción de empresas
- Optimización del algoritmo de matching

## 🔧 Configuración Avanzada

### Cambiar Base de Datos
Editar `config.py`:
```python
DATABASE_URL=postgresql://usuario:password@localhost/vinculacion_unrc
```

### Configurar Email
Editar `config.py`:
```python
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_password_de_aplicacion
```

### Personalizar IA
Editar `ai_matching.py`:
```python
MIN_MATCH_SCORE=0.6  # Score mínimo para recomendaciones
```

## 🚨 Solución de Problemas

### Error de Dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Error de Base de Datos
```bash
# Eliminar base de datos existente
rm vinculacion_unrc.db
# Ejecutar aplicación para recrear
python app.py
```

### Error de Permisos
```bash
# En Linux/Mac
chmod +x venv/bin/activate
# En Windows, ejecutar como administrador
```

## 📱 Acceso a la Plataforma

- **URL Local**: http://localhost:5000
- **URL Producción**: https://tu-dominio.com

## 🎓 Características Educativas

Esta plataforma demuestra:
- Desarrollo de APIs REST con Flask
- Implementación de autenticación JWT
- Uso de machine learning en aplicaciones web
- Generación de documentos PDF
- Diseño de interfaces modernas
- Implementación de KPIs y OKRs
- Arquitectura de microservicios

## 📞 Soporte

Para soporte técnico:
- Revisar logs en la consola
- Verificar configuración en `config.py`
- Consultar documentación en `README.md`

---

**¡Listo para usar!** 🎉

La plataforma está completamente funcional y lista para demostrar las capacidades de vinculación inteligente entre estudiantes y empresas.
