# Plataforma de Vinculación UNRC - 

Una plataforma web completa para la gestión de servicio social, practicas profesionales y empleo, en la Universidad Nacional Rosario Castellanos, que conecta estudiantes con empresas e instituciones para realizar su servicio social mediante inteligencia artificial.

## 🚀 Características Principales

### Para Estudiantes
- **Registro y validación**: Verificación automática de créditos (mínimo 75%)
- **Perfil personalizado**: Gestión de habilidades técnicas y blandas
- **Recomendaciones inteligentes**: Matching automático con empresas usando IA
- **Seguimiento de solicitudes**: Estado en tiempo real de aplicaciones
- **Generación de documentos**: Constancias, cartas y reportes automáticos

### Para Empresas
- **Gestión de cupos**: Control de disponibilidad de plazas
- **Evaluación de candidatos**: Revisión de perfiles y solicitudes
- **Comunicación directa**: Sistema de notificaciones integrado
- **Documentación oficial**: Generación automática de cartas de aceptación

### Para Administradores
- **Dashboard completo**: Estadísticas y métricas en tiempo real
- **Gestión de usuarios**: Control de estudiantes, empresas y administradores
- **Supervisión de solicitudes**: Monitoreo del proceso completo
- **Generación de reportes**: Documentos oficiales y constancias
- **KPIs y OKRs**: Medición del impacto del sistema

## 🛠️ Tecnologías Utilizadas

### Backend
- **Python 3.13.3**
- **Flask**: Framework web ligero y flexible
- **SQLAlchemy**: ORM para manejo de base de datos
- **Flask-JWT-Extended**: Autenticación con tokens JWT
- **ReportLab**: Generación de documentos PDF
- **Flask-Mail**: Envío de notificaciones por email
- **scikit-learn**: Algoritmos de machine learning para matching inteligente

### Frontend
- **HTML5 + CSS3**: Estructura y estilos modernos
- **Bootstrap 5**: Framework CSS responsivo
- **JavaScript ES6+**: Interactividad y funcionalidad
- **Font Awesome**: Iconografía profesional
- **SweetAlert2**: Notificaciones elegantes

### Base de Datos
- **SQLite**: Base de datos ligera para desarrollo
- **PostgreSQL**: Recomendado para producción

### Inteligencia Artificial
- **scikit-learn**: Algoritmos de machine learning
- **TF-IDF**: Análisis de similitud semántica
- **Random Forest**: Clasificación de compatibilidad
- **Cosine Similarity**: Matching inteligente

## 📋 Requisitos del Sistema

### Mínimos
- Python 3.13.3
- 2GB RAM
- 1GB espacio en disco
- Navegador web moderno

### Recomendados
- Python 3.13.3+
- 4GB RAM
- 5GB espacio en disco
- PostgreSQL 12+

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/vinculacion-unrc.git
cd vinculacion-unrc
```

### 2. Crear entorno virtual
```bash
python -m venv venv

# En Windows
venv\Scripts\activate

# En Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crear archivo `config.py` en la raíz del proyecto:
```python
# Configuración del servidor
PORT=5000
FLASK_ENV=development

# JWT Secret (cambiar en producción)
JWT_SECRET_KEY=vinculacion_unrc_super_secret_key_2024

# Configuración de base de datos
DATABASE_URL=sqlite:///vinculacion_unrc.db

# Configuración de email (opcional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=vinculacion.unrc@gmail.com
MAIL_PASSWORD=your_app_password_here

# Configuración de la aplicación
APP_NAME=Plataforma de Vinculación UNRC
APP_VERSION=1.0.0
UNIVERSITY_NAME=Universidad Nacional Rosario Castellanos

# Configuración de IA
AI_MODEL_PATH=./models/
ENABLE_AI_MATCHING=true
MIN_MATCH_SCORE=0.6

# Configuración de documentos
DOCUMENTS_PATH=./documents/
TEMPLATES_PATH=./templates/
```

### 5. Inicializar base de datos
```bash
python app.py
```

### 6. Ejecutar la aplicación
```bash
python app.py
```

La aplicación estará disponible en `http://localhost:5000`

