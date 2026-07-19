"""
Generador de Respuestas a Encuesta

Genera respuestas a las  preguntas Likert de la encuesta EBLET
a partir de los estados latentes calculados por el modelo psicológico.

"""

import pandas as pd
import numpy as np

from config import (
    STD_RUIDO,
    STD_RUIDO_ALTO,
    PREGUNTAS_CVF,
    preguntas_dimension,
)

def generar_bloque_likert(
    respuestas,
    columnas,
    base,
    desviacion,
):
    """
    Genera un bloque de respuestas Likert a partir de un valor base.

    Mantiene los valores dentro del rango 1-5 y devuelve enteros.
    """
    n = len(respuestas)

    for columna in columnas:
        ruido = np.random.normal(0, desviacion, n)
        respuestas[columna] = (
            np.clip(base + ruido, 1, 5)
            .round()
            .astype(int)
        )

def generar_respuestas_encuesta(df_empleados):
    """
    Genera respuestas a las preguntas de la encuesta EBLET.
    
    Args:
        df_empleados: DataFrame con metadata de empleados Y columnas
                      L_burnout, L_boreout, L_wellbeing, L_rotation
    
    Returns:
        DataFrame con 67 columnas Likert (q1 a q67)
    """
    n = len(df_empleados)
    todas_respuestas = pd.DataFrame(index=df_empleados.index)
    
    # 🆕 Extraer estados latentes del DataFrame
    L_burnout = df_empleados["L_burnout"].values
    L_boreout = df_empleados["L_boreout"].values
    L_wellbeing = df_empleados["L_wellbeing"].values
    L_rotation = df_empleados["L_rotation"].values
    
 
    # SECCIÓN C: CONTEXTO ORGANIZACIONAL (q1-q15)
   
    base_contexto = (
        2.0
        + L_wellbeing * 0.5
        - L_burnout * 0.15
        - L_boreout * 0.15
    )

    generar_bloque_likert(
        respuestas=todas_respuestas,
        columnas=preguntas_dimension("contexto"),
        base=base_contexto,
        desviacion=STD_RUIDO,
    )
    
 
    # SECCIÓN D: BURNOUT - MBI-GS (q16-q36)
   
    
    # Dimensión 1: Agotamiento Emocional (q16-q22)
    generar_bloque_likert(
        respuestas=todas_respuestas,
        columnas=preguntas_dimension("burnout_agotam"),
        base=L_burnout,
        desviacion=STD_RUIDO_ALTO,
    )
    
    # Dimensión 2: Cinismo/Despersonalización (q23-q29)
    generar_bloque_likert(
        respuestas=todas_respuestas,
        columnas=preguntas_dimension("burnout_cinismo"),
        base=L_burnout * 0.9,
        desviacion=STD_RUIDO_ALTO,
    )
    
    # Dimensión 3: Eficacia Profesional INVERTIDA (q30-q36)
    generar_bloque_likert(
        respuestas=todas_respuestas,
        columnas=preguntas_dimension("burnout_ineficacia"),
        base=6 - L_burnout,
        desviacion=STD_RUIDO_ALTO,
    )
    
    
    # SECCIÓN E: BOREOUT - EAL (q37-q44)
  
    generar_bloque_likert(
        respuestas=todas_respuestas,
        columnas=preguntas_dimension("aburrimiento_eal"),
        base=L_boreout,
        desviacion=STD_RUIDO_ALTO,
    )
    
   
    # SECCIÓN F: BIENESTAR - WHO-5 (q45-q49)
   
    generar_bloque_likert(
        respuestas=todas_respuestas,
        columnas=preguntas_dimension("bienestar_who5"),
        base=L_wellbeing,
        desviacion=STD_RUIDO,
    )
    
   
    # SECCIÓN G: SATISFACCIÓN + AUTOEFICACIA (q50-q56)
    
    
    # Satisfacción (q50-q53)
    generar_bloque_likert(
        respuestas=todas_respuestas,
        columnas=preguntas_dimension("satisfaccion"),
        base=L_wellbeing * 0.9,
        desviacion=STD_RUIDO,
    )
    
    # Autoeficacia (q54-q56)
    base_autoeficacia = L_wellbeing * 0.7 + 1.5

    generar_bloque_likert(
        respuestas=todas_respuestas,
        columnas=preguntas_dimension("autoeficacia"),
        base=base_autoeficacia,
        desviacion=STD_RUIDO,
    )
    

    # SECCIÓN H: ROTACIÓN - MOBLEY (q57-q59)

    generar_bloque_likert(
        respuestas=todas_respuestas,
        columnas=preguntas_dimension("rotacion"),
        base=L_rotation,
        desviacion=STD_RUIDO,
    )
    

    
  
    # SECCIÓN I: CULTURA CVF (q60-q67)
  
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