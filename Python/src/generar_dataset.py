import pandas as pd
import numpy as np
from empresas import generar_empresas
from empleados import generar_empleados
from modelo_psicologico import construir_modelo_psicologico
from encuesta import generar_respuestas_encuesta
from scores import calcular_kpis_empleado, calcular_kpis_empresa, clasificar_escenario_empresa, validar_clasificacion
from exportador import exportar_dataset_escenario, exportar_dataset_completo, crear_directorios, resumen_datasets


# GENERADOR PRINCIPAL DE DATASETS EBLET


def generar_dataset_escenario(escenario, n_empresas=50, n_empleados=2500, seed=42):
    """
    Pipeline completo de generación de dataset para un escenario.
    
    Args:
        escenario: Nombre del escenario (saludable, estable, riesgo_burnout, etc.)
        n_empresas: Número de empresas a generar
        n_empleados: Número total de empleados a generar
        seed: Semilla para reproducibilidad
    
    Returns:
        Tupla (df_empresas, df_empleados)
    """
    
    print(f"\n{'='*60}")
    print(f"GENERANDO ESCENARIO: {escenario.upper()}")
    print(f"{'='*60}")
    
    # Configurar semilla para reproducibilidad
    np.random.seed(seed)
    
   
    # PASO 1: Generar empresas
   
    print(f"\n📋 Paso 1: Generando {n_empresas} empresas...")
    df_empresas = generar_empresas(escenario, n_empresas)
    print(f"   {len(df_empresas)} empresas generadas")
    
    # PASO 2: Generar empleados
   
    print(f"\n👥 Paso 2: Generando {n_empleados} empleados...")
    df_empleados = generar_empleados(df_empresas, n_empleados)
    print(f"    {len(df_empleados)} empleados generados")
    
   
    # PASO 3: Aplicar modelo psicológico
    
    print(f"\n Paso 3: Aplicando modelo psicológico...")
    latentes = construir_modelo_psicologico(df_empleados)
    print(f"    Estados latentes calculados")
    print(f"      - Burnout medio: {latentes['burnout'].mean():.2f}")
    print(f"      - Boreout medio: {latentes['boreout'].mean():.2f}")
    print(f"      - Bienestar medio: {latentes['wellbeing'].mean():.2f}")
    print(f"      - Rotación media: {latentes['rotation'].mean():.2f}")
    
    
    # PASO 4: Generar respuestas a encuesta
   
    print(f"\n Paso 4: Generando respuestas a encuesta...")
    df_respuestas = generar_respuestas_encuesta(df_empleados, latentes)
    print(f"    {len(df_respuestas.columns)} preguntas generadas")
    
    
    # PASO 5: Combinar empleados con respuestas
    
    df_empleados_completo = pd.concat([
        df_empleados.reset_index(drop=True),
        df_respuestas
    ], axis=1)
    
   
    # PASO 6: Calcular KPIs
    
    print(f"\n Paso 5: Calculando KPIs...")
    df_empleados_con_kpis = calcular_kpis_empleado(df_empleados_completo)
    print(f"    KPIs calculados a nivel empleado")
    
    # =====================================================
    # PASO 7: Validar clasificación
    
    print(f"\n🔍 Paso 6: Validando clasificación de escenarios...")
    df_kpis_empresa = calcular_kpis_empresa(df_empleados_con_kpis)
    df_kpis_empresa = clasificar_escenario_empresa(df_kpis_empresa)
    df_validacion = validar_clasificacion(df_empresas, df_kpis_empresa)
    
    aciertos = df_validacion["clasificacion_correcta"].sum()
    total = len(df_validacion)
    precision = (aciertos / total) * 100
    
    print(f"    Clasificación validada: {aciertos}/{total} correctas ({precision:.1f}%)")
    
    
    # PASO 8: Exportar dataset
    
    print(f"\n Paso 7: Exportando dataset...")
    exportar_dataset_escenario(df_empresas, df_empleados_con_kpis, escenario)
    
    return df_empresas, df_empleados_con_kpis


def generar_todos_los_escenarios(n_empresas=50, n_empleados=2500):
    """
    Genera datasets para los 5 escenarios organizacionales.
    
    Args:
        n_empresas: Número de empresas por escenario
        n_empleados: Número de empleados por escenario
    
    Returns:
        Tupla (df_empresas_todas, df_empleados_todos)
    """
    
    print("\n" + "="*60)
    print(" INICIANDO GENERACIÓN DE DATASETS EBLET")
    print("="*60)
    
    # Crear directorios
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
    
    # Mostrar resumen
    resumen_datasets()
    
    return df_empresas_todas, df_empleados_todos



# EJECUCIÓN PRINCIPAL


if __name__ == "__main__":
    # Generar datasets con configuración por defecto
    # 50 empresas por escenario, 2500 empleados por escenario
    # Total: 250 empresas, 12500 empleados
    
    df_empresas, df_empleados = generar_todos_los_escenarios(
        n_empresas=50,
        n_empleados=2500
    )
    
    print("\n" + "="*60)
    print("GENERACIÓN COMPLETADA EXITOSAMENTE")
    print("="*60)
    print(f"\n Datasets disponibles en: datasets/")
    print(f" Total: {len(df_empresas)} empresas, {len(df_empleados)} empleados")
    print("\n Siguiente paso: Ejecutar notebooks de análisis")