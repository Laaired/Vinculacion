# Alternativa a SQLAlchemy - SQLite Nativo
# Plataforma de Vinculación UNRC

import sqlite3
import json
import hashlib
from datetime import datetime, date
from typing import Optional, List, Dict, Any
import os

class DatabaseManager:
    """Gestor de base de datos usando SQLite nativo"""
    
    def __init__(self, db_path: str = "vinculacion_unrc.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializar base de datos y crear tablas"""
        try:
            with sqlite3.connect(self.db_path) as conn:
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
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
                        birth_date DATE,
                        career TEXT NOT NULL,
                        semester INTEGER NOT NULL,
                        credits_percentage REAL DEFAULT 0.0,
                        gpa REAL DEFAULT 0.0,
                        skills_technical TEXT,
                        skills_soft TEXT,
                        interests TEXT,
                        languages TEXT,
                        experience TEXT,
                        cv_path TEXT,
                        photo_path TEXT,
                        is_available BOOLEAN DEFAULT 1,
                        profile_completed BOOLEAN DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
                        size TEXT,
                        website TEXT,
                        contact_name TEXT NOT NULL,
                        contact_position TEXT,
                        phone TEXT,
                        address TEXT,
                        description TEXT,
                        mission TEXT,
                        vision TEXT,
                        is_verified BOOLEAN DEFAULT 0,
                        is_active BOOLEAN DEFAULT 1,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
                        start_date DATE,
                        end_date DATE,
                        application_deadline DATE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
                        additional_info TEXT,
                        match_score REAL,
                        company_notes TEXT,
                        admin_notes TEXT,
                        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        reviewed_at TIMESTAMP,
                        responded_at TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (student_id) REFERENCES students (id),
                        FOREIGN KEY (opportunity_id) REFERENCES opportunities (id)
                    )
                ''')
                
                # Tabla de documentos
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS documents (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        document_type TEXT NOT NULL,
                        title TEXT NOT NULL,
                        description TEXT,
                        file_path TEXT NOT NULL,
                        file_size INTEGER,
                        mime_type TEXT,
                        student_id INTEGER,
                        company_id INTEGER,
                        generated_by TEXT,
                        metadata TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (student_id) REFERENCES students (id),
                        FOREIGN KEY (company_id) REFERENCES companies (id)
                    )
                ''')
                
                # Tabla de KPIs
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS kpis (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        description TEXT,
                        category TEXT NOT NULL,
                        current_value REAL DEFAULT 0.0,
                        target_value REAL,
                        previous_value REAL,
                        calculation_method TEXT,
                        data_source TEXT,
                        calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Tabla de OKRs
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS okrs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        objective TEXT NOT NULL,
                        description TEXT,
                        category TEXT NOT NULL,
                        target_metric TEXT NOT NULL,
                        target_value REAL NOT NULL,
                        current_value REAL DEFAULT 0.0,
                        period_start DATE NOT NULL,
                        period_end DATE NOT NULL,
                        is_active BOOLEAN DEFAULT 1,
                        completion_percentage REAL DEFAULT 0.0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                conn.commit()
                print("✅ Base de datos inicializada correctamente")
                
        except Exception as e:
            print(f"❌ Error inicializando base de datos: {e}")
            raise
    
    def get_connection(self):
        """Obtener conexión a la base de datos"""
        return sqlite3.connect(self.db_path)
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """Ejecutar consulta y retornar resultados como lista de diccionarios"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(query, params)
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            print(f"Error ejecutando consulta: {e}")
            return []
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Ejecutar consulta de actualización y retornar número de filas afectadas"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor.rowcount
        except Exception as e:
            print(f"Error ejecutando actualización: {e}")
            return 0
    
    def execute_insert(self, query: str, params: tuple = ()) -> int:
        """Ejecutar consulta de inserción y retornar ID del registro insertado"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error ejecutando inserción: {e}")
            return 0

