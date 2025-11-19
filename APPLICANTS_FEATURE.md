# Funcionalidad: Perfiles de Postulantes para Empresas

## Descripción

Se ha agregado una nueva sección en el panel de empresas que permite visualizar y explorar los perfiles de postulantes (estudiantes) disponibles en la plataforma. Esta funcionalidad incluye datos simulados de 5 postulantes con información completa.

## Características Implementadas

### 1. Vista de Listado de Postulantes
- **Ruta**: `/company/applicants`
- **Funcionalidad**: Muestra tarjetas con información resumida de cada postulante
- **Información mostrada**:
  - Nombre completo
  - ID de estudiante
  - Carrera
  - Semestre actual
  - Promedio académico (GPA)
  - Porcentaje de créditos completados
  - Score de compatibilidad (0-10)
  - Habilidades técnicas principales
  - Idiomas
  - Estado de disponibilidad

### 2. Sistema de Filtros
- **Filtro por Carrera**: Filtra postulantes por programa académico
- **Filtro por Semestre**: Muestra solo postulantes de semestre X o superior
- **Ordenamiento**: 
  - Por mejor puntuación de compatibilidad
  - Por promedio más alto
  - Por semestre más avanzado

### 3. Vista Detallada de Postulante
- Modal con información completa incluyendo:
  - **Información Personal**: Email, teléfono, fecha de nacimiento
  - **Información Académica**: Carrera, semestre, promedio, créditos
  - **Habilidades Técnicas**: Lista completa de competencias técnicas
  - **Habilidades Blandas**: Soft skills del candidato
  - **Idiomas**: Con niveles de dominio
  - **Experiencia Profesional**: Historial laboral detallado
  - **Certificaciones**: Certificados y cursos completados
  - **Proyectos**: Portfolio de proyectos realizados
  - **Áreas de Interés**: Campos de especialización preferidos
  - **Score de Compatibilidad**: Visualización destacada

### 4. Funcionalidades Adicionales
- Botón de contacto directo (abre cliente de email)
- Descarga de CV (cuando esté disponible)
- Diseño responsivo adaptable a móviles y tablets
- Animaciones suaves en tarjetas con efecto hover

## API Endpoints

### GET `/api/companies/applicants`
Obtiene la lista completa de postulantes con datos simulados.

**Respuesta**:
```json
{
  "applicants": [
    {
      "id": 1,
      "student_id": "EST001",
      "first_name": "Carlos",
      "last_name": "Rodríguez Martínez",
      "career": "Ingeniería en Sistemas",
      "semester": 7,
      "gpa": 8.9,
      "match_score": 9.2,
      ...
    }
  ],
  "total": 5
}
```

### GET `/api/companies/applicants/<id>`
Obtiene el perfil detallado de un postulante específico.

**Respuesta**:
```json
{
  "applicant": {
    "id": 1,
    "student_id": "EST001",
    "first_name": "Carlos",
    "last_name": "Rodríguez Martínez",
    "email": "carlos.rodriguez@estudiantes.unrc.mx",
    "skills_technical": ["Python", "JavaScript", "React", ...],
    "experience": [...],
    "certifications": [...],
    "projects": [...],
    ...
  }
}
```

## Postulantes Simulados

Se han creado 5 perfiles de postulantes con información realista:

1. **Carlos Rodríguez Martínez**
   - Ingeniería en Sistemas, 7° semestre
   - Score: 9.2/10
   - Especialidad: Desarrollo Full Stack
   - Experiencia en Python, JavaScript, React, Node.js

2. **María González López**
   - Ingeniería en Computación, 8° semestre
   - Score: 8.5/10
   - Especialidad: Quality Assurance
   - Experiencia en Testing automatizado, Java, Selenium

3. **Juan Pérez García**
   - Ingeniería en Sistemas, 6° semestre
   - Score: 8.7/10
   - Especialidad: Frontend Development
   - Experiencia en React, Vue.js, UX/UI Design

4. **Ana Martínez Sánchez**
   - Ingeniería en Sistemas, 9° semestre
   - Score: 7.9/10
   - Especialidad: DevOps
   - Experiencia en Docker, Kubernetes, AWS, CI/CD

5. **Roberto Villalobos Cruz**
   - Ingeniería en Tecnologías de la Información, 5° semestre
   - Score: 7.5/10
   - Especialidad: Data Analysis
   - Experiencia en Python, Power BI, Data Science

## Acceso a la Funcionalidad

### Desde el Perfil de Empresa
1. Botón superior: "Ver Postulantes" (azul) en `/company/profile`
2. Banner destacado: Banner azul grande con botón "Ver Perfiles de Postulantes"
3. Pestaña en el menú: "Perfiles de Postulantes" con badge "¡Nuevo!"

### Navegación Directa
- URL: `http://localhost:5000/company/applicants`

## Tecnologías Utilizadas
- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Framework CSS**: Bootstrap 5
- **Iconos**: Font Awesome
- **Diseño**: Responsivo con tarjetas y modal

## Pruebas

Para probar la funcionalidad, ejecuta:

```bash
python test_applicants.py
```

Este script verificará:
- ✓ Endpoints API funcionando
- ✓ Datos de postulantes cargados
- ✓ Página renderizándose correctamente

## Próximos Pasos (Mejoras Futuras)

1. Integración con base de datos real de estudiantes
2. Sistema de búsqueda avanzada por palabras clave
3. Filtros adicionales (disponibilidad, ubicación, rango salarial)
4. Comparación lado a lado de múltiples candidatos
5. Sistema de favoritos/guardados
6. Historial de candidatos contactados
7. Integración con sistema de mensajería interna
8. Exportar perfiles a PDF
9. Recomendaciones basadas en IA según necesidades de la empresa
10. Analytics de perfiles más visitados

## Archivos Modificados/Creados

### Nuevos Archivos
- `templates/company_applicants.html` - Vista principal de postulantes
- `test_applicants.py` - Script de pruebas
- `APPLICANTS_FEATURE.md` - Esta documentación

### Archivos Modificados
- `routes/company_routes.py` - Agregados endpoints `/applicants` y `/applicants/<id>`
- `app.py` - Agregada ruta `/company/applicants`
- `templates/company_dashboard.html` - Agregado botón y pestaña de acceso

## Soporte

Para preguntas o reportar problemas con esta funcionalidad, contacta al equipo de desarrollo.
