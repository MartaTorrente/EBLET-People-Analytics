"""
Módulo de Costes de Rotación

Calcula el impacto económico de la rotación laboral basado en:
- SHRM: coste de reemplazo = 6-9 meses de salario
- Gallup: 50%-200% del salario anual
- Cobee/Pluxee: metodología detallada

"""

import pandas as pd


from config import(
    FACTORES_PERFIL,
    TRAMOS_ROTACION
)



# TASAS DE ROTACIÓN SEGÚN KPI


def kpi_a_tasa_rotacion(kpi_rotacion: float) -> float:
    """
    Convierte el KPI de intención de cambio en una tasa anual estimada.

    La conversión representa un supuesto de escenarios del framework,
    no una probabilidad calibrada con datos reales.
    """
    if not 1 <= kpi_rotacion <= 5:
        raise ValueError(
            "kpi_rotacion debe estar comprendido entre 1 y 5."
        )

    for tramo in TRAMOS_ROTACION:
        if kpi_rotacion <= tramo["max_kpi"]:
            return tramo["tasa"]

    raise RuntimeError(
        "No se pudo convertir el KPI de rotación."
    )


def tasa_rotacion_a_categoria(tasa):
    """Categoriza la tasa de rotación para visualización."""
    if tasa <= 0.10:
        return "Baja"
    elif tasa <= 0.20:
        return "Normal"
    elif tasa <= 0.35:
        return "Alta"
    else:
        return "Crítica"



# CÁLCULO INDIVIDUAL


def calcular_coste_rotacion_empleado(row):
    """
    Calcula el coste esperado de rotación para un empleado individual.
    
    Fórmula:
        Coste_Esperado = (salario × Factor_Perfil × Tasa_Salida_Estimada
)
    """
    salario = row["salario"]
    seniority = row["seniority"]
    kpi_rot = row["kpi_rotacion"]
    
    # Factor según perfil
    factor = FACTORES_PERFIL.get(seniority, 0.75)
    
    # Coste de reemplazo si el empleado se va
    coste_reemplazo = salario * factor
    
    # Tasa anual estimada según el KPI de intención de cambio
    tasa_salida_estimada = kpi_a_tasa_rotacion(kpi_rot)
    
    # Coste esperado según el escenario de salida
    coste_esperado = coste_reemplazo * tasa_salida_estimada
    
    return round(coste_esperado, 2)



# CÁLCULO AGREGADO POR EMPRESA


def calcular_costes_empresa(df_empleados):
    """
    Calcula los costes de rotación a nivel empresa.
    """
    df = df_empleados.copy()
    
    # Calcular costes individuales
    df["coste_rotacion_individual"] = df.apply(
        calcular_coste_rotacion_empleado, axis=1
    )
    
    # Agregar por empresa
    costes_empresa = df.groupby("empresa_id").agg({
        "coste_rotacion_individual": "sum",
        "empleado_id": "count",
        "kpi_rotacion": "mean",
        "salario": ["mean", "sum"]
    }).reset_index()
    
    # Aplanar columnas multi-nivel
    costes_empresa.columns = [
        "empresa_id",
        "coste_total_rotacion",
        "n_empleados",
        "kpi_rotacion_promedio",
        "salario_medio",
        "masa_salarial"
    ]
    
    # Métricas adicionales
    costes_empresa["coste_por_empleado"] = (
        costes_empresa["coste_total_rotacion"] / costes_empresa["n_empleados"]
    ).round(2)
    
    costes_empresa["tasa_rotacion_estimada"] = costes_empresa["kpi_rotacion_promedio"].apply(
        kpi_a_tasa_rotacion
    )
    
    costes_empresa["categoria_rotacion"] = costes_empresa["tasa_rotacion_estimada"].apply(
        tasa_rotacion_a_categoria
    )
    
    costes_empresa["n_bajas_estimadas"] = (
        costes_empresa["n_empleados"] * costes_empresa["tasa_rotacion_estimada"]
    ).round(0).astype(int)
    
    costes_empresa["coste_pct_masa_salarial"] = (
        (costes_empresa["coste_total_rotacion"] / costes_empresa["masa_salarial"]) * 100
    ).round(2)
    
    return costes_empresa



