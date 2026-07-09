"""
EBLET v2.0 - Modelo Psicológico

Calcula los estados latentes de burnout, boreout, bienestar y rotación
a partir de los valores base del escenario y los efectos organizacionales.

Versión 2.1: Incluye variabilidad individual realista
- Factores individuales (resiliencia, sensibilidad)
- Ruido organizacional aumentado
- Outliers naturales (5% empleados atípicos)
"""

import numpy as np
import pandas as pd

from config import (
    CULTURE_EFFECTS,
    MODALITY_EFFECTS,
    DEPARTMENT_EFFECTS,
    STD_LATENTE,
    STD_RUIDO,
    STD_RUIDO_ALTO,
    STD_RESILIENCIA,
    STD_SENSIBILIDAD,
    PORCENTAJE_OUTLIERS,
    OUTLIER_BOOST,
    OUTLIER_STD
)


def aplicar_efectos(df, L_burnout, L_boreout, L_wellbeing):
    """
    Aplica los efectos organizacionales (cultura, modalidad, departamento)
    a los estados latentes.
    """
    # Efecto de cultura CVF
    for cultura, efectos in CULTURE_EFFECTS.items():
        mask = df["cultura"] == cultura
        L_burnout[mask] += efectos["burnout"]
        L_boreout[mask] += efectos["boreout"]
        L_wellbeing[mask] += efectos["wellbeing"]
    
    # Efecto de modalidad
    for modalidad, efectos in MODALITY_EFFECTS.items():
        mask = df["modalidad"] == modalidad
        L_burnout[mask] += efectos["burnout"]
        L_boreout[mask] += efectos["boreout"]
        L_wellbeing[mask] += efectos["wellbeing"]
    
    # Efecto de departamento
    for dept, efectos in DEPARTMENT_EFFECTS.items():
        mask = df["departamento"] == dept
        L_burnout[mask] += efectos["burnout"]
        L_boreout[mask] += efectos["boreout"]
    
    return L_burnout, L_boreout, L_wellbeing


def calcular_rotacion(L_burnout, L_boreout, L_wellbeing, n):
    """
    Calcula la intención de rotación basada en los estados latentes.
    Fórmula basada en el modelo de Mobley (1977).
    """
    # Fórmula: rotación = 1.5 + 0.35*burnout + 0.25*boreout + 0.30*(5-bienestar) + ruido
    L_rotation = (
        1.5 
        + 0.35 * L_burnout 
        + 0.25 * L_boreout 
        + 0.30 * (5 - L_wellbeing) 
        + np.random.normal(0, STD_RUIDO, n)
    )
    return L_rotation


def añadir_factores_individuales(n):
    """
    Genera factores individuales de personalidad que afectan
    cómo cada empleado experimenta el trabajo.
    
    Returns:
        factor_resiliencia: Cada persona tiene nivel diferente
        factor_sensibilidad: Cada persona tiene sensibilidad diferente
    """
    # Resiliencia: capacidad de afrontar adversidad
    factor_resiliencia = np.random.normal(0, STD_RESILIENCIA, n)
    
    # Sensibilidad: tendencia a experimentar malestar
    factor_sensibilidad = np.random.normal(0, STD_SENSIBILIDAD, n)
    
    return factor_resiliencia, factor_sensibilidad


def añadir_outliers(n, L_burnout, L_boreout, L_wellbeing):
    """
    Añade outliers naturales (5% de empleados con perfil atípico).
    
    En una empresa saludable, algunos empleados pueden estar mal.
    En una empresa crítica, algunos pueden estar bien (resilientes).
    """
    n_outliers = int(n * PORCENTAJE_OUTLIERS)
    if n_outliers == 0:
        return L_burnout, L_boreout, L_wellbeing
    
    # Seleccionar índices aleatorios para outliers
    outlier_idx = np.random.choice(n, size=n_outliers, replace=False)
    
    # Para cada outlier, decidir si es "positivo" o "negativo"
    # 50% outliers positivos (mejor de lo esperado)
    # 50% outliers negativos (peor de lo esperado)
    for idx in outlier_idx:
        if np.random.random() < 0.5:
            # Outlier positivo: mejor de lo esperado
            L_burnout[idx] -= OUTLIER_BOOST + np.random.normal(0, OUTLIER_STD)
            L_boreout[idx] -= OUTLIER_BOOST + np.random.normal(0, OUTLIER_STD)
            L_wellbeing[idx] += OUTLIER_BOOST + np.random.normal(0, OUTLIER_STD)
        else:
            # Outlier negativo: peor de lo esperado
            L_burnout[idx] += OUTLIER_BOOST + np.random.normal(0, OUTLIER_STD)
            L_boreout[idx] += OUTLIER_BOOST + np.random.normal(0, OUTLIER_STD)
            L_wellbeing[idx] -= OUTLIER_BOOST + np.random.normal(0, OUTLIER_STD)
    
    return L_burnout, L_boreout, L_wellbeing


