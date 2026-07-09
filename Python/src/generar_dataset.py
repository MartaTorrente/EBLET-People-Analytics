"""
EBLET v2.0 - Generador de Datasets

Orquestador principal que genera los datasets sintéticos para los 5 escenarios
organizacionales del framework EBLET.

Genera:
- 5 escenarios × 50 empresas × 50 empleados = 12,500 empleados
- 72 preguntas Likert por empleado (incluye CVF)
- KPIs, costes de rotación y validación
"""

import pandas as pd
import numpy as np
import os
import sys

# Añadir src al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from empresas import generar_empresas
from empleados import generar_empleados
from modelo_psicologico import construir_modelo_psicologico
from encuesta import generar_respuestas_encuesta
from scores import (
    calcular_kpis_empleado,
    calcular_kpis_empresa,
    clasificar_escenario_empresa,
    validar_clasificacion,
    analisis_fiabilidad
)
from costes_rotacion import calcular_coste_rotacion_empleado
from exportador import exportar_dataset_escenario
from config import SCENARIOS as ESCENARIOS


def generar_dataset_escenario(escenario, n_empresas=50, n_empleados=2500, seed=42):
    """
    Genera dataset completo para un escenario.
    
    Args:
        escenario: Nombre del escenario (ej: "saludable")
        n_empresas: Número de empresas a generar
        n_empleados: Número total de empleados
        seed: Semilla para reproducibilidad
    
    Returns:
        tuple: (df_empresas, df_empleados_con_kpis)
    """
    print("\n" + "="*60)
    print(f"GENERANDO ESCENARIO: {escenario.upper()}")
    print("="*60)
    
    np.random.seed(seed)
    
    # =====================================================
    # PASO 1: GENERAR EMPRESAS
    # =====================================================
    print(f"\n📋 Paso 1: Generando {n_empresas} empresas...")
    df_empresas = generar_empresas(escenario, n_empresas)
    print(f"   ✅ {n_empresas} empresas generadas")
    
    # =====================================================
    # PASO 2: GENERAR EMPLEADOS
    # =====================================================
    print(f"\n👥 Paso 2: Generando {n_empleados} empleados...")
    df_empleados = generar_empleados(df_empresas, n_empleados)
    print(f"   ✅ {n_empleados} empleados generados")
    
    # =====================================================
    # PASO 3: APLICAR MODELO PSICOLÓGICO
    # =====================================================
    print(f"\n🧠 Paso 3: Aplicando modelo psicológico...")
    df_empleados = construir_modelo_psicologico(df_empleados)
    
    print(f"   ✅ Estados latentes calculados")
    print(f"      - Burnout medio: {df_empleados['L_burnout'].mean():.2f}")
    print(f"      - Boreout medio: {df_empleados['L_boreout'].mean():.2f}")
    print(f"      - Bienestar medio: {df_empleados['L_wellbeing'].mean():.2f}")
    print(f"      - Rotación media: {df_empleados['L_rotation'].mean():.2f}")
    
    if "factor_resiliencia" in df_empleados.columns:
        print(f"      - Resiliencia media: {df_empleados['factor_resiliencia'].mean():.3f}")
        print(f"      - Sensibilidad media: {df_empleados['factor_sensibilidad'].mean():.3f}")
    
        # =====================================================
    # PASO 4: GENERAR RESPUESTAS ENCUESTA
    # =====================================================
    print(f"\n📝 Paso 4: Generando respuestas a encuesta...")
    df_respuestas = generar_respuestas_encuesta(df_empleados)
    
    # Combinar empleados con respuestas
    df_completo = pd.concat([
        df_empleados.drop(columns=["L_burnout", "L_boreout", "L_wellbeing", "L_rotation"], errors='ignore'),
        df_respuestas
    ], axis=1)
    
    n_preguntas = len([c for c in df_respuestas.columns if c.startswith('q')])
    print(f"   ✅ {n_preguntas} preguntas generadas")
    
    # =====================================================
    # PASO 5: CALCULAR KPIS
    # =====================================================
    print(f"\n📊 Paso 5: Calculando KPIs...")
    df_con_kpis = calcular_kpis_empleado(df_completo)
    print(f"   ✅ KPIs calculados a nivel empleado")
    
    # =====================================================
    # PASO 6: CALCULAR COSTES
    # =====================================================
    print(f"\n💰 Paso 6: Calculando costes de rotación...")
    df_con_kpis["coste_rotacion_individual"] = df_con_kpis.apply(
        calcular_coste_rotacion_empleado, axis=1
    )
    coste_total = df_con_kpis["coste_rotacion_individual"].sum()
    coste_medio = df_con_kpis["coste_rotacion_individual"].mean()
    print(f"   ✅ Coste total estimado: {coste_total:,.2f}€")
    print(f"   ✅ Coste medio por empleado: {coste_medio:,.2f}€")
    
    # =====================================================
    # PASO 7: VALIDAR CLASIFICACIÓN
    # =====================================================
    print(f"\n🔍 Paso 7: Validando clasificación de escenarios...")
    df_kpis_empresa = calcular_kpis_empresa(df_con_kpis)
    df_empresas_clasificadas = clasificar_escenario_empresa(df_kpis_empresa)
    
    df_validacion = validar_clasificacion(df_empresas, df_empresas_clasificadas)
    n_correctas = df_validacion["clasificacion_correcta"].sum()
    n_total = len(df_validacion)
    pct_correctas = (n_correctas / n_total) * 100
    
    print(f"   ✅ Clasificación validada: {n_correctas}/{n_total} correctas ({pct_correctas:.1f}%)")
    
    # =====================================================
    # PASO 8: CALCULAR FIABILIDAD
    # =====================================================
    print(f"\n🔬 Paso 8: Calculando fiabilidad (Alfa de Cronbach)...")
    fiabilidad = analisis_fiabilidad(df_con_kpis)
    
    print(f"   ✅ Fiabilidad calculada:")
    dimensiones_principales = [
        "Burnout - Agotamiento (MBI-GS)",
        "Burnout - Cinismo (MBI-GS)",
        "Burnout - Ineficacia (MBI-GS)",
        "Aburrimiento Laboral (EAL)",
        "Bienestar (WHO-5)"
    ]
    for _, row in fiabilidad.iterrows():
        if row["Dimensión"] in dimensiones_principales:
            print(f"      - {row['Dimensión']}: α = {row['Alfa_Cronbach']:.3f}")
    
    # =====================================================
    # PASO 9: EXPORTAR
    # =====================================================
    print(f"\n💾 Paso 9: Exportando dataset...")
    exportar_dataset_escenario(escenario, df_empresas, df_con_kpis)
    
    print(f"✅ Dataset '{escenario}' exportado:")
    print(f"   - {len(df_empresas)} empresas")
    print(f"   - {len(df_con_kpis)} empleados")
    print(f"   - Ruta: datasets/{escenario}/")
    
    return df_empresas, df_con_kpis