## 📁 Estructura del Proyecto

```
vinculacion-unrc/
├── app.py                 # Aplicación principal Flask
├── models.py             # Modelos de base de datos
├── ai_matching.py        # Motor de matching inteligente
├── config.py             # Configuración de la aplicación
├── requirements.txt      # Dependencias de Python
├── README.md            # Documentación
├── routes/              # Rutas de la API
│   ├── __init__.py
│   ├── auth_routes.py   # Autenticación
│   ├── student_routes.py # Estudiantes
│   ├── company_routes.py # Empresas
│   ├── admin_routes.py  # Administradores
│   ├── document_routes.py # Documentos
│   └── analytics_routes.py # Analytics y KPIs
├── templates/           # Plantillas HTML
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   └── register.html
├── static/             # Archivos estáticos
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── documents/          # Documentos generados
├── uploads/            # Archivos subidos
└── models/             # Modelos de IA
```

## 🔧 Configuración de Producción

### 1. Base de datos PostgreSQL
```bash
# Instalar PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Crear base de datos
sudo -u postgres createdb vinculacion_unrc

# Configurar usuario
sudo -u postgres createuser --interactive
```

### 2. Variables de entorno de producción
```python
FLASK_ENV=production
DATABASE_URL=postgresql://usuario:password@localhost/vinculacion_unrc
JWT_SECRET_KEY=secreto_super_seguro_de_produccion
MAIL_SERVER=smtp.tu-servidor.com
MAIL_USERNAME=tu-email@dominio.com
MAIL_PASSWORD=tu-password-seguro
```

### 3. Usar Gunicorn para producción
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📊 API Endpoints

### Autenticación
- `POST /api/auth/register/student` - Registro de estudiante
- `POST /api/auth/register/company` - Registro de empresa
- `POST /api/auth/login` - Inicio de sesión
- `GET /api/auth/profile` - Perfil del usuario
- `GET /api/auth/verify` - Verificar token

### Estudiantes
- `GET /api/students/profile/{id}` - Obtener perfil
- `PUT /api/students/profile/{id}` - Actualizar perfil
- `POST /api/students/upload-cv/{id}` - Subir CV
- `GET /api/students/recommendations/{id}` - Obtener recomendaciones
- `POST /api/students/apply/{id}` - Aplicar a empresa
- `GET /api/students/requests/{id}` - Obtener solicitudes

### Empresas
- `GET /api/companies/profile` - Obtener perfil
- `PUT /api/companies/profile` - Actualizar perfil
- `GET /api/companies/opportunities` - Obtener oportunidades
- `POST /api/companies/opportunities` - Crear oportunidad
- `GET /api/companies/requests` - Obtener solicitudes
- `PUT /api/companies/requests/{id}/respond` - Responder solicitud
- `GET /api/companies/stats` - Obtener estadísticas

### Administradores
- `GET /api/admin/dashboard` - Dashboard principal
- `GET /api/admin/students` - Lista de estudiantes
- `GET /api/admin/companies` - Lista de empresas
- `GET /api/admin/requests` - Lista de solicitudes
- `PUT /api/admin/users/{id}/toggle-status` - Activar/desactivar usuario

### Documentos
- `POST /api/documents/generate/constancia-creditos` - Generar constancia
- `POST /api/documents/generate/carta-presentacion` - Generar carta
- `POST /api/documents/generate/carta-aceptacion` - Generar aceptación
- `POST /api/documents/generate/reporte-mensual` - Generar reporte
- `GET /api/documents/download/{id}` - Descargar documento

### Analytics y KPIs
- `GET /api/analytics/kpis` - Obtener KPIs
- `POST /api/analytics/kpis/update` - Actualizar KPIs
- `GET /api/analytics/okrs` - Obtener OKRs
- `POST /api/analytics/okrs/update` - Actualizar OKRs
- `GET /api/analytics/dashboard` - Dashboard de analytics
- `GET /api/analytics/trends` - Obtener tendencias

## 🤖 Inteligencia Artificial

### Motor de Matching
La plataforma utiliza un motor de matching inteligente que combina:

