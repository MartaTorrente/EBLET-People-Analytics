"""
EBLET v2.0 - People Analytics Framework
Configuración Central del Sistema

Instrumentos validados:
- MBI-GS (Schaufeli et al., 1996): Burnout
- EAL (Martínez-Lugo & Rodríguez-Montalbán, 2017): Aburrimiento Laboral
- WHO-5 (Topp et al., 2015): Bienestar
- Rothlin & Werder (2007): Infraocupación
- Bandura (1997): Autoeficacia
- Mobley (1977): Intención de Rotación

Cultura organizacional:
- Competing Values Framework (Cameron & Quinn, 2011)
  - Adhocracia (Innovadora)
  - Clan (Colaborativa)
  - Jerarquica (Tradicional)
  - Mercado (Exigente)
"""

import numpy as np

# =====================================================
# 1. ESTRUCTURA DE LA ENCUESTA (v2.0)
# =====================================================

# Rangos de preguntas por dimensión (numeración Likert 1-64)
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
    "infraocupacion":     {"rango": range(60, 65),  "n_items": 5},   # q60-q64
}

# Total de preguntas Likert
N_PREGUNTAS_LIKERT = 64

# =====================================================
# 2. ESCENARIOS ORGANIZACIONALES
# =====================================================
# Valores base calibrados con puntos de corte de instrumentos validados:
# - MBI-GS: Burnout alto ≥ 3.86 (Schaufeli et al., 1996)
# - EAL: Aburrimiento significativo ≥ 3.0 (Martínez-Lugo, 2017)
# - WHO-5: Bienestar bajo < 2.6 (Topp et al., 2015)

# =====================================================
# 2. ESCENARIOS ORGANIZACIONALES
# =====================================================
# Valores base calibrados con puntos de corte de instrumentos validados:
# - MBI-GS: Burnout alto ≥ 3.86 (Schaufeli et al., 1996)
# - EAL: Aburrimiento significativo ≥ 3.0 (Martínez-Lugo, 2017)
# - WHO-5: Bienestar bajo < 2.6 (Topp et al., 2015)

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
        "boreout_base": 1.7,       # ⬇️ AJUSTADO: bien por debajo del umbral 2.0
        "wellbeing_base": 2.3,     # ⬇️ AJUSTADO: por debajo del umbral 3.0
        "rotation_base": 4.0,
        "culture_mix": {
            "Adhocracia": 0.10,
            "Clan": 0.15,
            "Jerarquica": 0.25,
            "Mercado": 0.50        # Cultura de Mercado predomina
        }
    },
        "riesgo_boreout": {
        "burnout_base": 1.5,       # ⬇️ AJUSTADO: de 1.8 a 1.5 para compensar efectos
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
# =====================================================
# 3. EFECTOS DE CULTURA ORGANIZACIONAL (CVF - Cameron & Quinn)
# =====================================================
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

# =====================================================
# 4. EFECTOS DE MODALIDAD DE TRABAJO
# =====================================================
# Basado en estudios post-pandemia (Bloom, 2022; Oakman et al., 2020)

MODALITY_EFFECTS = {
    "Presencial": {"burnout": +0.10, "boreout": -0.10, "wellbeing": -0.05},
    "Híbrido":    {"burnout": 0.00,  "boreout": 0.00,  "wellbeing": +0.15},
    "Remoto":     {"burnout": -0.10, "boreout": +0.20, "wellbeing": +0.05}
}

# =====================================================
# 5. EFECTOS DE DEPARTAMENTO
# =====================================================

DEPARTMENT_EFFECTS = {
    "Desarrollo": {"burnout": +0.20, "boreout": -0.10},
    "Datos":      {"burnout": +0.10, "boreout": 0.00},
    "Producto":   {"burnout": +0.15, "boreout": -0.05},
    "RRHH":       {"burnout": -0.10, "boreout": +0.10},
    "Ventas":     {"burnout": +0.30, "boreout": -0.15}
}

# =====================================================
# 6. UMBRALES DE CLASIFICACIÓN (basados en literatura)
# =====================================================

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

# =====================================================
# 7. PARÁMETROS DE GENERACIÓN
# =====================================================

LIKERT_MIN = 1
LIKERT_MAX = 5

N_EMPLEADOS_DEFAULT = 2500
N_EMPRESAS_DEFAULT = 50

# Desviaciones estándar para generación de respuestas
STD_LATENTE = 0.5      # Variabilidad del estado psicológico latente
STD_RUIDO = 0.3        # Ruido individual en respuestas
STD_RUIDO_ALTO = 0.4   # Ruido para dimensiones más variables

# =====================================================
# 8. COSTES DE ROTACIÓN (SHRM/Gallup)
# =====================================================

FACTORES_PERFIL = {
    "Junior": 0.50,      # 50% del salario anual
    "Mid": 0.75,         # 75% del salario anual
    "Senior": 1.00,      # 100% del salario anual
    "Lead": 1.50         # 150% del salario anual
}