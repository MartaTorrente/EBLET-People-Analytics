# 🧠 Pulso Laboral
### Plataforma de People Analytics para el análisis del bienestar laboral, burnout y boreout

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-orange)
![NumPy](https://img.shields.io/badge/NumPy-Scientific%20Computing-blueviolet)
![Status](https://img.shields.io/badge/Status-En%20desarrollo-success)
![License](https://img.shields.io/badge/License-MIT-green)

---

# 📖 Descripción

**Pulso Laboral** es un proyecto de **People Analytics** orientado al estudio del bienestar laboral mediante la generación y análisis de datos sintéticos basados en un instrumento propio denominado **EBLET (Encuesta de Bienestar Laboral y Experiencia en el Trabajo)**.

El objetivo es desarrollar una plataforma capaz de simular organizaciones completas, generar respuestas realistas a un cuestionario de bienestar laboral y obtener indicadores psicométricos que permitan analizar fenómenos como:

- Burnout
- Boreout
- Bienestar laboral
- Autoeficacia
- Intención de rotación

Todo ello respetando relaciones estadísticas y psicométricas coherentes con la literatura científica.

---

# 🎯 Objetivos

## Objetivo general

Diseñar una plataforma de simulación y análisis de datos de Recursos Humanos que permita estudiar el bienestar organizacional mediante técnicas de análisis de datos y People Analytics.

## Objetivos específicos

- Diseñar un instrumento de evaluación del bienestar laboral (EBLET).
- Simular organizaciones con características realistas.
- Generar empleados con perfiles laborales coherentes.
- Simular respuestas individuales a una encuesta de bienestar.
- Calcular indicadores psicométricos.
- Validar estadísticamente el instrumento.
- Crear datasets listos para análisis exploratorio, visualización y Machine Learning.

---

# 🚀 Misión

Crear una herramienta abierta que permita practicar técnicas de análisis de datos aplicadas al ámbito de Recursos Humanos utilizando datos sintéticos pero estadísticamente coherentes.

El proyecto pretende servir como puente entre:

- Psicología Organizacional
- People Analytics
- Ciencia de Datos
- Machine Learning
- Business Intelligence

---

# 🌍 Alcance

Actualmente el proyecto permite generar empresas ficticias pertenecientes al sector tecnológico español.

Cada organización posee características propias:

- ciudad
- sector
- cultura organizacional
- tamaño

Cada empleado dispone de variables como:

- género
- edad
- experiencia
- antigüedad
- modalidad de trabajo
- departamento
- puesto
- seniority
- salario
- tamaño del equipo

Posteriormente cada empleado responde al cuestionario EBLET.

---

# 📋 Instrumento EBLET

El instrumento desarrollado consta de **48 preguntas** distribuidas en siete bloques.

## Sección 1

Información laboral

Variables sociodemográficas y profesionales.

---

## Sección 2

Hábitos saludables

- sueño
- ejercicio
- vacaciones
- apoyo psicológico
- utilización del servicio

---

## Sección 3

Organización del trabajo

Dimensiones evaluadas:

- apoyo del responsable
- equilibrio vida-trabajo
- autonomía
- apoyo social
- presión laboral

---

## Sección 4

Burnout

Basado en el **Maslach Burnout Inventory – General Survey (MBI-GS)**.

Dimensiones:

- Agotamiento emocional
- Cinismo
- Baja eficacia profesional

---

## Sección 5

Boreout

Basado en los trabajos de:

- Rothlin & Werder
- Bianchi et al.

Dimensiones:

- Desinterés
- Falta de reto
- Infraocupación

---

## Sección 6

Bienestar

Incluye:

- satisfacción laboral
- autoeficacia

---

## Sección 7

Intención de cambio

Evalúa la probabilidad de abandonar la organización.

---

# 📊 Arquitectura del proyecto

El proyecto genera cuatro tablas relacionadas mediante identificadores únicos.

## Empresas

```
empresa_id
nombre
ciudad
sector
cultura
tamaño
```

---

## Empleados

```
empleado_id
empresa_id

género
edad
experiencia
antigüedad

departamento
puesto
seniority

modalidad
salario
tamaño_equipo
```

---

## Encuestas

```
encuesta_id
empleado_id

Q1
Q2
...
Q48
```

---

## Scores

```
encuesta_id
empleado_id

Manager Support
Work-Life Balance
Autonomy
Social Support
Pressure

Burnout

Exhaustion
Cynicism
Reduced Efficacy
Global

Boreout

Disinterest
Lack of Challenge
Underload
Global

Wellbeing

Job Satisfaction
Self-Efficacy
Global

Turnover Intention
```

---

# 🧮 Metodología

El modelo sigue un enfoque de simulación basado en variables latentes.

Cada empleado recibe un perfil psicológico oculto:

- Healthy
- Engaged
- Burnout
- Boreout

Este perfil modifica variables como:

- presión
- autonomía
- satisfacción
- equilibrio vida-trabajo
- apoyo social
- apoyo del responsable

Posteriormente dichas variables generan las respuestas individuales del cuestionario mediante modelos probabilísticos con ruido controlado.

Finalmente se calculan los indicadores psicométricos correspondientes.

---

# 📈 Validación

El proyecto incorpora un proceso de validación automática que incluye:

- Estadísticos descriptivos
- Distribuciones
- Correlaciones esperadas
- Consistencia interna
- Alfa de Cronbach
- Análisis Factorial Exploratorio (próximamente)
- Índice KMO (próximamente)
- Test de Bartlett (próximamente)

---

# 🤖 Aplicaciones

Los datos generados pueden utilizarse para:

- Análisis Exploratorio de Datos (EDA)
- Dashboards en Power BI
- Machine Learning
- Clustering
- Predicción de burnout
- Predicción de rotación
- People Analytics
- Validación psicométrica
- Portfolio de Data Analytics

---

# 🛠 Tecnologías

- Python
- Pandas
- NumPy
- SciPy
- Matplotlib
- Scikit-Learn
- Power BI

---

# 📁 Estructura del repositorio

```
Pulso-Laboral/

│
├── config.py
├── generador_empresas.py
├── generador_empleados.py
├── generador_encuestas.py
├── scoring.py
├── validacion.py
├── analisis_psicometrico.py
├── main.py
│
├── empresas.csv
├── empleados.csv
├── encuestas.csv
├── scores.csv
│
├── README.md
└── LICENSE
```

---

# 🔮 Próximas mejoras

- Dashboard interactivo en Power BI.
- Predicción de burnout mediante Machine Learning.
- Predicción de intención de rotación.
- Segmentación de empleados mediante clustering.
- Análisis Factorial Confirmatorio (CFA).
- Validación completa del instrumento EBLET.
- Generación de informes automáticos en PDF.
- API para generación de datasets personalizados.

---

# 📄 Licencia

Este proyecto se distribuye bajo licencia **MIT**.

---

# 👨‍💻 Autor

Proyecto desarrollado como iniciativa de aprendizaje y portfolio en **Data Analytics**, **People Analytics** y **Psicometría aplicada a Recursos Humanos**.

---

> *"No se puede mejorar aquello que no se mide. Pulso Laboral nace con el objetivo de convertir el bienestar organizacional en información útil para la toma de decisiones basada en datos."*
