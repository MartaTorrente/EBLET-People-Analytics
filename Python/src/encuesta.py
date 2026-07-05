import numpy as np
import pandas as pd

# =====================================================
# GENERADOR DE RESPUESTAS A LA ENCUESTA EBLET
# =====================================================
# Transforma estados psicológicos latentes en respuestas
# a las 48 preguntas de la encuesta.
# =====================================================


def generar_respuestas_encuesta(df, latentes):
    """
    Transforma estados psicológicos latentes en respuestas a la encuesta.
    
    Args:
        df: DataFrame de empleados con variables organizacionales
        latentes: Diccionario con arrays de estados psicológicos
    
    Returns:
        DataFrame con 43 columnas (q6 a q48) con respuestas Likert 1-5
    """
    
    n = len(df)
    respuestas = {}
    
    # =====================================================
    # SECCIÓN 3: CONTEXTO ORGANIZACIONAL (q6-q20)
    # =====================================================
    # Estas preguntas miden factores organizacionales
    # Usamos wellbeing_base como proxy de calidad del contexto
    
    for q in range(6, 21):
        respuestas[f'q{q}'] = np.clip(
            np.random.normal(df["wellbeing_base"].values, 0.7, n),
            1, 5
        ).round().astype(int)
    
    # =====================================================
    # SECCIÓN 4: BURNOUT (q21-q29)
    # =====================================================
    # Preguntas 21-23: Agotamiento Emocional
    for q in range(21, 24):
        respuestas[f'q{q}'] = np.clip(
            latentes["burnout"] + np.random.normal(0, 0.3, n),
            1, 5
        ).round().astype(int)
    
    # Preguntas 24-26: Cinismo/Despersonalización
    for q in range(24, 27):
        respuestas[f'q{q}'] = np.clip(
            latentes["burnout"] * 0.9 + np.random.normal(0, 0.35, n),
            1, 5
        ).round().astype(int)
    
    # Preguntas 27-29: Baja Eficacia Profesional
    for q in range(27, 30):
        respuestas[f'q{q}'] = np.clip(
            latentes["burnout"] * 0.85 + np.random.normal(0, 0.4, n),
            1, 5
        ).round().astype(int)
    
    # =====================================================
    # SECCIÓN 5: BOREOUT (q30-q38)
    # =====================================================
    # Preguntas 30-32: Desinterés
    for q in range(30, 33):
        respuestas[f'q{q}'] = np.clip(
            latentes["boreout"] + np.random.normal(0, 0.3, n),
            1, 5
        ).round().astype(int)
    
    # Preguntas 33-35: Falta de Reto
    for q in range(33, 36):
        respuestas[f'q{q}'] = np.clip(
            latentes["boreout"] * 0.95 + np.random.normal(0, 0.35, n),
            1, 5
        ).round().astype(int)
    
    # Preguntas 36-38: Infraocupación y Ocultamiento
    for q in range(36, 39):
        respuestas[f'q{q}'] = np.clip(
            latentes["boreout"] * 0.9 + np.random.normal(0, 0.4, n),
            1, 5
        ).round().astype(int)
    
    # =====================================================
    # SECCIÓN 6: BIENESTAR Y AUTOEFICACIA (q39-q45)
    # =====================================================
    # Preguntas 39-42: Bienestar/Satisfacción
    for q in range(39, 43):
        respuestas[f'q{q}'] = np.clip(
            latentes["wellbeing"] + np.random.normal(0, 0.3, n),
            1, 5
        ).round().astype(int)
    
    # Preguntas 43-45: Autoeficacia Laboral
    for q in range(43, 46):
        respuestas[f'q{q}'] = np.clip(
            latentes["wellbeing"] * 0.8 + np.random.normal(1.0, 0.4, n),
            1, 5
        ).round().astype(int)
    
    # =====================================================
    # SECCIÓN 7: INTENCIÓN DE ROTACIÓN (q46-q48)
    # =====================================================
    for q in range(46, 49):
        respuestas[f'q{q}'] = np.clip(
            latentes["rotation"] + np.random.normal(0, 0.3, n),
            1, 5
        ).round().astype(int)
    
    return pd.DataFrame(respuestas)