"""
Exportador de Datasets

Exporta y carga los datasets generados utilizando una ruta fija
relativa a la raíz del proyecto.
"""

from pathlib import Path

import pandas as pd

from config import SCENARIOS


SRC_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SRC_DIR.parent
DATASETS_DIR = PROJECT_DIR / "datasets"


def crear_directorios() -> None:
    """
    Crea la estructura de directorios necesaria para los datasets.
    """
    DATASETS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    for escenario in SCENARIOS:
        (
            DATASETS_DIR / escenario
        ).mkdir(
            parents=True,
            exist_ok=True,
        )

    print(
        f"✅ Directorios de datasets creados en: "
        f"{DATASETS_DIR}"
    )


def exportar_dataset_escenario(
    escenario: str,
    df_empresas: pd.DataFrame,
    df_empleados: pd.DataFrame,
) -> None:
    """
    Exporta los datasets de un escenario a CSV.

    Args:
        escenario:
            Nombre del escenario.
        df_empresas:
            DataFrame de empresas.
        df_empleados:
            DataFrame de empleados con KPIs.
    """
    if escenario not in SCENARIOS:
        raise ValueError(
            f"Escenario no válido: {escenario!r}"
        )

    if not isinstance(df_empresas, pd.DataFrame):
        raise TypeError(
            "df_empresas debe ser un DataFrame."
        )

    if not isinstance(df_empleados, pd.DataFrame):
        raise TypeError(
            "df_empleados debe ser un DataFrame."
        )

    ruta_base = DATASETS_DIR / escenario

    ruta_base.mkdir(
        parents=True,
        exist_ok=True,
    )

    df_empresas.to_csv(
        ruta_base / "empresas.csv",
        index=False,
    )

    df_empleados.to_csv(
        ruta_base / "empleados.csv",
        index=False,
    )

    try:
        from scores import calcular_kpis_empresa

        df_kpis = calcular_kpis_empresa(
            df_empleados
        )

        df_kpis.to_csv(
            ruta_base / "kpis_empresa.csv",
            index=False,
        )

    except Exception as error:
        print(
            "   ⚠️ No se pudieron exportar "
            f"los KPIs de empresa: {error}"
        )


def exportar_dataset_completo(
    df_empresas: pd.DataFrame,
    df_empleados: pd.DataFrame,
) -> None:
    """
    Exporta los datasets consolidados.
    """
    DATASETS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    df_empresas.to_csv(
        DATASETS_DIR / "empresas_completo.csv",
        index=False,
    )

    df_empleados.to_csv(
        DATASETS_DIR / "empleados_completo.csv",
        index=False,
    )


def cargar_dataset_escenario(
    escenario: str,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Carga los datasets de empresas y empleados de un escenario.
    """
    if escenario not in SCENARIOS:
        raise ValueError(
            f"Escenario no válido: {escenario!r}"
        )

    ruta_base = DATASETS_DIR / escenario

    df_empresas = pd.read_csv(
        ruta_base / "empresas.csv"
    )

    df_empleados = pd.read_csv(
        ruta_base / "empleados.csv"
    )

    return df_empresas, df_empleados


def resumen_datasets() -> None:
    """
    Muestra un resumen de los datasets disponibles.
    """
    print("\n" + "=" * 60)
    print("RESUMEN DE DATASETS")
    print("=" * 60)

    for escenario in SCENARIOS:
        try:
            df_empresas, df_empleados = (
                cargar_dataset_escenario(
                    escenario
                )
            )

            print(f"\n📊 {escenario.upper()}:")
            print(
                f"   Empresas: "
                f"{len(df_empresas)}"
            )
            print(
                f"   Empleados: "
                f"{len(df_empleados)}"
            )

        except FileNotFoundError:
            print(
                f"\n⚠️ {escenario.upper()}: "
                "Dataset no encontrado"
            )