import pandas as pd
import os
from pathlib import Path

# =====================================================
# EXPORTADOR DE DATASETS EBLET
# =====================================================
# Gestiona la exportación de datasets a CSV
# organizados por escenario.
# =====================================================


def crear_directorios():
    """
    Crea la estructura de directorios para los datasets.
    """
    
    escenarios = ["saludable", "estable", "riesgo_burnout", "riesgo_boreout", "critico"]
    
    for escenario in escenarios:
        Path(f"datasets/{escenario}").mkdir(parents=True, exist_ok=True)
    
    print("✅ Directorios de datasets creados")


def exportar_dataset_escenario(df_empresas, df_empleados, escenario):
    """
    Exporta datasets de un escenario a CSV.
    
    Args:
        df_empresas: DataFrame de empresas
        df_empleados: DataFrame de empleados con respuestas y KPIs
        escenario: Nombre del escenario
    """
    
    ruta_base = f"datasets/{escenario}"
    
    # Exportar empresas
    df_empresas.to_csv(f"{ruta_base}/empresas.csv", index=False)
    
    # Exportar empleados (con respuestas y KPIs)
    df_empleados.to_csv(f"{ruta_base}/empleados.csv", index=False)
    
    # Exportar KPIs de empresa
    from scores import calcular_kpis_empresa
    df_kpis = calcular_kpis_empresa(df_empleados)
    df_kpis.to_csv(f"{ruta_base}/kpis_empresa.csv", index=False)
    
    print(f"✅ Dataset '{escenario}' exportado:")
    print(f"   - {len(df_empresas)} empresas")
    print(f"   - {len(df_empleados)} empleados")
    print(f"   - Ruta: {ruta_base}/")


def exportar_dataset_completo(df_empresas_todas, df_empleados_todos):
    """
    Exporta dataset completo con todos los escenarios.
    
    Args:
        df_empresas_todas: DataFrame con todas las empresas
        df_empleados_todos: DataFrame con todos los empleados
    """
    
    # Dataset completo
    df_empresas_todas.to_csv("datasets/empresas_todas.csv", index=False)
    df_empleados_todos.to_csv("datasets/empleados_todos.csv", index=False)
    
    print(f"\n✅ Dataset completo exportado:")
    print(f"   - {len(df_empresas_todas)} empresas totales")
    print(f"   - {len(df_empleados_todos)} empleados totales")


def cargar_dataset_escenario(escenario):
    """
    Carga dataset de un escenario desde CSV.
    
    Args:
        escenario: Nombre del escenario
    
    Returns:
        Tupla (df_empresas, df_empleados)
    """
    
    ruta_base = f"datasets/{escenario}"
    
    df_empresas = pd.read_csv(f"{ruta_base}/empresas.csv")
    df_empleados = pd.read_csv(f"{ruta_base}/empleados.csv")
    
    return df_empresas, df_empleados


def resumen_datasets():
    """
    Muestra resumen de todos los datasets generados.
    """
    
    print("\n" + "="*60)
    print("RESUMEN DE DATASETS GENERADOS")
    print("="*60)
    
    escenarios = ["saludable", "estable", "riesgo_burnout", "riesgo_boreout", "critico"]
    
    total_empresas = 0
    total_empleados = 0
    
    for escenario in escenarios:
        ruta = f"datasets/{escenario}/empleados.csv"
        
        if os.path.exists(ruta):
            df = pd.read_csv(ruta)
            n_empresas = df["empresa_id"].nunique()
            n_empleados = len(df)
            
            total_empresas += n_empresas
            total_empleados += n_empleados
            
            print(f"\n📊 {escenario.upper()}:")
            print(f"   Empresas: {n_empresas}")
            print(f"   Empleados: {n_empleados}")
        else:
            print(f"\n⚠️  {escenario.upper()}: No encontrado")
    
    print("\n" + "="*60)
    print(f"TOTAL: {total_empresas} empresas, {total_empleados} empleados")
    print("="*60 + "\n")