class User:
    """Modelo de Usuario usando SQLite nativo"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def create(self, email: str, password: str, role: str) -> Optional[int]:
        """Crear nuevo usuario"""
        password_hash = self._hash_password(password)
        query = '''
            INSERT INTO users (email, password_hash, role)
            VALUES (?, ?, ?)
        '''
        return self.db.execute_insert(query, (email, password_hash, role))
    
    def get_by_email(self, email: str) -> Optional[Dict]:
        """Obtener usuario por email"""
        query = 'SELECT * FROM users WHERE email = ?'
        results = self.db.execute_query(query, (email,))
        return results[0] if results else None
    
    def get_by_id(self, user_id: int) -> Optional[Dict]:
        """Obtener usuario por ID"""
        query = 'SELECT * FROM users WHERE id = ?'
        results = self.db.execute_query(query, (user_id,))
        return results[0] if results else None
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verificar contraseña"""
        return self._hash_password(password) == password_hash
    
    def update_last_login(self, user_id: int):
        """Actualizar último login"""
        query = 'UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?'
        self.db.execute_update(query, (user_id,))
    
    def _hash_password(self, password: str) -> str:
        """Hash de contraseña usando SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def to_dict(self, user_data: Dict) -> Dict:
        """Convertir datos de usuario a diccionario"""
        return {
            'id': user_data['id'],
            'email': user_data['email'],
            'role': user_data['role'],
            'is_active': bool(user_data['is_active']),
            'created_at': user_data['created_at'],
            'last_login': user_data['last_login']
        }

class Student:
    """Modelo de Estudiante usando SQLite nativo"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def create(self, user_id: int, first_name: str, last_name: str, 
               student_id: str, career: str, semester: int, **kwargs) -> Optional[int]:
        """Crear nuevo estudiante"""
        query = '''
            INSERT INTO students (user_id, first_name, last_name, student_id, career, semester,
                                phone, birth_date, credits_percentage, gpa, skills_technical,
                                skills_soft, interests, languages, experience)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            user_id, first_name, last_name, student_id, career, semester,
            kwargs.get('phone'), kwargs.get('birth_date'), 
            kwargs.get('credits_percentage', 0.0), kwargs.get('gpa', 0.0),
            json.dumps(kwargs.get('skills_technical', [])),
            json.dumps(kwargs.get('skills_soft', [])),
            json.dumps(kwargs.get('interests', [])),
            json.dumps(kwargs.get('languages', [])),
            json.dumps(kwargs.get('experience', []))
        )
        return self.db.execute_insert(query, params)
    
    def get_by_id(self, student_id: int) -> Optional[Dict]:
        """Obtener estudiante por ID"""
        query = 'SELECT * FROM students WHERE id = ?'
        results = self.db.execute_query(query, (student_id,))
        return results[0] if results else None
    
    def get_by_user_id(self, user_id: int) -> Optional[Dict]:
        """Obtener estudiante por user_id"""
        query = 'SELECT * FROM students WHERE user_id = ?'
        results = self.db.execute_query(query, (user_id,))
        return results[0] if results else None
    
    def get_by_student_id(self, student_id: str) -> Optional[Dict]:
        """Obtener estudiante por número de estudiante"""
        query = 'SELECT * FROM students WHERE student_id = ?'
        results = self.db.execute_query(query, (student_id,))
        return results[0] if results else None
    
    def update(self, student_id: int, **kwargs) -> bool:
        """Actualizar estudiante"""
        set_clauses = []
        params = []
        
        for key, value in kwargs.items():
            if key in ['skills_technical', 'skills_soft', 'interests', 'languages', 'experience']:
                set_clauses.append(f"{key} = ?")
                params.append(json.dumps(value))
            else:
                set_clauses.append(f"{key} = ?")
                params.append(value)
        
        if not set_clauses:
            return False
        
        set_clauses.append("updated_at = CURRENT_TIMESTAMP")
        params.append(student_id)
        
        query = f"UPDATE students SET {', '.join(set_clauses)} WHERE id = ?"
        return self.db.execute_update(query, tuple(params)) > 0
    
    def get_skills_technical(self, student_data: Dict) -> List[str]:
        """Obtener habilidades técnicas"""
        return json.loads(student_data['skills_technical']) if student_data['skills_technical'] else []
    
    def get_skills_soft(self, student_data: Dict) -> List[str]:
        """Obtener habilidades blandas"""
        return json.loads(student_data['skills_soft']) if student_data['skills_soft'] else []
    
    def get_interests(self, student_data: Dict) -> List[str]:
        """Obtener intereses"""
        return json.loads(student_data['interests']) if student_data['interests'] else []
    
    def get_languages(self, student_data: Dict) -> List[str]:
        """Obtener idiomas"""
        return json.loads(student_data['languages']) if student_data['languages'] else []
    
    def get_experience(self, student_data: Dict) -> List[str]:
        """Obtener experiencia"""
        return json.loads(student_data['experience']) if student_data['experience'] else []
    
    def to_dict(self, student_data: Dict) -> Dict:
        """Convertir datos de estudiante a diccionario"""
        return {
            'id': student_data['id'],
            'user_id': student_data['user_id'],
            'first_name': student_data['first_name'],
            'last_name': student_data['last_name'],
            'student_id': student_data['student_id'],
            'phone': student_data['phone'],
            'birth_date': student_data['birth_date'],
            'career': student_data['career'],
            'semester': student_data['semester'],
            'credits_percentage': student_data['credits_percentage'],
            'gpa': student_data['gpa'],
            'skills_technical': self.get_skills_technical(student_data),
            'skills_soft': self.get_skills_soft(student_data),
            'interests': self.get_interests(student_data),
            'languages': self.get_languages(student_data),
            'experience': self.get_experience(student_data),
            'cv_path': student_data['cv_path'],
            'photo_path': student_data['photo_path'],
            'is_available': bool(student_data['is_available']),
            'profile_completed': bool(student_data['profile_completed']),
            'created_at': student_data['created_at'],
            'updated_at': student_data['updated_at']
        }

class Company:
    """Modelo de Empresa usando SQLite nativo"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def create(self, user_id: int, company_name: str, rfc: str, 
               industry: str, contact_name: str, **kwargs) -> Optional[int]:
        """Crear nueva empresa"""
        query = '''
            INSERT INTO companies (user_id, company_name, rfc, industry, contact_name,
                                 size, website, contact_position, phone, address,
                                 description, mission, vision)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            user_id, company_name, rfc, industry, contact_name,
            kwargs.get('size'), kwargs.get('website'), kwargs.get('contact_position'),
            kwargs.get('phone'), kwargs.get('address'), kwargs.get('description'),
            kwargs.get('mission'), kwargs.get('vision')
        )
        return self.db.execute_insert(query, params)
    
    def get_by_id(self, company_id: int) -> Optional[Dict]:
        """Obtener empresa por ID"""
        query = 'SELECT * FROM companies WHERE id = ?'
        results = self.db.execute_query(query, (company_id,))
        return results[0] if results else None
    
    def get_by_user_id(self, user_id: int) -> Optional[Dict]:
        """Obtener empresa por user_id"""
        query = 'SELECT * FROM companies WHERE user_id = ?'
        results = self.db.execute_query(query, (user_id,))
        return results[0] if results else None
    
    def get_by_rfc(self, rfc: str) -> Optional[Dict]:
        """Obtener empresa por RFC"""
        query = 'SELECT * FROM companies WHERE rfc = ?'
        results = self.db.execute_query(query, (rfc,))
        return results[0] if results else None
    
    def update(self, company_id: int, **kwargs) -> bool:
        """Actualizar empresa"""
        set_clauses = []
        params = []
        
        for key, value in kwargs.items():
            set_clauses.append(f"{key} = ?")
            params.append(value)
        
        if not set_clauses:
            return False
        
        set_clauses.append("updated_at = CURRENT_TIMESTAMP")
        params.append(company_id)
        
        query = f"UPDATE companies SET {', '.join(set_clauses)} WHERE id = ?"
        return self.db.execute_update(query, tuple(params)) > 0
    
    def to_dict(self, company_data: Dict) -> Dict:
        """Convertir datos de empresa a diccionario"""
        return {
            'id': company_data['id'],
            'user_id': company_data['user_id'],
            'company_name': company_data['company_name'],
            'rfc': company_data['rfc'],
            'industry': company_data['industry'],
            'size': company_data['size'],
            'website': company_data['website'],
            'contact_name': company_data['contact_name'],
            'contact_position': company_data['contact_position'],
            'phone': company_data['phone'],
            'address': company_data['address'],
            'description': company_data['description'],
            'mission': company_data['mission'],
            'vision': company_data['vision'],
            'is_verified': bool(company_data['is_verified']),
            'is_active': bool(company_data['is_active']),
            'created_at': company_data['created_at'],
            'updated_at': company_data['updated_at']
        }

# Instancia global de la base de datos
db_manager = DatabaseManager()
user_model = User(db_manager)
student_model = Student(db_manager)
company_model = Company(db_manager)
