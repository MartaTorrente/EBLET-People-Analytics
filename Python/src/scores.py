import pandas as pd
import numpy as np

# =====================================================
# CALCULADORA DE KPIs EBLET
# =====================================================
# Calcula indicadores a nivel empleado y empresa
# a partir de las respuestas a la encuesta.
# =====================================================


def calcular_kpis_empleado(df_respuestas):
    """
    Calcula KPIs a nivel empleado a partir de las respuestas.
    
    Args:
        df_respuestas: DataFrame con columnas q6 a q48
    
    Returns:
        DataFrame con KPIs añadidos
    """
    
    df = df_respuestas.copy()
    
    # KPI Burnout: Media de preguntas 21-29
    df["kpi_burnout"] = df[[f'q{i}' for i in range(21, 30)]].mean(axis=1)
    
    # KPI Boreout: Media de preguntas 30-38
    df["kpi_boreout"] = df[[f'q{i}' for i in range(30, 39)]].mean(axis=1)
    
    # KPI Bienestar: Media de preguntas 39-45
    df["kpi_bienestar"] = df[[f'q{i}' for i in range(39, 46)]].mean(axis=1)
    
    # KPI Rotación: Media de preguntas 46-48
    df["kpi_rotacion"] = df[[f'q{i}' for i in range(46, 49)]].mean(axis=1)
    
    # KPI Contexto: Media de preguntas 6-20
    df["kpi_contexto"] = df[[f'q{i}' for i in range(6, 21)]].mean(axis=1)
    
    # =====================================================
    # SUB-DIMENSIONES (opcional, para análisis detallado)
    # =====================================================
    
    # Burnout sub-dimensiones
    df["burnout_agotamiento"] = df[[f'q{i}' for i in range(21, 24)]].mean(axis=1)
    df["burnout_cinismo"] = df[[f'q{i}' for i in range(24, 27)]].mean(axis=1)
    df["burnout_ineficacia"] = df[[f'q{i}' for i in range(27, 30)]].mean(axis=1)
    
    # Boreout sub-dimensiones
    df["boreout_desinteres"] = df[[f'q{i}' for i in range(30, 33)]].mean(axis=1)
    df["boreout_falta_reto"] = df[[f'q{i}' for i in range(33, 36)]].mean(axis=1)
    df["boreout_infraocupacion"] = df[[f'q{i}' for i in range(36, 39)]].mean(axis=1)
    
    # Bienestar sub-dimensiones
    df["bienestar_satisfaccion"] = df[[f'q{i}' for i in range(39, 43)]].mean(axis=1)
    df["bienestar_autoeficacia"] = df[[f'q{i}' for i in range(43, 46)]].mean(axis=1)
    
    return df


def calcular_kpis_empresa(df_empleados):
    """
    Agrega KPIs a nivel empresa.
    
    Args:
        df_empleados: DataFrame con KPIs a nivel empleado
    
    Returns:
        DataFrame con KPIs agregados por empresa
    """
    
    kpis_empresa = df_empleados.groupby("empresa_id").agg({
        "kpi_burnout": "mean",
        "kpi_boreout": "mean",
        "kpi_bienestar": "mean",
        "kpi_rotacion": "mean",
        "kpi_contexto": "mean",
        "empleado_id": "count"  # Número de empleados
    }).reset_index()
    
    kpis_empresa.rename(columns={"empleado_id": "n_empleados"}, inplace=True)
    
    # Redondear a 2 decimales
    for col in ["kpi_burnout", "kpi_boreout", "kpi_bienestar", "kpi_rotacion", "kpi_contexto"]:
        kpis_empresa[col] = kpis_empresa[col].round(2)
    
    return kpis_empresa


def clasificar_escenario_empresa(df_kpis_empresa):
    """
    Clasifica cada empresa en uno de los 5 escenarios según sus KPIs.
    
    Args:
        df_kpis_empresa: DataFrame con KPIs a nivel empresa
    
    Returns:
        DataFrame con columna 'escenario_predicho' añadida
    """
    
    df = df_kpis_empresa.copy()
    
    def clasificar(row):
        burnout = row["kpi_burnout"]
        boreout = row["kpi_boreout"]
        bienestar = row["kpi_bienestar"]
        
        # Reglas de clasificación
        if burnout >= 3.5 and boreout >= 3.5 and bienestar < 2.5:
            return "critico"
        elif burnout >= 3.5 and boreout < 3.0 and bienestar < 3.0:
            return "riesgo_burnout"
        elif burnout < 3.0 and boreout >= 3.5 and bienestar < 3.0:
            return "riesgo_boreout"
        elif burnout < 2.5 and boreout < 2.5 and bienestar > 3.5:
            return "saludable"
        else:
            return "estable"
    
    df["escenario_predicho"] = df.apply(clasificar, axis=1)
    
    return df


def validar_clasificacion(df_empresas_original, df_kpis_empresa):
    """
    Valida que la clasificación predicha coincida con el escenario real.
    
    Args:
        df_empresas_original: DataFrame original con columna 'escenario'
        df_kpis_empresa: DataFrame con KPIs y 'escenario_predicho'
    
    Returns:
        DataFrame con validación
    """
    
    df_validacion = df_empresas_original.merge(
        df_kpis_empresa[["empresa_id", "escenario_predicho"]],
        on="empresa_id",
        how="left"
    )
    
    df_validacion["clasificacion_correcta"] = (
        df_validacion["escenario"] == df_validacion["escenario_predicho"]
    )
    
    return df_validacion