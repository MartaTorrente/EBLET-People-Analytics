# 📊 Parámetros de Sintetización de Datos

## Justificación Metodológica de los Datos Sintéticos

Este documento explica los parámetros utilizados para generar los datos sintéticos del framework EBLET, incluyendo su justificación teórica y empírica.

---

## 🎯 Objetivo

Crear datasets sintéticos realistas que representen 5 escenarios organizacionales distintos, permitiendo:
- Validar el funcionamiento del framework
- Establecer puntos de referencia (benchmarks)
- Comparar resultados de organizaciones reales
- Facilitar la investigación en People Analytics

---

## 📐 Arquitectura del Modelo de Generación

### Flujo de Generación

```
1. Definir Empresa (metadata: sector, tamaño, cultura)
   ↓
2. Asignar Escenario Objetivo (1-5)
   ↓
3. Generar Empleados con perfiles demográficos
   ↓
4. Aplicar Modelo Psicológico (efectos organizacionales)
   ↓
5. Generar Respuestas a la Encuesta (43 preguntas Likert)
   ↓
6. Calcular KPIs por Empleado
   ↓
7. Agregar KPIs a Nivel Empresa
   ↓
8. Validar Clasificación en Escenario
   ↓
9. Exportar Dataset
```

---

## 🏢 Parámetros de Escenarios Organizacionales

### Valores Base por Escenario

Cada escenario tiene valores base para los 4 KPIs principales (escala 1-5):

| Escenario | Burnout | Boreout | Bienestar | Rotación | Justificación |
|-----------|---------|---------|-----------|----------|---------------|
| 🟢 **Saludable** | 2.0 | 1.8 | 4.2 | 1.5 | Organización óptima según literatura |
| 🟡 **Estable** | 2.6 | 2.2 | 3.4 | 2.3 | Media poblacional típica |
| 🟠 **Riesgo Burnout** | 4.2 | 2.0 | 2.4 | 4.0 | Sobrecarga laboral alta |
| 🔵 **Riesgo Boreout** | 2.2 | 4.3 | 2.5 | 3.8 | Infraestimulación alta |
| 🔴 **Crítico** | 4.5 | 4.4 | 1.8 | 4.8 | Ambos problemas simultáneos |

**Justificación:**
- Los valores se basan en estudios empíricos de prevalencia de burnout (15-30% de trabajadores) y boreout (10-20%)
- El escenario "Saludable" representa el percentil 90 de bienestar organizacional
- El escenario "Crítico" representa situaciones de crisis organizacional documentadas en casos de estudio

---

## 🎨 Efectos Organizacionales

### 1. Efecto de la Cultura Organizacional

La cultura modula los estados psicológicos de los empleados:

```python
CULTURE_EFFECTS = {
    "Innovadora":   {"burnout": -0.15, "boreout": -0.10, "wellbeing": +0.20},
    "Colaborativa": {"burnout": -0.25, "boreout": -0.10, "wellbeing": +0.30},
    "Tradicional":  {"burnout": +0.15, "boreout": +0.10, "wellbeing": -0.15},
    "Exigente":     {"burnout": +0.35, "boreout": -0.05, "wellbeing": -0.35}
}
```

**Justificación:**
- **Innovadora**: Autonomía y creatividad reducen burnout (Amabile, 1996)
- **Colaborativa**: Apoyo social protege contra burnout (Bakker & Demerouti, 2007)
- **Tradicional**: Rigidez aumenta burnout y boreout (Schaufeli & Taris, 2014)
- **Exigente**: Alta presión incrementa burnout significativamente (Karasek, 1979)

### 2. Efecto de la Modalidad de Trabajo

```python
MODALITY_EFFECTS = {
    "Presencial": {"burnout": +0.10, "boreout": -0.10, "wellbeing": -0.05},
    "Híbrido":    {"burnout": 0.00,  "boreout": 0.00,  "wellbeing": +0.15},
    "Remoto":     {"burnout": -0.10, "boreout": +0.20, "wellbeing": +0.05}
}
```

**Justificación:**
- **Presencial**: Mayor supervisión reduce boreout pero aumenta estrés (Gajendran & Harrison, 2007)
- **Híbrido**: Equilibrio óptimo según estudios post-pandemia (Bloom et al., 2015)
- **Remoto**: Reduce burnout por flexibilidad, pero aumenta boreout por aislamiento (Oakman et al., 2020)

### 3. Efecto del Departamento

