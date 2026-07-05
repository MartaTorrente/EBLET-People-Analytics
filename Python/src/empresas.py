import pandas as pd
import numpy as np

from config import SCENARIOS, N_EMPRESAS_DEFAULT

# =====================================================
# GENERADOR DE EMPRESAS POR ESCENARIO
# =====================================================

def generar_empresas(escenario: str, n_empresas: int = N_EMPRESAS_DEFAULT):
    """
    Genera empresas coherentes con un escenario organizacional.
    """

    cfg = SCENARIOS[escenario]

    empresas = pd.DataFrame({
        "empresa_id": [f"{escenario[:3].upper()}_{i:03d}" for i in range(n_empresas)],
        "nombre": [f"{escenario}_Corp_{i}" for i in range(n_empresas)],
        "ciudad": np.random.choice(["Madrid", "Barcelona", "Bilbao"], n_empresas),
        "sector": np.random.choice(["Tech", "Fintech", "Consultoría", "E-commerce"], n_empresas),
        "tamano": np.random.choice(["Micro", "Pequeña", "Mediana", "Grande"], n_empresas)
    })

    # =====================================================
    # ASIGNACIÓN DE CULTURA SEGÚN ESCENARIO
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


# =====================================================
# GENERADOR MULTI-ESCENARIO (FRAMEWORK COMPLETO)
# =====================================================

def generar_empresas_todos_escenarios(n_empresas: int = N_EMPRESAS_DEFAULT):
    """
    Genera dataset completo con los 5 escenarios.
    """

    df_total = []

    for escenario in SCENARIOS.keys():
        df = generar_empresas(escenario, n_empresas)
        df_total.append(df)

    return pd.concat(df_total, ignore_index=True)