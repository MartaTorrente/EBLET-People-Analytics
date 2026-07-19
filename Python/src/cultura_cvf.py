"""
Clasificador de Cultura Organizacional (CVF)

Clasifica la cultura organizacional percibida por los empleados
a partir de las respuestas q60-q67.

Este módulo implementa el Competing Values Framework:
- Adhocracia
- Clan
- Mercado
- Jerárquica
"""

import numpy as np
import pandas as pd

from config import (
    INFO_CVF,
    PREGUNTAS_CVF,
    preguntas_cvf,
)
from estilos import COLORES_CULTURA


# Alias conservado por compatibilidad con notebooks existentes.
COLORES_CVF = COLORES_CULTURA


def calcular_scores_cvf_individuo(
    row: pd.Series,
) -> dict:
    """
    Calcula los scores de las cuatro culturas para un empleado.

    Args:
        row:
            Fila con las respuestas q60-q67.

    Returns:
        Diccionario con el score medio de cada cultura.
    """
    scores = {}

    for cultura in PREGUNTAS_CVF:
        columnas = preguntas_cvf(cultura)
        scores[cultura] = float(row[columnas].mean())

    return scores


def clasificar_cultura_individual(
    scores: dict,
) -> dict:
    """
    Identifica la cultura con mayor puntuación individual.

    El índice de predominio expresa el peso relativo de la cultura
    ganadora sobre la suma de los cuatro scores. No representa una
    probabilidad estadística.

    Args:
        scores:
            Diccionario con los scores de las cuatro culturas.

    Returns:
        Cultura dominante, índice de predominio y scores originales.
    """
    if not scores:
        raise ValueError(
            "El diccionario de scores no puede estar vacío."
        )

    culturas_faltantes = set(PREGUNTAS_CVF) - set(scores)

    if culturas_faltantes:
        raise ValueError(
            "Faltan scores de cultura: "
            + ", ".join(sorted(culturas_faltantes))
        )

    cultura_dominante = max(
        scores,
        key=scores.get,
    )

    total = sum(scores.values())

    predominio = (
        scores[cultura_dominante] / total
        if total > 0
        else 0
    )

    return {
        "cultura_dominante": cultura_dominante,
        "confianza": round(predominio, 3),
        "scores": scores,
    }


def clasificar_cultura_empresa(
    df_empleados: pd.DataFrame,
) -> dict:
    """
    Clasifica la cultura percibida de una empresa.

    Los scores se calculan agregando las respuestas de todos
    los empleados de la organización.

    Args:
        df_empleados:
            DataFrame con las respuestas q60-q67.

    Returns:
        Cultura dominante, índice de predominio, scores medios
        y distribución relativa.
    """
    if df_empleados.empty:
        raise ValueError(
            "El DataFrame de empleados no puede estar vacío."
        )

    columnas_cvf = [
        columna
        for cultura in PREGUNTAS_CVF
        for columna in preguntas_cvf(cultura)
    ]

    columnas_faltantes = (
        set(columnas_cvf)
        - set(df_empleados.columns)
    )

    if columnas_faltantes:
        raise ValueError(
            "Faltan columnas CVF: "
            + ", ".join(sorted(columnas_faltantes))
        )

    scores_empresa = {}

    for cultura in PREGUNTAS_CVF:
        columnas = preguntas_cvf(cultura)

        scores_empresa[cultura] = float(
            df_empleados[columnas]
            .mean(axis=1)
            .mean()
        )

    cultura_dominante = max(
        scores_empresa,
        key=scores_empresa.get,
    )

    total = sum(scores_empresa.values())

    predominio = (
        scores_empresa[cultura_dominante] / total
        if total > 0
        else 0
    )

    distribucion = {
        cultura: round(
            score / total * 100,
            1,
        )
        if total > 0
        else 0
        for cultura, score in scores_empresa.items()
    }

    return {
        "cultura_dominante": cultura_dominante,
        "confianza": round(predominio, 3),
        "scores": scores_empresa,
        "distribucion_pct": distribucion,
    }


def generar_cultura_percibida(
    n_empleados: int,
    cultura_real: str,
    seed: int | None = None,
) -> pd.DataFrame:
    """
    Genera respuestas sintéticas q60-q67 para una cultura dominante.

    Esta función se conserva como utilidad independiente. El generador
    principal de EBLET crea actualmente las respuestas culturales desde
    encuesta.py.

    Args:
        n_empleados:
            Número de empleados que se generarán.
        cultura_real:
            Cultura utilizada como dominante en la simulación.
        seed:
            Semilla opcional para reproducibilidad.

    Returns:
        DataFrame con respuestas enteras q60-q67.

    Raises:
        ValueError:
            Si el número de empleados o la cultura no son válidos.
    """
    if not isinstance(n_empleados, int) or n_empleados <= 0:
        raise ValueError(
            "n_empleados debe ser un entero mayor que cero."
        )

    if cultura_real not in PREGUNTAS_CVF:
        raise ValueError(
            f"Cultura no válida: {cultura_real!r}. "
            f"Opciones: {', '.join(PREGUNTAS_CVF)}"
        )

    if seed is not None:
        np.random.seed(seed)

    respuestas = pd.DataFrame(
        index=range(n_empleados)
    )

    bases = {
        cultura: 2.0
        for cultura in PREGUNTAS_CVF
    }

    bases[cultura_real] += 2.0

    for cultura in PREGUNTAS_CVF:
        base = bases[cultura]

        for columna in preguntas_cvf(cultura):
            ruido = np.random.normal(
                0,
                0.6,
                n_empleados,
            )

            respuestas[columna] = (
                np.clip(
                    np.round(base + ruido),
                    1,
                    5,
                )
                .astype(int)
            )

    return respuestas


def validar_clasificacion_cultura(
    df_empleados: pd.DataFrame,
    cultura_esperada: str,
) -> bool:
    """
    Comprueba si la cultura detectada coincide con la esperada.
    """
    if cultura_esperada not in PREGUNTAS_CVF:
        raise ValueError(
            f"Cultura esperada no válida: "
            f"{cultura_esperada!r}"
        )

    resultado = clasificar_cultura_empresa(
        df_empleados
    )

    return (
        resultado["cultura_dominante"]
        == cultura_esperada
    )


def generar_informe_cultura(
    resultado_clasificacion: dict,
) -> str:
    """
    Genera un resumen textual de la cultura percibida.
    """
    cultura = resultado_clasificacion[
        "cultura_dominante"
    ]

    predominio = resultado_clasificacion[
        "confianza"
    ]

    distribucion = resultado_clasificacion[
        "distribucion_pct"
    ]

    info = INFO_CVF[cultura]

    informe = f"""
🏛️ CULTURA ORGANIZACIONAL PERCIBIDA (CVF)

🎯 Cultura dominante: {cultura.upper()}
📊 Índice de predominio: {predominio * 100:.1f} %
🧭 Ejes: {info["ejes"]}
💡 Descripción: {info["descripcion"]}

📈 DISTRIBUCIÓN RELATIVA
  🔵 Adhocracia: {distribucion["Adhocracia"]:5.1f} %
  🟢 Clan:       {distribucion["Clan"]:5.1f} %
  🟠 Mercado:    {distribucion["Mercado"]:5.1f} %
  ⚪ Jerárquica: {distribucion["Jerarquica"]:5.1f} %
"""

    return informe.strip()