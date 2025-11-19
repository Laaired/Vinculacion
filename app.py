from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
from flask_migrate import Migrate
import os
from datetime import timedelta
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Importar modelos y rutas
from models import db, User, Student, Company, Opportunity, Application, Document, KPI, OKR
from routes.auth_routes import auth_bp, admin_required
from routes.student_routes import student_bp
from routes.company_routes import company_bp
from routes.admin_routes import admin_bp
from routes.document_routes import document_bp
from routes.analytics_routes import analytics_bp
from ai_matching import matching_engine

def create_app():
    """Crear y configurar la aplicación Flask"""
    app = Flask(__name__)
    
    # Configuración
    app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'vinculacion_unrc_secret_key')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'vinculacion_unrc_secret_key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
    
    # Base de datos
    database_url = os.getenv('DATABASE_URL', 'sqlite:///vinculacion_unrc.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configuración de archivos
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Configuración de email
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', '')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', '')
    
    # Inicializar extensiones
    db.init_app(app)
    jwt = JWTManager(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    mail = Mail(app)
    migrate = Migrate(app, db)
    
    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(document_bp)
    app.register_blueprint(analytics_bp)
    
    # Crear directorios necesarios
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('uploads/cvs', exist_ok=True)
    os.makedirs('uploads/photos', exist_ok=True)
    os.makedirs('documents', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    
    return app

app = create_app()

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/login')
def login_page():
    """Página de login"""
    return render_template('login.html')

@app.route('/register')
def register_page():
    """Página de registro"""
    return render_template('register.html')

@app.route('/dashboard')
@admin_required
def dashboard():
    """Dashboard principal - Solo para administradores"""
    return render_template('dashboard.html')

@app.route('/student/profile')
def student_profile():
    """Perfil del estudiante"""
    return render_template('student_profile.html')

@app.route('/company/profile')
def company_profile():
    """Perfil de la empresa"""
    return render_template('company_profile.html')

@app.route('/company/applicants')
def company_applicants():
    """Vista de perfiles de postulantes"""
    return render_template('company_applicants.html')

@app.route('/admin')
def admin_dashboard():
    """Dashboard de administrador"""
    return render_template('admin_dashboard.html')

@app.route('/opportunities')
def opportunities():
    """Página de oportunidades"""
    return render_template('opportunities.html')

@app.route('/applications')
def applications():
    """Página de aplicaciones"""
    return render_template('applications.html')

@app.route('/analytics')
def analytics():
    """Página de analytics"""
    return render_template('analytics.html')

@app.route('/api/health')
def health_check():
    """Verificación de salud de la API"""
    return jsonify({
        'status': 'healthy',
        'message': 'Plataforma de Vinculación UNRC API',
        'version': '1.0.0',
        'timestamp': datetime.utcnow().isoformat()
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
            },
            {
                'email': 'estudiante2@unrc.edu.mx',
                'password': 'Estudiante123',
                'first_name': 'María',
                'last_name': 'González',
                'student_id': '2021002',
                'career': 'Administración',
                'semester': 8,
                'credits_percentage': 90.0,
                'gpa': 9.0,
                'skills_technical': ['Excel', 'PowerBI', 'SAP', 'Project Management'],
                'skills_soft': ['Gestión de proyectos', 'Análisis de datos', 'Negociación'],
                'interests': ['Consultoría', 'Estrategia empresarial', 'Innovación'],
                'languages': ['Español', 'Inglés', 'Francés'],
                'experience': ['Prácticas en empresa', 'Voluntariado']
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
        
        # Crear empresas de ejemplo
        companies_data = [
            {
                'email': 'empresa1@empresa.com',
                'password': 'Empresa123',
                'company_name': 'Tech Solutions México',
                'rfc': 'TSM123456789',
                'industry': 'Tecnología',
                'size': 'medium',
                'contact_name': 'Carlos Rodríguez',
                'contact_position': 'Director de Recursos Humanos',
                'phone': '555-123-4567',
                'address': 'Av. Tecnología 123, Ciudad de México',
                'description': 'Empresa líder en desarrollo de software y soluciones tecnológicas',
                'mission': 'Transformar el mundo a través de la tecnología',
                'vision': 'Ser la empresa tecnológica más innovadora de México'
            },
            {
                'email': 'empresa2@empresa.com',
                'password': 'Empresa123',
                'company_name': 'Consultoría Empresarial ABC',
                'rfc': 'CEA987654321',
                'industry': 'Consultoría',
                'size': 'large',
                'contact_name': 'Ana Martínez',
                'contact_position': 'Gerente de Talento',
                'phone': '555-987-6543',
                'address': 'Paseo de la Reforma 456, Ciudad de México',
                'description': 'Consultoría especializada en estrategia empresarial y gestión de talento',
                'mission': 'Impulsar el crecimiento de las empresas mexicanas',
                'vision': 'Ser la consultoría de referencia en América Latina'
            }
        ]
        
        for company_data in companies_data:
            user = User(
                email=company_data['email'],
                role='company'
            )
            user.set_password(company_data['password'])
            db.session.add(user)
            db.session.flush()
            
            company = Company(
                user_id=user.id,
                company_name=company_data['company_name'],
                rfc=company_data['rfc'],
                industry=company_data['industry'],
                size=company_data['size'],
                contact_name=company_data['contact_name'],
                contact_position=company_data['contact_position'],
                phone=company_data['phone'],
                address=company_data['address'],
                description=company_data['description'],
                mission=company_data['mission'],
                vision=company_data['vision'],
                is_verified=True
            )
            
            db.session.add(company)
        
        db.session.commit()
        
        # Crear oportunidades de ejemplo
        opportunities_data = [
            {
                'company_id': 2,  # Tech Solutions México
                'title': 'Desarrollador Full Stack',
                'description': 'Desarrollo de aplicaciones web usando tecnologías modernas',
                'type': 'internship',
                'required_skills': ['Python', 'JavaScript', 'React', 'Node.js'],
                'required_semester': 6,
                'required_careers': ['Ingeniería en Sistemas', 'Ingeniería en Computación'],
                'required_credits': 70.0,
                'duration_months': 6,
                'hours_per_week': 40,
                'salary': 15000.0,
                'benefits': ['Seguro médico', 'Capacitación', 'Horario flexible'],
                'location': 'Ciudad de México',
                'work_mode': 'hybrid',
                'available_positions': 2
            },
            {
                'company_id': 3,  # Consultoría Empresarial ABC
                'title': 'Consultor Junior',
                'description': 'Apoyo en proyectos de consultoría estratégica',
                'type': 'social_service',
                'required_skills': ['Excel', 'PowerBI', 'Análisis de datos'],
                'required_semester': 7,
                'required_careers': ['Administración', 'Contaduría', 'Economía'],
                'required_credits': 80.0,
                'duration_months': 4,
                'hours_per_week': 30,
                'salary': 0.0,
                'benefits': ['Experiencia profesional', 'Certificación', 'Networking'],
                'location': 'Ciudad de México',
                'work_mode': 'onsite',
                'available_positions': 3
            }
        ]
        
        for opp_data in opportunities_data:
            opportunity = Opportunity(
                company_id=opp_data['company_id'],
                title=opp_data['title'],
                description=opp_data['description'],
                type=opp_data['type'],
                required_semester=opp_data['required_semester'],
                required_careers=opp_data['required_careers'],
                required_credits=opp_data['required_credits'],
                duration_months=opp_data['duration_months'],
                hours_per_week=opp_data['hours_per_week'],
                salary=opp_data['salary'],
                benefits=opp_data['benefits'],
                location=opp_data['location'],
                work_mode=opp_data['work_mode'],
                available_positions=opp_data['available_positions']
            )
            
            opportunity.set_required_skills(opp_data['required_skills'])
            opportunity.set_required_careers(opp_data['required_careers'])
            opportunity.set_benefits(opp_data['benefits'])
            
            db.session.add(opportunity)
        
        db.session.commit()
        
        # Inicializar OKRs
        from routes.analytics_routes import OKRManager
        OKRManager.create_default_okrs()
        
        return jsonify({
            'message': 'Sistema inicializado exitosamente',
            'data': {
                'admin_created': True,
                'students_created': len(students_data),
                'companies_created': len(companies_data),
                'opportunities_created': len(opportunities_data)
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error inicializando sistema: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(error):
    """Manejo de errores 404"""
    return jsonify({'error': 'Endpoint no encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Manejo de errores 500"""
    db.session.rollback()
    return jsonify({'error': 'Error interno del servidor'}), 500

if __name__ == '__main__':
    with app.app_context():
        # Crear tablas si no existen
        db.create_all()
        
        # Cargar modelo de IA si existe
        matching_engine.load_model()
    
    # Ejecutar aplicación
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    
    app.run(host='0.0.0.0', port=port, debug=debug)
