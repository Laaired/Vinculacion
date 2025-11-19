# Aplicación Flask con SQLite Nativo - Plataforma de Vinculación UNRC
# Sin dependencias problemáticas como SQLAlchemy

import os
import sys
import json
import hashlib
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
import sqlite3

# Verificar Python version
if sys.version_info < (3, 8):
    print("❌ Error: Se requiere Python 3.8 o superior")
    sys.exit(1)

print(f"✅ Python version: {sys.version}")

# Crear aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'vinculacion_unrc_secret_key_2024'
app.config['JWT_SECRET_KEY'] = 'vinculacion_unrc_secret_key_2024'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Inicializar extensiones
jwt = JWTManager(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configuración de base de datos
DB_PATH = 'vinculacion_unrc.db'

def init_database():
    """Inicializar base de datos SQLite"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            
            # Tabla de usuarios
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('student', 'company', 'admin')),
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP
                )
            ''')
            
            # Tabla de estudiantes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    student_id TEXT UNIQUE NOT NULL,
                    phone TEXT,
                    career TEXT NOT NULL,
                    semester INTEGER NOT NULL,
                    credits_percentage REAL DEFAULT 0.0,
                    gpa REAL DEFAULT 0.0,
                    skills_technical TEXT,
                    skills_soft TEXT,
                    interests TEXT,
                    languages TEXT,
                    experience TEXT,
                    is_available BOOLEAN DEFAULT 1,
                    profile_completed BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Tabla de empresas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS companies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    company_name TEXT NOT NULL,
                    rfc TEXT UNIQUE NOT NULL,
                    industry TEXT NOT NULL,
                    contact_name TEXT NOT NULL,
                    phone TEXT,
                    address TEXT,
                    description TEXT,
                    is_verified BOOLEAN DEFAULT 0,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Tabla de oportunidades
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS opportunities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    type TEXT NOT NULL CHECK(type IN ('internship', 'social_service', 'job')),
                    required_skills TEXT,
                    required_semester INTEGER,
                    required_careers TEXT,
                    required_credits REAL DEFAULT 0.0,
                    duration_months INTEGER,
                    hours_per_week INTEGER,
                    salary REAL,
                    benefits TEXT,
                    location TEXT,
                    work_mode TEXT,
                    is_active BOOLEAN DEFAULT 1,
                    available_positions INTEGER DEFAULT 1,
                    filled_positions INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (company_id) REFERENCES companies (id)
                )
            ''')
            
            # Tabla de aplicaciones
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    opportunity_id INTEGER NOT NULL,
                    status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'reviewed', 'accepted', 'rejected')),
                    cover_letter TEXT,
                    match_score REAL,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    reviewed_at TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES students (id),
                    FOREIGN KEY (opportunity_id) REFERENCES opportunities (id)
                )
            ''')
            
            conn.commit()
            print("✅ Base de datos SQLite inicializada correctamente")
            
    except Exception as e:
        print(f"❌ Error inicializando base de datos: {e}")
        raise

def hash_password(password: str) -> str:
    """Hash de contraseña usando SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, password_hash: str) -> bool:
    """Verificar contraseña"""
    return hash_password(password) == password_hash

def execute_query(query: str, params: tuple = ()) -> list:
    """Ejecutar consulta y retornar resultados"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    except Exception as e:
        print(f"Error ejecutando consulta: {e}")
        return []

def execute_update(query: str, params: tuple = ()) -> int:
    """Ejecutar consulta de actualización"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount
    except Exception as e:
        print(f"Error ejecutando actualización: {e}")
        return 0

