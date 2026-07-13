# -*- coding: utf-8 -*-
"""
EBLET v2.1 - Clasificador Individual de Perfiles de Bienestar

Clasifica a cada persona en uno de los 6 perfiles segun sus KPIs.
Genera recomendaciones personalizadas para cada perfil.
Incluye analisis de cultura organizacional percibida (CVF).
Muestra posicion vs benchmark de 12,500 empleados.

Cambio clave:
- "Rotacion" renombrado a "Intencion de cambio laboral"


Basado en literatura cientifica:
- Maslach & Leiter (2016): Burnout y engagement
- Rothlin & Werder (2007): Boreout
- Topp et al. (2015): WHO-5
- Mobley (1977): Intencion de rotacion
- Cameron & Quinn (2011): CVF (Cultura)
"""

import pandas as pd
import numpy as np



# BENCHMARK DE REFERENCIA (percentiles)


BENCHMARK_PERCENTILES = {
    "burnout": {"p25": 2.1, "p50": 2.8, "p75": 3.6, "media": 2.9},
    "boreout": {"p25": 1.9, "p50": 2.5, "p75": 3.3, "media": 2.6},
    "bienestar": {"p25": 2.4, "p50": 3.1, "p75": 3.8, "media": 3.2}
}



# DEFINICION DE LOS 6 PERFILES

