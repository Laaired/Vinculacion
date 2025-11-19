# Versión alternativa de app.py con manejo de errores mejorado
# Plataforma de Vinculación UNRC

import os
import sys
from datetime import datetime

# Verificar Python version
if sys.version_info < (3, 8):
    print("❌ Error: Se requiere Python 3.8 o superior")
    print(f"Versión actual: {sys.version}")
    sys.exit(1)

print(f"✅ Python version: {sys.version}")

# Importaciones con manejo de errores
try:
    from flask import Flask, render_template, request, jsonify, send_file, current_app
    print("✅ Flask importado correctamente")
except ImportError as e:
    print(f"❌ Error importando Flask: {e}")
    print("Instalar con: pip install Flask==3.0.0")
    sys.exit(1)

try:
    from flask_sqlalchemy import SQLAlchemy
    print("✅ Flask-SQLAlchemy importado correctamente")
except ImportError as e:
    print(f"❌ Error importando Flask-SQLAlchemy: {e}")
    print("Instalar con: pip install Flask-SQLAlchemy==3.1.1")
    sys.exit(1)

try:
    from flask_jwt_extended import JWTManager
    print("✅ Flask-JWT-Extended importado correctamente")
except ImportError as e:
    print(f"❌ Error importando Flask-JWT-Extended: {e}")
    print("Instalar con: pip install Flask-JWT-Extended==4.6.0")
    sys.exit(1)

try:
    from flask_cors import CORS
    print("✅ Flask-CORS importado correctamente")
except ImportError as e:
    print(f"❌ Error importando Flask-CORS: {e}")
    print("Instalar con: pip install Flask-CORS==4.0.0")
    sys.exit(1)

try:
    from flask_mail import Mail
    print("✅ Flask-Mail importado correctamente")
except ImportError as e:
    print(f"⚠️  Flask-Mail no disponible: {e}")
    print("Continuando sin funcionalidad de email...")

try:
    from flask_migrate import Migrate
    print("✅ Flask-Migrate importado correctamente")
except ImportError as e:
    print(f"⚠️  Flask-Migrate no disponible: {e}")
    print("Continuando sin migraciones de base de datos...")

# Importar modelos
try:
    from models import db, User, Student, Company, Opportunity, Application, Document, KPI, OKR
    print("✅ Modelos de base de datos importados correctamente")
except ImportError as e:
    print(f"❌ Error importando modelos: {e}")
    print("Verificar que models.py existe y está correcto")
    sys.exit(1)

# Importar rutas con manejo de errores
try:
    from routes.auth_routes import auth_bp
    print("✅ Rutas de autenticación importadas")
except ImportError as e:
    print(f"⚠️  Error importando rutas de auth: {e}")

try:
    from routes.student_routes import student_bp
    print("✅ Rutas de estudiantes importadas")
except ImportError as e:
    print(f"⚠️  Error importando rutas de estudiantes: {e}")

try:
    from routes.company_routes import company_bp
    print("✅ Rutas de empresas importadas")
except ImportError as e:
    print(f"⚠️  Error importando rutas de empresas: {e}")

try:
    from routes.admin_routes import admin_bp
    print("✅ Rutas de administradores importadas")
except ImportError as e:
    print(f"⚠️  Error importando rutas de admin: {e}")

try:
    from routes.document_routes import document_bp
    print("✅ Rutas de documentos importadas")
except ImportError as e:
    print(f"⚠️  Error importando rutas de documentos: {e}")

try:
    from routes.analytics_routes import analytics_bp
    print("✅ Rutas de analytics importadas")
except ImportError as e:
    print(f"⚠️  Error importando rutas de analytics: {e}")

# Importar motor de IA con manejo de errores
try:
    from ai_matching import matching_engine
    print("✅ Motor de IA importado correctamente")
except ImportError as e:
    print(f"⚠️  Error importando motor de IA: {e}")
    print("Continuando sin funcionalidad de IA avanzada...")
    matching_engine = None

def create_app():
    """Crear y configurar la aplicación Flask"""
    app = Flask(__name__)
    
    # Configuración básica
    app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'vinculacion_unrc_secret_key')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'vinculacion_unrc_secret_key')
    
    # Base de datos
    database_url = os.getenv('DATABASE_URL', 'sqlite:///vinculacion_unrc.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configuración de archivos
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Configuración de email (opcional)
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', '')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', '')
    
    # Inicializar extensiones
    try:
        db.init_app(app)
        print("✅ Base de datos inicializada")
    except Exception as e:
        print(f"❌ Error inicializando base de datos: {e}")
        return None
    
    try:
        jwt = JWTManager(app)
        print("✅ JWT inicializado")
    except Exception as e:
        print(f"❌ Error inicializando JWT: {e}")
        return None
    
    try:
        cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
        print("✅ CORS configurado")
    except Exception as e:
        print(f"❌ Error configurando CORS: {e}")
        return None
    
    # Inicializar extensiones opcionales
    try:
        mail = Mail(app)
        print("✅ Email configurado")
    except Exception as e:
        print(f"⚠️  Email no configurado: {e}")
    
    try:
        migrate = Migrate(app, db)
        print("✅ Migraciones configuradas")
    except Exception as e:
        print(f"⚠️  Migraciones no configuradas: {e}")
    
    # Registrar blueprints
    try:
        app.register_blueprint(auth_bp)
        app.register_blueprint(student_bp)
        app.register_blueprint(company_bp)
        app.register_blueprint(admin_bp)
        app.register_blueprint(document_bp)
        app.register_blueprint(analytics_bp)
        print("✅ Blueprints registrados")
    except Exception as e:
        print(f"⚠️  Error registrando blueprints: {e}")
    
    # Crear directorios necesarios
    try:
        os.makedirs('uploads', exist_ok=True)
        os.makedirs('uploads/cvs', exist_ok=True)
        os.makedirs('uploads/photos', exist_ok=True)
        os.makedirs('documents', exist_ok=True)
        os.makedirs('models', exist_ok=True)
        print("✅ Directorios creados")
    except Exception as e:
        print(f"⚠️  Error creando directorios: {e}")
    
    return app

