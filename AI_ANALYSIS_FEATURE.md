# Análisis Inteligente de Postulantes - Sistema de IA

## 📋 Descripción

Se ha implementado un **sistema de análisis inteligente de postulantes** que utiliza una simulación de IA para:

- Analizar perfiles de estudiantes (CV) contra requerimientos de oportunidades
- Generar puntuaciones de compatibilidad (0-10)
- Clasificar candidatos en categorías (Altamente Recomendado, Recomendado, Considerar, No Recomendado)
- Proporcionar análisis detallado de fortalezas y brechas de cada candidato
- Ofrecer razones fundamentadas para cada recomendación

## 🚀 Características

### 1. **Nueva Pestaña: "Análisis de IA"**
   - Ubicada en el Dashboard de Empresa (`/company/profile`)
   - Permite seleccionar una oportunidad publicada
   - Genera automáticamente recomendaciones de candidatos

### 2. **API de Análisis**
   - **Endpoint:** `POST /api/companies/analyze-applications`
   - **Parámetros:** 
     ```json
     {
       "opportunity_id": 1
     }
     ```
   - **Respuesta:** Análisis completo con rankings, fortalezas y brechas

### 3. **Interfaz de Usuario**
   - **Resumen Ejecutivo** con estadísticas del análisis
   - **Candidatos Recomendados** (Acordeón interactivo)
   - **Candidatos No Recomendados** (Sección desplegable)
   - Botones de acción: Aceptar, Contactar

### 4. **Criterios de Evaluación**

#### Puntuación de Compatibilidad (0-10)
- **9+:** Altamente Recomendado
- **8-8.9:** Recomendado
- **7-7.9:** Considerar
- **<7:** No Recomendado

#### Factores Analizados
- Alineación de carrera y especialización
- Tecnologías/habilidades requeridas
- Requisitos académicos (semestre, promedio, créditos)
- Experiencia previa
- Certificaciones y logros
- Habilidades blandas

## 📊 Componentes del Análisis

### Para Cada Candidato se Proporciona:

1. **Ranking:** Posición relativa entre candidatos
2. **Puntuación:** Score de 0-10
3. **Recomendación:** Texto descriptivo del nivel
4. **Fortalezas:** Lista de habilidades que coinciden
5. **Brechas:** Áreas donde le falta desarrollo
6. **Razones:** Fundamento detallado del análisis

### Estadísticas Generales:

- Total de aplicaciones analizadas
- Cantidad de Altamente Recomendados
- Cantidad de Recomendados
- Cantidad a Considerar
- Cantidad No Recomendados
- Tasa de éxito estimada de contratación
- Confianza del modelo de IA

## 🔧 Cómo Usar

### 1. Acceder al Dashboard de Empresa
```
Navega a: /company/profile
```

### 2. Ir a la Pestaña "Análisis de IA"
```
Dashboard → Análisis de IA
```

### 3. Seleccionar Oportunidad
```
Dropdown: "Selecciona una oportunidad"
Opciones: Desarrollador Full Stack, Ingeniero QA, etc.
```

### 4. Ver Recomendaciones
```
El sistema analizará automáticamente todos los postulantes
Mostrará los mejores candidatos primero
```

### 5. Tomar Acciones
```
- Haz clic en "Aceptar" para contratar un candidato
- Haz clic en "Contactar" para enviar un mensaje
```

## 📈 Ejemplo de Salida

```
Ranking #1 🥇
Nombre: Carlos Rodríguez Martínez
Puntuación: 9.2/10
Carrera: Ingeniería en Sistemas

Recomendación: ALTAMENTE RECOMENDADO

✅ Fortalezas:
- Python
- JavaScript
- React
- SQL
- Trabajo en equipo

⚠️ Brechas:
- Experiencia en DevOps limitada

📋 Razones:
- Experiencia en tecnologías requeridas
- Semestre cursado coincide con requisitos
- Habilidades blandas alineadas
- Excelente promedio académico
```

## 🤖 Modelo de IA

- **Modelo:** CV-Matcher-v2.0
- **Confianza:** 94%
- **Tipo:** Simulación (Producción: TensorFlow/PyTorch)

## 🔮 Mejoras Futuras

1. **Integración con ML Real**
   - Usar modelos TensorFlow/PyTorch
   - NLP para análisis de CV
   - Training con datos históricos

2. **Análisis Avanzado**
   - Predicción de rotación
   - Análisis de cultura organizacional
   - Recomendaciones salariales

3. **Automatización**
   - Envío automático de correos
   - Generación de reportes PDF
   - Programación de entrevistas

4. **Integración**
   - LinkedIn API
   - Email automático
   - CRM del sistema

## 📝 Notas Técnicas

### Archivos Modificados
- `routes/company_routes.py` - Nueva ruta API
- `templates/company_profile.html` - Nueva pestaña y funciones

### Tecnologías Utilizadas
- Python Flask (Backend)
- JavaScript Vanilla (Frontend)
- Bootstrap 5 (UI)
- Chart.js (Estadísticas)

### API Endpoint
```
POST /api/companies/analyze-applications
Content-Type: application/json

{
  "opportunity_id": 1
}
```

## ✅ Checklist de Funcionalidad

- [x] Pestaña "Análisis de IA" agregada
- [x] Selector de oportunidades funcional
- [x] Endpoint API implementado
- [x] Análisis de candidatos simulado
- [x] Display de recomendaciones
- [x] Acordeones interactivos
- [x] Botones de acción (Aceptar, Contactar)
- [x] Estadísticas del análisis
- [x] Puntuaciones de compatibilidad
- [x] Análisis de fortalezas y brechas

## 🐛 Testing

Para probar la funcionalidad:

1. Accede a `/company/profile`
2. Ve a la pestaña "Análisis de IA"
3. Selecciona "Desarrollador Full Stack"
4. Verás el análisis de los 5 candidatos de prueba
5. Expande cada candidato para ver detalles

---

**Última actualización:** 13 de Noviembre, 2025
**Versión:** 1.0.0
