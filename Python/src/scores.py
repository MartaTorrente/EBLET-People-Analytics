"""
Calculadora de KPIs

Calcula indicadores a nivel empleado y empresa
a partir de las respuestas a la encuesta.

IMPORTANTE: Los ítems de Eficacia Profesional (q30-q36) del MBI-GS
están redactados en positivo, por lo que deben INVERTIRSE para que
un valor alto signifique más burnout.
"""

import pandas as pd
import numpy as np

from config import PREGUNTAS, UMBRALES
from cultura_cvf import clasificar_cultura_empresa, PREGUNTAS_CVF


def _obtener_columnas(rango):
    """Convierte un range a lista de nombres de columnas."""
    return [f'q{i}' for i in rango]



# KPIs A NIVEL EMPLEADO

def calcular_kpis_empleado(df_respuestas):
    """
    Calcula KPIs a nivel empleado a partir de las respuestas.
    
    Args:
        df_respuestas: DataFrame con columnas q1 a q72
    
    Returns:
        DataFrame con KPIs añadidos
    """
    df = df_respuestas.copy()
    
    
    # KPIs PRINCIPALES
    
    
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
    
   
    # SUB-DIMENSIONES (para análisis detallado)
   
    
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
    
  
    # 🆕 KPIs DE CULTURA CVF (q65-q72)
   
    # Solo si existen las columnas CVF
    try:
                
        for cultura, info in PREGUNTAS_CVF.items():
            preguntas = [f'q{p}' for p in info["preguntas"]]
            # Verificar que las columnas existen
            if all(p in df.columns for p in preguntas):
                df[f"cvf_{cultura.lower()}"] = df[preguntas].mean(axis=1)
        
        # Cultura dominante individual
        culturas = list(PREGUNTAS_CVF.keys())
        cultura_cols = [f"cvf_{c.lower()}" for c in culturas]
        cultura_cols_existentes = [c for c in cultura_cols if c in df.columns]
        
        if len(cultura_cols_existentes) == len(cultura_cols):
            df["cultura_percibida"] = df[cultura_cols_existentes].idxmax(axis=1).str.replace("cvf_", "")
    except ImportError:
        # Si no existe cultura_cvf, continuar sin calcular cultura
        pass
    
    return df



# KPIs A NIVEL EMPRESA


def calcular_kpis_empresa(df_empleados):
    """
    Agrega KPIs a nivel empresa, incluyendo cultura percibida (si existe).
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
    
    # Redondear KPIs
    for col in kpis_principales:
        kpis_empresa[col] = kpis_empresa[col].round(2)
    
    # 🆕 Añadir cultura percibida por empresa (SOLO si existen las columnas CVF)
    try:
        
        
        # Verificar que todas las preguntas CVF existen en el DataFrame
        todas_preguntas_cvf = []
        for info in PREGUNTAS_CVF.values():
            todas_preguntas_cvf.extend([f'q{p}' for p in info["preguntas"]])
        
        columnas_existentes = all(col in df_empleados.columns for col in todas_preguntas_cvf)
        
        if columnas_existentes:
            culturas_percibidas = []
            for empresa_id in kpis_empresa["empresa_id"]:
                df_empresa = df_empleados[df_empleados["empresa_id"] == empresa_id]
                resultado = clasificar_cultura_empresa(df_empresa)
                culturas_percibidas.append(resultado["cultura_dominante"])
            
            kpis_empresa["cultura_percibida"] = culturas_percibidas
        else:
            print("   ⚠️ Columnas CVF (q65-q72) no encontradas. Saltando clasificación cultural.")
    except (ImportError, KeyError) as e:
        print(f"   ⚠️ No se pudo clasificar cultura: {e}")
    
    return kpis_empresa



# CLASIFICACIÓN DE ESCENARIOS


def clasificar_escenario_empresa(df_kpis_empresa):
    """
    Clasifica cada empresa en uno de los 5 escenarios según sus KPIs.
    
    Lógica:
    - CRÍTICO: burnout ALTO + boreout ALTO + bienestar MUY BAJO
    - RIESGO BURNOUT: burnout ALTO + boreout NO ALTO + bienestar BAJO
    - RIESGO BOREOUT: burnout NO ALTO + boreout ALTO + bienestar BAJO
    - SALUDABLE: ambos problemas bajos + bienestar ALTO
    - ESTABLE: todo lo demás
    
    """
    df = df_kpis_empresa.copy()
    
    # Umbrales calibrados para clasificación robusta
    BURNOUT_ALTO = 3.5
    BOREOUT_ALTO = 3.0
    BIENESTAR_BAJO = 2.6
    BIENESTAR_ALTO = 3.5
    
    def clasificar(row):
        burnout = row["kpi_burnout"]
        boreout = row["kpi_boreout"]
        bienestar = row["kpi_bienestar"]
        
        # CRÍTICO
        if burnout >= BURNOUT_ALTO and boreout >= BOREOUT_ALTO and bienestar < BIENESTAR_BAJO:
            return "critico"
        # RIESGO BURNOUT
        elif burnout >= BURNOUT_ALTO and boreout < BOREOUT_ALTO and bienestar < 3.0:
            return "riesgo_burnout"
        # RIESGO BOREOUT
        elif burnout < BURNOUT_ALTO and boreout >= BOREOUT_ALTO and bienestar < 3.0:
            return "riesgo_boreout"
        # SALUDABLE
        elif burnout < 2.5 and boreout < BOREOUT_ALTO and bienestar > BIENESTAR_ALTO:
            return "saludable"
        # ESTABLE
        else:
            return "estable"
    
    df["escenario_predicho"] = df.apply(clasificar, axis=1)
    
    return df



# VALIDACIÓN DE CLASIFICACIÓN


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



# ANÁLISIS DE FIABILIDAD (ALFA DE CRONBACH)


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
    
    # 🆕 Añadir dimensiones CVF si existen las columnas
    try:
        
        for cultura, info in PREGUNTAS_CVF.items():
            preguntas = [f'q{p}' for p in info["preguntas"]]
            if all(p in df_empleados.columns for p in preguntas):
                dimensiones[f"Cultura CVF - {cultura}"] = preguntas
    except ImportError:
        pass
    
    resultados = []
    for nombre, items in dimensiones.items():
        alpha = calcular_alfa_cronbach(df_empleados, items)
        resultados.append({
            "Dimensión": nombre,
            "N_ítems": len(items),
            "Alfa_Cronbach": round(alpha, 3) if not np.isnan(alpha) else np.nan
        })
    
    return pd.DataFrame(resultados)



# 🆕 KPIs DE CULTURA CVF (función independiente)


def calcular_kpis_cultura(df):
    """
    Calcula los scores de cultura CVF a nivel empleado.
    
    Args:
        df: DataFrame con columnas q65-q72
    
    Returns:
        DataFrame con columnas cvf_adhocracia, cvf_clan, cvf_mercado, 
        cvf_jerarquica y cultura_percibida añadidas
    """

    
    df = df.copy()
    
    # Scores por cultura para cada empleado
    for cultura, info in PREGUNTAS_CVF.items():
        preguntas = [f'q{p}' for p in info["preguntas"]]
        df[f"cvf_{cultura.lower()}"] = df[preguntas].mean(axis=1)
    
    # Cultura dominante individual
    culturas = list(PREGUNTAS_CVF.keys())
    cultura_cols = [f"cvf_{c.lower()}" for c in culturas]
    df["cultura_percibida"] = df[cultura_cols].idxmax(axis=1).str.replace("cvf_", "")
    
    return df