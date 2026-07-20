"""
Módulo de configuración central del framework EBLET.
===================================================

Centraliza todos los parámetros utilizados:

- Estructura de la encuesta.
- Dimensiones psicométricas.
- Escenarios organizacionales.
- Parámetros de simulación.
- Umbrales de clasificación.
- Efectos de cultura organizacional.
- Costes de rotación.

Modificar este archivo permite ajustar el comportamiento del framework
sin alterar la lógica de los algoritmos.

"""
from pathlib import Path

print("📁 Directorio actual:", Path.cwd().resolve())
print(
    "📁 Ruta real de datasets:",
    (Path.cwd() / "datasets").resolve()
)

# 1. ESTRUCTURA DE LA ENCUESTA 


# Rangos de preguntas por dimensión (numeración Likert 1-67)
PREGUNTAS = {
    "contexto":           {"rango": range(1, 16),   "n_items": 15},  # q1-q15
    "burnout_agotam":     {"rango": range(16, 23),  "n_items": 7},   # q16-q22
    "burnout_cinismo":    {"rango": range(23, 30),  "n_items": 7},   # q23-q29
    "burnout_ineficacia": {"rango": range(30, 37),  "n_items": 7,    # q30-q36 (INVERTIR)
                           "invertir": True},
    "aburrimiento_eal":   {"rango": range(37, 45),  "n_items": 8},   # q37-q44
    "bienestar_who5":     {"rango": range(45, 50),  "n_items": 5},   # q45-q49
    "satisfaccion":       {"rango": range(50, 54),  "n_items": 4},   # q50-q53
    "autoeficacia":       {"rango": range(54, 57),  "n_items": 3},   # q54-q56
    "rotacion":           {"rango": range(57, 60),  "n_items": 3},   # q57-q59
    "cvf_adhocracia":  {"rango": range(60, 62), "n_items": 2},
    "cvf_clan":        {"rango": range(62, 64), "n_items": 2},
    "cvf_mercado":     {"rango": range(64, 66), "n_items": 2},
    "cvf_jerarquica":  {"rango": range(66, 68), "n_items": 2},
}

# Total de preguntas Likert
N_PREGUNTAS_LIKERT = 67



# 2. ESCENARIOS ORGANIZACIONALES

# Valores base calibrados con puntos de corte de instrumentos validados:


SCENARIOS = {
    "saludable": {
        "burnout_base": 1.8,       # Muy por debajo del umbral alto (3.86)
        "boreout_base": 1.7,       # Muy por debajo del umbral (3.0)
        "wellbeing_base": 4.3,     # Muy por encima del umbral bajo (2.6)
        "rotation_base": 1.5,
        "culture_mix": {
            "Adhocracia": 0.30,
            "Clan": 0.50,
            "Jerarquica": 0.10,
            "Mercado": 0.10
        }
    },
    "estable": {
        "burnout_base": 2.5,
        "boreout_base": 2.2,
        "wellbeing_base": 3.4,
        "rotation_base": 2.3,
        "culture_mix": {
            "Adhocracia": 0.20,
            "Clan": 0.30,
            "Jerarquica": 0.25,
            "Mercado": 0.25
        }
    },
    "riesgo_burnout": {
        "burnout_base": 4.2,       # Alto burnout (por encima de 3.86)
        "boreout_base": 1.7,       # AJUSTADO: bien por debajo del umbral 2.0
        "wellbeing_base": 2.3,     # AJUSTADO: por debajo del umbral 3.0
        "rotation_base": 4.0,
        "culture_mix": {
            "Adhocracia": 0.10,
            "Clan": 0.15,
            "Jerarquica": 0.25,
            "Mercado": 0.50        # Cultura de Mercado predomina
        }
    },
        "riesgo_boreout": {
        "burnout_base": 1.5,       # AJUSTADO: de 1.8 a 1.5 
        "boreout_base": 4.3,       # Alto boreout (por encima de 3.0)
        "wellbeing_base": 2.3,     # Por debajo del umbral 3.0
        "rotation_base": 3.8,
        "culture_mix": {
            "Adhocracia": 0.15,
            "Clan": 0.15,
            "Jerarquica": 0.50,    # Cultura Jerárquica predomina
            "Mercado": 0.20
        }
    
    },
    "critico": {
        "burnout_base": 4.5,       # Máximo riesgo
        "boreout_base": 4.3,
        "wellbeing_base": 1.8,
        "rotation_base": 4.7,
        "culture_mix": {
            "Adhocracia": 0.05,
            "Clan": 0.05,
            "Jerarquica": 0.30,
            "Mercado": 0.60        # Cultura de Mercado extrema
        }
    }
}

