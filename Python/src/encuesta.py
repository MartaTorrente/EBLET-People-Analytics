"""
EBLET v2.0 - Generador de Respuestas a la Encuesta

Transforma estados psicológicos latentes en respuestas a las 64 preguntas
de la encuesta EBLET v2.0, basada en instrumentos validados:
- MBI-GS (Burnout)
- EAL (Aburrimiento Laboral)
- WHO-5 (Bienestar)
- Rothlin & Werder (Infraocupación)
- Bandura (Autoeficacia)
- Mobley (Rotación)
"""

import numpy as np
import pandas as pd

from config import PREGUNTAS, STD_RUIDO, STD_RUIDO_ALTO


def generar_respuestas_encuesta(df, latentes):
    """
    Transforma estados psicológicos latentes en respuestas a la encuesta.
    
    Args:
        df: DataFrame de empleados con variables organizacionales
        latentes: Diccionario con arrays de estados psicológicos
            - burnout: estado de burnout
            - boreout: estado de boreout/aburrimiento
            - wellbeing: estado de bienestar
    
    Returns:
        DataFrame con 64 columnas (q1 a q64) con respuestas Likert 1-5
    """
    
    n = len(df)
    todas_respuestas = {}
    
    # =====================================================
    # SECCIÓN C: CONTEXTO ORGANIZACIONAL (q1-q15)
    # =====================================================
    # Basado en JD-R Model (Demerouti et al., 2001)
    
    for q in range(1, 16):
        todas_respuestas[f'q{q}'] = np.clip(
            np.random.normal(df["wellbeing_base"].values, 0.7, n),
            1, 5
        ).round().astype(int)
    
    # =====================================================
    # SECCIÓN D: BURNOUT - MBI-GS COMPLETO (q16-q36)
    # =====================================================
    
    # Dimensión 1: Agotamiento (q16-q22) - 7 ítems
    for q in range(16, 23):
        todas_respuestas[f'q{q}'] = np.clip(
            latentes["burnout"] + np.random.normal(0, STD_RUIDO, n),
            1, 5
        ).round().astype(int)
    
    # Dimensión 2: Cinismo (q23-q29) - 7 ítems
    for q in range(23, 30):
        todas_respuestas[f'q{q}'] = np.clip(
            latentes["burnout"] * 0.95 + np.random.normal(0, STD_RUIDO, n),
            1, 5
        ).round().astype(int)
    
    # Dimensión 3: Eficacia Profesional (q30-q36) - 7 ítems INVERTIDOS
    # Estos ítems son positivos: alta eficacia = bajo burnout
    for q in range(30, 37):
        todas_respuestas[f'q{q}'] = np.clip(
            (5 - latentes["burnout"]) * 0.9 + np.random.normal(0.5, STD_RUIDO_ALTO, n),
            1, 5
        ).round().astype(int)
    
    # =====================================================
    # SECCIÓN E: ABURRIMIENTO LABORAL - EAL COMPLETO (q37-q44)
    # =====================================================
    # Basado en Martínez-Lugo & Rodríguez-Montalbán (2017)
    
    for q in range(37, 45):
        todas_respuestas[f'q{q}'] = np.clip(
            latentes["boreout"] + np.random.normal(0, STD_RUIDO, n),
            1, 5
        ).round().astype(int)
    
    # =====================================================
    # SECCIÓN F: BIENESTAR - WHO-5 COMPLETO (q45-q49)
    # =====================================================
    # Basado en Topp et al. (2015)
    
    for q in range(45, 50):
        todas_respuestas[f'q{q}'] = np.clip(
            latentes["wellbeing"] + np.random.normal(0, STD_RUIDO, n),
            1, 5
        ).round().astype(int)
    
    # =====================================================
    # SECCIÓN G: SATISFACCIÓN + AUTOEFICACIA (q50-q56)
    # =====================================================
    
    # Satisfacción (q50-q53) - 4 ítems
    for q in range(50, 54):
        todas_respuestas[f'q{q}'] = np.clip(
            latentes["wellbeing"] * 0.95 + np.random.normal(0.2, STD_RUIDO, n),
            1, 5
        ).round().astype(int)
    
    # Autoeficacia (q54-q56) - 3 ítems (Bandura, 1997)
    for q in range(54, 57):
        todas_respuestas[f'q{q}'] = np.clip(
            latentes["wellbeing"] * 0.7 + np.random.normal(1.2, STD_RUIDO_ALTO, n),
            1, 5
        ).round().astype(int)
    
    # =====================================================
    # SECCIÓN H: INTENCIÓN DE ROTACIÓN (q57-q59)
    # =====================================================
    # Basado en Mobley (1977)
    
    for q in range(57, 60):
        todas_respuestas[f'q{q}'] = np.clip(
            latentes["rotation"] + np.random.normal(0, STD_RUIDO, n),
            1, 5
        ).round().astype(int)
    
    # =====================================================
    # SECCIÓN I: INFRAOCUPACIÓN Y OCULTAMIENTO (q60-q64)
    # =====================================================
    # Basado en Rothlin & Werder (2007)
    
    for q in range(60, 65):
        todas_respuestas[f'q{q}'] = np.clip(
            latentes["boreout"] * 0.9 + np.random.normal(0.3, STD_RUIDO_ALTO, n),
            1, 5
        ).round().astype(int)
    
    return pd.DataFrame(todas_respuestas)