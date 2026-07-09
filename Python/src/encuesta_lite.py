# -*- coding: utf-8 -*-
"""EBLET-Lite v2.0: 23 preguntas para clasificacion individual + cultura CVF

Estructura:
- Burnout: 4 preguntas (MBI-GS)
- Boreout: 4 preguntas (EAL)
- Bienestar: 4 preguntas (WHO-5)
- Rotacion: 3 preguntas (Mobley)
- Cultura CVF: 8 preguntas (2 por cultura)
Total: 23 preguntas (~8 minutos)
"""

import numpy as np
import pandas as pd

PREGUNTAS_LITE = {
    "burnout": {"preguntas": [16, 19, 23, 28], "peso": 4, "items": {
        16: "Me siento emocionalmente agotado/a por mi trabajo.",
        19: "Trabajar todo el dia es un verdadero esfuerzo.",
        23: "He desarrollado una actitud distante hacia mi trabajo.",
        28: "Me he vuelto menos entusiasta con mi trabajo."}},
    "boreout": {"preguntas": [37, 39, 41, 43], "peso": 4, "items": {
        37: "Mi trabajo me resulta monotono y repetitivo.",
        39: "Tengo la sensacion de que mi trabajo carece de sentido.",
        41: "A menudo me aburro en el trabajo.",
        43: "Siento que estoy infrautilizado/a en mis funciones."}},
    "bienestar": {"preguntas": [45, 46, 47, 48], "peso": 4, "items": {
        45: "Me he sentido alegre y de buen humor.",
        46: "Me he sentido tranquilo/a y relajado/a.",
        47: "Me he sentido activo/a y vigoroso/a.",
        48: "He tenido energia para hacer las cosas del dia a dia."}},
    "rotacion": {"preguntas": [57, 58, 59], "peso": 3, "items": {
        57: "Estoy buscando activamente otro empleo.",
        58: "Es probable que cambie de empresa el proximo ano.",
        59: "A veces pienso en dejar mi trabajo."}},
    "cultura_cvf": {"preguntas": [65, 66, 67, 68, 69, 70, 71, 72], "peso": 8, "items": {
        65: "En mi organizacion se fomenta experimentar con nuevas ideas.",
        66: "Se valora la creatividad y la innovacion.",
        67: "Existe buena colaboracion entre companeros.",
        68: "Mi responsable se preocupa por las personas.",
        69: "Los objetivos son prioritarios en mi organizacion.",
        70: "Existe presion por conseguir resultados.",
        71: "Los procedimientos estan claramente definidos.",
        72: "Hay normas y reglas que seguir."}}
}

TEXTO_PREGUNTAS = {}
for dim, info in PREGUNTAS_LITE.items():
    for q, texto in info["items"].items():
        TEXTO_PREGUNTAS[q] = texto

PREGUNTAS_ORDENADAS = [16, 19, 23, 28, 37, 39, 41, 43, 45, 46, 47, 48, 57, 58, 59, 65, 66, 67, 68, 69, 70, 71, 72]


def calcular_kpis_lite(respuestas):
    """Calcula KPIs + cultura a partir de las 23 respuestas."""
    if isinstance(respuestas, pd.DataFrame):
        if len(respuestas) == 1:
            respuestas = respuestas.iloc[0].to_dict()
        else:
            raise ValueError("Solo se admite una fila")
    
    kpis = {}
    kpis["burnout"] = np.mean([respuestas.get(f'q{q}', respuestas.get(q, 3)) for q in PREGUNTAS_LITE["burnout"]["preguntas"]])
    kpis["boreout"] = np.mean([respuestas.get(f'q{q}', respuestas.get(q, 3)) for q in PREGUNTAS_LITE["boreout"]["preguntas"]])
    kpis["bienestar"] = np.mean([respuestas.get(f'q{q}', respuestas.get(q, 3)) for q in PREGUNTAS_LITE["bienestar"]["preguntas"]])
    kpis["rotacion"] = np.mean([respuestas.get(f'q{q}', respuestas.get(q, 3)) for q in PREGUNTAS_LITE["rotacion"]["preguntas"]])
    
    # Cultura CVF (8 preguntas, 2 por cultura)
    kpis["cultura_adhocracia"] = np.mean([respuestas.get(f'q{q}', respuestas.get(q, 3)) for q in [65, 66]])
    kpis["cultura_clan"] = np.mean([respuestas.get(f'q{q}', respuestas.get(q, 3)) for q in [67, 68]])
    kpis["cultura_mercado"] = np.mean([respuestas.get(f'q{q}', respuestas.get(q, 3)) for q in [69, 70]])
    kpis["cultura_jerarquica"] = np.mean([respuestas.get(f'q{q}', respuestas.get(q, 3)) for q in [71, 72]])
    
    culturas = {
        "Adhocracia": kpis["cultura_adhocracia"],
        "Clan": kpis["cultura_clan"],
        "Mercado": kpis["cultura_mercado"],
        "Jerarquica": kpis["cultura_jerarquica"]
    }
    kpis["cultura_dominante"] = max(culturas, key=culturas.get)
    kpis["cultura_scores"] = culturas
    return kpis


