# 🧠 EBLET - People Analytics: Análisis del Bienestar Laboral en el Sector Tecnológico Español

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?logo=powerbi)
![Pandas](https://img.shields.io/badge/Pandas-2.3.3-150458?logo=pandas)
![NumPy](https://img.shields.io/badge/NumPy-2.3.3-013243?logo=numpy)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter)

**Proyecto Final del Curso de Análisis de Datos**  
*Autora: Marta Torrente | Julio 2026*

</div>

---

## 📋 Tabla de Contenidos

- [🎯 Descripción del Proyecto](#-descripción-del-proyecto)
- [🔍 Contexto y Justificación](#-contexto-y-justificación)
- [🎯 Objetivos](#-objetivos)
- [🔬 Metodología](#-metodología)
- [📊 Dataset Sintético](#-dataset-sintético)
- [🛠️ Tecnologías Utilizadas](#️-tecnologías-utilizadas)
- [📁 Estructura del Repositorio](#-estructura-del-repositorio)
- [🚀 Instalación y Uso](#-instalación-y-uso)
- [📈 Resultados Clave](#-resultados-clave)
- [💼 Aportación Empresarial](#-aportación-empresarial)
- [📚 Referencias Bibliográficas](#-referencias-bibliográficas)
- [📄 Licencia](#-licencia)

---

## 🎯 Descripción del Proyecto

**EBLET (Encuesta de Bienestar Laboral y Experiencia en el Trabajo)** es un proyecto de People Analytics que analiza la relación entre **Burnout** (agotamiento laboral) y **Boreout** (aburrimiento laboral) y su impacto en la intención de rotación de empleados del sector tecnológico español.

El proyecto combina:
- 🧪 **Generación de datos sintéticos** con propiedades psicométricas validadas
- 📊 **Análisis exploratorio** en Jupyter Notebook
- 🎨 **Dashboard interactivo** en Power BI
- 📝 **Informe científico** con hallazgos y recomendaciones

---

## 🔍 Contexto y Justificación

La rotación laboral en el sector tecnológico español supera el **20% anual**, generando costes estimados de **18.000€ por empleado** en procesos de selección y formación. Sin embargo, las estrategias de retención tradicionales se centran casi exclusivamente en el **Burnout**, ignorando un fenómeno igualmente dañino: el **Boreout** (aburrimiento por falta de retos).

Este proyecto aborda esa brecha analizando **ambos constructos de forma simultánea**, demostrando que son fenómenos psicológicos opuestos que requieren **estrategias de intervención diferenciadas**.

---

## 🎯 Objetivos

1. **Diseñar una encuesta psicométrica** (EBLET) basada en escalas validadas (MBI-GS, Rothlin & Werder)
2. **Generar un dataset sintético** de 2.500 empleados con propiedades estadísticas realistas
3. **Validar la consistencia interna** de las escalas mediante Alfa de Cronbach
4. **Analizar la correlación** entre Burnout y Boreout (hipótesis: correlación negativa)
5. **Cuantificar el impacto financiero** de la rotación en las empresas
6. **Proponer recomendaciones** de RRHH basadas en datos

---

## 🔬 Metodología

### Diseño de la Encuesta EBLET (48 ítems)

| Sección | Preguntas | Escala | Referencia Teórica |
|---------|-----------|--------|-------------------|
| Información laboral | Demográficas | Mixta | - |
| Hábitos saludables | Q1-Q5 | Mixta (no Likert) | - |
| Organización del trabajo | Q6-Q20 | Likert 1-5 | - |
| **Burnout** | Q21-Q29 | Likert 1-5 | **MBI-GS** (Schaufeli et al., 1996) |
| **Boreout** | Q30-Q38 | Likert 1-5 | **Rothlin & Werder** (2007) |
| Bienestar y Autoeficacia | Q39-Q45 | Likert 1-5 | **Bandura** (1997) |
| Intención de cambio | Q46-Q48 | Likert 1-5 | - |

### Modelo de Datos (Esquema en Estrella)

```
┌─────────────┐         ┌─────────────┐
│  empresas   │1      * │  empleados  │
│  (50 regs)  ├─────────┤  (2500 regs)│
└─────────────┘         └──────┬──────┘
                               │1
                               │
                           *   │   *
                    ┌──────────┴──────────┐
                    │                     │
             ┌──────┴──────┐       ┌──────┴──────┐
             │  encuestas  │1    1 │   scores    │
             │  (2500 regs)├───────┤  (2500 regs)│
             └─────────────┘       └─────────────┘
```

---

## 📊 Dataset Sintético

El dataset contiene **4 tablas** con las siguientes características:

| Tabla | Registros | Columnas | Descripción |
|-------|-----------|----------|-------------|
| `empresas.csv` | 50 | 6 | Datos de empresas tech españolas |
| `empleados.csv` | 2.500 | 10 | Datos demográficos y laborales |
| `encuestas.csv` | 2.500 | 50 | Respuestas a las 48 preguntas |
| `scores.csv` | 2.500 | 13 | Índices calculados (Burnout, Boreout, etc.) |

### Propiedades Psicométricas Validadas

- ✅ **Correlación Burnout-Boreout**: -0.20 (constructos opuestos)
- ✅ **Alfa de Cronbach Burnout**: 0.98 (excelente fiabilidad)
- ✅ **Alfa de Cronbach Boreout**: 0.95 (excelente fiabilidad)
- ✅ **Tasa de rotación alta**: ~20% (realista para el sector)

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Uso |
|------------|-----|
| **Python 3.13** | Generación del dataset y análisis |
| **Pandas** | Manipulación de datos |
| **NumPy** | Cálculos estadísticos y generación aleatoria |
| **Matplotlib/Seaborn** | Visualizaciones en Jupyter |
| **Jupyter Notebook** | Análisis exploratorio documentado |
| **Power BI** | Dashboard interactivo |
| **DAX** | Medidas y cálculos en Power BI |
| **Git/GitHub** | Control de versiones y entrega |

---

## 📁 Estructura del Repositorio

```
EBLET-People-Analytics/
│
├── 📄 README.md                    ← Este archivo
│
├── 📁 01_generacion/
│   ├── generar_dataset.py          ← Script principal de generación
│   ├── config.py                   ← Configuración y parámetros
│   └── validacion.py               ← Validación psicométrica
│
├── 📁 02_datos/
│   ├── empresas.csv                ← 50 empresas
│   ├── empleados.csv               ← 2.500 empleados
│   ├── encuestas.csv               ← 2.500 encuestas (48 preguntas)
│   └── scores.csv                  ← Índices calculados
│
├── 📁 03_analisis/
│   └── analisis_EBLET.ipynb        ← Análisis exploratorio completo
│
├── 📁 04_powerbi/
│   ├── dashboard_EBLET.pbix        ← Archivo de Power BI
│   ├── dashboard_EBLET.pdf         ← Exportación del dashboard
│   └── formulas_DAX.md             ← Documentación de medidas DAX
│
├── 📁 05_informe/
│   └── informe_final.pdf           ← Informe científico (4 páginas)
│
└── 📁 06_presentacion/
    └── presentacion_defensa.pdf    ← Diapositivas para la defensa
```

---

## 🚀 Instalación y Uso

### Prerrequisitos

- Python 3.10 o superior
- Power BI Desktop (para el dashboard)

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/EBLET-People-Analytics.git
cd EBLET-People-Analytics
```

### 2. Instalar dependencias

```bash
pip install pandas numpy matplotlib seaborn scipy jupyter
```

### 3. Generar el dataset

```bash
cd 01_generacion
python generar_dataset.py
```

Los 4 archivos CSV se generarán en la carpeta `02_datos/`.

### 4. Ejecutar el análisis exploratorio

```bash
cd ../03_analisis
jupyter notebook analisis_EBLET.ipynb
```

### 5. Abrir el dashboard en Power BI

Abrir el archivo `04_powerbi/dashboard_EBLET.pbix` con Power BI Desktop.

---

## 📈 Resultados Clave

### 1. Correlación Burnout-Boreout: **-0.20**

![Correlación](https://via.placeholder.com/600x300?text=Scatter+Plot+Burnout+vs+Boreout)

Se confirma la hipótesis de que son **constructos opuestos**: empleados con alto Burnout tienden a tener bajo Boreout, y viceversa.

### 2. Distribución por Seniority

| Seniority | Burnout Medio | Boreout Medio | Rotación Alta |
|-----------|---------------|---------------|---------------|
| Junior    | **3.2**       | 1.8           | 28%           |
| Mid       | 2.6           | 2.1           | 22%           |
| Senior    | 2.1           | **2.8**       | 18%           |
| Lead      | 1.9           | **3.1**       | 15%           |

**Hallazgo clave**: Los perfiles **Senior y Lead** presentan los niveles más altos de **Boreout**, mientras que los **Junior** sufren más **Burnout**.

### 3. Impacto Financiero

- **Empleados con alta intención de rotación**: ~500 (20%)
- **Coste estimado de rotación**: **~9.000.000€** para las 50 empresas analizadas
- **Coste medio por empleado**: 18.000€

### 4. Factores de Riesgo Identificados

- 🔴 **Alta presión laboral** → Burnout (r = 0.96)
- 🔴 **Baja autonomía** → Burnout (r = -0.96)
- 🔵 **Bajo bienestar** → Boreout (r = -0.39)
- 🔵 **Modalidad Remota** → Mayor Boreout en Seniors

---

## 💼 Aportación Empresarial

### Recomendaciones de RRHH basadas en datos:

#### Para empleados con **Burnout** (principalmente Juniors):
1. ✅ Implementar políticas de **desconexión digital**
2. ✅ Ofrecer **apoyo psicológico** (solo 40% de empresas lo ofrece)
3. ✅ Reducir **plazos ajustados** y carga laboral excesiva
4. ✅ Fomentar el **feedback constructivo** del manager

#### Para empleados con **Boreout** (principalmente Seniors/Leads):
1. ✅ Diseñar **planes de carrera** con nuevos desafíos
2. ✅ Asignar **proyectos de mentoring** (aprovechar su experiencia)
3. ✅ Ofrecer **formación continua** en tecnologías emergentes
4. ✅ Permitir mayor **autonomía** en la organización del trabajo

### Impacto esperado:
- Reducción del **30%** en la intención de rotación
- Ahorro estimado de **~2.7M€** anuales en costes de reemplazo
- Mejora del **clima laboral** y la productividad

---

## 📚 Referencias Bibliográficas

- Bandura, A. (1997). *Self-efficacy: The exercise of control*. W.H. Freeman.
- Bianchi, R., et al. (2019). Boreout: A systematic review. *Journal of Occupational Health Psychology*.
- Maslach, C., & Leiter, M. P. (2016). Understanding the burnout experience. *World Psychiatry*, 15(2), 103-115.
- Rothlin, P., & Werder, R. (2007). *Boreout: Overcoming the Drift from Underwork at Work*. Springer.
- Schaufeli, W. B., et al. (1996). The measurement of burnout: A review. *European Journal of Work and Organizational Psychology*.

---

## 📄 Licencia

Este proyecto ha sido desarrollado como trabajo final del **Curso de Análisis de Datos** (2026).  
El código y los datos sintéticos son de libre uso con fines educativos, citando la fuente.

---

<div align="center">

**¿Te ha gustado el proyecto?** ¡Déjame una ⭐ en el repositorio!

*Desarrollado con ❤️ usando Python y Power BI*

</div>
