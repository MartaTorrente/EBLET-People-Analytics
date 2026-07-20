"""
EBLET-Lite  - Cálculo de KPIs desde 23 preguntas
=====================================================
Mapeo de preguntas de la encuesta de Google Forms:
- q10-q13: Burnout (4 preguntas)
- q14-q17: Boreout (4 preguntas)
- q18-q21: Bienestar WHO-5 (4 preguntas)
- q22-q24: Rotación/Intención de cambio (3 preguntas)
- q25-q32: Cultura CVF (8 preguntas)
"""

import numpy as np


def calcular_kpis_lite(respuestas):
    """
    Calcula los KPIs a partir de las respuestas de EBLET-Lite.
    
    Args:
        respuestas: Diccionario con claves 'q10' a 'q32' (23 preguntas)
                   O lista/array de 23 valores en orden
    
    Returns:
        Diccionario con los KPIs calculados
    """
    # Si es diccionario, extraer valores
    if isinstance(respuestas, dict):
        # Burnout: q10-q13
        burnout_vals = [respuestas[f'q{i}'] for i in range(10, 14)]
        # Boreout: q14-q17
        boreout_vals = [respuestas[f'q{i}'] for i in range(14, 18)]
        # Bienestar: q18-q21
        bienestar_vals = [respuestas[f'q{i}'] for i in range(18, 22)]
        # Rotación: q22-q24
        rotacion_vals = [respuestas[f'q{i}'] for i in range(22, 25)]
        # Cultura CVF: q25-q32
        cvf_vals = [respuestas[f'q{i}'] for i in range(25, 33)]
    else:
        # Si es lista/array, usar índices
        burnout_vals = respuestas[0:4]      # q10-q13
        boreout_vals = respuestas[4:8]      # q14-q17
        bienestar_vals = respuestas[8:12]   # q18-q21
        rotacion_vals = respuestas[12:15]   # q22-q24
        cvf_vals = respuestas[15:23]        # q25-q32
    
    # Calcular KPIs
    kpis = {
        "burnout": np.mean(burnout_vals),
        "boreout": np.mean(boreout_vals),
        "bienestar": np.mean(bienestar_vals),
        "rotacion": np.mean(rotacion_vals),
        "cvf_adhocracia": np.mean(cvf_vals[0:2]),   # q25-q26
        "cvf_clan": np.mean(cvf_vals[2:4]),         # q27-q28
        "cvf_mercado": np.mean(cvf_vals[4:6]),      # q29-q30
        "cvf_jerarquica": np.mean(cvf_vals[6:8])    # q31-q32
    }
    
    # Determinar cultura dominante
    culturas = {
        "Adhocracia": kpis["cvf_adhocracia"],
        "Clan": kpis["cvf_clan"],
        "Mercado": kpis["cvf_mercado"],
        "Jerarquica": kpis["cvf_jerarquica"]
    }
    kpis["cultura_dominante"] = max(culturas, key=culturas.get)
    kpis["cultura_scores"] = culturas
    
    return kpis


def validar_respuestas(respuestas):
    """
    Valida que las respuestas sean correctas.
    
    Args:
        respuestas: Diccionario o lista de respuestas
    
    Returns:
        Tuple (valido, mensaje)
    """
    if isinstance(respuestas, dict):
        # Verificar que tenga todas las preguntas
        preguntas_requeridas = [f'q{i}' for i in range(10, 33)]
        faltantes = [p for p in preguntas_requeridas if p not in respuestas]
        
        if faltantes:
            return False, f"Faltan preguntas: {', '.join(faltantes)}"
        
        # Verificar rangos
        for q, val in respuestas.items():
            if not (1 <= val <= 5):
                return False, f"La pregunta {q} tiene valor {val} (debe ser 1-5)"
        
        return True, "Respuestas válidas"
    
    elif isinstance(respuestas, (list, np.ndarray)):
        if len(respuestas) != 23:
            return False, f"Se esperaban 23 respuestas, se recibieron {len(respuestas)}"
        
        for i, val in enumerate(respuestas):
            if not (1 <= val <= 5):
                return False, f"La respuesta {i+1} tiene valor {val} (debe ser 1-5)"
        
        return True, "Respuestas válidas"
    
    else:
        return False, "Formato de respuestas no válido"


# Ejemplo de uso
if __name__ == "__main__":
    # Caso de prueba: Persona con boreout alto
    respuestas_ejemplo = {
        # Burnout (q10-q13): bajo
        'q10': 2, 'q11': 1, 'q12': 2, 'q13': 1,
        # Boreout (q14-q17): alto
        'q14': 5, 'q15': 4, 'q16': 5, 'q17': 4,
        # Bienestar (q18-q21): bajo
        'q18': 2, 'q19': 2, 'q20': 2, 'q21': 1,
        # Rotación (q22-q24): medio-alto
        'q22': 3, 'q23': 4, 'q24': 3,
        # Cultura CVF (q25-q32)
        'q25': 2, 'q26': 2,  # Adhocracia
        'q27': 3, 'q28': 3,  # Clan
        'q29': 3, 'q30': 4,  # Mercado
        'q31': 5, 'q32': 5   # Jerarquica
    }
    
    # Validar
    valido, mensaje = validar_respuestas(respuestas_ejemplo)
    print(f"Validación: {mensaje}")
    
    # Calcular KPIs
    kpis = calcular_kpis_lite(respuestas_ejemplo)
    
    print("\n📊 KPIs calculados:")
    for kpi, valor in kpis.items():
        if isinstance(valor, float):
            print(f"   {kpi}: {valor:.2f}")
        else:
            print(f"   {kpi}: {valor}")