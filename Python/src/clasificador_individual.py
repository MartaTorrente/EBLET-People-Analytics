# -*- coding: utf-8 -*-
"""
EBLET - Clasificador Individual de Perfiles de Bienestar
=============================================================

Clasifica a cada persona en uno de los cinco perfiles principales
de bienestar laboral según sus KPIs.

Perfiles:
- Equilibrio
- Estable
- Riesgo de Burnout
- Riesgo de Boreout
- Crítico

La intención de cambio laboral se mantiene como indicador
complementario, pero no determina el perfil principal.

Incluye:
- Clasificación individual.
- Percentiles respecto al benchmark.
- Análisis de cultura organizacional percibida.
- Generación de informes individuales.
- Recomendaciones según el perfil.

Basado en:
- Maslach & Leiter (2016): Burnout y engagement.
- Rothlin & Werder (2007): Boreout.
- Topp et al. (2015): WHO-5.
- Mobley (1977): Intención de rotación.
- Cameron & Quinn (2011): Cultura organizacional CVF.
"""

import numpy as np
import pandas as pd


# =====================================================
# BENCHMARK DE REFERENCIA
# =====================================================

BENCHMARK_PERCENTILES = {
    "burnout": {
        "p25": 2.1,
        "p50": 2.8,
        "p75": 3.6,
        "media": 2.9
    },
    "boreout": {
        "p25": 1.9,
        "p50": 2.5,
        "p75": 3.3,
        "media": 2.6
    },
    "bienestar": {
        "p25": 2.4,
        "p50": 3.1,
        "p75": 3.8,
        "media": 3.2
    },
    "rotacion": {
        "p25": 2.0,
        "p50": 3.0,
        "p75": 4.0
    }
}


# =====================================================
# UMBRALES DE CLASIFICACIÓN
# =====================================================

# Un valor igual o superior a 3.5 entra en riesgo.
UMBRAL_RIESGO = 3.5

# Requisitos para considerar un perfil de equilibrio.
UMBRAL_EQUILIBRIO = 2.5
UMBRAL_BIENESTAR_ALTO = 3.5


# =====================================================
# DEFINICIÓN DE LOS CINCO PERFILES
# =====================================================

