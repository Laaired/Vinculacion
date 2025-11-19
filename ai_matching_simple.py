# Versión simplificada de ai_matching.py para Windows
# Sin dependencias problemáticas como matplotlib y seaborn

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os
from datetime import datetime
import json

class AIMatchingEngine:
    """Motor de matching inteligente usando técnicas de Machine Learning"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.scaler = StandardScaler()
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False
        self.model_path = './models/ai_matching_model.pkl'
        
    def prepare_student_features(self, student):
        """Prepara características del estudiante para el modelo"""
        features = {
            'semester': student.semester,
            'credits_percentage': student.credits_percentage,
            'gpa': student.gpa,
            'career_encoded': self._encode_career(student.career),
            'skills_count': len(student.get_skills_technical()) + len(student.get_skills_soft()),
            'languages_count': len(student.get_languages()),
            'experience_count': len(student.get_experience()),
            'profile_completeness': self._calculate_profile_completeness(student)
        }
        
        # Combinar habilidades e intereses para análisis de texto
        text_features = ' '.join(
            student.get_skills_technical() + 
            student.get_skills_soft() + 
            student.get_interests()
        )
        
        return features, text_features
    
    def prepare_opportunity_features(self, opportunity):
        """Prepara características de la oportunidad para el modelo"""
        features = {
            'required_semester': opportunity.required_semester or 0,
            'required_credits': opportunity.required_credits or 0,
            'duration_months': opportunity.duration_months or 0,
            'hours_per_week': opportunity.hours_per_week or 0,
            'has_salary': 1 if opportunity.salary and opportunity.salary > 0 else 0,
            'type_encoded': self._encode_opportunity_type(opportunity.type),
            'required_skills_count': len(opportunity.get_required_skills()),
            'required_careers_count': len(opportunity.get_required_careers()),
            'benefits_count': len(opportunity.get_benefits())
        }
        
        # Combinar descripción y habilidades requeridas para análisis de texto
        text_features = ' '.join([
            opportunity.description or '',
            ' '.join(opportunity.get_required_skills()),
            ' '.join(opportunity.get_benefits())
        ])
        
        return features, text_features
    
    def calculate_semantic_similarity(self, student_text, opportunity_text):
        """Calcula similitud semántica usando TF-IDF"""
        try:
            if not student_text.strip() or not opportunity_text.strip():
                return 0.0
            
            # Vectorizar textos
            texts = [student_text, opportunity_text]
            tfidf_matrix = self.vectorizer.fit_transform(texts)
            
            # Calcular similitud coseno
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return similarity
            
        except Exception as e:
            print(f"Error calculando similitud semántica: {e}")
            return 0.0
    
    def calculate_structured_similarity(self, student_features, opportunity_features):
        """Calcula similitud basada en características estructuradas"""
        try:
            # Normalizar características numéricas
            student_array = np.array(list(student_features.values())).reshape(1, -1)
            opportunity_array = np.array(list(opportunity_features.values())).reshape(1, -1)
            
            # Calcular distancia euclidiana normalizada
            distance = np.linalg.norm(student_array - opportunity_array)
            max_distance = np.sqrt(len(student_features))  # Distancia máxima posible
            
            similarity = 1 - (distance / max_distance)
            return max(0, similarity)  # Asegurar que no sea negativo
            
        except Exception as e:
            print(f"Error calculando similitud estructurada: {e}")
            return 0.0
    
    def calculate_compatibility_score(self, student, opportunity):
        """Calcula score de compatibilidad usando múltiples algoritmos"""
        try:
            # Preparar características
            student_features, student_text = self.prepare_student_features(student)
            opportunity_features, opportunity_text = self.prepare_opportunity_features(opportunity)
            
            # Calcular similitudes
            semantic_sim = self.calculate_semantic_similarity(student_text, opportunity_text)
            structured_sim = self.calculate_structured_similarity(student_features, opportunity_features)
            
            # Verificar requisitos básicos
            basic_compatibility = self._check_basic_requirements(student, opportunity)
            
            # Calcular score final con pesos
            weights = {
                'semantic': 0.4,
                'structured': 0.4,
                'basic': 0.2
            }
            
            final_score = (
                semantic_sim * weights['semantic'] +
                structured_sim * weights['structured'] +
                basic_compatibility * weights['basic']
            )
            
            # Ajustar score basado en factores adicionales
            final_score = self._apply_additional_factors(final_score, student, opportunity)
            
            return round(min(1.0, max(0.0, final_score)), 3)
            
        except Exception as e:
            print(f"Error calculando score de compatibilidad: {e}")
            return 0.0
    
    def get_top_recommendations(self, student, opportunities, top_n=10):
        """Obtiene las mejores recomendaciones para un estudiante"""
        try:
            recommendations = []
            
            for opportunity in opportunities:
                if not opportunity.is_active:
                    continue
                
                score = self.calculate_compatibility_score(student, opportunity)
                
                if score >= 0.3:  # Solo incluir recomendaciones con score >= 30%
                    recommendations.append({
                        'opportunity': opportunity,
                        'score': score,
                        'company': opportunity.company
                    })
            
            # Ordenar por score descendente
            recommendations.sort(key=lambda x: x['score'], reverse=True)
            
            return recommendations[:top_n]
            
        except Exception as e:
            print(f"Error obteniendo recomendaciones: {e}")
            return []
    
    def train_model(self, applications_data):
        """Entrena el modelo de ML con datos históricos"""
        try:
            if not applications_data:
                print("No hay datos suficientes para entrenar el modelo")
                return False
            
            # Preparar datos de entrenamiento
            X = []
            y = []
            
            for app_data in applications_data:
                student_features, _ = self.prepare_student_features(app_data['student'])
                opportunity_features, _ = self.prepare_opportunity_features(app_data['opportunity'])
                
                # Combinar características
                combined_features = {**student_features, **opportunity_features}
                X.append(list(combined_features.values()))
                
                # Etiqueta: 1 si fue aceptada, 0 si no
                y.append(1 if app_data['status'] == 'accepted' else 0)
            
            X = np.array(X)
            y = np.array(y)
            
            # Dividir datos
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Normalizar características
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Entrenar modelo
            self.model.fit(X_train_scaled, y_train)
            
            # Evaluar modelo
            train_score = self.model.score(X_train_scaled, y_train)
            test_score = self.model.score(X_test_scaled, y_test)
            
            print(f"Modelo entrenado - Train Score: {train_score:.3f}, Test Score: {test_score:.3f}")
            
            # Guardar modelo
            self._save_model()
            self.is_trained = True
            
            return True
            
        except Exception as e:
            print(f"Error entrenando modelo: {e}")
            return False
    
    def predict_success_probability(self, student, opportunity):
        """Predice la probabilidad de éxito usando el modelo entrenado"""
        try:
            if not self.is_trained:
                return 0.5  # Valor por defecto si el modelo no está entrenado
            
            # Preparar características
            student_features, _ = self.prepare_student_features(student)
            opportunity_features, _ = self.prepare_opportunity_features(opportunity)
            
            # Combinar características
            combined_features = {**student_features, **opportunity_features}
            X = np.array(list(combined_features.values())).reshape(1, -1)
            
            # Normalizar
            X_scaled = self.scaler.transform(X)
            
            # Predecir probabilidad
            probability = self.model.predict_proba(X_scaled)[0][1]
            
            return round(probability, 3)
            
        except Exception as e:
            print(f"Error prediciendo probabilidad: {e}")
            return 0.5
    
    def _encode_career(self, career):
        """Codifica carrera como número"""
        career_mapping = {
            'Ingeniería en Sistemas': 1,
            'Ingeniería Industrial': 2,
            'Administración': 3,
            'Contaduría': 4,
            'Mercadotecnia': 5,
            'Psicología': 6,
            'Derecho': 7,
            'Medicina': 8,
            'Enfermería': 9,
            'Arquitectura': 10
        }
        return career_mapping.get(career, 0)
    
    def _encode_opportunity_type(self, opp_type):
        """Codifica tipo de oportunidad como número"""
        type_mapping = {
            'internship': 1,
            'social_service': 2,
            'job': 3
        }
        return type_mapping.get(opp_type, 0)
    
    def _calculate_profile_completeness(self, student):
        """Calcula qué tan completo está el perfil del estudiante"""
        total_fields = 8
        completed_fields = 0
        
        if student.first_name and student.last_name:
            completed_fields += 1
        if student.career:
            completed_fields += 1
        if student.semester:
            completed_fields += 1
        if student.credits_percentage > 0:
            completed_fields += 1
        if student.get_skills_technical():
            completed_fields += 1
        if student.get_skills_soft():
            completed_fields += 1
        if student.get_languages():
            completed_fields += 1
        if student.get_experience():
            completed_fields += 1
        
        return completed_fields / total_fields
    
    def _check_basic_requirements(self, student, opportunity):
        """Verifica si el estudiante cumple los requisitos básicos"""
        score = 0.0
        total_checks = 0
        
        # Verificar semestre
        if opportunity.required_semester:
            total_checks += 1
            if student.semester >= opportunity.required_semester:
                score += 1
        
        # Verificar créditos
        if opportunity.required_credits:
            total_checks += 1
            if student.credits_percentage >= opportunity.required_credits:
                score += 1
        
        # Verificar carreras
        if opportunity.get_required_careers():
            total_checks += 1
            if student.career in opportunity.get_required_careers():
                score += 1
        
        return score / total_checks if total_checks > 0 else 1.0
    
    def _apply_additional_factors(self, base_score, student, opportunity):
        """Aplica factores adicionales para ajustar el score"""
        adjusted_score = base_score
        
        # Factor de disponibilidad
        if not student.is_available:
            adjusted_score *= 0.5
        
        # Factor de perfil completo
        profile_completeness = self._calculate_profile_completeness(student)
        adjusted_score *= (0.5 + profile_completeness * 0.5)
        
        # Factor de experiencia previa
        if student.get_experience():
            adjusted_score *= 1.1
        
        # Factor de idiomas
        if len(student.get_languages()) > 1:
            adjusted_score *= 1.05
        
        return min(1.0, adjusted_score)
    
    def _save_model(self):
        """Guarda el modelo entrenado"""
        try:
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            
            model_data = {
                'model': self.model,
                'scaler': self.scaler,
                'vectorizer': self.vectorizer,
                'trained_at': datetime.utcnow().isoformat()
            }
            
            joblib.dump(model_data, self.model_path)
            print(f"Modelo guardado en {self.model_path}")
            
        except Exception as e:
            print(f"Error guardando modelo: {e}")
    
    def load_model(self):
        """Carga el modelo entrenado"""
        try:
            if os.path.exists(self.model_path):
                model_data = joblib.load(self.model_path)
                self.model = model_data['model']
                self.scaler = model_data['scaler']
                self.vectorizer = model_data['vectorizer']
                self.is_trained = True
                print(f"Modelo cargado desde {self.model_path}")
                return True
            else:
                print("No se encontró modelo previamente entrenado")
                return False
                
        except Exception as e:
            print(f"Error cargando modelo: {e}")
            return False
    
    def get_model_info(self):
        """Obtiene información del modelo"""
        return {
            'is_trained': self.is_trained,
            'model_path': self.model_path,
            'model_type': 'RandomForestClassifier',
            'features_used': [
                'semester', 'credits_percentage', 'gpa', 'career_encoded',
                'skills_count', 'languages_count', 'experience_count',
                'profile_completeness', 'required_semester', 'required_credits',
                'duration_months', 'hours_per_week', 'has_salary',
                'type_encoded', 'required_skills_count', 'required_careers_count',
                'benefits_count'
            ]
        }

# Instancia global del motor de matching
matching_engine = AIMatchingEngine()
