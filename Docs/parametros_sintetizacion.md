# 📊 Parámetros de Sintetización de Datos - EBLET v2.0

## Justificación Metodológica de los Datos Sintéticos

**Versión:** 2.0  
**Fecha:** Julio 2026

---

## 1. Objetivo

Crear datasets sintéticos realistas que representen 5 escenarios organizacionales distintos, permitiendo:
- Validar el funcionamiento del framework
- Establecer puntos de referencia (benchmarks)
- Comparar resultados de organizaciones reales
- Cuantificar el impacto económico de la rotación

---

## 2. Arquitectura del Modelo de Generación

### Flujo de Generación

```
1. Definir Empresa (metadata: sector, tamaño, cultura CVF)
   ↓
2. Asignar Escenario Objetivo (1-5)
   ↓
3. Generar Empleados con perfiles demográficos
   ↓
4. Aplicar Modelo Psicológico (efectos organizacionales)
   ↓
5. Generar Respuestas a la Encuesta (64 preguntas Likert)
   ↓
6. Calcular KPIs por Empleado
   ↓
7. Calcular Costes de Rotación por Empleado
   ↓
8. Agregar KPIs y Costes a Nivel Empresa
   ↓
9. Validar Clasificación en Escenario
   ↓
10. Exportar Dataset
```

---

## 3. Parámetros de Escenarios Organizacionales

### 3.1 Valores Base por Escenario

Cada escenario tiene valores base para los 4 KPIs principales (escala 1-5):

| Escenario | Burnout | Boreout | Bienestar | Rotación | Justificación |
|-----------|---------|---------|-----------|----------|---------------|
| 🟢 **Saludable** | 1.8 | 1.7 | 4.3 | 1.5 | Muy por debajo de umbrales de riesgo |
| 🟡 **Estable** | 2.5 | 2.2 | 3.4 | 2.3 | Media poblacional típica |
| 🟠 **Riesgo Burnout** | 4.2 | 1.7 | 2.3 | 4.0 | Por encima del umbral MBI-GS (3.86) |
| 🔵 **Riesgo Boreout** | 1.5 | 4.3 | 2.3 | 3.8 | Por encima del umbral EAL (3.0) |
| 🔴 **Crítico** | 4.5 | 4.3 | 1.8 | 4.7 | Ambos problemas simultáneos |

### 3.2 Mezcla de Culturas CVF por Escenario

| Escenario | Adhocracia | Clan | Jerárquica | Mercado |
|-----------|------------|------|------------|---------|
| Saludable | 0.30 | **0.50** | 0.10 | 0.10 |
| Estable | 0.20 | 0.30 | 0.25 | 0.25 |
| Riesgo Burnout | 0.10 | 0.15 | 0.25 | **0.50** |
| Riesgo Boreout | 0.15 | 0.15 | **0.50** | 0.20 |
| Crítico | 0.05 | 0.05 | 0.30 | **0.60** |

**Justificación:** Las culturas CVF (Cameron & Quinn, 2011) tienen efectos predecibles sobre el bienestar, calibrados según la literatura del modelo JD-R.

---

## 4. Efectos Psicológicos Organizacionales

### 4.1 Efecto de la Cultura (CVF)

```python
CULTURE_EFFECTS = {
    "Adhocracia":  {"burnout": -0.15, "boreout": -0.10, "wellbeing": +0.20},
    "Clan":        {"burnout": -0.25, "boreout": -0.10, "wellbeing": +0.30},
    "Jerarquica":  {"burnout": +0.15, "boreout": +0.10, "wellbeing": -0.15},
    "Mercado":     {"burnout": +0.35, "boreout": -0.05, "wellbeing": -0.35}
}
```

**Justificación:**
- **Clan**: El apoyo social es el recurso #1 contra el burnout (Bakker & Demerouti, 2007)
- **Adhocracia**: La autonomía y creatividad reducen el aburrimiento (Amabile, 1996)
- **Mercado**: La presión por resultados incrementa el burnout (Maslach & Leiter, 2016)
- **Jerárquica**: La burocracia y rutina aumentan el boreout (Rothlin & Werder, 2007)

### 4.2 Efecto de la Modalidad de Trabajo

```python
MODALITY_EFFECTS = {
    "Presencial": {"burnout": +0.10, "boreout": -0.10, "wellbeing": -0.05},
    "Híbrido":    {"burnout": 0.00,  "boreout": 0.00,  "wellbeing": +0.15},
    "Remoto":     {"burnout": -0.10, "boreout": +0.20, "wellbeing": +0.05}
}
```

**Justificación:**
- **Presencial**: Más estrés por desplazamientos, pero menos aislamiento
- **Híbrido**: Equilibrio óptimo según estudios post-pandemia (Bloom, 2022)
- **Remoto**: Reduce burnout por flexibilidad, pero aumenta boreout por aislamiento (Oakman et al., 2020)

### 4.3 Efecto del Departamento

```python
DEPARTMENT_EFFECTS = {
    "Desarrollo": {"burnout": +0.20, "boreout": -0.10},
    "Datos":      {"burnout": +0.10, "boreout": 0.00},
    "Producto":   {"burnout": +0.15, "boreout": -0.05},
    "RRHH":       {"burnout": -0.10, "boreout": +0.10},
    "Ventas":     {"burnout": +0.30, "boreout": -0.15}
}
```

---

## 5. Modelo Psicológico

### 5.1 Variables Latentes

```python
L_burnout = N(burnout_base + efectos, σ=0.5)
L_boreout = N(boreout_base + efectos, σ=0.5)
L_wellbeing = N(wellbeing_base + efectos, σ=0.5)
L_rotation = f(L_burnout, L_boreout, L_wellbeing)
```

