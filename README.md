# 🧠 EBLET - People Analytics Framework v2.0

## Framework de Referencia para el Bienestar Laboral y la Retención de Talento

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 Misión

Desarrollar un framework de People Analytics que permita:
- ✅ Evaluar el bienestar laboral mediante instrumentos validados (MBI-GS, EAL, WHO-5)
- ✅ Calcular indicadores de burnout, boreout y bienestar
- ✅ Clasificar organizaciones en 5 escenarios de referencia
- ✅ Cuantificar el **coste económico de la rotación**
- ✅ Generar diagnósticos accionables para Recursos Humanos

---

## 📋 Alcance

### Entradas
- **Encuesta EBLET v2.0**: 64 preguntas basadas en literatura científica
- **Datos demográficos y laborales** del empleado

### Procesamiento
- Cálculo automático de 5 KPIs (Burnout, Boreout, Bienestar, Rotación, Contexto)
- Cálculo de costes de rotación por empleado (SHRM/Gallup)
- Clasificación en 5 escenarios organizacionales (basado en CVF de Cameron & Quinn)
- Análisis de ROI de intervenciones de bienestar
- Generación de visualizaciones comparativas

### Salidas
- Datasets estructurados (12,500 empleados, 250 empresas)
- Indicadores cuantitativos con base científica
- Dashboard interactivo en Power BI
- Informe científico con recomendaciones
- Análisis de costes y ROI

---

## 🏢 Los 5 Escenarios Organizacionales

El framework clasifica las organizaciones en 5 escenarios basados en la combinación de burnout, boreout y bienestar:

| # | Escenario | Burnout | Boreout | Bienestar | Características |
|---|-----------|---------|---------|-----------|-----------------|
| 🟢 | **Saludable** | Bajo (<2.5) | Bajo (<2.5) | Alto (>3.5) | Organización óptima |
| 🟡 | **Estable** | Moderado | Moderado | Medio | Funcional, margen de mejora |
| 🟠 | **Riesgo Burnout** | Alto (≥3.5) | Bajo (<2.5) | Bajo (<3.0) | Sobrecarga laboral |
| 🔵 | **Riesgo Boreout** | Bajo (<2.5) | Alto (≥3.5) | Bajo (<3.0) | Infraestimulación |
| 🔴 | **Crítico** | Alto (≥3.5) | Alto (≥3.5) | Muy bajo (<2.5) | Desalineación extrema |

---

## 📚 Bases Científicas

### Instrumentos Validados

| Instrumento | Dimensión | Referencia |
|-------------|-----------|------------|
| **MBI-GS** | Burnout | Schaufeli et al., 1996 |
| **EAL** | Aburrimiento Laboral | Martínez-Lugo & Rodríguez-Montalbán, 2017 |
| **WHO-5** | Bienestar | Topp et al., 2015 |
| **CVF** | Cultura Organizacional | Cameron & Quinn, 2011 |
| **JD-R** | Modelo General | Demerouti et al., 2001 |

### Umbrales Científicos

Los umbrales están calibrados con puntos de corte de instrumentos validados:
- **Burnout alto**: ≥ 3.86 (Percentil 75 del MBI-GS)
- **Boreout alto**: ≥ 3.00 (Umbral de la EAL)
- **Bienestar bajo**: < 2.60 (Umbral clínico del WHO-5)

---

## 💰 Costes de Rotación

El framework cuantifica el impacto económico del malestar laboral:

### Metodología
- Basada en **SHRM** (6-9 meses de salario por reemplazo)
- Basada en **Gallup** (50%-200% del salario anual)
- Basada en **Cobee/Pluxee** (metodología española)

### Factores por Perfil

| Seniority | Factor | Coste Estimado |
|-----------|--------|----------------|
| Junior | 50% salario | ~15,000€ |
| Mid | 75% salario | ~30,000€ |
| Senior | 100% salario | ~55,000€ |
| Lead | 150% salario | ~110,000€ |

### Resultados del Dataset Sintético

- **Coste total de rotación**: ~357M€ anuales
- **Coste medio por empleado**: ~28,600€
- **% sobre masa salarial**: ~44%
- **Ahorro potencial (30% reducción)**: ~107M€

---

## 🗂️ Estructura del Proyecto

```
EBLET-People-Analytics/
│
├── src/                           # Código fuente
│   ├── config.py                  # Configuración central (CVF, umbrales)
│   ├── empresas.py                # Generador de empresas sintéticas
│   ├── empleados.py               # Generador de empleados
│   ├── modelo_psicologico.py      # Modelo de estados latentes
│   ├── encuesta.py                # Generador de respuestas (64 preguntas)
│   ├── scores.py                  # Calculadora de KPIs
│   ├── costes_rotacion.py         # 💰 Módulo de costes (NUEVO)
│   ├── exportador.py              # Exportador de datasets
│   ├── exportar_para_powerbi.py   # Exportador para Power BI
│   ├── generar_dataset.py         # Orquestador principal
│   └── utils.py                   # Utilidades
│
├── datasets/                      # Datos generados
│   ├── saludable/                 # 2500 empleados
│   ├── estable/                   # 2500 empleados
│   ├── riesgo_burnout/            # 2500 empleados
│   ├── riesgo_boreout/            # 2500 empleados
│   └── critico/                   # 2500 empleados
│
├── powerbi_data/                  # Datos normalizados para Power BI
│   ├── dim_empleados.csv
│   ├── dim_empresas.csv
│   ├── dim_encuesta.csv
│   ├── fact_kpis.csv              # Con costes de rotación
│   ├── costes_empresa.csv         # 💰 NUEVO
│   ├── costes_escenario.csv       # 💰 NUEVO
│   ├── recomendaciones_roi.csv    # 💰 NUEVO
│   └── resumen_empresas.csv
│
├── notebooks/                     # Análisis exploratorio
│   ├── 01_EDA_comparativo.ipynb   # EDA + 6 gráficos comparativos
│   ├── 02_Analisis_profundo.ipynb # ANOVA, fiabilidad, factorial
│   ├── 03_Clustering.ipynb        # Identificación de perfiles
│   └── 04_Analisis_Costes.ipynb   # 💰 Análisis económico (NUEVO)
│
├── docs/                          # Documentación
│   ├── metodologia.md             # Marco teórico + CVF
│   ├── parametros_sintetizacion.md # Justificación + costes
│   ├── encuesta_eblet.md          # Encuesta completa
│   ├── formulas_dax.md            # Fórmulas Power BI
│   └── estructura_presentacion.md # Guía de defensa
│
├── requirements.txt               # Dependencias Python
└── README.md                      # Este archivo
```

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/EBLET-People-Analytics.git
cd EBLET-People-Analytics
```

### 2. Crear entorno virtual

```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# Mac/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 📊 Uso Rápido

