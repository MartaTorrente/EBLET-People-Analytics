"""
EBLET v2.0 - Modelo Psicológico

Transforma variables organizacionales en estados psicológicos latentes:
burnout, boreout, bienestar y rotación.

Basado en:
- JD-R Model (Demerouti et al., 2001)
- Maslach Burnout Inventory (Maslach et al., 1981)
- Boreout Theory (Rothlin & Werder, 2007)
- Teoría de Turnover (Mobley, 1977)
"""

import numpy as np
import pandas as pd

from config import (
    CULTURE_EFFECTS, MODALITY_EFFECTS, DEPARTMENT_EFFECTS,
    STD_LATENTE
)


def aplicar_efectos(df, L_burnout, L_boreout, L_wellbeing):
    """
    Aplica efectos organizacionales sobre los estados psicológicos.
    """
    
    # Cultura (CVF - Cameron & Quinn)
    for c, e in CULTURE_EFFECTS.items():
        idx = df["cultura"] == c
        L_burnout[idx] += e["burnout"]
        L_boreout[idx] += e["boreout"]
        L_wellbeing[idx] += e["wellbeing"]
    
    # Modalidad
    for m, e in MODALITY_EFFECTS.items():
        idx = df["modalidad"] == m
        L_burnout[idx] += e["burnout"]
        L_boreout[idx] += e["boreout"]
        L_wellbeing[idx] += e["wellbeing"]
    
    # Departamento
    for d, e in DEPARTMENT_EFFECTS.items():
        idx = df["departamento"] == d
        L_burnout[idx] += e["burnout"]
        L_boreout[idx] += e["boreout"]
    
    return L_burnout, L_boreout, L_wellbeing


def calcular_rotacion(L_burnout, L_boreout, L_wellbeing, noise=0.4):
    """
    Modelo de intención de rotación basado en teoría de turnover (Mobley, 1977).
    """
    
    rotacion = (
        1.5
        + 0.35 * L_burnout
        + 0.25 * L_boreout
        + 0.30 * (5 - L_wellbeing)
        + np.random.normal(0, noise, len(L_burnout))
    )
    
    return np.clip(rotacion, 1, 5)


def construir_modelo_psicologico(df):
    """
    Ejecuta el modelo completo psicológico sobre un dataframe de empleados.
    
    Usa los valores base del escenario de cada empresa (definidos en config.py)
    y aplica los efectos organizacionales (cultura CVF, modalidad, departamento).
    """
    
    n = len(df)
    
    # USAR VALORES BASE DEL ESCENARIO
    L_burnout = np.random.normal(df["burnout_base"].values, STD_LATENTE, n)
    L_boreout = np.random.normal(df["boreout_base"].values, STD_LATENTE, n)
    L_wellbeing = np.random.normal(df["wellbeing_base"].values, STD_LATENTE, n)
    
    # Aplicar efectos organizacionales
    L_burnout, L_boreout, L_wellbeing = aplicar_efectos(
        df, L_burnout, L_boreout, L_wellbeing
    )
    
    # Clipping psicométrico (escala 1-5)
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