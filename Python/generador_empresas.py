import random
import pandas as pd
from config import CIUDADES, SECTORES, TAMANOS_EMPRESA, CULTURAS

def generar_empresas(n_empresas=50):

    empresas = []

    for i in range(n_empresas):

        empresas.append({
            "empresa_id": f"EMP_{i:03d}",
            "nombre": f"Tech{i}",
            "ciudad": random.choices(list(CIUDADES.keys()), weights=list(CIUDADES.values()))[0],
            "sector": random.choice(SECTORES),
            "cultura": random.choices(list(CULTURAS.keys()), weights=list(CULTURAS.values()))[0],
            "tamano": random.choices(list(TAMANOS_EMPRESA.keys()), weights=list(TAMANOS_EMPRESA.values()))[0]
        })

    return pd.DataFrame(empresas)