def construir_modelo_psicologico(df):
    """
    Construye el modelo psicológico completo para todos los empleados.
    
    Args:
        df: DataFrame con metadata de empleados (cultura, modalidad, etc.)
    
    Returns:
        DataFrame con estados latentes añadidos
    """
    n = len(df)
    
    # =====================================================
    # 1. VALORES BASE DEL ESCENARIO
    # =====================================================
    # Cada empleado parte de los valores base de su escenario
    L_burnout = df["burnout_base"].values.copy().astype(float)
    L_boreout = df["boreout_base"].values.copy().astype(float)
    L_wellbeing = df["wellbeing_base"].values.copy().astype(float)
    
    # Añadir variabilidad inicial (cada empleado parte ligeramente diferente)
    L_burnout += np.random.normal(0, STD_LATENTE, n)
    L_boreout += np.random.normal(0, STD_LATENTE, n)
    L_wellbeing += np.random.normal(0, STD_LATENTE, n)
    
    # =====================================================
    # 2. EFECTOS ORGANIZACIONALES
    # =====================================================
    L_burnout, L_boreout, L_wellbeing = aplicar_efectos(
        df, L_burnout, L_boreout, L_wellbeing
    )
    
    # =====================================================
    # 3. FACTORES INDIVIDUALES (personalidad)
    # =====================================================
    factor_resiliencia, factor_sensibilidad = añadir_factores_individuales(n)
    
    # La resiliencia reduce burnout y boreout, aumenta bienestar
    L_burnout = L_burnout - factor_resiliencia + factor_sensibilidad * 0.5
    L_boreout = L_boreout - factor_resiliencia * 0.7 + factor_sensibilidad * 0.3
    L_wellbeing = L_wellbeing + factor_resiliencia * 0.5 - factor_sensibilidad * 0.4
    
    # =====================================================
    # 4. RUIDO INDIVIDUAL ADICIONAL
    # =====================================================
    L_burnout += np.random.normal(0, STD_RUIDO_ALTO, n)
    L_boreout += np.random.normal(0, STD_RUIDO_ALTO, n)
    L_wellbeing += np.random.normal(0, STD_RUIDO, n)
    
    # =====================================================
    # 5. OUTLIERS NATURALES (5% de empleados atípicos)
    # =====================================================
    L_burnout, L_boreout, L_wellbeing = añadir_outliers(
        n, L_burnout, L_boreout, L_wellbeing
    )
    
    # =====================================================
    # 6. CLIPPING (valores entre 1 y 5)
    # =====================================================
    L_burnout = np.clip(L_burnout, 1.0, 5.0)
    L_boreout = np.clip(L_boreout, 1.0, 5.0)
    L_wellbeing = np.clip(L_wellbeing, 1.0, 5.0)
    
    # =====================================================
    # 7. CALCULAR ROTACIÓN
    # =====================================================
    L_rotation = calcular_rotacion(L_burnout, L_boreout, L_wellbeing, n)
    L_rotation = np.clip(L_rotation, 1.0, 5.0)
    
    # =====================================================
    # 8. GUARDAR EN DATAFRAME
    # =====================================================
    df["L_burnout"] = L_burnout
    df["L_boreout"] = L_boreout
    df["L_wellbeing"] = L_wellbeing
    df["L_rotation"] = L_rotation
    
    # Factores individuales (para análisis posterior)
    df["factor_resiliencia"] = factor_resiliencia
    df["factor_sensibilidad"] = factor_sensibilidad
    
    return df