# CÁLCULO AGREGADO POR ESCENARIO


def calcular_costes_escenario(df_empleados):
    """
    Calcula los costes de rotación agregados por escenario.
    """
    df = df_empleados.copy()
    
    df["coste_rotacion_individual"] = df.apply(
        calcular_coste_rotacion_empleado, axis=1
    )
    
    costes_escenario = df.groupby("escenario").agg({
        "coste_rotacion_individual": ["sum", "mean"],
        "empleado_id": "count",
        "kpi_rotacion": "mean",
        "salario": "mean"
    }).reset_index()
    
    costes_escenario.columns = [
        "escenario",
        "coste_total",
        "coste_medio_por_empleado",
        "n_empleados",
        "kpi_rotacion_promedio",
        "salario_medio"
    ]
    
    costes_escenario["tasa_rotacion_estimada"] = costes_escenario["kpi_rotacion_promedio"].apply(
        kpi_a_tasa_rotacion
    )
    
    costes_escenario["n_bajas_estimadas"] = (
        costes_escenario["n_empleados"] * costes_escenario["tasa_rotacion_estimada"]
    ).round(0).astype(int)
    
    return costes_escenario



# ANÁLISIS DE ROI DE INTERVENCIÓN


def calcular_roi_intervencion(coste_actual, coste_intervencion, porcentaje_reduccion):
    """
    Calcula el ROI de una intervención de bienestar.
    """
    ahorro = coste_actual * porcentaje_reduccion
    beneficio_neto = ahorro - coste_intervencion
    roi = (beneficio_neto / coste_intervencion) * 100 if coste_intervencion > 0 else 0
    payback = (coste_intervencion / (ahorro / 12)) if ahorro > 0 else None
    
    return {
        "ahorro_estimado": round(ahorro, 2),
        "beneficio_neto": round(beneficio_neto, 2),
        "roi_porcentaje": round(roi, 2),
        "payback_meses": round(payback, 1) if payback else None
    }


def generar_recomendaciones_roi(costes_empresa):
    """
    Genera recomendaciones de intervención basadas en ROI.
    """
    recomendaciones = []
    
    for _, row in costes_empresa.iterrows():
        empresa_id = row["empresa_id"]
        coste_actual = row["coste_total_rotacion"]
        escenario = row.get("escenario", "desconocido")
        
       
        coste_intervencion = coste_actual * 0.25
        
        # Diferentes escenarios de reducción
        for reduccion in [0.20, 0.30, 0.50]:
            roi = calcular_roi_intervencion(
                coste_actual, coste_intervencion, reduccion
            )
            
            recomendaciones.append({
                "empresa_id": empresa_id,
                "escenario": escenario,
                "coste_actual": coste_actual,
                "coste_intervencion": round(coste_intervencion, 2),
                "reduccion_objetivo": f"{int(reduccion*100)}%",
                "ahorro_estimado": roi["ahorro_estimado"],
                "beneficio_neto": roi["beneficio_neto"],
                "roi_porcentaje": roi["roi_porcentaje"],
                "payback_meses": roi["payback_meses"]
            })
    
    return pd.DataFrame(recomendaciones)



# RESUMEN EJECUTIVO


def generar_resumen_ejecutivo(df_empleados):
    """
    Genera un resumen ejecutivo de costes para presentación.
    """
    costes_totales = df_empleados.apply(
        calcular_coste_rotacion_empleado, axis=1
    ).sum()
    
    n_empleados = len(df_empleados)
    n_empresas = df_empleados["empresa_id"].nunique()
    masa_salarial_total = df_empleados["salario"].sum()
    
    return {
        "total_empleados": n_empleados,
        "total_empresas": n_empresas,
        "coste_total_rotación": round(costes_totales, 2),
        "coste_medio_por_empleado": round(costes_totales / n_empleados, 2),
        "masa_salarial_total": round(masa_salarial_total, 2),
        "coste_pct_masa_salarial": round((costes_totales / masa_salarial_total) * 100, 2),
        "ahorro_potencial_30": round(costes_totales * 0.30, 2)
    }