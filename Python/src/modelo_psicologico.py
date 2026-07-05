import numpy as np
import pandas as pd


# MODELO PSICOLÓGICO EBLET

# Este módulo transforma variables organizacionales
# en estados psicológicos latentes:
# burnout, boreout, bienestar y rotación

# EFECTOS TEÓRICOS ORGANIZACIONALES


EFECTO_CULTURA = {
    "Innovadora": {
        "burnout": -0.15,
        "boreout": -0.10,
        "wellbeing": +0.20
    },
    "Colaborativa": {
        "burnout": -0.25,
        "boreout": -0.10,
        "wellbeing": +0.30
    },
    "Tradicional": {
        "burnout": +0.15,
        "boreout": +0.10,
        "wellbeing": -0.15
    },
    "Exigente": {
        "burnout": +0.35,
        "boreout": -0.05,
        "wellbeing": -0.35
    }
}

EFECTO_MODALIDAD = {
    "Presencial": {
        "burnout": +0.10,
        "boreout": -0.10,
        "wellbeing": -0.05
    },
    "Híbrido": {
        "burnout": 0.00,
        "boreout": 0.00,
        "wellbeing": +0.15
    },
    "Remoto": {
        "burnout": -0.10,
        "boreout": +0.20,
        "wellbeing": +0.05
    }
}

EFECTO_DEPARTAMENTO = {
    "Desarrollo": {"burnout": +0.20, "boreout": -0.10},
    "Datos": {"burnout": +0.10, "boreout": 0.00},
    "Producto": {"burnout": +0.15, "boreout": -0.05},
    "RRHH": {"burnout": -0.10, "boreout": +0.10},
    "Ventas": {"burnout": +0.30, "boreout": -0.15}
}



# EFECTOS SOBRE LATENTES


def aplicar_efectos(df, L_burnout, L_boreout, L_wellbeing):
    """
    Aplica efectos organizacionales sobre los estados psicológicos.
    """
    
    # Cultura
    for c, e in EFECTO_CULTURA.items():
        idx = df["cultura"] == c
        L_burnout[idx] += e["burnout"]
        L_boreout[idx] += e["boreout"]
        L_wellbeing[idx] += e["wellbeing"]
    
    # Modalidad
    for m, e in EFECTO_MODALIDAD.items():
        idx = df["modalidad"] == m
        L_burnout[idx] += e["burnout"]
        L_boreout[idx] += e["boreout"]
        L_wellbeing[idx] += e["wellbeing"]
    
    # Departamento
    for d, e in EFECTO_DEPARTAMENTO.items():
        idx = df["departamento"] == d
        L_burnout[idx] += e["burnout"]
        L_boreout[idx] += e["boreout"]
    
    return L_burnout, L_boreout, L_wellbeing



# ROTACIÓN 


def calcular_rotacion(L_burnout, L_boreout, L_wellbeing, noise=0.4):
    """
    Modelo de intención de rotación basado en teoría de turnover
    (Mobley, 1977).
    """
    
    rotacion = (
        1.5
        + 0.35 * L_burnout
        + 0.25 * L_boreout
        + 0.30 * (5 - L_wellbeing)
        + np.random.normal(0, noise, len(L_burnout))
    )
    
    return np.clip(rotacion, 1, 5)


# PIPELINE COMPLETO DEL MODELO (CORREGIDO)


def construir_modelo_psicologico(df):
    """
     usa los valores base del escenario de cada empresa.
    """
    
    n = len(df)
    
    # USAR VALORES BASE DEL ESCENARIO
    L_burnout = np.random.normal(df["burnout_base"].values, 0.5, n)
    L_boreout = np.random.normal(df["boreout_base"].values, 0.5, n)
    L_wellbeing = np.random.normal(df["wellbeing_base"].values, 0.5, n)
    
    # Aplicar efectos organizacionales
    L_burnout, L_boreout, L_wellbeing = aplicar_efectos(
        df, L_burnout, L_boreout, L_wellbeing
    )
    
    # Clipping psicométrico
    L_burnout = np.clip(L_burnout, 1, 5)
    L_boreout = np.clip(L_boreout, 1, 5)
    L_wellbeing = np.clip(L_wellbeing, 1, 5)
    
    # Calcular rotación
    L_rotation = calcular_rotacion(L_burnout, L_boreout, L_wellbeing)
    
    return {
        "burnout": L_burnout,
        "boreout": L_boreout,
        "wellbeing": L_wellbeing,
        "rotation": L_rotation
    }