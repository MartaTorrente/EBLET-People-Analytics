"""
Generador de Respuestas a Encuesta

Genera respuestas a las 72 preguntas Likert de la encuesta EBLET
a partir de los estados latentes calculados por el modelo psicológico.

"""

import pandas as pd
import numpy as np

from config import (
    STD_RUIDO,
    STD_RUIDO_ALTO,
    PREGUNTAS_CVF
)


def generar_respuestas_encuesta(df_empleados):
    """
    Genera respuestas a las 72 preguntas de la encuesta EBLET.
    
    Args:
        df_empleados: DataFrame con metadata de empleados Y columnas
                      L_burnout, L_boreout, L_wellbeing, L_rotation
    
    Returns:
        DataFrame con 72 columnas (q1 a q72)
    """
    n = len(df_empleados)
    todas_respuestas = pd.DataFrame(index=df_empleados.index)
    
    # 🆕 Extraer estados latentes del DataFrame
    L_burnout = df_empleados["L_burnout"].values
    L_boreout = df_empleados["L_boreout"].values
    L_wellbeing = df_empleados["L_wellbeing"].values
    L_rotation = df_empleados["L_rotation"].values
    
 
    # SECCIÓN C: CONTEXTO ORGANIZACIONAL (q1-q15)
   
    for q in range(1, 16):
        base = 2.0 + L_wellbeing * 0.5 + L_burnout * (-0.15) + L_boreout * (-0.15)
        ruido = np.random.normal(0, STD_RUIDO, n)
        todas_respuestas[f'q{q}'] = np.clip(base + ruido, 1, 5).round().astype(int)
    
 
    # SECCIÓN D: BURNOUT - MBI-GS (q16-q36)
   
    
    # Dimensión 1: Agotamiento Emocional (q16-q22)
    for q in range(16, 23):
        ruido = np.random.normal(0, STD_RUIDO_ALTO, n)
        todas_respuestas[f'q{q}'] = np.clip(L_burnout + ruido, 1, 5).round().astype(int)
    
    # Dimensión 2: Cinismo/Despersonalización (q23-q29)
    for q in range(23, 30):
        ruido = np.random.normal(0, STD_RUIDO_ALTO, n)
        todas_respuestas[f'q{q}'] = np.clip(L_burnout * 0.9 + ruido, 1, 5).round().astype(int)
    
    # Dimensión 3: Eficacia Profesional INVERTIDA (q30-q36)
    for q in range(30, 37):
        ruido = np.random.normal(0, STD_RUIDO_ALTO, n)
        todas_respuestas[f'q{q}'] = np.clip((6 - L_burnout) + ruido, 1, 5).round().astype(int)
    
    
    # SECCIÓN E: BOREOUT - EAL (q37-q44)
  
    for q in range(37, 45):
        ruido = np.random.normal(0, STD_RUIDO_ALTO, n)
        todas_respuestas[f'q{q}'] = np.clip(L_boreout + ruido, 1, 5).round().astype(int)
    
   
    # SECCIÓN F: BIENESTAR - WHO-5 (q45-q49)
   
    for q in range(45, 50):
        ruido = np.random.normal(0, STD_RUIDO, n)
        todas_respuestas[f'q{q}'] = np.clip(L_wellbeing + ruido, 1, 5).round().astype(int)
    
   
    # SECCIÓN G: SATISFACCIÓN + AUTOEFICACIA (q50-q56)
    
    
    # Satisfacción (q50-q53)
    for q in range(50, 54):
        ruido = np.random.normal(0, STD_RUIDO, n)
        todas_respuestas[f'q{q}'] = np.clip(L_wellbeing * 0.9 + ruido, 1, 5).round().astype(int)
    
    # Autoeficacia (q54-q56)
    for q in range(54, 57):
        ruido = np.random.normal(0, STD_RUIDO, n)
        base_autoeficacia = L_wellbeing * 0.7 + 1.5  # Correlación con bienestar
        todas_respuestas[f'q{q}'] = np.clip(base_autoeficacia + ruido, 1, 5).round().astype(int)
    

    # SECCIÓN H: ROTACIÓN - MOBLEY (q57-q59)

    for q in range(57, 60):
        ruido = np.random.normal(0, STD_RUIDO, n)
        todas_respuestas[f'q{q}'] = np.clip(L_rotation + ruido, 1, 5).round().astype(int)
    

    # SECCIÓN I: INFRAOCUPACIÓN - ROTHLIN (q60-q64)

    for q in range(60, 65):
        ruido = np.random.normal(0, STD_RUIDO_ALTO, n)
        todas_respuestas[f'q{q}'] = np.clip(L_boreout * 0.95 + ruido, 1, 5).round().astype(int)
    
  
    # SECCIÓN J: CULTURA CVF (q65-q72)
  
    cultura_boost = {
        "Adhocracia": {"Adhocracia": 2.0, "Clan": 0.0, "Mercado": 0.0, "Jerarquica": 0.0},
        "Clan":       {"Adhocracia": 0.0, "Clan": 2.0, "Mercado": 0.0, "Jerarquica": 0.0},
        "Mercado":    {"Adhocracia": 0.0, "Clan": 0.0, "Mercado": 2.0, "Jerarquica": 0.0},
        "Jerarquica": {"Adhocracia": 0.0, "Clan": 0.0, "Mercado": 0.0, "Jerarquica": 2.0}
    }
    
    base_cultura = 2.0
    
    for cultura, preguntas in PREGUNTAS_CVF.items():
        for q in preguntas:
            boost = df_empleados["cultura"].map(
                lambda c, cult=cultura: cultura_boost.get(c, {}).get(cult, 0.0)
            )
            ruido = np.random.normal(0, 0.6, n)
            todas_respuestas[f'q{q}'] = np.clip(
                base_cultura + boost.values + ruido,
                1, 5
            ).round().astype(int)
    
    return todas_respuestas