PERFILES = {
    "flourishing": {
        "nombre": "🟢 Flourishing",
        "emoji": "🟢",
        "color": "#2ecc71",
        "descripcion": "Te encuentras en tu mejor momento profesional. Disfrutas de un rendimiento optimo y un bienestar pleno.",
        "condicion": lambda k: (
            k["burnout"] < 2.5 and 
            k["boreout"] < 2.5 and 
            k["bienestar"] >= 3.5
        ),
        "prioridad": 1,
        "consejos": [
            "Mantén el equilibrio trabajo-vida que has conseguido",
            "Comparte tu energía y experiencia con compañeros",
            "Considera roles de mentoría o liderazgo",
            "Sigue cultivando tus relaciones profesionales"
        ],
        "senal_alerta": "Si sientes que tu motivación baja con el tiempo, busca nuevos retos",
        "recursos": [
            "Libro: 'Flourish' de Martin Seligman",
            "Práctica: Journaling de gratitud laboral",
            "Hábito: Mentoría informal con compañeros más junior"
        ]
    },
    
    "estable": {
        "nombre": "🟡 Estable Neutro",
        "emoji": "🟡",
        "color": "#f1c40f",
        "descripcion": "Te encuentras razonablemente bien, aunque hay espacio para mejorar. Estás en una zona de confort laboral.",
        "condicion": lambda k: (
            k["burnout"] < 3.0 and 
            k["boreout"] < 3.0 and 
            2.5 <= k["bienestar"] < 3.5
        ),
        "prioridad": 2,
        "consejos": [
            "Explora qué aspectos de tu trabajo te apasionan más",
            "Propón pequeños proyectos que te motiven",
            "Habla con tu responsable sobre desarrollo profesional",
            "Busca actividades de aprendizaje continuo"
        ],
        "senal_alerta": "Si llevas más de 6 meses en esta zona sin cambios, actúa antes de que la situación empeore",
        "recursos": [
            "Libro: 'Drive' de Daniel Pink",
            "Práctica: Job crafting (rediseñar tu puesto)",
            "Hábito: 1 hora/semana de aprendizaje nuevo"
        ]
    },
    
    "quemado": {
        "nombre": "🟠 Quemado Activo",
        "emoji": "🟠",
        "color": "#e67e22",
        "descripcion": "Tu nivel de desgaste profesional es elevado. La carga de trabajo y la falta de recuperación están afectando tu bienestar.",
        "condicion": lambda k: (
            k["burnout"] >= 3.5 and 
            k["boreout"] < 3.0
        ),
        "prioridad": 3,
        "consejos": [
            "Habla con tu responsable sobre tu carga actual de trabajo",
            "Establece límites claros: horarios, desconexión digital",
            "Prioriza el descanso y la recuperación",
            "Practica técnicas de gestión del estrés (mindfulness, ejercicio)",
            "Considera solicitar una reducción temporal de carga"
        ],
        "senal_alerta": "Si tienes síntomas físicos (insomnio, ansiedad, fatiga constante), consulta con un profesional de la salud",
        "recursos": [
            "Libro: 'Burnout' de Emily y Amelia Nagoski",
            "Práctica: Mindfulness 10 min/día",
            "Organización: Colegio Oficial de Psicología"
        ]
    },
    
    "aburrido": {
        "nombre": "🔵 Aburrido Crónico",
        "emoji": "🔵",
        "color": "#3498db",
        "descripcion": "No estás cansado, pero tu trabajo no te estimula lo suficiente. Sientes que tus capacidades no se aprovechan plenamente.",
        "condicion": lambda k: (
            k["burnout"] < 2.5 and 
            k["boreout"] >= 3.5
        ),
        "prioridad": 4,
        "consejos": [
            "Propón job crafting: rediseña tu puesto con tu responsable",
            "Busca proyectos transversales o innovadores",
            "Solicita formación en áreas nuevas",
            "Considera rotación interna a otro departamento",
            "Propón mejoras en procesos que te resultan repetitivos"
        ],
        "senal_alerta": "Importante: NO apliques soluciones de burnout (menos carga) - eso empeoraría tu situación",
        "recursos": [
            "Libro: 'Boreout' de Rothlin y Werder",
            "Práctica: Job crafting (Wrzesniewski & Dutton)",
            "Hábito: Proponer 1 mejora al mes"
        ]
    },
    
    "critico": {
        "nombre": "🔴 Crítico Dual",
        "emoji": "🔴",
        "color": "#e74c3c",
        "descripcion": "Tu situación es delicada: sientes tanto desgaste como falta de estímulo. Esta combinación requiere atención prioritaria.",
        "condicion": lambda k: (
            k["burnout"] >= 3.5 and 
            k["boreout"] >= 3.5
        ),
        "prioridad": 5,
        "consejos": [
            "Considera hablar con un profesional (psicólogo/coach)",
            "Habla con RRHH sobre tu situación",
            "Evalúa seriamente un cambio de entorno laboral",
            "Establece límites inmediatos e innegociables",
            "Prioriza tu salud mental sobre cualquier objetivo laboral"
        ],
        "senal_alerta": "Esta situación puede afectar seriamente tu salud. No la pospongas.",
        "recursos": [
            "Teléfono de la Esperanza: 717 003 717",
            "Libro: 'The Burnout Challenge' de Michael Leiter",
            "Organización: Colegio Oficial de Psicología"
        ]
    },
    
    "vuelo": {
        "nombre": "⚫ Desvinculado",
        "emoji": "⚫",
        "color": "#34495e",
        "descripcion": "Tu nivel de desvinculación con la organización es elevado. Es probable que estés replanteándote tu continuidad.",
        "condicion": lambda k: (
            k["rotacion"] >= 3.5 and 
            k["bienestar"] < 3.0
        ),
        "prioridad": 6,
        "consejos": [
            "Antes de tomar decisiones, identifica qué no funciona exactamente",
            "Asegúrate de que un nuevo entorno no repita los mismos patrones",
            "Si decides cambiar, negocia condiciones beneficiosas",
            "Mantén relaciones profesionales positivas",
            "Aprovecha para reflexionar sobre tu carrera a largo plazo"
        ],
        "senal_alerta": "Cambiar de empresa sin resolver patrones internos puede hacer que la situación se repita",
        "recursos": [
            "Libro: 'What Color is Your Parachute?' de Richard Bolles",
            "Práctica: Ikigai (propósito profesional)",
            "Red: LinkedIn Learning para nuevas habilidades"
        ]
    }
}



# FUNCIONES AUXILIARES


def calcular_percentil(valor, kpi):
    """Calcula el percentil de un valor respecto al benchmark."""
    bench = BENCHMARK_PERCENTILES[kpi]
    
    if valor <= bench["p25"]:
        return int((valor / bench["p25"]) * 25)
    elif valor <= bench["p50"]:
        return 25 + int(((valor - bench["p25"]) / (bench["p50"] - bench["p25"])) * 25)
    elif valor <= bench["p75"]:
        return 50 + int(((valor - bench["p50"]) / (bench["p75"] - bench["p50"])) * 25)
    else:
        return 75 + int(((valor - bench["p75"]) / (5 - bench["p75"])) * 25)


def nivel_intencion_cambio(valor):
    """
    Clasifica el nivel de intención de cambio laboral.
    Usa lenguaje prudente y psicológicamente adecuado.
    """
    if valor >= 4.0:
        return "Elevada", "🔴"
    elif valor >= 3.0:
        return "Media", "🟡"
    else:
        return "Baja", "🟢"


