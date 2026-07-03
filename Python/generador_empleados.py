import random
import numpy as np
import pandas as pd

from config import DEPARTAMENTOS, SENIORITY, PERFILES, MODALIDAD, SALARIOS

def generar_empleados(empresas, n=2500):

    registros = []

    empresas_list = empresas.to_dict("records")

    for i in range(n):

        emp = random.choice(empresas_list)

        seniority = random.choices(list(SENIORITY.keys()), weights=list(SENIORITY.values()))[0]
        perfil = random.choices(list(PERFILES.keys()), weights=list(PERFILES.values()))[0]
        departamento = random.choice(DEPARTAMENTOS)
        modalidad = random.choices(list(MODALIDAD.keys()), weights=list(MODALIDAD.values()))[0]

        edad = np.random.randint(22, 60)

        experiencia = max(0, edad - 22 + np.random.normal(0, 2))
        antiguedad = max(0, np.random.normal(3, 2))

        registros.append({
            "empleado_id": f"EMP_{i:05d}",
            "empresa_id": emp["empresa_id"],
            "genero": random.choice(["Hombre", "Mujer"]),
            "edad": edad,
            "experiencia": round(experiencia, 1),
            "antiguedad": round(antiguedad, 1),
            "departamento": departamento,
            "seniority": seniority,
            "modalidad": modalidad,
            "salario": SALARIOS[seniority]
        })

    return pd.DataFrame(registros)