### 5.2 Fórmula de Rotación

Basada en la teoría de turnover de Mobley (1977):

```python
rotation = 1.5 + 0.35*burnout + 0.25*boreout + 0.30*(5-wellbeing) + noise
```

---

## 6. Cálculo de KPIs

### 6.1 KPIs a Nivel Empleado

```python
KPI_Contexto = mean(q6:q20)        # 15 preguntas (JD-R)
KPI_Burnout = mean(q21:q36)        # 16 preguntas (MBI-GS completo)
  # Con q30-q36 invertidas (eficacia profesional)
KPI_Boreout = mean(q37:q44) + mean(q60:q64)  # EAL + Infraocupación
KPI_Bienestar = mean(q45:q49) + mean(q50:q53)  # WHO-5 + Satisfacción
KPI_Rotacion = mean(q57:q59)       # 3 preguntas (Mobley)
```

### 6.2 KPIs a Nivel Empresa

```python
KPI_Empresa = mean(KPIs_empleados)
```

---

## 7. 💰 Modelo de Costes de Rotación

### 7.1 Base Metodológica

Los costes de rotación se calculan según las metodologías de:
- **SHRM** (Society for Human Resource Management): coste de reemplazo = 6-9 meses de salario
- **Gallup**: 50%-200% del salario anual
- **Cobee/Pluxee**: metodología detallada para empresas españolas

### 7.2 Fórmula Base

```python
Coste_Esperado_Empleado = (Salario × Factor_Perfil) × Probabilidad_Salida
```

### 7.3 Factores por Perfil (SHRM/Gallup)

| Seniority | Factor | Justificación |
|-----------|--------|---------------|
| **Junior** | 0.50 (50%) | Fácil de reemplazar, rampa corta |
| **Mid** | 0.75 (75%) | Conocimiento específico del puesto |
| **Senior** | 1.00 (100%) | Conocimiento crítico, difícil reemplazo |
| **Lead** | 1.50 (150%) | Impacto estratégico, muy difícil reemplazo |

### 7.4 Tasas de Rotación según KPI

| KPI Rotación | Tasa Anual Estimada |
|--------------|---------------------|
| 1.0 - 1.5 | 5% (muy baja) |
| 1.5 - 2.5 | 10% (normal) |
| 2.5 - 3.5 | 20% (alta) |
| 3.5 - 4.5 | 35% (muy alta) |
| 4.5 - 5.0 | 50% (crítica) |

### 7.5 Cálculo del ROI de Intervención

```python
ROI = (Ahorro - Coste_Intervención) / Coste_Intervención × 100
Ahorro = Coste_Actual × %_Reducción
Payback = Coste_Intervención / (Ahorro / 12)
```

### 7.6 Escenarios de Intervención

| Intervención | Coste | Reducción Esperada | ROI Esperado |
|--------------|-------|-------------------|--------------|
| Programa básico | 25% del coste actual | 20% | Positivo |
| Programa integral | 25% del coste actual | 35% | Alto |
| Transformación completa | 25% del coste actual | 50% | Muy alto |

---

## 8. Parámetros Demográficos

### 8.1 Distribución de Empleados

```python
edad = N(34, 8).clip(22, 60)
experiencia = edad - inicio_carrera + ruido
antiguedad = experiencia * factor_estabilidad
genero = [55% Hombre, 40% Mujer, 5% No binario]
modalidad = [30% Presencial, 45% Híbrido, 25% Remoto]
```

### 8.2 Rangos Salariales por Seniority

| Seniority | Experiencia | Rango Salarial |
|-----------|-------------|----------------|
| Junior | 0-2 años | 22k-35k € |
| Mid | 2-5 años | 30k-50k € |
| Senior | 5-10 años | 45k-70k € |
| Lead | 10+ años | 60k-95k € |

---

## 9. Tamaño del Dataset

### 9.1 Configuración por Defecto

```python
N_EMPRESAS_DEFAULT = 50      # por escenario
N_EMPLEADOS_DEFAULT = 2500   # por escenario
```

### 9.2 Totales

- 5 escenarios × 50 empresas = **250 empresas**
- 5 escenarios × 2500 empleados = **12,500 empleados**
- 12,500 × 64 preguntas = **800,000 respuestas**

---

## 10. Validación del Modelo

### 10.1 Criterios de Validación

1. **Coherencia interna**: Correlaciones entre KPIs teóricamente esperadas
2. **Diferenciación de escenarios**: ANOVA con diferencias significativas
3. **Clasificación correcta**: >90% de empresas clasificadas correctamente
4. **Fiabilidad psicométrica**: Alfa de Cronbach ≥ 0.70 en todas las dimensiones

### 10.2 Resultados Observados

- **Precisión de clasificación**: 92-100% por escenario
- **Fiabilidad (α)**: 0.795 - 0.933 (todos > 0.70)
- **Correlación Burnout-Bienestar**: r ≈ -0.72
- **Efect size (η²)**: > 0.14 (grande)

---

## 11. Reproducibilidad

El generador usa semillas aleatorias para garantizar reproducibilidad:

```python
np.random.seed(42 + i)  # donde i es el índice del escenario
```

---

## 12. Referencias

Cobee. (2024). *Calcular costes de rotación laboral*. https://cobee.io/blog/calcular-costes-rotacion-laboral/

Gallup. (2023). *State of the Global Workplace Report*.

SHRM. (2023). *Employee turnover cost benchmark report*. Society for Human Resource Management.

---

**Versión del documento:** 2.0  
**Última actualización:** Julio 2026