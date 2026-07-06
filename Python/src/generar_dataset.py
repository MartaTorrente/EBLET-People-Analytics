"""
EBLET v2.0 - Generador Principal de Datasets

Orquesta todo el pipeline de generación de datos sintéticos
para los 5 escenarios organizacionales, incluyendo cálculo
de costes de rotación.
"""

import pandas as pd
import numpy as np
import os

from empresas import generar_empresas
from empleados import generar_empleados
from modelo_psicologico import construir_modelo_psicologico
from encuesta import generar_respuestas_encuesta
from scores import (
    calcular_kpis_empleado, calcular_kpis_empresa,
    clasificar_escenario_empresa, validar_clasificacion,
    analisis_fiabilidad
)
from costes_rotacion import (
    calcular_coste_rotacion_empleado,
    calcular_costes_empresa,
    calcular_costes_escenario,
    generar_resumen_ejecutivo
)
from exportador import (
    exportar_dataset_escenario, exportar_dataset_completo,
    crear_directorios, resumen_datasets
)
from config import N_EMPRESAS_DEFAULT, N_EMPLEADOS_DEFAULT


# =====================================================
# ETIQUETAS DE ESCENARIOS
# =====================================================

ETIQUETAS_ES = {
    "saludable": "Saludable",
    "estable": "Estable",
    "riesgo_burnout": "Riesgo Burnout",
    "riesgo_boreout": "Riesgo Boreout",
    "critico": "Crítico"
}


# =====================================================
# GENERACIÓN POR ESCENARIO
# =====================================================

def generar_dataset_escenario(escenario, n_empresas=50, n_empleados=2500, seed=42):
    """
    Pipeline completo de generación de dataset para un escenario.
    """
    
    print(f"\n{'='*60}")
    print(f"GENERANDO ESCENARIO: {escenario.upper()}")
    print(f"{'='*60}")
    
    np.random.seed(seed)
    
    # PASO 1: Generar empresas
    print(f"\n📋 Paso 1: Generando {n_empresas} empresas...")
    df_empresas = generar_empresas(escenario, n_empresas)
    print(f"   ✅ {len(df_empresas)} empresas generadas")
    
    # PASO 2: Generar empleados
    print(f"\n👥 Paso 2: Generando {n_empleados} empleados...")
    df_empleados = generar_empleados(df_empresas, n_empleados)
    print(f"   ✅ {len(df_empleados)} empleados generados")
    
    # PASO 3: Aplicar modelo psicológico
    print(f"\n🧠 Paso 3: Aplicando modelo psicológico...")
    latentes = construir_modelo_psicologico(df_empleados)
    print(f"   ✅ Estados latentes calculados")
    print(f"      - Burnout medio: {latentes['burnout'].mean():.2f}")
    print(f"      - Boreout medio: {latentes['boreout'].mean():.2f}")
    print(f"      - Bienestar medio: {latentes['wellbeing'].mean():.2f}")
    print(f"      - Rotación media: {latentes['rotation'].mean():.2f}")
    
    # PASO 4: Generar respuestas a encuesta (64 preguntas)
    print(f"\n📝 Paso 4: Generando respuestas a encuesta (64 preguntas)...")
    df_respuestas = generar_respuestas_encuesta(df_empleados, latentes)
    print(f"   ✅ {len(df_respuestas.columns)} preguntas generadas")
    
    # PASO 5: Combinar empleados con respuestas
    df_empleados_completo = pd.concat([
        df_empleados.reset_index(drop=True),
        df_respuestas
    ], axis=1)
    
    # PASO 6: Calcular KPIs
    print(f"\n📊 Paso 5: Calculando KPIs...")
    df_empleados_con_kpis = calcular_kpis_empleado(df_empleados_completo)
    print(f"   ✅ KPIs calculados a nivel empleado")
    
    # PASO 7: Calcular costes de rotación
    print(f"\n💰 Paso 6: Calculando costes de rotación...")
    df_empleados_con_kpis["coste_rotacion_individual"] = df_empleados_con_kpis.apply(
        calcular_coste_rotacion_empleado, axis=1
    )
    coste_total = df_empleados_con_kpis["coste_rotacion_individual"].sum()
    coste_medio = df_empleados_con_kpis["coste_rotacion_individual"].mean()
    print(f"   ✅ Coste total estimado: {coste_total:,.2f}€")
    print(f"   ✅ Coste medio por empleado: {coste_medio:,.2f}€")
    
    # PASO 8: Validar clasificación
    print(f"\n🔍 Paso 7: Validando clasificación de escenarios...")
    df_kpis_empresa = calcular_kpis_empresa(df_empleados_con_kpis)
    df_kpis_empresa = clasificar_escenario_empresa(df_kpis_empresa)
    df_validacion = validar_clasificacion(df_empresas, df_kpis_empresa)
    
    aciertos = df_validacion["clasificacion_correcta"].sum()
    total = len(df_validacion)
    precision = (aciertos / total) * 100
    
    print(f"   ✅ Clasificación validada: {aciertos}/{total} correctas ({precision:.1f}%)")
    
    # PASO 9: Calcular fiabilidad (Alfa de Cronbach)
    print(f"\n🔬 Paso 8: Calculando fiabilidad (Alfa de Cronbach)...")
    fiabilidad = analisis_fiabilidad(df_empleados_con_kpis)
    print("   ✅ Fiabilidad calculada:")
    for _, row in fiabilidad.head(5).iterrows():
        print(f"      - {row['Dimensión']}: α = {row['Alfa_Cronbach']:.3f}")
    
    # PASO 10: Exportar dataset
    print(f"\n💾 Paso 9: Exportando dataset...")
    exportar_dataset_escenario(df_empresas, df_empleados_con_kpis, escenario)
    
    return df_empresas, df_empleados_con_kpis


