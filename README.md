# 🧠 EBLET - People Analytics Framework

## Framework de Referencia para el Bienestar Laboral y la Retención de Talento

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 Misión

Desarrollar un framework de People Analytics que permita:
- ✅ Evaluar el bienestar laboral mediante una encuesta estructurada (EBLET)
- ✅ Calcular indicadores de burnout, boreout y bienestar
- ✅ Generar automáticamente diagnósticos organizacionales
- ✅ Facilitar la toma de decisiones en Recursos Humanos

---

## 📋 Alcance

### Entradas
- **Encuesta EBLET**: 48 preguntas basadas en literatura científica
- **Datos demográficos y laborales** del empleado

### Procesamiento
- Cálculo automático de KPIs (Burnout, Boreout, Bienestar, Rotación, Contexto)
- Agregación por trabajador y por empresa
- Comparación con escenarios de referencia
- Segmentación por colectivos
- Generación de visualizaciones

### Salidas
- Dataset estructurado
- Indicadores cuantitativos
- Dashboard interactivo
- Informe automático
- Recomendaciones de intervención

---

## 🏢 Los 5 Escenarios Organizacionales

El framework clasifica las organizaciones en 5 escenarios basados en la combinación de burnout, boreout y bienestar:

| # | Escenario | Burnout | Boreout | Bienestar | Características |
|---|-----------|---------|---------|-----------|-----------------|
| 🟢 | **Saludable** | Bajo | Bajo | Alto | Organización óptima, alta retención |
| 🟡 | **Estable** | Moderado | Moderado | Medio | Funcional, margen de mejora |
| 🟠 | **Riesgo Burnout** | Alto | Bajo | Bajo | Sobrecarga laboral |
| 🔵 | **Riesgo Boreout** | Bajo | Alto | Bajo | Infraestimulación |
| 🔴 | **Crítico** | Alto | Alto | Muy bajo | Desalineación organizativa extrema |

---

## 🗂️ Estructura del Proyecto

```
EBLET-People-Analytics/
│
├── src/                           # Código fuente
│   ├── config.py                  # Configuración central (escenarios, umbrales)
│   ├── empresas.py                # Generador de empresas sintéticas
│   ├── empleados.py               # Generador de empleados con perfiles
│   ├── modelo_psicologico.py      # Modelo de estados latentes
│   ├── encuesta.py                # Generador de respuestas a la encuesta
│   ├── scores.py                  # Calculadora de KPIs
│   ├── exportador.py              # Exportador de datasets
│   ├── utils.py                   # Utilidades generales
│   └── generar_dataset.py         # Orquestador principal
│
├── datasets/                      # Datos generados
│   ├── saludable/                 # 2500 empleados
│   ├── estable/                   # 2500 empleados
│   ├── riesgo_burnout/            # 2500 empleados
│   ├── riesgo_boreout/            # 2500 empleados
│   └── critico/                   # 2500 empleados
│
├── notebooks/                     # Análisis exploratorio
│   ├── 01_EDA_comparativo.ipynb   # EDA + 6 gráficos comparativos
│   ├── 02_Analisis_profundo.ipynb # Análisis inferencial y predictivo
│   └── 03_Clustering.ipynb        # Identificación de perfiles
│
├── docs/                          # Documentación
│   ├── metodologia.md             # Marco teórico
│   ├── parametros_sintetizacion.md # Justificación de parámetros
│   └── manual_tecnico.md          # Guía técnica
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

### 2. Crear entorno virtual (recomendado)

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
- 5 carpetas en `datasets/` con CSVs estructurados

### Ejecutar análisis

```bash
# Abrir Jupyter
jupyter notebook

# Ejecutar notebooks en orden:
# 1. notebooks/01_EDA_comparativo.ipynb
# 2. notebooks/02_Analisis_profundo.ipynb
# 3. notebooks/03_Clustering.ipynb
```

---

## 🧪 Metodología

### Instrumento de Medición: EBLET

La **Encuesta de Bienestar Laboral y Experiencia en el Trabajo (EBLET)** consta de 48 preguntas organizadas en 7 secciones:

1. **Información laboral** (11 preguntas demográficas)
2. **Hábitos saludables** (5 preguntas)
3. **Organización del trabajo** (15 preguntas, Likert 1-5)
4. **Burnout** (9 preguntas, basado en MBI-GS)
5. **Boreout** (9 preguntas, basado en Rothlin & Werder)
6. **Bienestar y Autoeficacia** (7 preguntas)
7. **Intención de rotación** (3 preguntas)

### Modelo Psicológico

Basado en:
- **JD-R Model** (Demerouti et al., 2001)
- **Maslach Burnout Inventory** (Maslach et al., 1981)
- **Boreout Theory** (Rothlin & Werder, 2007)
- **Teoría de Turnover** (Mobley, 1977)

### Cálculo de KPIs

Cada KPI se calcula como la media de las preguntas correspondientes:

```python
KPI_Burnout = mean(q21:q29)
KPI_Boreout = mean(q30:q38)
KPI_Bienestar = mean(q39:q45)
KPI_Rotacion = mean(q46:q48)
KPI_Contexto = mean(q6:q20)
```

---

## 📈 Visualizaciones

El framework incluye 6 tipos de gráficos comparativos:

1. **Radar Chart**: KPIs medios por escenario
2. **Boxplots**: Distribución de Burnout y Boreout
3. **Stacked Bar**: Proporción de empleados en riesgo
4. **Heatmap**: Correlaciones entre dimensiones
5. **Scatter Plot**: Mapa de posicionamiento Burnout vs Boreout
6. **Bar Chart Segmentado**: KPIs por colectivos

---

## 📚 Referencias Bibliográficas

- Demerouti, E., et al. (2001). *The job demands-resources model of burnout*. Journal of Applied Psychology.
- Maslach, C., et al. (1981). *Maslach Burnout Inventory*. Consulting Psychologists Press.
- Rothlin, P., & Werder, G. (2007). *Boreout: Overcoming the Discontent of Underworked*. Redwheel/Weiser.
- Mobley, W. H. (1977). *Intermediate linkages in the decision to leave an organization*. Organizational Behavior and Human Performance.
- Schaufeli, W. B., et al. (1996). *Oldenburg Burnout Inventory*.
- Bandura, A. (1997). *Self-efficacy: The exercise of control*. W.H. Freeman.


---

## 👥 Autores

- **Marta Torrente** - *Proyecto Final Data Analyst* 