CODIGOS_ESCENARIO = {
    "saludable": "SAL",
    "estable": "EST",
    "riesgo_burnout": "RBU",
    "riesgo_boreout": "RBO",
    "critico": "CRI",
}

# 3. EFECTOS DE CULTURA ORGANIZACIONAL (CVF - Cameron y Quinn)

# Basado en el Competing Values Framework:
# - Adhocracia: Externo + Flexible → Innovación, creatividad
# - Clan: Interno + Flexible → Cohesión, apoyo
# - Jerarquica: Interno + Control → Procesos, estabilidad
# - Mercado: Externo + Control → Resultados, competitividad

CULTURE_EFFECTS = {
    # Adhocracia (Innovadora): Autonomía y creatividad protegen
    "Adhocracia":  {"burnout": -0.15, "boreout": -0.10, "wellbeing": +0.20},
    
    # Clan (Colaborativa): Apoyo social es el recurso #1 contra burnout
    "Clan":        {"burnout": -0.25, "boreout": -0.10, "wellbeing": +0.30},
    
    # Jerarquica (Tradicional): Burocracia y rutina aumentan boreout
    "Jerarquica":  {"burnout": +0.15, "boreout": +0.10, "wellbeing": -0.15},
    
    # Mercado (Exigente): Presión por resultados erosiona bienestar
    "Mercado":     {"burnout": +0.35, "boreout": -0.05, "wellbeing": -0.35}
}

#
# 4. EFECTOS DE MODALIDAD DE TRABAJO



MODALITY_EFFECTS = {
    "Presencial": {"burnout": +0.10, "boreout": -0.10, "wellbeing": -0.05},
    "Híbrido":    {"burnout": 0.00,  "boreout": 0.00,  "wellbeing": +0.15},
    "Remoto":     {"burnout": -0.10, "boreout": +0.20, "wellbeing": +0.05}
}


# 5. EFECTOS DE DEPARTAMENTO


DEPARTMENT_EFFECTS = {
    "Desarrollo": {"burnout": +0.20, "boreout": -0.10},
    "Datos":      {"burnout": +0.10, "boreout": 0.00},
    "Producto":   {"burnout": +0.15, "boreout": -0.05},
    "RRHH":       {"burnout": -0.10, "boreout": +0.10},
    "Ventas":     {"burnout": +0.30, "boreout": -0.15}
}


# 6. UMBRALES DE CLASIFICACIÓN (basados en literatura)


UMBRALES = {
    # Umbrales MBI-GS convertidos a escala 1-5
    "burnout_alto": 3.86,    # Percentil 75 MBI-GS (Schaufeli et al., 1996)
    "burnout_bajo": 2.50,    # Percentil 25
    
    # Umbrales EAL
    "boreout_alto": 3.00,    # Umbral EAL (Martínez-Lugo, 2017)
    "boreout_bajo": 2.00,
    
    # Umbrales WHO-5
    "bienestar_alto": 3.50,  # Bienestar óptimo
    "bienestar_bajo": 2.60,  # Riesgo de depresión (Topp et al., 2015)
}

