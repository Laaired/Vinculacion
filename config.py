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
