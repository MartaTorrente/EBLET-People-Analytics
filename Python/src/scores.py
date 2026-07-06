"""
EBLET v2.0 - Calculadora de KPIs

Calcula indicadores a nivel empleado y empresa
a partir de las respuestas a la encuesta v2.0.

IMPORTANTE: Los ítems de Eficacia Profesional (q30-q36) del MBI-GS
están redactados en positivo, por lo que deben INVERTIRSE para que
un valor alto signifique más burnout.
"""

import pandas as pd
import numpy as np

from config import PREGUNTAS, UMBRALES


def _obtener_columnas(rango):
    """Convierte un range a lista de nombres de columnas."""
    return [f'q{i}' for i in rango]


def calcular_kpis_empleado(df_respuestas):
    """
    Calcula KPIs a nivel empleado a partir de las respuestas.
    
    Args:
        df_respuestas: DataFrame con columnas q1 a q64
    
    Returns:
        DataFrame con KPIs añadidos
    """
    df = df_respuestas.copy()
    
    # =====================================================
    # KPIs PRINCIPALES
    # =====================================================
    
    # KPI Contexto: Media de q1-q15
    df["kpi_contexto"] = df[_obtener_columnas(range(1, 16))].mean(axis=1)
    
    # KPI Burnout: Media de q16-q36 (con q30-q36 INVERTIDAS)
    burnout_agotam = df[_obtener_columnas(range(16, 23))].mean(axis=1)
    burnout_cinismo = df[_obtener_columnas(range(23, 30))].mean(axis=1)
    burnout_ineficacia_raw = df[_obtener_columnas(range(30, 37))].mean(axis=1)
    # INVERSIÓN: eficacia alta = burnout bajo
    burnout_ineficacia = 6 - burnout_ineficacia_raw
    
    df["kpi_burnout"] = (burnout_agotam + burnout_cinismo + burnout_ineficacia) / 3
    
    # KPI Boreout: Combinación de EAL (q37-q44) + Infraocupación (q60-q64)
    boreout_eal = df[_obtener_columnas(range(37, 45))].mean(axis=1)
    boreout_infra = df[_obtener_columnas(range(60, 65))].mean(axis=1)
    df["kpi_boreout"] = (boreout_eal * 8 + boreout_infra * 5) / 13
    
    # KPI Bienestar: Combinación de WHO-5 (q45-q49) + Satisfacción (q50-q53)
    bienestar_who5 = df[_obtener_columnas(range(45, 50))].mean(axis=1)
    satisfaccion = df[_obtener_columnas(range(50, 54))].mean(axis=1)
    df["kpi_bienestar"] = (bienestar_who5 * 5 + satisfaccion * 4) / 9
    
    # KPI Rotación: Media de q57-q59
    df["kpi_rotacion"] = df[_obtener_columnas(range(57, 60))].mean(axis=1)
    
    # =====================================================
    # SUB-DIMENSIONES (para análisis detallado)
    # =====================================================
    
    # Burnout - Sub-dimensiones MBI-GS
    df["burnout_agotamiento"] = burnout_agotam
    df["burnout_cinismo"] = burnout_cinismo
    df["burnout_ineficacia"] = burnout_ineficacia
    
    # Boreout - Sub-dimensiones
    df["boreout_aburrimiento_eal"] = boreout_eal
    df["boreout_infraocupacion"] = boreout_infra
    
    # Bienestar - Sub-dimensiones
    df["bienestar_who5"] = bienestar_who5
    df["bienestar_satisfaccion"] = satisfaccion
    df["bienestar_autoeficacia"] = df[_obtener_columnas(range(54, 57))].mean(axis=1)
    
    return df


def calcular_kpis_empresa(df_empleados):
    """
    Agrega KPIs a nivel empresa.
    """
    kpis_principales = [
        "kpi_burnout", "kpi_boreout", "kpi_bienestar",
        "kpi_rotacion", "kpi_contexto"
    ]
    
    kpis_empresa = df_empleados.groupby("empresa_id").agg({
        **{kpi: "mean" for kpi in kpis_principales},
        "empleado_id": "count"
    }).reset_index()
    
    kpis_empresa.rename(columns={"empleado_id": "n_empleados"}, inplace=True)
    
    # Redondear a 2 decimales
    for col in kpis_principales:
        kpis_empresa[col] = kpis_empresa[col].round(2)
    
    return kpis_empresa