PERFILES = {
    "flourishing": {
        "nombre": "🟢 Equilibrio",
        "emoji": "🟢",
        "color": "#5B8A72",
        "descripcion": (
            "Presentas niveles reducidos de burnout y boreout, "
            "acompañados de un nivel elevado de bienestar laboral."
        ),
        "consejos": [
            "Mantén el equilibrio entre trabajo y vida personal",
            "Continúa desarrollando actividades profesionales estimulantes",
            "Comparte buenas prácticas con tus compañeros",
            "Mantén espacios regulares de descanso y recuperación"
        ],
        "senal_alerta": (
            "Presta atención a posibles cambios prolongados "
            "en tu motivación, energía o satisfacción laboral."
        ),
        "recursos": [
            "Práctica: revisión periódica del equilibrio laboral",
            "Hábito: aprendizaje y desarrollo continuo",
            "Actividad: participación en proyectos motivadores"
        ]
    },

    "estable": {
        "nombre": "🟡 Estable",
        "emoji": "🟡",
        "color": "#C6A15B",
        "descripcion": (
            "No presentas niveles elevados de burnout o boreout, "
            "aunque existe margen para mejorar tu bienestar laboral."
        ),
        "consejos": [
            "Identifica los aspectos de tu trabajo que más te motivan",
            "Propón pequeños retos o proyectos de mejora",
            "Habla con tu responsable sobre desarrollo profesional",
            "Mantén hábitos de descanso y desconexión"
        ],
        "senal_alerta": (
            "Si el malestar o la falta de motivación persisten, "
            "conviene revisar sus posibles causas."
        ),
        "recursos": [
            "Práctica: job crafting o rediseño de tareas",
            "Hábito: una actividad de aprendizaje semanal",
            "Actividad: revisión periódica de objetivos profesionales"
        ]
    },

    "quemado": {
        "nombre": "🟠 Riesgo de Burnout",
        "emoji": "🟠",
        "color": "#B36A3C",
        "descripcion": (
            "Tu puntuación de burnout alcanza el umbral de riesgo. "
            "El desgaste y la falta de recuperación podrían estar "
            "afectando a tu bienestar laboral."
        ),
        "consejos": [
            "Revisa tu carga y ritmo de trabajo",
            "Establece límites claros de horario y desconexión",
            "Prioriza el descanso y la recuperación",
            "Habla con tu responsable sobre las demandas actuales",
            "Solicita apoyo profesional si el malestar persiste"
        ],
        "senal_alerta": (
            "Si aparecen síntomas persistentes de ansiedad, insomnio "
            "o agotamiento, consulta con un profesional de la salud."
        ),
        "recursos": [
            "Práctica: desconexión digital",
            "Hábito: pausas y recuperación planificadas",
            "Recurso: profesional de la salud o psicología"
        ]
    },

    "aburrido": {
        "nombre": "🔵 Riesgo de Boreout",
        "emoji": "🔵",
        "color": "#3E6C8F",
        "descripcion": (
            "Tu puntuación de boreout alcanza el umbral de riesgo. "
            "Es posible que tus tareas no proporcionen suficiente "
            "estimulación, variedad o sentido profesional."
        ),
        "consejos": [
            "Explora posibilidades de rediseño de tus tareas",
            "Solicita proyectos con mayor variedad o dificultad",
            "Propón mejoras en procesos repetitivos",
            "Busca oportunidades de formación",
            "Valora opciones de movilidad interna"
        ],
        "senal_alerta": (
            "Reducir todavía más la carga de trabajo podría aumentar "
            "la falta de estimulación."
        ),
        "recursos": [
            "Práctica: job crafting o rediseño del puesto",
            "Hábito: propuesta periódica de mejoras",
            "Actividad: participación en proyectos transversales"
        ]
    },

    "critico": {
        "nombre": "🔴 Crítico",
        "emoji": "🔴",
        "color": "#8F2D2D",
        "descripcion": (
            "Tus puntuaciones de burnout y boreout alcanzan "
            "simultáneamente el umbral de riesgo. Esta combinación "
            "requiere una atención prioritaria."
        ),
        "consejos": [
            "Analiza conjuntamente la carga y el contenido de tu trabajo",
            "Habla con tu responsable o con Recursos Humanos",
            "Establece límites inmediatos y espacios de recuperación",
            "Valora cambios en tareas, responsabilidades o entorno",
            "Solicita apoyo profesional si la situación persiste"
        ],
        "senal_alerta": (
            "La combinación de desgaste y desmotivación puede afectar "
            "de manera importante al bienestar. No conviene posponer "
            "su evaluación."
        ),
        "recursos": [
            "Recurso: profesional de la salud o psicología",
            "Práctica: evaluación de demandas y recursos laborales",
            "Actividad: revisión estructurada de la situación profesional"
        ]
    }
}


# =====================================================
# FUNCIONES AUXILIARES
# =====================================================

def calcular_percentil(valor, kpi):
    """
    Calcula el percentil aproximado de un valor respecto al benchmark.

    Args:
        valor: Puntuación del KPI en escala 1-5.
        kpi: Nombre del KPI en BENCHMARK_PERCENTILES.

    Returns:
        Percentil entero entre 0 y 100.
    """

    if kpi not in BENCHMARK_PERCENTILES:
        raise KeyError(
            f"El KPI '{kpi}' no existe en el benchmark."
        )

    bench = BENCHMARK_PERCENTILES[kpi]

    valor = float(valor)

    if valor <= bench["p25"]:
        percentil = (
            valor / bench["p25"]
        ) * 25

    elif valor <= bench["p50"]:
        percentil = 25 + (
            (valor - bench["p25"])
            / (bench["p50"] - bench["p25"])
        ) * 25

    elif valor <= bench["p75"]:
        percentil = 50 + (
            (valor - bench["p50"])
            / (bench["p75"] - bench["p50"])
        ) * 25

    else:
        percentil = 75 + (
            (valor - bench["p75"])
            / (5 - bench["p75"])
        ) * 25

    # Garantizar un resultado entre 0 y 100.
    percentil = np.clip(percentil, 0, 100)

    return int(round(percentil))


