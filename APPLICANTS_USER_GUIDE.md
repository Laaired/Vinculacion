# Guía Rápida: Cómo Usar la Sección de Perfiles de Postulantes

## Acceso a la Funcionalidad

### Opción 1: Desde el Dashboard de Empresa

1. Inicia sesión como empresa en la plataforma
2. Ve al Dashboard de Empresa
3. Encontrarás un botón azul "Ver Postulantes" en la parte superior derecha
4. Haz clic en el botón para acceder a la sección

### Opción 2: Desde las Pestañas del Dashboard

1. En el Dashboard de Empresa
2. Busca la pestaña "Perfiles de Postulantes" en el menú de pestañas
3. Haz clic en la pestaña para navegar a la sección

### Opción 3: URL Directa

Navega directamente a: `http://localhost:5000/company/applicants`

---

## Funcionalidades Principales

### 1. Vista de Tarjetas de Postulantes

Cada tarjeta muestra:
- **Nombre completo** del postulante
- **ID de estudiante**
- **Badge de puntuación** (0-10) en la esquina superior derecha
- **Carrera** que está cursando
- **Semestre actual**
- **Promedio académico** (GPA)
- **Porcentaje de créditos** completados
- **Primeras 4 habilidades técnicas** (+ contador de adicionales)
- **Idiomas** que domina
- **Número de aplicaciones** realizadas
- **Estado de disponibilidad**
- **Botón "Ver Perfil Completo"** para más detalles

### 2. Sistema de Filtros

#### Filtro por Carrera
```
Ubicación: Primera columna de filtros
Opciones:
- Todas las carreras
- Ingeniería en Sistemas
- Ingeniería en Computación
- Ingeniería en Tecnologías de la Información
```

#### Filtro por Semestre Mínimo
```
Ubicación: Segunda columna de filtros
Opciones:
- Todos
- 5° Semestre o más
- 6° Semestre o más
- 7° Semestre o más
- 8° Semestre o más
```

#### Ordenamiento
```
Ubicación: Tercera columna de filtros
Opciones:
- Mejor puntuación (por defecto)
- Promedio más alto
- Semestre más avanzado
```

### 3. Ver Perfil Completo (Modal)

Al hacer clic en "Ver Perfil Completo" se abre un modal grande con:

#### Panel Izquierdo (Información Resumida)
- **Tarjeta de Información Personal**
  - ID de estudiante
  - Email (con link para enviar correo)
  - Teléfono
  - Fecha de nacimiento
  - Botón para descargar CV

- **Tarjeta de Información Académica**
  - Carrera completa
  - Semestre actual
  - Promedio (GPA) destacado
  - Porcentaje de créditos con barra de progreso

- **Tarjeta de Score de Compatibilidad**
  - Número grande destacado (ej: 9.2/10)

#### Panel Derecho (Información Detallada)
- **Habilidades Técnicas**: Lista completa de competencias técnicas en badges
- **Habilidades Blandas**: Soft skills del candidato
- **Idiomas**: Con nivel de dominio especificado
- **Experiencia Profesional**: 
  - Puesto
  - Empresa
  - Duración/Período
  - Descripción detallada
- **Certificaciones**:
  - Nombre del certificado
  - Institución emisora
  - Año de obtención
- **Proyectos**:
  - Nombre del proyecto
  - Descripción
  - Tecnologías utilizadas
  - Link al proyecto (si está disponible)
- **Áreas de Interés**: Campos de especialización preferidos

#### Acciones Disponibles
- **Botón "Cerrar"**: Cierra el modal
- **Botón "Contactar"**: Abre el cliente de email con el correo del postulante prellenado

---

## Ejemplos de Uso

### Caso 1: Buscar Desarrollador Full Stack Experimentado

1. Accede a la sección de Perfiles de Postulantes
2. Configura los filtros:
   - Carrera: "Ingeniería en Sistemas"
   - Semestre: "7° Semestre o más"
   - Ordenar por: "Mejor puntuación"
3. Revisa las tarjetas resultantes
4. Haz clic en "Ver Perfil Completo" del candidato con mejor score
5. Revisa las habilidades técnicas para verificar conocimiento en React, Node.js, etc.
6. Si es un buen match, haz clic en "Contactar" para enviar un email

### Caso 2: Encontrar Candidatos de Semestres Avanzados

1. Accede a la sección
2. Selecciona "8° Semestre o más" en el filtro de semestre
3. Ordena por "Semestre más avanzado"
4. Los candidatos próximos a graduarse aparecerán primero

### Caso 3: Revisar Todos los Candidatos de una Carrera

1. Selecciona la carrera específica en el filtro
2. Deja los demás filtros en "Todos"
3. Revisa todas las tarjetas para tener una vista general
4. Profundiza en los perfiles que te interesen

---

## Tips y Mejores Prácticas

### Para Empresas

1. **Usa los filtros estratégicamente**
   - Combina carrera + semestre + ordenamiento para encontrar el candidato ideal
   
2. **Revisa el score de compatibilidad**
   - Scores de 8.5+ indican candidatos muy compatibles
   - Scores de 7.0-8.4 indican buenos candidatos con algunas brechas
   
3. **Presta atención a las certificaciones**
   - Las certificaciones demuestran compromiso con el aprendizaje continuo
   
4. **Revisa los proyectos**
   - Los proyectos muestran experiencia práctica real
   
5. **Considera la experiencia profesional**
   - Freelance y prácticas previas son valiosas
   
6. **Contacta múltiples candidatos**
   - No te limites a uno solo, contacta 2-3 candidatos top

### Navegación Rápida

- **Actualizar datos**: Botón "Actualizar" en la esquina superior derecha
- **Volver al Dashboard**: Link en el menú superior o botón "Atrás" del navegador
- **Abrir múltiples perfiles**: Puedes abrir el modal, revisar y cerrar para ver otro sin recargar

---

## Solución de Problemas

### No se cargan los postulantes
- Verifica tu conexión a internet
- Refresca la página (F5)
- Haz clic en el botón "Actualizar"

### Los filtros no funcionan
- Asegúrate de seleccionar al menos una opción
- Prueba reiniciando los filtros (selecciona "Todos")

### El modal no se abre
- Verifica que JavaScript esté habilitado en tu navegador
- Refresca la página
- Intenta con otro navegador

### No puedo contactar al candidato
- Verifica que tengas un cliente de email configurado
- Copia manualmente el email del perfil si es necesario

---

## Atajos de Teclado

- **ESC**: Cerrar modal de perfil
- **F5**: Refrescar la página
- **Ctrl + F**: Buscar en la página

---

## Preguntas Frecuentes

**P: ¿Los datos de los postulantes son reales?**
R: Actualmente son datos simulados para demostración. En producción, se conectarán a la base de datos real de estudiantes.

**P: ¿Puedo guardar candidatos favoritos?**
R: Esta funcionalidad estará disponible en una futura actualización.

**P: ¿Cómo se calcula el score de compatibilidad?**
R: Se basa en múltiples factores: habilidades técnicas, promedio académico, experiencia, certificaciones y coincidencia con requisitos típicos.

**P: ¿Puedo exportar los perfiles?**
R: La función de exportación a PDF estará disponible próximamente.

**P: ¿Los estudiantes ven que revisé su perfil?**
R: No, la visualización de perfiles es privada para la empresa.

---

## Contacto y Soporte

Para asistencia adicional o reportar problemas:
- Email: soporte@vinculacion.unrc.mx
- Teléfono: (555) 123-4567
- Horario: Lunes a Viernes, 9:00 AM - 6:00 PM

---

**Última actualización**: 2024
**Versión de la funcionalidad**: 1.0