def validar_respuestas(respuestas):
    """Valida que las respuestas sean correctas."""
    esperadas = set(PREGUNTAS_ORDENADAS)
    recibidas = set()
    for key in respuestas.keys():
        if isinstance(key, str) and key.startswith('q'):
            recibidas.add(int(key[1:]))
        else:
            recibidas.add(int(key))
    faltantes = esperadas - recibidas
    if faltantes:
        return False, f"Faltan: {faltantes}"
    for key, valor in respuestas.items():
        if not (1 <= valor <= 5):
            return False, f"Valor invalido en {key}: {valor}"
    return True, "OK"


def generar_texto_formulario():
    """Genera texto para Google Forms."""
    texto = "EBLET-Lite v2.0: Evaluacion Rapida de Bienestar Laboral\n\n"
    texto += "Escala: 1 (Totalmente en desacuerdo) a 5 (Totalmente de acuerdo)\n\n"
    
    secciones = {
        "BURNOUT": [16, 19, 23, 28],
        "BOREOUT": [37, 39, 41, 43],
        "BIENESTAR": [45, 46, 47, 48],
        "ROTACION": [57, 58, 59],
        "CULTURA - Innovacion": [65, 66],
        "CULTURA - Colaboracion": [67, 68],
        "CULTURA - Resultados": [69, 70],
        "CULTURA - Normas": [71, 72]
    }
    
    num = 1
    for seccion, preguntas in secciones.items():
        texto += f"\n--- {seccion} ---\n"
        for q in preguntas:
            texto += f"{num}. {TEXTO_PREGUNTAS[q]}\n"
            num += 1
    
    return texto


if __name__ == "__main__":
    print("=" * 70)
    print("EBLET-Lite v2.0: 23 PREGUNTAS")
    print("=" * 70)
    print("\nTEXTO PARA GOOGLE FORMS:\n")
    print(generar_texto_formulario())
    
    print("\n" + "=" * 70)
    print("TEST CON RESPUESTAS SIMULADAS")
    print("=" * 70)
    
    test = {
        'q16': 2, 'q19': 2, 'q23': 2, 'q28': 2,
        'q37': 5, 'q39': 4, 'q41': 5, 'q43': 5,
        'q45': 2, 'q46': 2, 'q47': 2, 'q48': 2,
        'q57': 4, 'q58': 4, 'q59': 4,
        'q65': 2, 'q66': 2,
        'q67': 2, 'q68': 2,
        'q69': 3, 'q70': 3,
        'q71': 5, 'q72': 5
    }
    
    valido, msg = validar_respuestas(test)
    print(f"\nValidacion: {msg}")
    
    kpis = calcular_kpis_lite(test)
    print("\nKPIs calculados:")
    for kpi, valor in kpis.items():
        if kpi != "cultura_scores":
            if isinstance(valor, (int, float)):
                print(f"   {kpi:20s}: {valor:.2f}")
            else:
                print(f"   {kpi:20s}: {valor}")
    
    print("\nCultura percibida:")
    for cultura, valor in kpis["cultura_scores"].items():
        estrella = " <-- DOMINANTE" if cultura == kpis["cultura_dominante"] else ""
        print(f"   {cultura:12s}: {valor:.0f}/5{estrella}")
    print(f"   => Dominante: {kpis['cultura_dominante']}")