def generar_todos_los_escenarios(n_empresas=50, n_empleados=2500):
    """
    Genera datasets para todos los escenarios.
    
    Args:
        n_empresas: Número de empresas por escenario
        n_empleados: Número de empleados por escenario
    
    Returns:
        tuple: (df_empresas_todos, df_empleados_todos)
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
    
    # Crear directorios
    from exportador import crear_directorios
    crear_directorios()
    print("✅ Directorios de datasets creados")
    
    # Generar cada escenario
    todos_empresas = []
    todos_empleados = []
    
    for i, escenario in enumerate(ESCENARIOS):
        print("\n" + "#"*60)
        print(f"# ESCENARIO {i+1}/{len(ESCENARIOS)}: {escenario.upper()}")
        print("#"*60)
        
        df_empresas, df_empleados = generar_dataset_escenario(
            escenario,
            n_empresas=n_empresas,
            n_empleados=n_empleados,
            seed=42 + i
        )
        
        todos_empresas.append(df_empresas)
        todos_empleados.append(df_empleados)
    
    # Consolidar todos los datasets
    df_empresas_todos = pd.concat(todos_empresas, ignore_index=True)
    df_empleados_todos = pd.concat(todos_empleados, ignore_index=True)
    
    print("\n✅ Dataset completo exportado:")
    print(f"   - {len(df_empresas_todos)} empresas totales")
    print(f"   - {len(df_empleados_todos)} empleados totales")
    
    # Resumen ejecutivo de costes
    print("\n" + "="*60)
    print("💰 RESUMEN EJECUTIVO DE COSTES")
    print("="*60)
    print(f"   👥 Total empleados: {len(df_empleados_todos):,}")
    print(f"   🏢 Total empresas: {df_empleados_todos['empresa_id'].nunique()}")
    print(f"   💸 Coste total de rotación: {df_empleados_todos['coste_rotacion_individual'].sum():,.2f}€")
    print(f"   💵 Coste medio por empleado: {df_empleados_todos['coste_rotacion_individual'].mean():,.2f}€")
    
    masa_salarial = df_empleados_todos["salario"].sum()
    coste_total = df_empleados_todos["coste_rotacion_individual"].sum()
    print(f"   📊 % sobre masa salarial: {(coste_total/masa_salarial)*100:.2f}%")
    print(f"   🎯 Ahorro potencial (30% reducción): {coste_total*0.3:,.2f}€")
    
    # Costes por escenario
    print("\n📊 Costes por escenario:")
    for escenario in ESCENARIOS:
        df_esc = df_empleados_todos[df_empleados_todos["escenario"] == escenario]
        coste_esc = df_esc["coste_rotacion_individual"].sum()
        # Estimación de bajas
        kpi_rot = df_esc["kpi_rotacion"].mean()
        if kpi_rot <= 1.5:
            tasa = 0.05
        elif kpi_rot <= 2.5:
            tasa = 0.10
        elif kpi_rot <= 3.5:
            tasa = 0.20
        elif kpi_rot <= 4.5:
            tasa = 0.35
        else:
            tasa = 0.50
        n_bajas = int(len(df_esc) * tasa)
        
        nombre_esc = escenario.replace("_", " ").title()
        print(f"   {nombre_esc:20s}: {coste_esc:>15,.2f}€ ({n_bajas} bajas est.)")
    
    return df_empresas_todos, df_empleados_todos


# =====================================================
# EJECUCIÓN PRINCIPAL
# =====================================================

if __name__ == "__main__":
    df_empresas, df_empleados = generar_todos_los_escenarios(
        n_empresas=50,
        n_empleados=2500
    )
    
    print("\n" + "="*60)
    print("RESUMEN DE DATASETS GENERADOS")
    print("="*60)
    
    for escenario in ESCENARIOS:
        df_esc = df_empleados[df_empleados["escenario"] == escenario]
        n_empresas = df_esc["empresa_id"].nunique()
        n_empleados = len(df_esc)
        print(f"\n📊 {escenario.upper()}:")
        print(f"   Empresas: {n_empresas}")
        print(f"   Empleados: {n_empleados}")
    
    print("\n" + "="*60)
    print(f"📊 Total: {len(df_empresas)} empresas, {len(df_empleados)} empleados")
    print("="*60)
    
    print("\n" + "="*60)
    print("✅ GENERACIÓN COMPLETADA EXITOSAMENTE")
    print("="*60)
    print("\n📁 Datasets disponibles en: datasets/")
    print(f"📊 Total: {len(df_empresas)} empresas, {len(df_empleados)} empleados")
    print("\n🚀 Siguiente paso: python src/exportar_para_powerbi.py")