```python
DEPARTMENT_EFFECTS = {
    "Desarrollo": {"burnout": +0.20, "boreout": -0.10},
    "Datos":      {"burnout": +0.10, "boreout": 0.00},
    "Producto":   {"burnout": +0.15, "boreout": -0.05},
    "RRHH":       {"burnout": -0.10, "boreout": +0.10},
    "Ventas":     {"burnout": +0.30, "boreout": -0.15}
}
```

**Justificación:**
- **Desarrollo**: Plazos ajustados y alta carga cognitiva (burnout alto)
- **Ventas**: Presión por objetivos y rechazo frecuente (burnout muy alto)
- **RRHH**: Menor presión operativa pero posible aburrimiento (boreout moderado)

---

## 🧠 Modelo Psicológico

### Variables Latentes

El modelo genera 4 variables latentes por empleado:

```python
L_burnout = N(burnout_base + efectos, σ=0.5)
L_boreout = N(boreout_base + efectos, σ=0.5)
L_wellbeing = N(wellbeing_base + efectos, σ=0.5)
L_rotation = f(L_burnout, L_boreout, L_wellbeing)
```

### Fórmula de Rotación

Basada en la teoría de turnover de Mobley (1977):

```python
rotation = 1.5 + 0.35*burnout + 0.25*boreout + 0.30*(5-wellbeing) + noise
```

**Justificación:**
- Burnout y boreout aumentan la intención de rotación
- Bienestar la disminuye (relación inversa)
- Coeficientes calibrados con meta-análisis (Rubio et al., 2015)

---

## 📝 Generación de Respuestas a la Encuesta

### Transformación de Latentes a Respuestas

Cada pregunta se genera como:

```python
respuesta_q = clip(latente + N(0, σ_ruido), 1, 5)
```

Donde:
- `latente`: Variable psicológica correspondiente (burnout, boreout, etc.)
- `σ_ruido`: Variabilidad individual (0.3-0.4)
- `clip(1, 5)`: Recorte a escala Likert 1-5

**Justificación:**
- El ruido simula variabilidad individual y errores de medición
- El recorte asegura respuestas válidas en la escala

### Ruido por Dimensión

| Dimensión | σ_ruido | Justificación |
|-----------|---------|---------------|
| Burnout - Agotamiento | 0.30 | Alta consistencia interna |
| Burnout - Cinismo | 0.35 | Variabilidad moderada |
| Burnout - Ineficacia | 0.40 | Mayor variabilidad individual |
| Boreout - Desinterés | 0.30 | Alta consistencia |
| Boreout - Falta de reto | 0.35 | Variabilidad moderada |
| Boreout - Infraocupación | 0.40 | Mayor variabilidad |
| Bienestar - Satisfacción | 0.30 | Alta consistencia |
| Bienestar - Autoeficacia | 0.40 | Depende de experiencia |
| Rotación | 0.30 | Intención conductual estable |

---

## 📊 Cálculo de KPIs

### KPIs a Nivel Empleado

```python
KPI_Burnout = mean(q21:q29)      # 9 preguntas
KPI_Boreout = mean(q30:q38)      # 9 preguntas
KPI_Bienestar = mean(q39:q45)    # 7 preguntas
KPI_Rotacion = mean(q46:q48)     # 3 preguntas
KPI_Contexto = mean(q6:q20)      # 15 preguntas
```

**Justificación:**
- Media simple para facilitar interpretación
- Cada KPI representa un constructo teórico validado
- Peso igual para todas las preguntas dentro de cada dimensión

### KPIs a Nivel Empresa

```python
KPI_Empresa = mean(KPIs_empleados)
```

**Justificación:**
- Agregación por media para representar el clima organizacional
- Permite comparar empresas de diferentes tamaños

---

## 🎯 Umbrales de Clasificación

### Clasificación de Empresas en Escenarios

```python
if burnout >= 3.5 and boreout >= 3.5 and bienestar < 2.5:
    escenario = "Crítico"
elif burnout >= 3.5 and boreout < 3.0 and bienestar < 3.0:
    escenario = "Riesgo Burnout"
elif burnout < 3.0 and boreout >= 3.5 and bienestar < 3.0:
    escenario = "Riesgo Boreout"
elif burnout < 2.5 and boreout < 2.5 and bienestar > 3.5:
    escenario = "Saludable"
else:
    escenario = "Estable"
```

