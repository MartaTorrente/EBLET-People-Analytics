"""
Generador de Empresas Sintéticas

Genera empresas coherentes con los escenarios organizacionales.
"""

import pandas as pd
import numpy as np

from config import (
    SCENARIOS,
    N_EMPRESAS_DEFAULT,
    CODIGOS_ESCENARIO,
)


def generar_empresas(
    escenario: str,
    n_empresas: int = N_EMPRESAS_DEFAULT,
):
    """
    Genera empresas coherentes con un escenario organizacional.

    Args:
        escenario: Nombre del escenario.
        n_empresas: Número de empresas a generar.

    Returns:
        DataFrame con metadata de las empresas.
    """
    if escenario not in SCENARIOS:
        escenarios_validos = ", ".join(SCENARIOS.keys())
        raise ValueError(
            f"Escenario no válido: {escenario!r}. "
            f"Opciones disponibles: {escenarios_validos}"
        )

    if not isinstance(n_empresas, int) or n_empresas <= 0:
        raise ValueError(
            "n_empresas debe ser un número entero mayor que cero."
        )

    cfg = SCENARIOS[escenario]
    codigo_escenario = CODIGOS_ESCENARIO[escenario]

    empresas = pd.DataFrame({
        "empresa_id": [
            f"{codigo_escenario}_{i:03d}"
            for i in range(n_empresas)
        ],
        "nombre": [
            f"{escenario}_Corp_{i}"
            for i in range(n_empresas)
        ],
        "ciudad": np.random.choice(
            ["Madrid", "Barcelona", "Bilbao", "Valencia", "Sevilla"],
            size=n_empresas,
        ),
        "sector": ["Tecnología"] * n_empresas,
        
    })

    # ASIGNACIÓN DE CULTURA SEGÚN CVF
    culturas = list(cfg["culture_mix"].keys())
    probabilidades = list(cfg["culture_mix"].values())

    empresas["cultura"] = np.random.choice(
        culturas,
        size=n_empresas,
        p=probabilidades,
    )

    # INFORMACIÓN DEL ESCENARIO
    empresas["escenario"] = escenario
    empresas["burnout_base"] = cfg["burnout_base"]
    empresas["boreout_base"] = cfg["boreout_base"]
    empresas["wellbeing_base"] = cfg["wellbeing_base"]
    empresas["rotation_base"] = cfg["rotation_base"]

    return empresas


def generar_empresas_todos_escenarios(
    n_empresas: int = N_EMPRESAS_DEFAULT,
):
    """
    Genera empresas para todos los escenarios configurados.
    """
    empresas_por_escenario = [
        generar_empresas(escenario, n_empresas)
        for escenario in SCENARIOS
    ]

    return pd.concat(
        empresas_por_escenario,
        ignore_index=True,
    )