### Generar datasets sintéticos

```bash
python src/generar_dataset.py
```

Esto generará:
- 5 escenarios × 50 empresas × 50 empleados = **12,500 empleados**
- Cálculo de costes de rotación por empleado
- Análisis de fiabilidad (Alfa de Cronbach)
- Validación de clasificación de escenarios

### Exportar para Power BI

```bash
python src/exportar_para_powerbi.py
```

Genera CSVs optimizados para importar en Power BI.

### Ejecutar análisis

```bash
jupyter notebook

# Ejecutar notebooks en orden:
# 1. notebooks/01_EDA_comparativo.ipynb
# 2. notebooks/02_Analisis_profundo.ipynb
# 3. notebooks/03_Clustering.ipynb
# 4. notebooks/04_Analisis_Costes.ipynb
```

---

## 🧪 Metodología

### Instrumento de Medición: EBLET v2.0

La encuesta consta de **64 preguntas Likert** organizadas en 7 secciones:

1. **Información laboral** (12 preguntas demográficas)
2. **Hábitos saludables** (5 preguntas)
3. **Contexto organizacional** (15 preguntas, JD-R Model)
4. **Burnout** (16 preguntas, **MBI-GS completo**)
5. **Aburrimiento laboral** (8 preguntas, **EAL completo**)
6. **Bienestar** (5 preguntas, **WHO-5 completo**)
7. **Satisfacción + Autoeficacia** (7 preguntas)
8. **Intención de rotación** (3 preguntas, Mobley)
9. **Infraocupación** (5 preguntas, Rothlin & Werder)

### Cultura Organizacional (CVF)

Basado en el **Competing Values Framework** de Cameron & Quinn (2011):

- **Adhocracia** (Innovadora): Creatividad, riesgo, innovación
- **Clan** (Colaborativa): Cohesión, mentoría, apoyo
- **Jerárquica** (Tradicional): Procesos, estabilidad, control
- **Mercado** (Exigente): Resultados, competitividad, logro

### Cálculo de KPIs

```python
KPI_Contexto = mean(q6:q20)
KPI_Burnout = mean(q21:q36)  # MBI-GS completo (con inversión)
KPI_Boreout = mean(q37:q44) + mean(q60:q64)  # EAL + Infraocupación
KPI_Bienestar = mean(q45:q49) + mean(q50:q53)  # WHO-5 + Satisfacción
KPI_Rotacion = mean(q57:q59)
```

---

## 📈 Visualizaciones

### 6 Gráficos Comparativos

1. **Radar Chart**: KPIs medios por escenario
2. **Boxplots**: Distribución de Burnout y Boreout
3. **Stacked Bar**: Proporción de empleados en riesgo
4. **Heatmap**: Correlaciones entre dimensiones
5. **Scatter Plot**: Mapa de posicionamiento Burnout vs Boreout
6. **Bar Chart Segmentado**: KPIs por colectivos

### Dashboard Power BI

- KPIs principales con formato condicional
- Análisis de costes por escenario
- Análisis de ROI de intervenciones
- Drill-down por empresa, departamento, seniority

---

## 📚 Referencias Bibliográficas

Bakker, A. B., & Demerouti, E. (2007). The Job Demands-Resources model: State of the art. *Journal of Managerial Psychology, 22*(3), 309-328.

Cameron, K. S., & Quinn, R. E. (2011). *Diagnosing and changing organizational culture: Based on the competing values framework* (3rd ed.). Jossey-Bass.

Demerouti, E., et al. (2001). The job demands-resources model of burnout. *Journal of Applied Psychology, 86*(3), 499-512.

Martínez-Lugo, I., & Rodríguez-Montalbán, J. (2017). Cuando el trabajo aburre: Análisis de las propiedades psicométricas de la EAL. *Revista Interamericana de Psicología*.

Maslach, C., & Leiter, M. P. (2016). Understanding the burnout experience. *World Psychiatry, 15*(2), 103-111.

Rothlin, P., & Werder, G. (2007). *Boreout: Overcoming the discontent of underworked*. Redwheel/Weiser.

Schaufeli, W. B., et al. (1996). Maslach Burnout Inventory-General Survey. *MBI manual*.

Topp, C. W., et al. (2015). The WHO-5 Well-Being Index: A systematic review. *Psychotherapy and Psychosomatics, 84*(3), 167-176.

---

## 👥 Autora

- **Marta Torrente** - *Proyecto final Data Analyst* 
