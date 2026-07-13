"""
Clasificador de Cultura Organizacional (CVF)

Clasifica la cultura según la PERCEPCIÓN de los empleados,
no según una declaración corporativa.

Este módulo implementa el Competing Values Framework (CVF)
para clasificar la cultura organizacional percibida a partir
de las respuestas q65-q72.
"""

import numpy as np
import pandas as pd
from config import CULTURE_EFFECTS

# PREGUNTAS CVF (q65-q72)


PREGUNTAS_CVF = {
    "Adhocracia": {
        "preguntas": [60, 61],
        "descripcion": "Innovación, creatividad, riesgo, experimentación",
        "ejes": "Externo + Flexible"
    },
    "Clan": {
        "preguntas": [62, 63],
        "descripcion": "Cohesión, mentoría, desarrollo personal, familia",
        "ejes": "Interno + Flexible"
    },
    "Mercado": {
        "preguntas": [64, 65],
        "descripcion": "Resultados, competitividad, logro de objetivos",
        "ejes": "Externo + Control"
    },
    "Jerarquica": {
        "preguntas": [66, 67],
        "descripcion": "Procesos, estabilidad, control, eficiencia",
        "ejes": "Interno + Control"
    }
}

# Colores para visualización
COLORES_CVF = {
    "Adhocracia": "#3498db",   # Azul
    "Clan": "#2ecc71",         # Verde
    "Mercado": "#e67e22",      # Naranja
    "Jerarquica": "#f1c40f"    # Amarillo
}





# CLASIFICADOR INDIVIDUAL


def calcular_scores_cvf_individuo(row):
    """
    Calcula los scores de las 4 culturas para un empleado individual.
    
    Args:
        row: Fila del DataFrame con respuestas q60-q67
    
    Returns:
        Diccionario con scores de cada cultura (0-5)
    """
    scores = {}
    for cultura, info in PREGUNTAS_CVF.items():
        preguntas = [f'q{p}' for p in info["preguntas"]]
        scores[cultura] = np.mean([row[p] for p in preguntas])
    return scores


def clasificar_cultura_individual(scores):
    """
    Clasifica la cultura dominante para un empleado individual.
    
    Args:
        scores: Diccionario con scores de cada cultura
    
    Returns:
        Diccionario con cultura dominante y confianza
    """
    cultura_dominante = max(scores, key=scores.get)
    total = sum(scores.values())
    confianza = scores[cultura_dominante] / total if total > 0 else 0  # Índice simple de predominio de la cultura ganadora. No representa una probabilidad estadística.
    
    return {
        "cultura_dominante": cultura_dominante,
        "confianza": round(confianza, 3),
        "scores": scores
    }


# CLASIFICADOR ORGANIZACIONAL (agregado)


def clasificar_cultura_empresa(df_empleados):
    """
    Clasifica la cultura dominante de una empresa según la percepción
    agregada de sus empleados.
    
    Args:
        df_empleados: DataFrame con empleados de una empresa
    
    Returns:
        Diccionario con cultura dominante y distribución
    """
    # Calcular scores medios por cultura
    scores_empresa = {}
    for cultura, info in PREGUNTAS_CVF.items():
        preguntas = [f'q{p}' for p in info["preguntas"]]
        scores_empresa[cultura] = df_empleados[preguntas].mean().mean()
    
    # Cultura dominante
    cultura_dominante = max(scores_empresa, key=scores_empresa.get)
    total = sum(scores_empresa.values())
    confianza = scores_empresa[cultura_dominante] / total if total > 0 else 0
    
    # Distribución porcentual
    distribucion = {
        cultura: round(score / total * 100, 1)
        for cultura, score in scores_empresa.items()
    }
    
    return {
        "cultura_dominante": cultura_dominante,
        "confianza": round(confianza, 3),
        "scores": scores_empresa,
        "distribucion_pct": distribucion
    }



# GENERADOR DE CULTURA PARA BENCHMARK


def generar_cultura_percibida(n_empleados, cultura_real, seed=None):
    """
    Genera respuestas CVF realistas para empleados de una empresa
    con una cultura real dada.
    
    Incluye variabilidad individual (no todos perciben igual).
    
    Args:
        n_empleados: Número de empleados
        cultura_real: Cultura "real" de la empresa (la dominante)
        seed: Semilla para reproducibilidad
    
    Returns:
        DataFrame con columnas q60-q67
    """
    if seed is not None:
        np.random.seed(seed)
    
    respuestas = pd.DataFrame(index=range(n_empleados))
    
    # Base: cada cultura tiene su "nivel base" según la cultura real
    # La cultura real tiene valores altos, las demás tienen valores medios-bajos
    bases = {
        "Adhocracia": 2.0,
        "Clan": 2.0,
        "Mercado": 2.0,
        "Jerarquica": 2.0
    }
    
    # La cultura real tiene boost de +2.0
    bases[cultura_real] += 2.0
    
    # Generar respuestas con variabilidad individual
    for cultura, info in PREGUNTAS_CVF.items():
        base = bases[cultura]
        for q in info["preguntas"]:
            # Cada empleado percibe con variabilidad
            ruido = np.random.normal(0, 0.6, n_empleados)
            valor = base + ruido
            respuestas[f'q{q}'] = np.clip(np.round(valor), 1, 5).astype(int)
    
    return respuestas



# VALIDADOR DE CONSISTENCIA


def validar_clasificacion_cultura(df_empleados, cultura_esperada):
    """
    Valida que la cultura percibida coincide con la cultura esperada.
    
    Args:
        df_empleados: DataFrame con empleados
        cultura_esperada: Cultura que debería dominar
    
    Returns:
        Boolean indicando si la clasificación es correcta
    """
    resultado = clasificar_cultura_empresa(df_empleados)
    return resultado["cultura_dominante"] == cultura_esperada



# RESUMEN EJECUTIVO


def generar_informe_cultura(resultado_clasificacion):
    """
    Genera un informe textual de la cultura detectada.
    """
    cultura = resultado_clasificacion["cultura_dominante"]
    confianza = resultado_clasificacion["confianza"]
    dist = resultado_clasificacion["distribucion_pct"]
    info = PREGUNTAS_CVF[cultura]
    
    informe = f"""

  🏛️  CULTURA ORGANIZACIONAL DETECTADA (CVF)                   

                                                               
  🎯 Cultura dominante: {cultura.upper()}                      
  📊 Confianza: {confianza*100:.1f}%                           
  🧭 Ejes: {info['ejes']}                                      
  💡 Descripción: {info['descripcion']}                        
                                                               
  📈 DISTRIBUCIÓN PERCIBIDA:                                   
    🔵 Adhocracia:  {dist['Adhocracia']:5.1f}%                 
    🟢 Clan:        {dist['Clan']:5.1f}%                       
    🟠 Mercado:     {dist['Mercado']:5.1f}%                    
    🟡 Jerárquica:  {dist['Jerarquica']:5.1f}%                 
                                                               

"""
    return informe