"""
Generador de Empleados Sintéticos

Genera empleados sintéticos asignados a las empresas previamente creadas.
"""

import numpy as np
import pandas as pd

from config import (
    CODIGOS_ESCENARIO,
    N_EMPLEADOS_DEFAULT,
)


def generar_empleados(
    empresas: pd.DataFrame,
    n_empleados: int = N_EMPLEADOS_DEFAULT,
) -> pd.DataFrame:
    """
    Genera empleados asignados a empresas de un único escenario.

    Args:
        empresas:
            DataFrame con las empresas previamente generadas.
        n_empleados:
            Número total de empleados que se generarán.

    Returns:
        DataFrame con empleados sintéticos y contexto organizacional.
    """
    if empresas.empty:
        raise ValueError(
            "El DataFrame de empresas no puede estar vacío."
        )

    if not isinstance(n_empleados, int) or n_empleados <= 0:
        raise ValueError(
            "n_empleados debe ser un entero mayor que cero."
        )

    escenarios = empresas["escenario"].dropna().unique()

    if len(escenarios) != 1:
        raise ValueError(
            "El DataFrame de empresas debe pertenecer a un único escenario."
        )

    escenario = escenarios[0]
    codigo_escenario = CODIGOS_ESCENARIO[escenario]

    # 1. ASIGNACIÓN EMPLEADO → EMPRESA
    empresa_asignada = np.random.choice(
        empresas["empresa_id"],
        size=n_empleados,
    )

    df = pd.DataFrame({
        "empleado_id": [
            f"{codigo_escenario}_EMP_{i:05d}"
            for i in range(n_empleados)
        ],
        "empresa_id": empresa_asignada,
    })

    # 2. HEREDAR CONTEXTO ORGANIZACIONAL
    df = df.merge(
        empresas,
        on="empresa_id",
        how="left",
        validate="many_to_one",
    )

    # 3. VARIABLES SOCIODEMOGRÁFICAS
    df["edad"] = (
        np.random.normal(34, 8, n_empleados)
        .clip(22, 60)
        .astype(int)
    )

    edad_inicio = np.random.uniform(
        18,
        25,
        n_empleados,
    )

    df["experiencia"] = (
        df["edad"]
        - edad_inicio
        + np.random.normal(0, 1.2, n_empleados)
    ).clip(0).round(1)

    estabilidad_factor = np.where(
        df["escenario"] == "saludable",
        0.9,
        np.where(
            df["escenario"] == "critico",
            0.3,
            0.6,
        ),
    )

    df["antiguedad"] = (
        df["experiencia"]
        * np.random.uniform(
            0.2,
            estabilidad_factor,
        )
    ).clip(0).round(1)

    # 4. VARIABLES ORGANIZACIONALES
    df["departamento"] = np.random.choice(
        [
            "Desarrollo",
            "Datos",
            "Producto",
            "RRHH",
            "Ventas",
        ],
        size=n_empleados,
    )

    distribucion_seniority = {
        "Junior": 0.20,
        "Mid": 0.45,
        "Senior": 0.25,
        "Lead": 0.10,
    }

    df["seniority"] = np.random.choice(
        list(distribucion_seniority.keys()),
        size=n_empleados,
        p=list(distribucion_seniority.values()),
    )

    df["modalidad"] = np.random.choice(
        [
            "Presencial",
            "Híbrido",
            "Remoto",
        ],
        size=n_empleados,
        p=[0.30, 0.45, 0.25],
    )

    df["genero"] = np.random.choice(
        [
            "Hombre",
            "Mujer",
            "No binario",
        ],
        size=n_empleados,
        p=[0.55, 0.40, 0.05],
    )

    # 5. SALARIO SEGÚN SENIORITY
    def generar_salario(seniority: str) -> int:
        rangos = {
            "Junior": (22000, 35000),
            "Mid": (30000, 50000),
            "Senior": (45000, 70000),
            "Lead": (60000, 95000),
        }

        salario_minimo, salario_maximo = rangos[seniority]

        media = (
            salario_minimo + salario_maximo
        ) / 2

        desviacion = (
            salario_maximo - salario_minimo
        ) / 6

        return int(
            np.random.normal(
                media,
                desviacion,
            )
        )

    df["salario"] = df["seniority"].apply(
        generar_salario
    )

    return df