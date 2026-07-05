import numpy as np

# =====================================================
# EBLET - PEOPLE ANALYTICS FRAMEWORK
# CONFIGURACIÓN CENTRAL DEL SISTEMA
# =====================================================

# =====================================================
# 1. ESCENARIOS ORGANIZACIONALES
# =====================================================

SCENARIOS = {
    "saludable": {
        "burnout_base": 2.0,
        "boreout_base": 1.8,
        "wellbeing_base": 4.2,
        "rotation_base": 1.5,
        "culture_mix": {
            "Innovadora": 0.40,
            "Colaborativa": 0.40,
            "Tradicional": 0.10,
            "Exigente": 0.10
        }
    },
    "estable": {
        "burnout_base": 2.6,
        "boreout_base": 2.2,
        "wellbeing_base": 3.4,
        "rotation_base": 2.3,
        "culture_mix": {
            "Innovadora": 0.25,
            "Colaborativa": 0.35,
            "Tradicional": 0.25,
            "Exigente": 0.15
        }
    },
    "riesgo_burnout": {
        "burnout_base": 4.2,
        "boreout_base": 2.0,
        "wellbeing_base": 2.4,
        "rotation_base": 4.0,
        "culture_mix": {
            "Innovadora": 0.10,
            "Colaborativa": 0.20,
            "Tradicional": 0.30,
            "Exigente": 0.40
        }
    },
    "riesgo_boreout": {
        "burnout_base": 2.2,
        "boreout_base": 4.3,
        "wellbeing_base": 2.5,
        "rotation_base": 3.8,
        "culture_mix": {
            "Innovadora": 0.15,
            "Colaborativa": 0.20,
            "Tradicional": 0.25,
            "Exigente": 0.40
        }
    },
    "critico": {
        "burnout_base": 4.5,
        "boreout_base": 4.4,
        "wellbeing_base": 1.8,
        "rotation_base": 4.8,
        "culture_mix": {
            "Innovadora": 0.05,
            "Colaborativa": 0.10,
            "Tradicional": 0.35,
            "Exigente": 0.50
        }
    }
}

# =====================================================
# 2. EFECTOS PSICOLÓGICOS GLOBALMENTE FIJOS
# =====================================================

CULTURE_EFFECTS = {
    "Innovadora":   {"burnout": -0.15, "boreout": -0.10, "wellbeing": +0.20},
    "Colaborativa": {"burnout": -0.25, "boreout": -0.10, "wellbeing": +0.30},
    "Tradicional":  {"burnout": +0.15, "boreout": +0.10, "wellbeing": -0.15},
    "Exigente":     {"burnout": +0.35, "boreout": -0.05, "wellbeing": -0.35}
}

MODALITY_EFFECTS = {
    "Presencial": {"burnout": +0.10, "boreout": -0.10, "wellbeing": -0.05},
    "Híbrido":    {"burnout": 0.00,  "boreout": 0.00,  "wellbeing": +0.15},
    "Remoto":     {"burnout": -0.10, "boreout": +0.20, "wellbeing": +0.05}
}

DEPARTMENT_EFFECTS = {
    "Desarrollo": {"burnout": +0.20, "boreout": -0.10},
    "Datos":      {"burnout": +0.10, "boreout": 0.00},
    "Producto":   {"burnout": +0.15, "boreout": -0.05},
    "RRHH":       {"burnout": -0.10, "boreout": +0.10},
    "Ventas":     {"burnout": +0.30, "boreout": -0.15}
}

# =====================================================
# 3. ESCALAS DEL MODELO
# =====================================================

LIKERT_MIN = 1
LIKERT_MAX = 5

N_EMPLEADOS_DEFAULT = 2500
N_EMPRESAS_DEFAULT = 50

# =====================================================
# 4. UMBRALES DE CLASIFICACIÓN
# =====================================================

UMBRALES = {
    "burnout_alto": 3.5,
    "burnout_bajo": 2.5,
    "boreout_alto": 3.5,
    "boreout_bajo": 2.5,
    "bienestar_alto": 3.5,
    "bienestar_bajo": 2.5
}