# Rutas básicas
def setup_routes(app):
    """Configurar rutas básicas"""
    
    @app.route('/')
    def index():
        """Página principal"""
        try:
            return render_template('index.html')
        except Exception as e:
            return jsonify({
                'message': 'Plataforma de Vinculación UNRC',
                'status': 'running',
                'error': str(e)
            })
    
    @app.route('/api/health')
    def health_check():
        """Verificación de salud de la API"""
        return jsonify({
            'status': 'healthy',
            'message': 'Plataforma de Vinculación UNRC API',
            'version': '1.0.0',
            'timestamp': datetime.utcnow().isoformat(),
            'python_version': sys.version,
            'features': {
                'database': 'SQLite',
                'authentication': 'JWT',
                'ai_matching': matching_engine is not None,
                'document_generation': True
            }
        })
    
    @app.route('/api/init', methods=['POST'])
    def initialize_system():
        """Inicializar sistema con datos de ejemplo"""
        try:
            # Verificar si ya hay datos
            if User.query.count() > 0:
                return jsonify({'message': 'Sistema ya inicializado'}), 200
            
            # Crear usuario administrador
            admin_user = User(
                email='admin@unrc.edu.mx',
                role='admin'
            )
            admin_user.set_password('Admin123')
            db.session.add(admin_user)
            
            # Crear estudiantes de ejemplo
            students_data = [
                {
                    'email': 'estudiante1@unrc.edu.mx',
                    'password': 'Estudiante123',
                    'first_name': 'Juan',
                    'last_name': 'Pérez',
                    'student_id': '2021001',
                    'career': 'Ingeniería en Sistemas',
                    'semester': 7,
                    'credits_percentage': 85.0,
                    'gpa': 8.5,
                    'skills_technical': ['Python', 'JavaScript', 'SQL', 'Git'],
                    'skills_soft': ['Trabajo en equipo', 'Comunicación', 'Liderazgo'],
                    'interests': ['Desarrollo web', 'Inteligencia artificial', 'Ciberseguridad'],
                    'languages': ['Español', 'Inglés'],
                    'experience': ['Proyectos universitarios', 'Freelance']
                }
            ]
            
            for student_data in students_data:
                user = User(
                    email=student_data['email'],
                    role='student'
                )
                user.set_password(student_data['password'])
                db.session.add(user)
                db.session.flush()
                
                student = Student(
                    user_id=user.id,
                    first_name=student_data['first_name'],
                    last_name=student_data['last_name'],
                    student_id=student_data['student_id'],
                    career=student_data['career'],
                    semester=student_data['semester'],
                    credits_percentage=student_data['credits_percentage'],
                    gpa=student_data['gpa']
                )
                
                student.set_skills_technical(student_data['skills_technical'])
                student.set_skills_soft(student_data['skills_soft'])
                student.set_interests(student_data['interests'])
                student.set_languages(student_data['languages'])
                student.set_experience(student_data['experience'])
                student.profile_completed = True
                
                db.session.add(student)
            
            db.session.commit()
            
            return jsonify({
                'message': 'Sistema inicializado exitosamente',
                'data': {
                    'admin_created': True,
                    'students_created': len(students_data)
                }
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error inicializando sistema: {str(e)}'}), 500

# Crear aplicación
app = create_app()

if app is None:
    print("❌ Error: No se pudo crear la aplicación")
    sys.exit(1)

# Configurar rutas
setup_routes(app)

# Manejo de errores
@app.errorhandler(404)
def not_found(error):
    """Manejo de errores 404"""
    return jsonify({'error': 'Endpoint no encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Manejo de errores 500"""
    try:
        db.session.rollback()
    except:
        pass
    return jsonify({'error': 'Error interno del servidor'}), 500

if __name__ == '__main__':
    print("\n" + "="*50)
    print("   PLATAFORMA DE VINCULACIÓN UNRC")
    print("="*50)
    
    try:
        with app.app_context():
            # Crear tablas si no existen
            db.create_all()
            print("✅ Tablas de base de datos creadas")
            
            # Cargar modelo de IA si existe
            if matching_engine:
                matching_engine.load_model()
                print("✅ Motor de IA cargado")
    except Exception as e:
        print(f"⚠️  Error inicializando base de datos: {e}")
    
    # Ejecutar aplicación
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    
    print(f"\n🚀 Iniciando servidor en puerto {port}")
    print(f"📱 URL: http://localhost:{port}")
    print(f"🔧 Modo debug: {debug}")
    print("\n" + "="*50)
    
    try:
        app.run(host='0.0.0.0', port=port, debug=debug)
    except Exception as e:
        print(f"❌ Error ejecutando aplicación: {e}")
        print("\n💡 Soluciones:")
        print("1. Verificar que el puerto 5000 esté libre")
        print("2. Ejecutar: pip install -r requirements.txt")
        print("3. Verificar que todas las dependencias estén instaladas")
        sys.exit(1)