def clasificar_individuo(kpis):
    """Clasifica a una persona en uno de los 6 perfiles."""
    # Calcular percentiles (solo para los 3 KPIs principales)
    percentiles = {
        "burnout": calcular_percentil(kpis["burnout"], "burnout"),
        "boreout": calcular_percentil(kpis["boreout"], "boreout"),
        "bienestar": calcular_percentil(kpis["bienestar"], "bienestar")
    }
    
    # Buscar perfil que cumpla la condicion
    for key, perfil in PERFILES.items():
        if perfil["condicion"](kpis):
            return {
                "perfil": key,
                "nombre": perfil["nombre"],
                "emoji": perfil["emoji"],
                "color": perfil["color"],
                "descripcion": perfil["descripcion"],
                "consejos": perfil["consejos"],
                "senal_alerta": perfil["senal_alerta"],
                "recursos": perfil["recursos"],
                "kpis": kpis,
                "percentiles": percentiles
            }
    
    # Si ningun perfil encaja perfectamente, asignar el mas cercano
    return {
        "perfil": "estable",
        "nombre": "🟡 Estable Neutro",
        "emoji": "🟡",
        "color": "#f1c40f",
        "descripcion": "Tu situación actual no encaja claramente en ningún patrón específico. Te encuentras en una zona intermedia.",
        "consejos": PERFILES["estable"]["consejos"],
        "senal_alerta": "Si sientes malestar persistente, consulta con un profesional",
        "recursos": PERFILES["estable"]["recursos"],
        "kpis": kpis,
        "percentiles": percentiles
    }


def clasificar_dataframe(df_kpis):
    """Clasifica multiples individuos a la vez."""
    df = df_kpis.copy()
    
    perfiles = []
    nombres = []
    
    for _, row in df.iterrows():
        kpis = {
            "burnout": row["burnout"],
            "boreout": row["boreout"],
            "bienestar": row["bienestar"],
            "rotacion": row["rotacion"],
            "contexto": row.get("contexto", 3.0)
        }
        
        if "cultura_dominante" in row:
            kpis["cultura_dominante"] = row["cultura_dominante"]
            kpis["cultura_scores"] = {
                "Adhocracia": row.get("cultura_adhocracia", 3),
                "Clan": row.get("cultura_clan", 3),
                "Mercado": row.get("cultura_mercado", 3),
                "Jerarquica": row.get("cultura_jerarquica", 3)
            }
        
        resultado = clasificar_individuo(kpis)
        perfiles.append(resultado["perfil"])
        nombres.append(resultado["nombre"])
    
    df["perfil"] = perfiles
    df["perfil_nombre"] = nombres
    
    return df



# GENERADOR DE INFORME INDIVIDUAL (v2.1)