def nivel_intencion_cambio(valor):
    """
    Clasifica el nivel de intención de cambio laboral.

    La intención de cambio es un indicador complementario
    y no determina el perfil principal.
    """

    if valor >= 4.0:
        return "Elevada", "🔴"

    if valor >= 3.0:
        return "Media", "🟡"

    return "Baja", "🟢"


def obtener_perfil(perfil_key, kpis, percentiles):
    """
    Construye el diccionario completo de resultado
    para un perfil determinado.
    """

    perfil = PERFILES[perfil_key]

    return {
        "perfil": perfil_key,
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


# =====================================================
# CLASIFICACIÓN INDIVIDUAL
# =====================================================

def clasificar_individuo(kpis):
    """
    Clasifica a una persona en uno de los cinco perfiles EBLET-Lite.

    Orden de clasificación:
    1. Crítico.
    2. Riesgo de Burnout.
    3. Riesgo de Boreout.
    4. Equilibrio.
    5. Estable.

    Criterios:
    - Crítico:
        burnout >= 3.5 y boreout >= 3.5

    - Riesgo de Burnout:
        burnout >= 3.5 y boreout < 3.5

    - Riesgo de Boreout:
        burnout < 3.5 y boreout >= 3.5

    - Equilibrio:
        burnout < 2.5,
        boreout < 2.5,
        bienestar >= 3.5

    - Estable:
        resto de combinaciones.

    La intención de cambio laboral no sustituye al perfil principal.
    """

    claves_requeridas = [
        "burnout",
        "boreout",
        "bienestar",
        "rotacion"
    ]

    faltantes = [
        clave
        for clave in claves_requeridas
        if clave not in kpis
    ]

    if faltantes:
        raise KeyError(
            "Faltan los siguientes KPIs para clasificar: "
            + ", ".join(faltantes)
        )

    burnout = float(kpis["burnout"])
    boreout = float(kpis["boreout"])
    bienestar = float(kpis["bienestar"])
    rotacion = float(kpis["rotacion"])

    valores = {
        "burnout": burnout,
        "boreout": boreout,
        "bienestar": bienestar,
        "rotacion": rotacion
    }

    for nombre, valor in valores.items():
        if not 1 <= valor <= 5:
            raise ValueError(
                f"El KPI '{nombre}' tiene valor {valor}. "
                "Debe estar entre 1 y 5."
            )

    percentiles = {
        "burnout": calcular_percentil(
            burnout,
            "burnout"
        ),
        "boreout": calcular_percentil(
            boreout,
            "boreout"
        ),
        "bienestar": calcular_percentil(
            bienestar,
            "bienestar"
        ),
        "rotacion": calcular_percentil(
            rotacion,
            "rotacion"
        )
    }

    # 1. Crítico
    if (
        burnout >= UMBRAL_RIESGO
        and boreout >= UMBRAL_RIESGO
    ):
        perfil_key = "critico"

    # 2. Riesgo de Burnout
    elif burnout >= UMBRAL_RIESGO:
        perfil_key = "quemado"

    # 3. Riesgo de Boreout
    elif boreout >= UMBRAL_RIESGO:
        perfil_key = "aburrido"

    # 4. Equilibrio
    elif (
        burnout < UMBRAL_EQUILIBRIO
        and boreout < UMBRAL_EQUILIBRIO
        and bienestar >= UMBRAL_BIENESTAR_ALTO
    ):
        perfil_key = "flourishing"

    # 5. Estable
    else:
        perfil_key = "estable"

    return obtener_perfil(
        perfil_key,
        kpis,
        percentiles
    )


# =====================================================
# CLASIFICACIÓN DE DATAFRAMES
# =====================================================

def clasificar_dataframe(df_kpis):
    """
    Clasifica múltiples individuos en los cinco perfiles EBLET-Lite.

    El DataFrame debe contener:
    - burnout
    - boreout
    - bienestar
    - rotacion

    Opcionalmente puede contener:
    - contexto
    - cultura_dominante
    - cultura_adhocracia
    - cultura_clan
    - cultura_mercado
    - cultura_jerarquica
    """

    columnas_requeridas = [
        "burnout",
        "boreout",
        "bienestar",
        "rotacion"
    ]

    columnas_faltantes = [
        columna
        for columna in columnas_requeridas
        if columna not in df_kpis.columns
    ]

    if columnas_faltantes:
        raise KeyError(
            "Faltan columnas necesarias para clasificar: "
            + ", ".join(columnas_faltantes)
        )

    df = df_kpis.copy()

    perfiles = []
    nombres = []

    for _, row in df.iterrows():

        kpis = {
            "burnout": row["burnout"],
            "boreout": row["boreout"],
            "bienestar": row["bienestar"],
            "rotacion": row["rotacion"],
            "contexto": row.get(
                "contexto",
                3.0
            )
        }

        if "cultura_dominante" in df.columns:
            kpis["cultura_dominante"] = row.get(
                "cultura_dominante"
            )

            kpis["cultura_scores"] = {
                "Adhocracia": row.get(
                    "cultura_adhocracia",
                    3.0
                ),
                "Clan": row.get(
                    "cultura_clan",
                    3.0
                ),
                "Mercado": row.get(
                    "cultura_mercado",
                    3.0
                ),
                "Jerarquica": row.get(
                    "cultura_jerarquica",
                    3.0
                )
            }

        resultado = clasificar_individuo(kpis)

        perfiles.append(
            resultado["perfil"]
        )

        nombres.append(
            resultado["nombre"]
        )

    df["perfil"] = perfiles
    df["perfil_nombre"] = nombres

    return df


# =====================================================
# GENERADOR DE INFORME INDIVIDUAL
# =====================================================

def generar_informe_individual(
    kpis,
    perfil_resultado,
    respuestas_raw=None
):
    """
    Genera un informe visual en texto para un individuo.

    Orden:
    1. Perfil de bienestar.
    2. Indicadores principales.
    3. Cultura organizacional percibida.
    4. Intención de cambio laboral.
    5. Posición respecto al benchmark.
    6. Recomendaciones.
    """

    perfil = perfil_resultado

    percentiles = perfil_resultado.get(
        "percentiles",
        {}
    )

    def barra_porcentaje(valor, max_val=5):
        porcentaje = (
            float(valor)
            / max_val
        ) * 100

        bloques_llenos = int(
            porcentaje / 5
        )

        bloques_llenos = min(
            max(bloques_llenos, 0),
            20
        )

        return (
            "█" * bloques_llenos
            + "░" * (20 - bloques_llenos)
        )

    def semaforo_kpi(
        valor,
        umbral_bajo,
        umbral_alto,
        invertido=False
    ):
        if invertido:
            if valor <= umbral_bajo:
                return "🔴"

            if valor >= umbral_alto:
                return "🟢"

            return "🟡"

        if valor >= umbral_alto:
            return "🔴"

        if valor <= umbral_bajo:
            return "🟢"

        return "🟡"

    def nivel_texto(percentil):
        if percentil >= 75:
            return "ELEVADO"

        if percentil >= 50:
            return "MEDIO-ALTO"

        if percentil >= 25:
            return "MEDIO-BAJO"

        return "BAJO"

    informe = f"""

============================================================
🎯 TU PERFIL DE BIENESTAR LABORAL
============================================================

{perfil["nombre"]}

{perfil["descripcion"]}


📊 INDICADORES PRINCIPALES
------------------------------------------------------------

"""

    kpis_info = [
        (
            "🔥 Burnout",
            kpis["burnout"],
            2.5,
            UMBRAL_RIESGO,
            False
        ),
        (
            "😴 Boreout",
            kpis["boreout"],
            2.5,
            UMBRAL_RIESGO,
            False
        ),
        (
            "💚 Bienestar",
            kpis["bienestar"],
            2.5,
            3.5,
            True
        )
    ]

    for (
        nombre,
        valor,
        umbral_bajo,
        umbral_alto,
        invertido
    ) in kpis_info:

        barra = barra_porcentaje(valor)

        semaforo = semaforo_kpi(
            valor,
            umbral_bajo,
            umbral_alto,
            invertido
        )

        porcentaje = int(
            (float(valor) / 5) * 100
        )

        informe += (
            f"{nombre:16s}: "
            f"{float(valor):.2f}/5 "
            f"({porcentaje:3d} %) "
            f"{barra} {semaforo}\n"
        )

    # -------------------------------------------------
    # Cultura organizacional
    # -------------------------------------------------

    if "cultura_scores" in kpis:
        informe += """

🏛️ CULTURA DE LA ORGANIZACIÓN
Según tu percepción
------------------------------------------------------------

"""

        cultura_emojis = {
            "Adhocracia": "🔵",
            "Clan": "🟢",
            "Mercado": "🟠",
            "Jerarquica": "🟡"
        }

        cultura_descripciones = {
            "Adhocracia": (
                "Innovación, creatividad y experimentación"
            ),
            "Clan": (
                "Colaboración, apoyo y desarrollo personal"
            ),
            "Mercado": (
                "Resultados, competitividad y logro"
            ),
            "Jerarquica": (
                "Procesos, estabilidad y normas"
            )
        }

        cultura_dominante = kpis.get(
            "cultura_dominante",
            "Desconocida"
        )

        for cultura, valor in kpis["cultura_scores"].items():

            emoji = cultura_emojis.get(
                cultura,
                "⚪"
            )

            barra = barra_porcentaje(valor)

            es_dominante = (
                "⭐"
                if cultura == cultura_dominante
                else ""
            )

            informe += (
                f"{emoji} {cultura:12s}: "
                f"{float(valor):.2f}/5 "
                f"{barra} {es_dominante}\n"
            )

        descripcion_cultura = (
            cultura_descripciones.get(
                cultura_dominante,
                ""
            )
        )

        informe += (
            "\nCultura predominante: "
            f"{str(cultura_dominante).upper()}\n"
            f"{descripcion_cultura}\n"
        )

    # -------------------------------------------------
    # Indicadores complementarios
    # -------------------------------------------------

    informe += """

🔗 INDICADORES COMPLEMENTARIOS
------------------------------------------------------------

"""

    intencion_cambio = float(
        kpis.get(
            "rotacion",
            3.0
        )
    )

    nivel_cambio, emoji_cambio = (
        nivel_intencion_cambio(
            intencion_cambio
        )
    )

    barra_cambio = barra_porcentaje(
        intencion_cambio
    )

    informe += (
        "🔀 Intención de cambio laboral: "
        f"{nivel_cambio} {emoji_cambio}\n"
        f"   Puntuación: {intencion_cambio:.2f}/5\n"
        f"   {barra_cambio}\n"
    )

    # Mantener el cálculo empleado anteriormente.
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

    informe += (
        "\n💼 Indicador complementario de compromiso: "
        f"{nivel_compromiso} {emoji_compromiso}\n"
    )

    # -------------------------------------------------
    # Benchmark
    # -------------------------------------------------

    informe += """

📈 POSICIÓN RESPECTO AL BENCHMARK
12.500 empleados sintéticos
------------------------------------------------------------

"""

    nombres_kpi = {
        "burnout": "🔥 Burnout",
        "boreout": "😴 Boreout",
        "bienestar": "💚 Bienestar",
        "rotacion": "🔀 Intención de cambio"
    }

    for nombre_kpi in [
        "burnout",
        "boreout",
        "bienestar",
        "rotacion"
    ]:
        percentil = percentiles.get(
            nombre_kpi,
            50
        )

        nivel = nivel_texto(
            percentil
        )

        informe += (
            f"{nombres_kpi[nombre_kpi]:24s}: "
            f"Percentil {percentil:3d} "
            f"({nivel})\n"
        )

    # -------------------------------------------------
    # Recomendaciones
    # -------------------------------------------------

    informe += """

🎯 RECOMENDACIONES
------------------------------------------------------------

"""

    for indice, consejo in enumerate(
        perfil["consejos"],
        start=1
    ):
        informe += (
            f"{indice}. {consejo}\n"
        )

    perfil_key = perfil["perfil"]

    if perfil_key in [
        "quemado",
        "aburrido",
        "critico"
    ]:
        if intencion_cambio >= 3.5:
            informe += """

💡 Reflexión complementaria:

La intención de cambio laboral también es elevada. Antes de
tomar una decisión, conviene identificar qué aspectos concretos
del trabajo contribuyen a la situación y valorar si pueden
abordarse dentro de la organización actual.
"""

        elif intencion_cambio < 2.5:
            informe += """

💡 Reflexión complementaria:

Aunque la intención de cambio laboral no es elevada, las
puntuaciones muestran desgaste o falta de estimulación. Sería
recomendable actuar antes de que esta situación se mantenga
durante un periodo prolongado.
"""

    informe += f"""

⚠️ SEÑAL DE ATENCIÓN
------------------------------------------------------------

{perfil["senal_alerta"]}


📚 RECURSOS RECOMENDADOS
------------------------------------------------------------

"""

    for recurso in perfil["recursos"]:
        informe += (
            f"• {recurso}\n"
        )

    informe += """

============================================================
Nota: EBLET-Lite es una herramienta descriptiva y no constituye
un diagnóstico psicológico o clínico.
============================================================
"""

    return informe


# =====================================================
# PRUEBAS DEL CLASIFICADOR
# =====================================================

def ejecutar_pruebas_clasificador():
    """
    Ejecuta pruebas básicas para comprobar los cinco perfiles
    y el comportamiento exacto del umbral 3.5.
    """

    pruebas = [
        {
            "nombre": "Equilibrio",
            "kpis": {
                "burnout": 2.0,
                "boreout": 2.0,
                "bienestar": 4.0,
                "rotacion": 2.0
            },
            "esperado": "flourishing"
        },
        {
            "nombre": "Estable",
            "kpis": {
                "burnout": 3.0,
                "boreout": 3.0,
                "bienestar": 3.0,
                "rotacion": 3.0
            },
            "esperado": "estable"
        },
        {
            "nombre": "Riesgo de Burnout",
            "kpis": {
                "burnout": 3.5,
                "boreout": 3.0,
                "bienestar": 2.5,
                "rotacion": 3.0
            },
            "esperado": "quemado"
        },
        {
            "nombre": "Riesgo de Boreout",
            "kpis": {
                "burnout": 3.0,
                "boreout": 3.5,
                "bienestar": 2.5,
                "rotacion": 3.0
            },
            "esperado": "aburrido"
        },
        {
            "nombre": "Crítico",
            "kpis": {
                "burnout": 3.5,
                "boreout": 3.5,
                "bienestar": 2.0,
                "rotacion": 4.0
            },
            "esperado": "critico"
        },
        {
            "nombre": (
                "Burnout con boreout intermedio"
            ),
            "kpis": {
                "burnout": 4.0,
                "boreout": 3.25,
                "bienestar": 2.5,
                "rotacion": 4.5
            },
            "esperado": "quemado"
        },
        {
            "nombre": (
                "Boreout con burnout intermedio"
            ),
            "kpis": {
                "burnout": 3.25,
                "boreout": 4.0,
                "bienestar": 2.5,
                "rotacion": 4.5
            },
            "esperado": "aburrido"
        }
    ]

    print(
        "PRUEBAS DEL CLASIFICADOR "
        "INDIVIDUAL EBLET-LITE"
    )
    print("=" * 65)

    for prueba in pruebas:

        resultado = clasificar_individuo(
            prueba["kpis"]
        )

        obtenido = resultado["perfil"]
        esperado = prueba["esperado"]

        assert obtenido == esperado, (
            f"Error en '{prueba['nombre']}': "
            f"esperado '{esperado}', "
            f"obtenido '{obtenido}'."
        )

        print(
            f"✅ {prueba['nombre']}: "
            f"{resultado['nombre']}"
        )

    print("=" * 65)
    print(
        "✅ Todas las pruebas se han "
        "completado correctamente."
    )
    print(
        "✅ Los valores iguales a 3.5 "
        "se incluyen en la zona de riesgo."
    )


# =====================================================
# EJECUCIÓN DIRECTA
# =====================================================

if __name__ == "__main__":
    ejecutar_pruebas_clasificador()