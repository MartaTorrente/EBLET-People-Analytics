"""
Exportador de Datasets

Exporta los datasets generados a CSV en la estructura de carpetas por escenario.
"""

import pandas as pd
from pathlib import Path
from config import SCENARIOS


def crear_directorios():
    """Crea los directorios necesarios para los datasets."""
 
    
    Path("datasets").mkdir(exist_ok=True)
    
    for escenario in SCENARIOS:
        Path(f"datasets/{escenario}").mkdir(parents=True, exist_ok=True)
    
    print("✅ Directorios de datasets creados")


def exportar_dataset_escenario(escenario, df_empresas, df_empleados):
    """
    Exporta dataset de un escenario a CSV.
    
    Args:
        escenario: Nombre del escenario (string)
        df_empresas: DataFrame de empresas
        df_empleados: DataFrame de empleados con KPIs
    """
    # 🆕 VALIDACIÓN DE TIPOS
    if not isinstance(df_empresas, pd.DataFrame):
        raise TypeError(
            f"df_empresas debe ser DataFrame, es {type(df_empresas).__name__}: {df_empresas}"
        )
    if not isinstance(df_empleados, pd.DataFrame):
        raise TypeError(
            f"df_empleados debe ser DataFrame, es {type(df_empleados).__name__}"
        )
    
    ruta_base = f"datasets/{escenario}"
    Path(ruta_base).mkdir(parents=True, exist_ok=True)
    
    # Exportar empresas
    df_empresas.to_csv(f"{ruta_base}/empresas.csv", index=False)
    
    # Exportar empleados
    df_empleados.to_csv(f"{ruta_base}/empleados.csv", index=False)
    
    # Exportar KPIs de empresa
    try:
        from scores import calcular_kpis_empresa
        df_kpis = calcular_kpis_empresa(df_empleados)
        df_kpis.to_csv(f"{ruta_base}/kpis_empresa.csv", index=False)
    except Exception as e:
        print(f"   ⚠️ No se pudieron exportar KPIs de empresa: {e}")


def exportar_dataset_completo(df_empresas, df_empleados):
    """Exporta dataset completo unificado."""
    df_empresas.to_csv("datasets/empresas_completo.csv", index=False)
    df_empleados.to_csv("datasets/empleados_completo.csv", index=False)


def cargar_dataset_escenario(escenario):
    """Carga dataset de un escenario desde CSV."""
    ruta_base = f"datasets/{escenario}"
    
    df_empresas = pd.read_csv(f"{ruta_base}/empresas.csv")
    df_empleados = pd.read_csv(f"{ruta_base}/empleados.csv")
    
    return df_empresas, df_empleados


def resumen_datasets():
    """Muestra resumen de todos los datasets."""
    from config import SCENARIOS
    
    print("\n" + "="*60)
    print("RESUMEN DE DATASETS")
    print("="*60)
    
    for escenario in SCENARIOS:
        try:
            df_empresas, df_empleados = cargar_dataset_escenario(escenario)
            print(f"\n📊 {escenario.upper()}:")
            print(f"   Empresas: {len(df_empresas)}")
            print(f"   Empleados: {len(df_empleados)}")
        except FileNotFoundError:
            print(f"\n⚠️ {escenario.upper()}: Dataset no encontrado")