def generar_informe_individual(kpis, perfil_resultado, respuestas_raw=None):
    """
    Genera un informe visual en texto para un individuo.
    
    Orden de prioridad:
    1. Perfil de bienestar
    2. Indicadores principales (Burnout, Boreout, Bienestar)
    3. Cultura organizacional percibida
    4. Intención de cambio laboral (complementario)
    5. Recomendaciones personalizadas
    """
    perfil = perfil_resultado
    percentiles = perfil_resultado.get("percentiles", {})
    
    def barra_porcentaje(valor, max_val=5):
        pct = (valor / max_val) * 100
        filled = int(pct / 5)
        return "█" * filled + "░" * (20 - filled)
    
    def semaforo_kpi(valor, umbral_bajo, umbral_alto, invertido=False):
        if invertido:
            if valor <= umbral_bajo: return "🔴"
            elif valor >= umbral_alto: return "🟢"
            else: return "🟡"
        else:
            if valor >= umbral_alto: return "🔴"
            elif valor <= umbral_bajo: return "🟢"
            else: return "🟡"
    
    def nivel_texto(percentil):
        if percentil >= 75: return "ELEVADO"
        elif percentil >= 50: return "MEDIO-ALTO"
        elif percentil >= 25: return "MEDIO-BAJO"
        else: return "BAJO"
    
    def texto_respuesta(valor):
        textos = {
            1: "Totalmente en desacuerdo",
            2: "En desacuerdo",
            3: "Neutral",
            4: "De acuerdo",
            5: "Totalmente de acuerdo"
        }
        return textos.get(int(round(valor)), "Sin respuesta")
    
  
    # 1. PERFIL DE BIENESTAR
    
    informe = f"""

  🎯 TU PERFIL DE BIENESTAR LABORAL


                    {perfil['nombre']}

  💬 {perfil['descripcion']}


  📊 TUS INDICADORES PRINCIPALES

"""
    
   
    # 2. INDICADORES PRINCIPALES (Burnout, Boreout, Bienestar)
   
    kpis_info = [
        ("🔥 Burnout", kpis['burnout'], 2.5, 3.5, False),
        ("😴 Boreout", kpis['boreout'], 2.5, 3.5, False),
        ("💚 Bienestar", kpis['bienestar'], 3.5, 2.5, True)
    ]
    
    for nombre, valor, umb_bajo, umb_alto, invertido in kpis_info:
        barra_vis = barra_porcentaje(valor)
        sem = semaforo_kpi(valor, umb_bajo, umb_alto, invertido)
        pct = int((valor / 5) * 100)
        informe += f"║    {nombre:12s}: {pct:3d}% {barra_vis} {sem}\n"
    
    informe += "║\n"
    
    
    # 3. CULTURA ORGANIZACIONAL PERCIBIDA
  
    if "cultura_scores" in kpis:
        informe += "\n"
        informe += "  🏛️ CULTURA DE TU ORGANIZACIÓN (según tu percepción)\n"
        informe += "\n"
        
        cultura_emojis = {
            "Adhocracia": "🔵",
            "Clan": "🟢",
            "Mercado": "🟠",
            "Jerarquica": "🟡"
        }
        
        cultura_descripciones = {
            "Adhocracia": "Innovación, creatividad, experimentación",
            "Clan": "Familia, colaboración, desarrollo personal",
            "Mercado": "Resultados, competitividad, logros",
            "Jerarquica": "Procesos, estabilidad, normas"
        }
        
        for cultura, valor in kpis["cultura_scores"].items():
            emoji = cultura_emojis.get(cultura, "⚪")
            barra_vis = barra_porcentaje(valor)
            es_dominante = "⭐" if cultura == kpis.get("cultura_dominante") else "  "
            informe += f"    {emoji} {cultura:12s}: {valor:.0f}/5 {barra_vis} {es_dominante}\n"
        
        informe += "\n"
        
        cultura_dom = kpis.get("cultura_dominante", "Desconocida")
        desc_cultura = cultura_descripciones.get(cultura_dom, "")
        informe += f"    🎯 Cultura predominante: {cultura_dom.upper()}\n"
        informe += f"       ({desc_cultura})\n"
        informe += "\n"
    
   
    # 4. INDICADORES COMPLEMENTARIOS
 
    informe += "\n"
    informe += "  🔗 INDICADORES COMPLEMENTARIOS\n"
    informe += "\n"
    
    # Intención de cambio laboral (renombrado)
    intencion_cambio = kpis.get("rotacion", 3)
    nivel_cambio, emoji_cambio = nivel_intencion_cambio(intencion_cambio)
    barra_vis = barra_porcentaje(intencion_cambio)
    
    informe += f"    🔀 Intención de cambio laboral: {nivel_cambio} {emoji_cambio}\n"
    informe += f"                   {barra_vis}\n"
    informe += "\n"
    
    # Compromiso con la organización (invertido de rotación)
    compromiso = 5 - intencion_cambio
    if compromiso >= 4:
        nivel_compromiso = "Elevado"
        emoji_compromiso = "🟢"
    elif compromiso >= 3:
        nivel_compromiso = "Medio"
        emoji_compromiso = "🟡"
    else:
        nivel_compromiso = "Bajo"
        emoji_compromiso = "🔴"
    
    informe += f"    💼 Compromiso con la organización: {nivel_compromiso} {emoji_compromiso}\n"
    informe += "\n"
    
    # Posición vs benchmark
    informe += "    📈 Tu posición respecto al benchmark (12,500 empleados):\n"
    for kpi in ["burnout", "boreout", "bienestar"]:
        percentil = percentiles.get(kpi, 50)
        nombre_kpi = {
            "burnout": "🔥 Burnout",
            "boreout": "😴 Boreout",
            "bienestar": "💚 Bienestar"
        }[kpi]
        nivel = nivel_texto(percentil)
        informe += f"       {nombre_kpi:12s}: Percentil {percentil:3d} ({nivel})\n"
    
    informe += "\n"
    

    # 5. RECOMENDACIONES PERSONALIZADAS
  
    informe += "\n"
    informe += "  🎯 RECOMENDACIONES PERSONALIZADAS\n"
    informe += "\n"
    
    # Recomendaciones base del perfil
    for i, consejo in enumerate(perfil["consejos"], 1):
        informe += f"    {i}. {consejo}\n"
    
    informe += "\n"
    
    # 🆕 Recomendaciones adicionales según combinación con intención de cambio
    perfil_key = perfil["perfil"]
    intencion = kpis.get("rotacion", 3)
    
    if perfil_key in ["quemado", "aburrido", "critico"]:
        if intencion >= 3.5:
            informe += "    💡 REFLEXIÓN ADICIONAL:\n"
            informe += "    Es posible que estés considerando un cambio de empleo. Antes de\n"
            informe += "    tomar una decisión, identifica qué aspectos concretos de tu\n"
            informe += "    trabajo están contribuyendo a esta situación y valora si podrían\n"
            informe += "    abordarse dentro de tu organización actual.\n"
        elif intencion < 2.5:
            informe += "    💡 REFLEXIÓN ADICIONAL:\n"
            informe += "    Aunque actualmente no pareces plantearte un cambio de empleo,\n"
            informe += "    tus respuestas indican un nivel elevado de desgaste o\n"
            informe += "    desmotivación. Sería recomendable actuar antes de que esta\n"
            informe += "    situación se cronifique.\n"
    
    informe += "\n"
    
    # Señal de alerta
    informe += f"  ⚠️  {perfil['senal_alerta']}\n"
    informe += "\n"
    
    # Recursos
    informe += "\n"
    informe += "  📚 RECURSOS RECOMENDADOS\n"
    informe += "\n"
    
    for recurso in perfil["recursos"]:
        informe += f"    • {recurso}\n"
    
    informe += """

"""
    
    return informe



