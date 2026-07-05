import pandas as pd
import numpy as np

# =====================================================
# UTILIDADES GENERALES EBLET
# =====================================================


def mostrar_info_dataframe(df, nombre="DataFrame"):
    """
    Muestra información resumida de un DataFrame.
    """
    print(f"\n{'='*60}")
    print(f"INFORMACIÓN: {nombre}")
    print(f"{'='*60}")
    print(f"Filas: {len(df):,}")
    print(f"Columnas: {len(df.columns)}")
    print(f"\nColumnas:")
    for col in df.columns:
        print(f"  - {col} ({df[col].dtype})")
    print(f"{'='*60}\n")


def calcular_estadisticos_latentes(df_empleados):
    """
    Calcula estadísticos descriptivos de los KPIs.
    """
    kpis = ["kpi_burnout", "kpi_boreout", "kpi_bienestar", "kpi_rotacion", "kpi_contexto"]
    
    stats = df_empleados[kpis].describe()
    
    print("\n📊 ESTADÍSTICOS DESCRIPTIVOS DE KPIs:")
    print(stats.round(2))
    
    return stats


def comparar_escenarios(df_empleados_todos):
    """
    Compara KPIs medios entre escenarios.
    """
    comparacion = df_empleados_todos.groupby("escenario").agg({
        "kpi_burnout": "mean",
        "kpi_boreout": "mean",
        "kpi_bienestar": "mean",
        "kpi_rotacion": "mean",
        "kpi_contexto": "mean"
    }).round(2)
    
    print("\n📊 COMPARACIÓN DE KPIs POR ESCENARIO:")
    print(comparacion)
    
    return comparacion