# =====================================================
# GENERACIÓN DE TODOS LOS ESCENARIOS
# =====================================================

def generar_todos_los_escenarios(n_empresas=50, n_empleados=2500):
    """
    Genera datasets para los 5 escenarios organizacionales.
    """
    
    print("\n" + "="*60)
    print("🚀 INICIANDO GENERACIÓN DE DATASETS EBLET v2.0")
    print("="*60)
    print("\n📋 Instrumentos validados:")
    print("   - MBI-GS (Burnout)")
    print("   - EAL (Aburrimiento Laboral)")
    print("   - WHO-5 (Bienestar)")
    print("   - Rothlin & Werder (Infraocupación)")
    print("   - Bandura (Autoeficacia)")
    print("   - Mobley (Rotación)")
    print("   - SHRM/Gallup (Costes de Rotación)")
    print("\n📚 Cultura organizacional: CVF (Cameron & Quinn, 2011)")
    print("   - Adhocracia, Clan, Jerarquica, Mercado")
    
    crear_directorios()
    
    escenarios = ["saludable", "estable", "riesgo_burnout", "riesgo_boreout", "critico"]
    
    todas_empresas = []
    todos_empleados = []
    
    for i, escenario in enumerate(escenarios, 1):
        print(f"\n{'#'*60}")
        print(f"# ESCENARIO {i}/5: {escenario.upper()}")
        print(f"{'#'*60}")
        
        df_empresas, df_empleados = generar_dataset_escenario(
            escenario,
            n_empresas=n_empresas,
            n_empleados=n_empleados,
            seed=42 + i
        )
        
        todas_empresas.append(df_empresas)
        todos_empleados.append(df_empleados)
    
    # Concatenar todos los datasets
    df_empresas_todas = pd.concat(todas_empresas, ignore_index=True)
    df_empleados_todos = pd.concat(todos_empleados, ignore_index=True)
    
    # Exportar dataset completo
    exportar_dataset_completo(df_empresas_todas, df_empleados_todos)
    
    # =====================================================
    # RESUMEN EJECUTIVO DE COSTES
    # =====================================================
    print("\n" + "="*60)
    print("💰 RESUMEN EJECUTIVO DE COSTES")
    print("="*60)
    resumen = generar_resumen_ejecutivo(df_empleados_todos)
    print(f"   👥 Total empleados: {resumen['total_empleados']:,}")
    print(f"   🏢 Total empresas: {resumen['total_empresas']}")
    print(f"   💸 Coste total de rotación: {resumen['coste_total_rotacion']:,.2f}€")
    print(f"   💵 Coste medio por empleado: {resumen['coste_medio_por_empleado']:,.2f}€")
    print(f"   📊 % sobre masa salarial: {resumen['coste_pct_masa_salarial']:.2f}%")
    print(f"   🎯 Ahorro potencial (30% reducción): {resumen['ahorro_potencial_30']:,.2f}€")
    
    # =====================================================
    # COSTES POR ESCENARIO (CORREGIDO)
    # =====================================================
    print("\n📊 Costes por escenario:")
    
    # Crear DataFrame con columna escenario_nombre para el cálculo
    df_con_etiquetas = df_empleados_todos.copy()
    df_con_etiquetas["escenario_nombre"] = df_con_etiquetas["escenario"].map(ETIQUETAS_ES)
    
    costes_esc = calcular_costes_escenario(df_con_etiquetas)
    for _, row in costes_esc.iterrows():
        print(f"   {row['escenario']:20s}: {row['coste_total']:>12,.2f}€ ({row['n_bajas_estimadas']} bajas est.)")
    
    # Mostrar resumen de datasets
    resumen_datasets()
    
    return df_empresas_todas, df_empleados_todos


# =====================================================
# EJECUCIÓN PRINCIPAL
# =====================================================

if __name__ == "__main__":
    df_empresas, df_empleados = generar_todos_los_escenarios(
        n_empresas=50,
        n_empleados=2500
    )
    
    print("\n" + "="*60)
    print("✅ GENERACIÓN COMPLETADA EXITOSAMENTE")
    print("="*60)
    print(f"\n📁 Datasets disponibles en: datasets/")
    print(f"📊 Total: {len(df_empresas)} empresas, {len(df_empleados)} empleados")
    print("\n🚀 Siguiente paso: python src/exportar_para_powerbi.py")