def clasificar_escenario_empresa(df_kpis_empresa):
    """
    Clasifica cada empresa en uno de los 5 escenarios según sus KPIs.
    
    Umbrales basados en:
    - MBI-GS (Schaufeli et al., 1996): Burnout alto ≥ 3.86
    - EAL (Martínez-Lugo, 2017): Aburrimiento alto ≥ 3.0
    - WHO-5 (Topp et al., 2015): Bienestar bajo < 2.6
    
    Lógica corregida:
    - CRÍTICO: burnout ALTO + boreout ALTO + bienestar MUY BAJO
    - RIESGO BURNOUT: burnout ALTO + boreout BAJO + bienestar BAJO
    - RIESGO BOREOUT: burnout BAJO + boreout ALTO + bienestar BAJO
    - SALUDABLE: burnout BAJO + boreout BAJO + bienestar ALTO
    - ESTABLE: todo lo demás
    """
    df = df_kpis_empresa.copy()
    
    # Umbrales calibrados para clasificación robusta
    BURNOUT_ALTO = 3.5      # Umbral para considerar burnout significativo
    BURNOUT_BAJO = 2.5      # Umbral para considerar burnout bajo
    BOREOUT_ALTO = 3.5      # Umbral para considerar boreout significativo
    BOREOUT_BAJO = 2.5      # Umbral para considerar boreout bajo
    BIENESTAR_ALTO = 3.5    # Umbral para considerar bienestar alto
    BIENESTAR_BAJO = 2.5    # Umbral para considerar bienestar bajo
    
    def clasificar(row):
        burnout = row["kpi_burnout"]
        boreout = row["kpi_boreout"]
        bienestar = row["kpi_bienestar"]
        
        # CRÍTICO: ambos problemas altos + bienestar muy bajo
        if burnout >= BURNOUT_ALTO and boreout >= BOREOUT_ALTO and bienestar < BIENESTAR_BAJO:
            return "critico"
        # RIESGO BURNOUT: burnout alto + boreout bajo + bienestar bajo
        elif burnout >= BURNOUT_ALTO and boreout < BOREOUT_BAJO and bienestar < 3.0:
            return "riesgo_burnout"
        # RIESGO BOREOUT: burnout bajo + boreout alto + bienestar bajo
        elif burnout < BURNOUT_BAJO and boreout >= BOREOUT_ALTO and bienestar < 3.0:
            return "riesgo_boreout"
        # SALUDABLE: ambos problemas bajos + bienestar alto
        elif burnout < BURNOUT_BAJO and boreout < BOREOUT_BAJO and bienestar > BIENESTAR_ALTO:
            return "saludable"
        # ESTABLE: todo lo demás
        else:
            return "estable"
    
    df["escenario_predicho"] = df.apply(clasificar, axis=1)
    
    return df

def validar_clasificacion(df_empresas_original, df_kpis_empresa):
    """
    Valida que la clasificación predicha coincida con el escenario real.
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


def calcular_alfa_cronbach(df, items):
    """
    Calcula el Alfa de Cronbach para una dimensión.
    """
    df_items = df[items].dropna()
    n_items = len(items)
    
    if n_items < 2:
        return np.nan
    
    # Varianza de cada ítem
    item_variances = df_items.var(axis=0, ddof=1)
    sum_item_var = item_variances.sum()
    
    # Varianza del total
    total_variance = df_items.sum(axis=1).var(ddof=1)
    
    if total_variance == 0:
        return np.nan
    
    # Fórmula del alfa de Cronbach
    alpha = (n_items / (n_items - 1)) * (1 - sum_item_var / total_variance)
    
    return alpha


def analisis_fiabilidad(df_empleados):
    """
    Calcula la fiabilidad (Alfa de Cronbach) de todas las dimensiones.
    """
    dimensiones = {
        "Burnout - Agotamiento (MBI-GS)": [f'q{i}' for i in range(16, 23)],
        "Burnout - Cinismo (MBI-GS)": [f'q{i}' for i in range(23, 30)],
        "Burnout - Ineficacia (MBI-GS)": [f'q{i}' for i in range(30, 37)],
        "Aburrimiento Laboral (EAL)": [f'q{i}' for i in range(37, 45)],
        "Bienestar (WHO-5)": [f'q{i}' for i in range(45, 50)],
        "Satisfacción Laboral": [f'q{i}' for i in range(50, 54)],
        "Autoeficacia (Bandura)": [f'q{i}' for i in range(54, 57)],
        "Intención de Rotación (Mobley)": [f'q{i}' for i in range(57, 60)],
        "Infraocupación (Rothlin)": [f'q{i}' for i in range(60, 65)],
        "Contexto Organizacional (JD-R)": [f'q{i}' for i in range(1, 16)],
    }
    
    resultados = []
    for nombre, items in dimensiones.items():
        alpha = calcular_alfa_cronbach(df_empleados, items)
        resultados.append({
            "Dimensión": nombre,
            "N_ítems": len(items),
            "Alfa_Cronbach": round(alpha, 3) if not np.isnan(alpha) else np.nan
        })
    
    return pd.DataFrame(resultados)