def execute_insert(query: str, params: tuple = ()) -> int:
    """Ejecutar consulta de inserción"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid
    except Exception as e:
        print(f"Error ejecutando inserción: {e}")
        return 0

# Rutas de la API
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
        'database': 'SQLite Native',
        'features': {
            'authentication': 'JWT',
            'database': 'SQLite Native',
            'ai_matching': 'Basic',
            'document_generation': 'Basic'
        }
    })

@app.route('/api/auth/register/student', methods=['POST'])
def register_student():
    """Registro de estudiante"""
    try:
        data = request.get_json()
        
        # Validaciones básicas
        required_fields = ['email', 'password', 'first_name', 'last_name', 'student_id', 'career', 'semester']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'El campo {field} es requerido'}), 400
        
        # Verificar si el email ya existe
        existing_user = execute_query('SELECT id FROM users WHERE email = ?', (data['email'],))
        if existing_user:
            return jsonify({'error': 'El email ya está registrado'}), 409
        
        # Verificar si el student_id ya existe
        existing_student = execute_query('SELECT id FROM students WHERE student_id = ?', (data['student_id'],))
        if existing_student:
            return jsonify({'error': 'El número de estudiante ya está registrado'}), 409
        
        # Crear usuario
        user_id = execute_insert(
            'INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)',
            (data['email'], hash_password(data['password']), 'student')
        )
        
        if not user_id:
            return jsonify({'error': 'Error creando usuario'}), 500
        
        # Crear estudiante
        student_id = execute_insert(
            '''INSERT INTO students (user_id, first_name, last_name, student_id, career, semester,
                                   phone, credits_percentage, gpa, skills_technical, skills_soft,
                                   interests, languages, experience)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (user_id, data['first_name'], data['last_name'], data['student_id'], data['career'], data['semester'],
             data.get('phone'), data.get('credits_percentage', 0.0), data.get('gpa', 0.0),
             json.dumps(data.get('skills_technical', [])), json.dumps(data.get('skills_soft', [])),
             json.dumps(data.get('interests', [])), json.dumps(data.get('languages', [])),
             json.dumps(data.get('experience', [])))
        )
        
        if not student_id:
            return jsonify({'error': 'Error creando estudiante'}), 500
        
        # Generar token
        token = create_access_token(identity=user_id)
        
        return jsonify({
            'message': 'Estudiante registrado exitosamente',
            'token': token,
            'user_id': user_id,
            'student_id': student_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Error en el registro: {str(e)}'}), 500

@app.route('/api/auth/register/company', methods=['POST'])
def register_company():
    """Registro de empresa"""
    try:
        data = request.get_json()
        
        # Validaciones básicas
        required_fields = ['email', 'password', 'company_name', 'rfc', 'industry', 'contact_name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'El campo {field} es requerido'}), 400
        
        # Verificar si el email ya existe
        existing_user = execute_query('SELECT id FROM users WHERE email = ?', (data['email'],))
        if existing_user:
            return jsonify({'error': 'El email ya está registrado'}), 409
        
        # Verificar si el RFC ya existe
        existing_company = execute_query('SELECT id FROM companies WHERE rfc = ?', (data['rfc'],))
        if existing_company:
            return jsonify({'error': 'El RFC ya está registrado'}), 409
        
        # Crear usuario
        user_id = execute_insert(
            'INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)',
            (data['email'], hash_password(data['password']), 'company')
        )
        
        if not user_id:
            return jsonify({'error': 'Error creando usuario'}), 500
        
        # Crear empresa
        company_id = execute_insert(
            '''INSERT INTO companies (user_id, company_name, rfc, industry, contact_name,
                                    phone, address, description)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (user_id, data['company_name'], data['rfc'], data['industry'], data['contact_name'],
             data.get('phone'), data.get('address'), data.get('description'))
        )
        
        if not company_id:
            return jsonify({'error': 'Error creando empresa'}), 500
        
        # Generar token
        token = create_access_token(identity=user_id)
        
        return jsonify({
            'message': 'Empresa registrada exitosamente',
            'token': token,
            'user_id': user_id,
            'company_id': company_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Error en el registro: {str(e)}'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Inicio de sesión"""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email y contraseña son requeridos'}), 400
        
        # Buscar usuario
        users = execute_query('SELECT * FROM users WHERE email = ?', (data['email'],))
        
        if not users or not verify_password(data['password'], users[0]['password_hash']):
            return jsonify({'error': 'Credenciales inválidas'}), 401
        
        user = users[0]
        
        if not user['is_active']:
            return jsonify({'error': 'Usuario inactivo'}), 403
        
        # Actualizar último login
        execute_update('UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?', (user['id'],))
        
        # Generar token
        token = create_access_token(identity=user['id'])
        
        # Obtener perfil según el rol
        profile = None
        if user['role'] == 'student':
            students = execute_query('SELECT * FROM students WHERE user_id = ?', (user['id'],))
            if students:
                student = students[0]
                profile = {
                    'id': student['id'],
                    'first_name': student['first_name'],
                    'last_name': student['last_name'],
                    'student_id': student['student_id'],
                    'career': student['career'],
                    'semester': student['semester'],
                    'credits_percentage': student['credits_percentage'],
                    'gpa': student['gpa']
                }
        elif user['role'] == 'company':
            companies = execute_query('SELECT * FROM companies WHERE user_id = ?', (user['id'],))
            if companies:
                company = companies[0]
                profile = {
                    'id': company['id'],
                    'company_name': company['company_name'],
                    'rfc': company['rfc'],
                    'industry': company['industry'],
                    'contact_name': company['contact_name']
                }
        
        return jsonify({
            'message': 'Inicio de sesión exitoso',
            'token': token,
            'user': {
                'id': user['id'],
                'email': user['email'],
                'role': user['role'],
                'is_active': bool(user['is_active'])
            },
            'profile': profile
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el inicio de sesión: {str(e)}'}), 500

@app.route('/api/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Obtener perfil del usuario autenticado"""
    try:
        user_id = get_jwt_identity()
        users = execute_query('SELECT * FROM users WHERE id = ?', (user_id,))
        
        if not users:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        user = users[0]
        
        # Obtener perfil según el rol
        profile = None
        if user['role'] == 'student':
            students = execute_query('SELECT * FROM students WHERE user_id = ?', (user_id,))
            if students:
                student = students[0]
                profile = {
                    'id': student['id'],
                    'first_name': student['first_name'],
                    'last_name': student['last_name'],
                    'student_id': student['student_id'],
                    'career': student['career'],
                    'semester': student['semester'],
                    'credits_percentage': student['credits_percentage'],
                    'gpa': student['gpa'],
                    'skills_technical': json.loads(student['skills_technical']) if student['skills_technical'] else [],
                    'skills_soft': json.loads(student['skills_soft']) if student['skills_soft'] else [],
                    'interests': json.loads(student['interests']) if student['interests'] else [],
                    'languages': json.loads(student['languages']) if student['languages'] else [],
                    'experience': json.loads(student['experience']) if student['experience'] else []
                }
        elif user['role'] == 'company':
            companies = execute_query('SELECT * FROM companies WHERE user_id = ?', (user_id,))
            if companies:
                company = companies[0]
                profile = {
                    'id': company['id'],
                    'company_name': company['company_name'],
                    'rfc': company['rfc'],
                    'industry': company['industry'],
                    'contact_name': company['contact_name'],
                    'phone': company['phone'],
                    'address': company['address'],
                    'description': company['description']
                }
        
        return jsonify({
            'user': {
                'id': user['id'],
                'email': user['email'],
                'role': user['role'],
                'is_active': bool(user['is_active'])
            },
            'profile': profile
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error al obtener perfil: {str(e)}'}), 500

@app.route('/api/init', methods=['POST'])
def initialize_system():
    """Inicializar sistema con datos de ejemplo"""
    try:
        # Verificar si ya hay datos
        users = execute_query('SELECT COUNT(*) as count FROM users')
        if users[0]['count'] > 0:
            return jsonify({'message': 'Sistema ya inicializado'}), 200
        
        # Crear usuario administrador
        admin_id = execute_insert(
            'INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)',
            ('admin@unrc.edu.mx', hash_password('Admin123'), 'admin')
        )
        
        # Crear estudiante de ejemplo
        student_user_id = execute_insert(
            'INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)',
            ('estudiante1@unrc.edu.mx', hash_password('Estudiante123'), 'student')
        )
        
        student_id = execute_insert(
            '''INSERT INTO students (user_id, first_name, last_name, student_id, career, semester,
                                   credits_percentage, gpa, skills_technical, skills_soft,
                                   interests, languages, experience)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (student_user_id, 'Juan', 'Pérez', '2021001', 'Ingeniería en Sistemas', 7,
             85.0, 8.5, json.dumps(['Python', 'JavaScript', 'SQL']),
             json.dumps(['Trabajo en equipo', 'Comunicación']),
             json.dumps(['Desarrollo web', 'IA']), json.dumps(['Español', 'Inglés']),
             json.dumps(['Proyectos universitarios']))
        )
        
        # Crear empresa de ejemplo
        company_user_id = execute_insert(
            'INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)',
            ('empresa1@empresa.com', hash_password('Empresa123'), 'company')
        )
        
        company_id = execute_insert(
            '''INSERT INTO companies (user_id, company_name, rfc, industry, contact_name,
                                    description)
               VALUES (?, ?, ?, ?, ?, ?)''',
            (company_user_id, 'Tech Solutions México', 'TSM123456789', 'Tecnología',
             'Carlos Rodríguez', 'Empresa líder en desarrollo de software')
        )
        
        # Crear oportunidad de ejemplo
        opportunity_id = execute_insert(
            '''INSERT INTO opportunities (company_id, title, description, type,
                                        required_skills, required_semester, required_careers,
                                        duration_months, hours_per_week, salary, location)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (company_id, 'Desarrollador Full Stack', 'Desarrollo de aplicaciones web',
             'internship', json.dumps(['Python', 'JavaScript', 'React']), 6,
             json.dumps(['Ingeniería en Sistemas']), 6, 40, 15000.0, 'Ciudad de México')
        )
        
        return jsonify({
            'message': 'Sistema inicializado exitosamente',
            'data': {
                'admin_created': True,
                'student_created': True,
                'company_created': True,
                'opportunity_created': True
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Error inicializando sistema: {str(e)}'}), 500

@app.route('/api/students/recommendations/<int:student_id>', methods=['GET'])
@jwt_required()
def get_recommendations(student_id):
    """Obtener recomendaciones de oportunidades para el estudiante"""
    try:
        current_user_id = get_jwt_identity()
        
        # Verificar permisos
        users = execute_query('SELECT role FROM users WHERE id = ?', (current_user_id,))
        if not users or users[0]['role'] not in ['admin'] and current_user_id != student_id:
            return jsonify({'error': 'No tienes permisos para ver recomendaciones'}), 403
        
        # Obtener estudiante
        students = execute_query('SELECT * FROM students WHERE id = ?', (student_id,))
        if not students:
            return jsonify({'error': 'Estudiante no encontrado'}), 404
        
        student = students[0]
        
        # Obtener oportunidades activas
        opportunities = execute_query('SELECT * FROM opportunities WHERE is_active = 1')
        
        # Filtrar oportunidades según perfil del estudiante
        recommendations = []
        for opp in opportunities:
            # Verificar requisitos básicos
            if opp['required_semester'] and student['semester'] < opp['required_semester']:
                continue
            if opp['required_credits'] and student['credits_percentage'] < opp['required_credits']:
                continue
            
            # Calcular score de compatibilidad básico
            match_score = 0.5  # Score básico
            
            # Ajustar score según habilidades
            if opp['required_skills']:
                required_skills = json.loads(opp['required_skills'])
                student_skills = json.loads(student['skills_technical']) if student['skills_technical'] else []
                common_skills = set(student_skills).intersection(set(required_skills))
                if required_skills:
                    match_score += len(common_skills) / len(required_skills) * 0.3
            
            if match_score >= 0.3:  # Solo mostrar oportunidades con score >= 30%
                recommendations.append({
                    'opportunity': {
                        'id': opp['id'],
                        'title': opp['title'],
                        'description': opp['description'],
                        'type': opp['type'],
                        'duration_months': opp['duration_months'],
                        'hours_per_week': opp['hours_per_week'],
                        'salary': opp['salary'],
                        'location': opp['location']
                    },
                    'match_score': round(match_score, 2)
                })
        
        # Ordenar por score de compatibilidad
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        
        return jsonify({
            'recommendations': recommendations[:10],  # Top 10
            'total': len(recommendations)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error al obtener recomendaciones: {str(e)}'}), 500

@app.route('/api/companies/opportunities', methods=['GET'])
@jwt_required()
def get_company_opportunities():
    """Obtener oportunidades de la empresa"""
    try:
        current_user_id = get_jwt_identity()
        
        # Verificar que es empresa
        users = execute_query('SELECT role FROM users WHERE id = ?', (current_user_id,))
        if not users or users[0]['role'] != 'company':
            return jsonify({'error': 'Acceso denegado'}), 403
        
        # Obtener empresa
        companies = execute_query('SELECT id FROM companies WHERE user_id = ?', (current_user_id,))
        if not companies:
            return jsonify({'error': 'Perfil de empresa no encontrado'}), 404
        
        company_id = companies[0]['id']
        
        # Obtener oportunidades
        opportunities = execute_query('SELECT * FROM opportunities WHERE company_id = ?', (company_id,))
        
        return jsonify({
            'opportunities': opportunities,
            'total': len(opportunities)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error al obtener oportunidades: {str(e)}'}), 500

@app.route('/api/analytics/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard():
    """Obtener datos del dashboard principal"""
    try:
        current_user_id = get_jwt_identity()
        
        # Verificar que es admin
        users = execute_query('SELECT role FROM users WHERE id = ?', (current_user_id,))
        if not users or users[0]['role'] != 'admin':
            return jsonify({'error': 'Acceso denegado - Se requieren permisos de administrador'}), 403
        
        # Estadísticas generales
        total_students = execute_query('SELECT COUNT(*) as count FROM students')[0]['count']
        total_companies = execute_query('SELECT COUNT(*) as count FROM companies')[0]['count']
        total_opportunities = execute_query('SELECT COUNT(*) as count FROM opportunities')[0]['count']
        total_applications = execute_query('SELECT COUNT(*) as count FROM applications')[0]['count']
        
        # Aplicaciones por estado
        applications_by_status = execute_query('''
            SELECT status, COUNT(*) as count 
            FROM applications 
            GROUP BY status
        ''')
        
        # Estudiantes por carrera
        students_by_career = execute_query('''
            SELECT career, COUNT(*) as count 
            FROM students 
            GROUP BY career 
            ORDER BY count DESC 
            LIMIT 10
        ''')
        
        return jsonify({
            'overview': {
                'total_students': total_students,
                'total_companies': total_companies,
                'total_opportunities': total_opportunities,
                'total_applications': total_applications
            },
            'applications_by_status': {row['status']: row['count'] for row in applications_by_status},
            'students_by_career': {row['career']: row['count'] for row in students_by_career}
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error al obtener dashboard: {str(e)}'}), 500

# Manejo de errores
@app.errorhandler(404)
def not_found(error):
    """Manejo de errores 404"""
    return jsonify({'error': 'Endpoint no encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Manejo de errores 500"""
    return jsonify({'error': 'Error interno del servidor'}), 500

if __name__ == '__main__':
    print("\n" + "="*50)
    print("   PLATAFORMA DE VINCULACIÓN UNRC")
    print("   Versión SQLite Nativo")
    print("="*50)
    
    # Inicializar base de datos
    init_database()
    
    # Crear directorios necesarios
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('uploads/cvs', exist_ok=True)
    os.makedirs('uploads/photos', exist_ok=True)
    os.makedirs('documents', exist_ok=True)
    
    print("✅ Directorios creados")
    print("✅ Base de datos inicializada")
    print("✅ JWT configurado")
    print("✅ CORS configurado")
    
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
        sys.exit(1)
