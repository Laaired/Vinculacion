from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import json

db = SQLAlchemy()

class User(db.Model):
    """Modelo base para todos los usuarios del sistema"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'student', 'company', 'admin'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relaciones polimórficas
    student_profile = db.relationship('Student', backref='user', uselist=False, cascade='all, delete-orphan')
    company_profile = db.relationship('Company', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash y guarda la contraseña"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica la contraseña"""
        return check_password_hash(self.password_hash, password)
    
    def generate_token(self):
        """Genera token JWT"""
        return create_access_token(identity=self.id)
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

class Student(db.Model):
    """Modelo para estudiantes"""
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Información personal
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    birth_date = db.Column(db.Date)
    
    # Información académica
    career = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    credits_percentage = db.Column(db.Float, default=0.0)
    gpa = db.Column(db.Float, default=0.0)
    
    # Perfil profesional
    skills_technical = db.Column(db.Text)  # JSON string
    skills_soft = db.Column(db.Text)  # JSON string
    interests = db.Column(db.Text)  # JSON string
    languages = db.Column(db.Text)  # JSON string
    experience = db.Column(db.Text)  # JSON string
    
    # Documentos
    cv_path = db.Column(db.String(255))
    photo_path = db.Column(db.String(255))
    
    # Estado
    is_available = db.Column(db.Boolean, default=True)
    profile_completed = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    applications = db.relationship('Application', backref='student', lazy='dynamic')
    
    def get_skills_technical(self):
        """Obtiene habilidades técnicas como lista"""
        return json.loads(self.skills_technical) if self.skills_technical else []
    
    def set_skills_technical(self, skills):
        """Establece habilidades técnicas"""
        self.skills_technical = json.dumps(skills)
    
    def get_skills_soft(self):
        """Obtiene habilidades blandas como lista"""
        return json.loads(self.skills_soft) if self.skills_soft else []
    
    def set_skills_soft(self, skills):
        """Establece habilidades blandas"""
        self.skills_soft = json.dumps(skills)
    
    def get_interests(self):
        """Obtiene intereses como lista"""
        return json.loads(self.interests) if self.interests else []
    
    def set_interests(self, interests):
        """Establece intereses"""
        self.interests = json.dumps(interests)
    
    def get_languages(self):
        """Obtiene idiomas como lista"""
        return json.loads(self.languages) if self.languages else []
    
    def set_languages(self, languages):
        """Establece idiomas"""
        self.languages = json.dumps(languages)
    
    def get_experience(self):
        """Obtiene experiencia como lista"""
        return json.loads(self.experience) if self.experience else []
    
    def set_experience(self, experience):
        """Establece experiencia"""
        self.experience = json.dumps(experience)
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'student_id': self.student_id,
            'phone': self.phone,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'career': self.career,
            'semester': self.semester,
            'credits_percentage': self.credits_percentage,
            'gpa': self.gpa,
            'skills_technical': self.get_skills_technical(),
            'skills_soft': self.get_skills_soft(),
            'interests': self.get_interests(),
            'languages': self.get_languages(),
            'experience': self.get_experience(),
            'cv_path': self.cv_path,
            'photo_path': self.photo_path,
            'is_available': self.is_available,
            'profile_completed': self.profile_completed,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Company(db.Model):
    """Modelo para empresas"""
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Información de la empresa
    company_name = db.Column(db.String(100), nullable=False)
    rfc = db.Column(db.String(13), unique=True, nullable=False)
    industry = db.Column(db.String(100), nullable=False)
    size = db.Column(db.String(20))  # 'small', 'medium', 'large'
    website = db.Column(db.String(255))
    
    # Información de contacto
    contact_name = db.Column(db.String(100), nullable=False)
    contact_position = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    
    # Descripción
    description = db.Column(db.Text)
    mission = db.Column(db.Text)
    vision = db.Column(db.Text)
    
    # Estado
    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    opportunities = db.relationship('Opportunity', backref='company', lazy='dynamic')
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'company_name': self.company_name,
            'rfc': self.rfc,
            'industry': self.industry,
            'size': self.size,
            'website': self.website,
            'contact_name': self.contact_name,
            'contact_position': self.contact_position,
            'phone': self.phone,
            'address': self.address,
            'description': self.description,
            'mission': self.mission,
            'vision': self.vision,
            'is_verified': self.is_verified,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Opportunity(db.Model):
    """Modelo para oportunidades (prácticas, servicio social, empleo)"""
    __tablename__ = 'opportunities'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    
    # Información básica
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'internship', 'social_service', 'job'
    
    # Requisitos
    required_skills = db.Column(db.Text)  # JSON string
    required_semester = db.Column(db.Integer)
    required_careers = db.Column(db.Text)  # JSON string
    required_credits = db.Column(db.Float, default=0.0)
    
    # Detalles
    duration_months = db.Column(db.Integer)
    hours_per_week = db.Column(db.Integer)
    salary = db.Column(db.Float)
    benefits = db.Column(db.Text)  # JSON string
    location = db.Column(db.String(255))
    work_mode = db.Column(db.String(20))  # 'remote', 'onsite', 'hybrid'
    
    # Estado
    is_active = db.Column(db.Boolean, default=True)
    available_positions = db.Column(db.Integer, default=1)
    filled_positions = db.Column(db.Integer, default=0)
    
    # Fechas
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    application_deadline = db.Column(db.Date)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    applications = db.relationship('Application', backref='opportunity', lazy='dynamic')
    
    def get_required_skills(self):
        """Obtiene habilidades requeridas como lista"""
        return json.loads(self.required_skills) if self.required_skills else []
    
    def set_required_skills(self, skills):
        """Establece habilidades requeridas"""
        self.required_skills = json.dumps(skills)
    
    def get_required_careers(self):
        """Obtiene carreras requeridas como lista"""
        return json.loads(self.required_careers) if self.required_careers else []
    
    def set_required_careers(self, careers):
        """Establece carreras requeridas"""
        self.required_careers = json.dumps(careers)
    
    def get_benefits(self):
        """Obtiene beneficios como lista"""
        return json.loads(self.benefits) if self.benefits else []
    
    def set_benefits(self, benefits):
        """Establece beneficios"""
        self.benefits = json.dumps(benefits)
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'company_id': self.company_id,
            'title': self.title,
            'description': self.description,
            'type': self.type,
            'required_skills': self.get_required_skills(),
            'required_semester': self.required_semester,
            'required_careers': self.get_required_careers(),
            'required_credits': self.required_credits,
            'duration_months': self.duration_months,
            'hours_per_week': self.hours_per_week,
            'salary': self.salary,
            'benefits': self.get_benefits(),
            'location': self.location,
            'work_mode': self.work_mode,
            'is_active': self.is_active,
            'available_positions': self.available_positions,
            'filled_positions': self.filled_positions,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'application_deadline': self.application_deadline.isoformat() if self.application_deadline else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Application(db.Model):
    """Modelo para aplicaciones de estudiantes"""
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunities.id'), nullable=False)
    
    # Estado de la aplicación
    status = db.Column(db.String(20), default='pending')  # 'pending', 'reviewed', 'accepted', 'rejected'
    
    # Información adicional
    cover_letter = db.Column(db.Text)
    additional_info = db.Column(db.Text)
    
    # Evaluación
    match_score = db.Column(db.Float)  # Score de compatibilidad IA
    company_notes = db.Column(db.Text)
    admin_notes = db.Column(db.Text)
    
    # Fechas
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)
    responded_at = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'opportunity_id': self.opportunity_id,
            'status': self.status,
            'cover_letter': self.cover_letter,
            'additional_info': self.additional_info,
            'match_score': self.match_score,
            'company_notes': self.company_notes,
            'admin_notes': self.admin_notes,
            'applied_at': self.applied_at.isoformat() if self.applied_at else None,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'responded_at': self.responded_at.isoformat() if self.responded_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Document(db.Model):
    """Modelo para documentos generados"""
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Información del documento
    document_type = db.Column(db.String(50), nullable=False)  # 'constancia', 'carta', 'reporte'
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Archivo
    file_path = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer)
    mime_type = db.Column(db.String(100))
    
    # Relaciones
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    
    # Metadatos
    generated_by = db.Column(db.String(50))  # 'system', 'admin', 'student'
    document_metadata = db.Column(db.Text)  # JSON string
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_metadata(self):
        """Obtiene metadatos como diccionario"""
        return json.loads(self.document_metadata) if self.document_metadata else {}
    
    def set_metadata(self, metadata):
        """Establece metadatos"""
        self.document_metadata = json.dumps(metadata)
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'document_type': self.document_type,
            'title': self.title,
            'description': self.description,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'mime_type': self.mime_type,
            'student_id': self.student_id,
            'company_id': self.company_id,
            'generated_by': self.generated_by,
            'metadata': self.get_metadata(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class KPI(db.Model):
    """Modelo para KPIs del sistema"""
    __tablename__ = 'kpis'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Información del KPI
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)  # 'registrations', 'placements', 'matches'
    
    # Valores
    current_value = db.Column(db.Float, default=0.0)
    target_value = db.Column(db.Float)
    previous_value = db.Column(db.Float)
    
    # Metadatos
    calculation_method = db.Column(db.String(100))
    data_source = db.Column(db.String(100))
    
    # Timestamps
    calculated_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'current_value': self.current_value,
            'target_value': self.target_value,
            'previous_value': self.previous_value,
            'calculation_method': self.calculation_method,
            'data_source': self.data_source,
            'calculated_at': self.calculated_at.isoformat() if self.calculated_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class OKR(db.Model):
    """Modelo para OKRs del sistema"""
    __tablename__ = 'okrs'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Información del OKR
    objective = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)  # 'placement', 'matching', 'satisfaction'
    
    # Objetivos
    target_metric = db.Column(db.String(100), nullable=False)
    target_value = db.Column(db.Float, nullable=False)
    current_value = db.Column(db.Float, default=0.0)
    
    # Período
    period_start = db.Column(db.Date, nullable=False)
    period_end = db.Column(db.Date, nullable=False)
    
    # Estado
    is_active = db.Column(db.Boolean, default=True)
    completion_percentage = db.Column(db.Float, default=0.0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def calculate_completion(self):
        """Calcula el porcentaje de completado"""
        if self.target_value > 0:
            self.completion_percentage = min(100.0, (self.current_value / self.target_value) * 100.0)
        else:
            self.completion_percentage = 0.0
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'objective': self.objective,
            'description': self.description,
            'category': self.category,
            'target_metric': self.target_metric,
            'target_value': self.target_value,
            'current_value': self.current_value,
            'period_start': self.period_start.isoformat() if self.period_start else None,
            'period_end': self.period_end.isoformat() if self.period_end else None,
            'is_active': self.is_active,
            'completion_percentage': self.completion_percentage,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
