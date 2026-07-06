"""
EBLET v2.0 - Generador de Empresas Sintéticas

Genera empresas coherentes con los escenarios organizacionales,
usando la clasificación de culturas según Cameron & Quinn (CVF).
"""

import pandas as pd
import numpy as np

from config import SCENARIOS, N_EMPRESAS_DEFAULT


def generar_empresas(escenario: str, n_empresas: int = N_EMPRESAS_DEFAULT):
    """
    Genera empresas coherentes con un escenario organizacional.
    
    Args:
        escenario: Nombre del escenario (saludable, estable, etc.)
        n_empresas: Número de empresas a generar
    
    Returns:
        DataFrame con metadata de las empresas
    """
    
    cfg = SCENARIOS[escenario]
    
    # Generar metadata básica
    empresas = pd.DataFrame({
        "empresa_id": [f"{escenario[:3].upper()}_{i:03d}" for i in range(n_empresas)],
        "nombre": [f"{escenario}_Corp_{i}" for i in range(n_empresas)],
        "ciudad": np.random.choice(
            ["Madrid", "Barcelona", "Bilbao", "Valencia", "Sevilla"],
            n_empresas
        ),
        "sector": np.random.choice(
            ["Tecnología", "Finanzas", "Salud", "Educación", "Retail"],
            n_empresas
        ),
        "tamano": np.random.choice(
            ["Micro", "Pequeña", "Mediana", "Grande"],
            n_empresas,
            p=[0.10, 0.30, 0.40, 0.20]
        )
    })
    
    # =====================================================
    # ASIGNACIÓN DE CULTURA SEGÚN CVF (Cameron & Quinn)
    # =====================================================
    
    culturas = list(cfg["culture_mix"].keys())
    probs = list(cfg["culture_mix"].values())
    
    empresas["cultura"] = np.random.choice(
        culturas,
        size=n_empresas,
        p=probs
    )
    
    # =====================================================
    # METADATA DEL ESCENARIO
    # =====================================================
    
    empresas["escenario"] = escenario
    empresas["burnout_base"] = cfg["burnout_base"]
    empresas["boreout_base"] = cfg["boreout_base"]
    empresas["wellbeing_base"] = cfg["wellbeing_base"]
    empresas["rotation_base"] = cfg["rotation_base"]
    
    return empresas


def generar_empresas_todos_escenarios(n_empresas: int = N_EMPRESAS_DEFAULT):
    """
    Genera dataset completo con los 5 escenarios.
    """
    
    df_total = []
    
    for escenario in SCENARIOS.keys():
        df = generar_empresas(escenario, n_empresas)
        df_total.append(df)
    
    return pd.concat(df_total, ignore_index=True)