**Justificación:**
- Umbrales basados en percentiles de distribuciones normativas
- 3.5 = percentil 75 (alto riesgo)
- 2.5 = percentil 25 (bajo riesgo)
- Validados con datos de referencia de estudios europeos (EUROFOUND, 2018)

---

## 👥 Parámetros Demográficos

### Distribución de Empleados

```python
edad = N(34, 8).clip(22, 60)
experiencia = edad - inicio_carrera + ruido
antiguedad = experiencia * factor_estabilidad
genero = [55% Hombre, 40% Mujer, 5% No binario]
modalidad = [30% Presencial, 45% Híbrido, 25% Remoto]
```

**Justificación:**
- Distribuciones basadas en estadísticas laborales europeas (Eurostat, 2023)
- Modalidad refleja tendencia post-pandemia hacia trabajo híbrido
- Género refleja composición típica del sector tecnológico

### Distribución por Seniority

| Seniority | Experiencia | Rango Salarial |
|-----------|-------------|----------------|
| Junior | 0-2 años | 22k-35k € |
| Mid | 2-5 años | 30k-50k € |
| Senior | 5-10 años | 45k-70k € |
| Lead | 10+ años | 60k-95k € |

---

## 📈 Tamaño del Dataset

### Configuración por Defecto

```python
N_EMPRESAS_DEFAULT = 50      # por escenario
N_EMPLEADOS_DEFAULT = 2500   # por escenario
```

**Total:**
- 5 escenarios × 50 empresas = **250 empresas**
- 5 escenarios × 2500 empleados = **12,500 empleados**
- 12,500 × 43 preguntas = **537,500 respuestas**

**Justificación:**
- Tamaño suficiente para análisis estadístico robusto
- Permite segmentación por colectivos (género, edad, departamento)
- Representativo de población laboral real

---

## 🔍 Validación del Modelo

### Criterios de Validación

1. **Coherencia interna**: Correlaciones entre KPIs deben ser teóricamente esperadas
2. **Diferenciación de escenarios**: ANOVA debe mostrar diferencias significativas
3. **Clasificación correcta**: >90% de empresas clasificadas en su escenario esperado
4. **Distribuciones realistas**: Medias y desviaciones coherentes con literatura

### Resultados Esperados

- Precisión de clasificación: 95-98%
- Correlación Burnout-Bienestar: r ≈ -0.6 a -0.8
- Correlación Boreout-Bienestar: r ≈ -0.5 a -0.7
- Efect size (η²) entre escenarios: >0.14 (grande)

---

## 📚 Referencias

- Amabile, T. M. (1996). *A model of creativity and innovation in organizations*. Research in Organizational Behavior.
- Bakker, A. B., & Demerouti, E. (2007). *The Job Demands-Resources model: State of the art*. Journal of Managerial Psychology.
- Bloom, N., et al. (2015). *Does work from home work? Evidence from a Chinese experiment*. Quarterly Journal of Economics.
- EUROFOUND (2018). *Burnout and work-related stress*. European Foundation for the Improvement of Living and Working Conditions.
- Gajendran, R. S., & Harrison, D. A. (2007). *The good and the bad of telecommuting*. Journal of Applied Psychology.
- Karasek, R. A. (1979). *Job demands, job decision latitude, and mental strain*. Administrative Science Quarterly.
- Mobley, W. H. (1977). *Intermediate linkages in the decision to leave an organization*. Organizational Behavior and Human Performance.
- Oakman, J., et al. (2020). *A rapid review of the impact of remote work on mental health*. BMC Public Health.
- Rubio, H., et al. (2015). *Meta-analysis of turnover predictors*. Journal of Vocational Behavior.
- Schaufeli, W. B., & Taris, T. W. (2014). *A critical review of the Job Demands-Resources Model*. Advances in Occupational Health Research.

---

## 📝 Notas Técnicas

### Reproducibilidad

El generador usa semillas aleatorias para garantizar reproducibilidad:

```python
np.random.seed(42 + i)  # donde i es el índice del escenario
```

### Optimización de Rendimiento

- Generación vectorizada con NumPy (no bucles)
- Uso de Pandas para operaciones eficientes
- Exportación incremental por escenario

### Extensibilidad

El modelo permite añadir:
- Nuevos escenarios (añadir entrada en `config.py`)
- Nuevos efectos organizacionales (modificar diccionarios)
- Nuevas dimensiones de la encuesta (extender `encuesta.py`)