# EJECUCION DE PRUEBA

if __name__ == "__main__":
    from encuesta_lite import calcular_kpis_lite, validar_respuestas
    
    print(" TEST DEL CLASIFICADOR INDIVIDUAL (EBLET-Lite v2.1)")
    print("="*80)
    
    # Caso 1: Persona aburrida con alta intención de cambio
    print("\n🔵 CASO 1: Persona aburrida con alta intención de cambio")
    respuestas_1 = {
        # Burnout (q10-q13): bajo
        'q10': 2, 'q11': 2, 'q12': 2, 'q13': 2,
        # Boreout (q14-q17): alto
        'q14': 5, 'q15': 4, 'q16': 5, 'q17': 5,
        # Bienestar (q18-q21): bajo
        'q18': 2, 'q19': 2, 'q20': 2, 'q21': 2,
        # Rotación (q22-q24): alta
        'q22': 4, 'q23': 4, 'q24': 4,
        # Cultura CVF (q25-q32): Jerarquica predominante
        'q25': 2, 'q26': 2,  # Adhocracia
        'q27': 2, 'q28': 2,  # Clan
        'q29': 3, 'q30': 3,  # Mercado
        'q31': 5, 'q32': 5   # Jerarquica
    }
    
    valido, msg = validar_respuestas(respuestas_1)
    print(f"Validación: {msg}")
    
    kpis_1 = calcular_kpis_lite(respuestas_1)
    resultado_1 = clasificar_individuo(kpis_1)
    print(generar_informe_individual(kpis_1, resultado_1, respuestas_1))
    
    # Caso 2: Persona quemada con BAJA intención de cambio
    print("\n🟠 CASO 2: Persona quemada con baja intención de cambio")
    respuestas_2 = {
        # Burnout (q10-q13): alto
        'q10': 5, 'q11': 5, 'q12': 4, 'q13': 4,
        # Boreout (q14-q17): bajo
        'q14': 2, 'q15': 2, 'q16': 2, 'q17': 2,
        # Bienestar (q18-q21): bajo
        'q18': 2, 'q19': 1, 'q20': 2, 'q21': 2,
        # Rotación (q22-q24): baja
        'q22': 2, 'q23': 2, 'q24': 2,
        # Cultura CVF (q25-q32): Mercado predominante
        'q25': 2, 'q26': 2,  # Adhocracia
        'q27': 2, 'q28': 2,  # Clan
        'q29': 5, 'q30': 5,  # Mercado
        'q31': 3, 'q32': 3   # Jerarquica
    }
    
    valido, msg = validar_respuestas(respuestas_2)
    print(f"Validación: {msg}")
    
    kpis_2 = calcular_kpis_lite(respuestas_2)
    resultado_2 = clasificar_individuo(kpis_2)
    print(generar_informe_individual(kpis_2, resultado_2, respuestas_2))