# 7. PARÁMETROS DE GENERACIÓN


LIKERT_MIN = 1
LIKERT_MAX = 5

N_EMPLEADOS_DEFAULT = 2500
N_EMPRESAS_DEFAULT = 50

# Desviaciones estándar para generación de respuestas


STD_LATENTE = 0.5       # Reducido de 0.7 a 0.5
STD_RUIDO = 0.3         # Reducido de 0.4 a 0.3
STD_RUIDO_ALTO = 0.4    # Reducido de 0.5 a 0.4

# Factores individuales (moderados)
STD_RESILIENCIA = 0.2   # ← Reducido de 0.3 a 0.2
STD_SENSIBILIDAD = 0.15 # ← Reducido de 0.25 a 0.15

# Outliers naturales (3% en lugar de 5%)
PORCENTAJE_OUTLIERS = 0.03  # Reducido de 0.05 a 0.03
OUTLIER_BOOST = 1.0         # Reducido de 1.5 a 1.0
OUTLIER_STD = 0.3           # Reducido de 0.5 a 0.3


# 8. COSTES DE ROTACIÓN (SHRM/Gallup)

TRAMOS_ROTACION = [
    {"max_kpi": 1.5, "tasa": 0.05},
    {"max_kpi": 2.5, "tasa": 0.10},
    {"max_kpi": 3.5, "tasa": 0.20},
    {"max_kpi": 4.5, "tasa": 0.35},
    {"max_kpi": 5.0, "tasa": 0.50},
]

FACTORES_PERFIL = {
    "Junior": 0.50,      # 50% del salario anual
    "Mid": 0.75,         # 75% del salario anual
    "Senior": 1.00,      # 100% del salario anual
    "Lead": 1.50         # 150% del salario anual
}

# 9. PREGUNTAS CVF (q60-q67) - Percepción Cultural

# 8 preguntas: 2 por cada cultura del CVF

PREGUNTAS_CVF = {
    "Adhocracia": [60, 61],   # Innovación, creatividad
    "Clan": [62, 63],         # Cohesión, familia
    "Mercado": [64, 65],      # Resultados, competitividad
    "Jerarquica": [66, 67]    # Procesos, estabilidad
}

# Información descriptiva del Competing Values Framework

INFO_CVF = {
    "Adhocracia": {
        "descripcion": (
            "Innovación, creatividad, riesgo y experimentación"
        ),
        "ejes": "Externo + Flexible",
    },
    "Clan": {
        "descripcion": (
            "Cohesión, mentoría, desarrollo personal y colaboración"
        ),
        "ejes": "Interno + Flexible",
    },
    "Mercado": {
        "descripcion": (
            "Resultados, competitividad y logro de objetivos"
        ),
        "ejes": "Externo + Control",
    },
    "Jerarquica": {
        "descripcion": (
            "Procesos, estabilidad, control y eficiencia"
        ),
        "ejes": "Interno + Control",
    },
}


# Total de preguntas con CVF
N_PREGUNTAS_TOTAL = 67  

# ==========================================================
# FUNCIONES AUXILIARES
# ==========================================================

def preguntas_dimension(nombre):
    """
    Devuelve la lista de preguntas de una dimensión.

    Ejemplo:
        preguntas_dimension("burnout_agotam")
        -> ["q16", "q17", ..., "q22"]
    """
    return [f"q{i}" for i in PREGUNTAS[nombre]["rango"]]


def preguntas_cvf(cultura):
    """
    Devuelve las preguntas asociadas a una cultura CVF.

    Ejemplo:
        preguntas_cvf("Clan")
        -> ["q62", "q63"]
    """
    return [f"q{i}" for i in PREGUNTAS_CVF[cultura]]


def todas_las_preguntas():
    """
    Devuelve todas las preguntas Likert del sistema.
    """
    return [f"q{i}" for i in range(1, N_PREGUNTAS_TOTAL + 1)]