1. **Análisis Semántico**: Usando TF-IDF para analizar similitud entre perfiles
2. **Análisis Estructurado**: Comparación de características numéricas
3. **Machine Learning**: Random Forest para predecir compatibilidad
4. **Factores Adicionales**: Disponibilidad, completitud del perfil, experiencia

### Modelos NLP Implementados
Actualmente se utiliza un único modelo/proceso NLP basado en TF-IDF (TfidfVectorizer) para extracción de características y cálculo de similitud semántica (cosine similarity). No se usan embeddings, spaCy ni modelos transformers; el RandomForest opera sobre características estructuradas y no es un modelo de lenguaje.
Archivos relacionados: ai_matching.py y ai_matching_simple.py.

### Algoritmo de Scoring
```python
score = (
    semantic_similarity * 0.4 +
    structured_similarity * 0.4 +
    basic_compatibility * 0.2
)
```

### Características Analizadas
- Habilidades técnicas y blandas
- Carrera y semestre
- Porcentaje de créditos
- Experiencia previa
- Idiomas
- Intereses profesionales

## 📈 KPIs y OKRs

### KPIs Implementados
- **Registros**: Total de estudiantes y empresas registradas
- **Colocación**: Tasa de aceptación y colocación por carrera
- **Matching**: Score promedio y distribución de compatibilidad

### OKRs Implementados
- **Colocación**: Aumentar estudiantes colocados
- **Satisfacción**: Mejorar tasa de satisfacción de empresas
- **Matching**: Optimizar algoritmo de compatibilidad

## 🔐 Seguridad

- **Autenticación JWT**: Tokens seguros con expiración
- **Validación de datos**: Sanitización de entradas
- **Hash de contraseñas**: Bcrypt para seguridad
- **CORS configurado**: Control de acceso cross-origin
- **Rate limiting**: Protección contra ataques
- **Validación de archivos**: Verificación de tipos y tamaños

## 📈 Monitoreo y Logs

### Logs de aplicación
```bash
# Ver logs en tiempo real
tail -f app.log

# Logs de errores
grep "ERROR" app.log
```

### Métricas importantes
- Usuarios activos
- Solicitudes procesadas
- Documentos generados
- Tiempo de respuesta
- Score de matching promedio

## 🎯 Cuentas de Demostración

### Administrador
- **Email**: admin@unrc.edu.mx
- **Contraseña**: Admin123

### Estudiante
- **Email**: estudiante1@unrc.edu.mx
- **Contraseña**: Estudiante123

### Empresa
- **Email**: empresa1@empresa.com
- **Contraseña**: Empresa123

## 🚀 Funcionalidades Destacadas

### 1. Matching Inteligente
- Análisis de compatibilidad en tiempo real
- Recomendaciones personalizadas
- Score de matching del 0-100%

### 2. Generación de Documentos
- Constancias de créditos automáticas
- Cartas de presentación personalizadas
- Reportes mensuales detallados

### 3. Dashboard Analytics
- KPIs en tiempo real
- OKRs con seguimiento automático
- Tendencias y estadísticas

### 4. Interfaz Moderna
- Diseño responsivo
- Experiencia de usuario optimizada
- Notificaciones elegantes

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama para feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🆘 Soporte

Para soporte técnico o preguntas:
- Email: soporte@unrc.edu.mx
- Documentación: [Wiki del proyecto](https://github.com/tu-usuario/vinculacion-unrc/wiki)
- Issues: [GitHub Issues](https://github.com/tu-usuario/vinculacion-unrc/issues)

## 🎯 Roadmap

### Versión 2.0
- [ ] Integración con sistemas universitarios
- [ ] App móvil nativa
- [ ] Dashboard avanzado con analytics
- [ ] Sistema de calificaciones
- [ ] Integración con calendarios

### Versión 2.1
- [ ] Chat en tiempo real
- [ ] Video llamadas integradas
- [ ] Sistema de recomendaciones ML avanzado
- [ ] API pública
- [ ] Webhooks para integraciones

---

**Desarrollado con ❤️ para la Universidad Nacional Rosario Castellanos**

*Plataforma de Vinculación Inteligente - Conectando talento con oportunidades*
