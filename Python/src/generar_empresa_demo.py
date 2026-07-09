"""
EBLET v2.0 - Generador de Empresa Demo (LegacyTech Solutions)

Genera una empresa ficticia con perfil de Riesgo Boreout:
- Empresa tech madura (15 años)
- Cultura Jerárquica predominante
- Boreout alto, Burnout bajo
- 180 empleados
- Diferenciación generacional clara
"""

import pandas as pd
import numpy as np
from pathlib import Path

# =====================================================
# CONFIGURACIÓN DE LA EMPRESA DEMO
# =====================================================

N_EMPLEADOS = 180
SEED = 2026  # Reproducibilidad

# Perfil objetivo de KPIs
KPI_OBJETIVO = {
    "burnout": 2.2,      # Bajo
    "boreout": 4.1,      # ALTO
    "bienestar": 2.5,    # Bajo
    "rotacion": 3.6,     # Alta
    "contexto": 2.6      # Medio-bajo
}

# Distribución de departamentos
DEPARTAMENTOS = {
    "Desarrollo": 0.40,  # 72 empleados
    "Datos": 0.25,       # 45 empleados
    "Producto": 0.15,    # 27 empleados
    "RRHH": 0.10,        # 18 empleados
    "Ventas": 0.10       # 18 empleados
}

# Distribución de culturas CVF
CULTURAS = {
    "Jerarquica": 0.80,  # 80% - burocracia
    "Mercado": 0.20      # 20% - algo de presión
}

# Distribución de modalidad
MODALIDAD = {
    "Presencial": 0.70,
    "Híbrido": 0.30,
    "Remoto": 0.00       # No hay remoto (empresa tradicional)
}

# Distribución de seniority (plantilla envejecida)
SENIORITY = {
    "Junior": 0.15,      # 27 empleados
    "Mid": 0.25,         # 45 empleados
    "Senior": 0.40,      # 72 empleados - MAYORÍA
    "Lead": 0.20         # 36 empleados
}

# =====================================================
# FUNCIÓN PRINCIPAL
# =====================================================

def generar_empresa_demo():
    """Genera empresa demo LegacyTech Solutions."""
    
    print("="*70)
    print("🏢 GENERANDO EMPRESA DEMO: LEGACYTECH SOLUTIONS")
    print("="*70)
    
    np.random.seed(SEED)
    
    # =====================================================
    # 1. GENERAR METADATA DE EMPLEADOS
    # =====================================================
    
    print("\n📋 Paso 1: Generando metadata de empleados...")
    
    empleados = pd.DataFrame({
        "empleado_id": [f"DEMO_{i:03d}" for i in range(1, N_EMPLEADOS + 1)],
        "empresa_id": ["DEMO_001"] * N_EMPLEADOS,
        "escenario": ["demo"] * N_EMPLEADOS
    })
    
    # Edad (plantilla envejecida)
    edad_base = np.random.normal(38, 7, N_EMPLEADOS).clip(25, 58).astype(int)
    empleados["edad"] = edad_base
    
    # Experiencia
    edad_inicio = np.random.uniform(18, 24, N_EMPLEADOS)
    empleados["experiencia"] = (edad_base - edad_inicio + np.random.normal(0, 1, N_EMPLEADOS)).clip(0).round(1)
    
    # Antigüedad (alta en empresa estable)
    empleados["antiguedad"] = (empleados["experiencia"] * np.random.uniform(0.4, 0.9, N_EMPLEADOS)).clip(0).round(1)
    
    # Departamento
    empleados["departamento"] = np.random.choice(
        list(DEPARTAMENTOS.keys()),
        size=N_EMPLEADOS,
        p=list(DEPARTAMENTOS.values())
    )
    
    # Seniority
    empleados["seniority"] = np.random.choice(
        list(SENIORITY.keys()),
        size=N_EMPLEADOS,
        p=list(SENIORITY.values())
    )
    
    # Modalidad
    empleados["modalidad"] = np.random.choice(
        list(MODALIDAD.keys()),
        size=N_EMPLEADOS,
        p=list(MODALIDAD.values())
    )
    
    # Género
    empleados["genero"] = np.random.choice(
        ["Hombre", "Mujer", "No binario"],
        N_EMPLEADOS,
        p=[0.60, 0.35, 0.05]  # Más hombres en tech tradicional
    )
    
    # Salario (coherente con seniority)
    rangos_salariales = {
        "Junior": (25000, 35000),
        "Mid": (35000, 50000),
        "Senior": (50000, 70000),
        "Lead": (65000, 90000)
    }
    
    salarios = []
    for _, row in empleados.iterrows():
        min_s, max_s = rangos_salariales[row["seniority"]]
        salario = int(np.random.normal((min_s + max_s) / 2, (max_s - min_s) / 6))
        salarios.append(salario)
    
    empleados["salario"] = salarios
    
    print(f"   ✅ {len(empleados)} empleados generados")
    print(f"   - Edad media: {empleados['edad'].mean():.1f} años")
    print(f"   - Experiencia media: {empleados['experiencia'].mean():.1f} años")
    print(f"   - Antigüedad media: {empleados['antiguedad'].mean():.1f} años")
    
    # =====================================================
    # 2. GENERAR RESPUESTAS A LA ENCUESTA (64 preguntas)
    # =====================================================
    
    print("\n📝 Paso 2: Generando respuestas a encuesta (64 preguntas)...")
    
    respuestas = pd.DataFrame(index=empleados.index)
    
    # --- SECCIÓN C: CONTEXTO (q1-q15) ---
    # Contexto medio-bajo (2.6) con variabilidad
    for q in range(1, 16):
        respuestas[f'q{q}'] = np.clip(
            np.random.normal(KPI_OBJETIVO["contexto"], 0.8, N_EMPLEADOS),
            1, 5
        ).round().astype(int)
    
    # --- SECCIÓN D: BURNOUT (q16-q36) ---
    # Burnout bajo (2.2) pero con diferenciación por departamento/seniority
    
    # Ajustes por departamento
    ajustes_burnout = {
        "Desarrollo": 0.3,   # Más burnout en desarrollo
        "Datos": 0.0,
        "Producto": 0.2,
        "RRHH": -0.3,        # Menos burnout en RRHH
        "Ventas": 0.5        # Más burnout en ventas
    }
    
    # Ajustes por seniority
    ajustes_seniority_burnout = {
        "Junior": 0.4,       # Juniors con más burnout
        "Mid": 0.1,
        "Senior": -0.2,      # Seniors con menos burnout
        "Lead": 0.0
    }
    
    # Agotamiento (q16-q22)
    for q in range(16, 23):
        base = KPI_OBJETIVO["burnout"]
        ajustes = empleados["departamento"].map(ajustes_burnout) + empleados["seniority"].map(ajustes_seniority_burnout)
        respuestas[f'q{q}'] = np.clip(
            base + ajustes + np.random.normal(0, 0.5, N_EMPLEADOS),
            1, 5
        ).round().astype(int)
    
    # Cinismo (q23-q29)
    for q in range(23, 30):
        base = KPI_OBJETIVO["burnout"] * 0.9
        ajustes = empleados["departamento"].map(ajustes_burnout) + empleados["seniority"].map(ajustes_seniority_burnout)
        respuestas[f'q{q}'] = np.clip(
            base + ajustes + np.random.normal(0, 0.5, N_EMPLEADOS),
            1, 5
        ).round().astype(int)
    
    # Eficacia (q30-q36) - INVERTIDO (alto = buen rendimiento)
    for q in range(30, 37):
        base = 5 - KPI_OBJETIVO["burnout"]  # Invertir
        ajustes = empleados["departamento"].map(ajustes_burnout) * -0.5
        respuestas[f'q{q}'] = np.clip(
            base + ajustes + np.random.normal(0, 0.6, N_EMPLEADOS),
            1, 5
        ).round().astype(int)
    
    # --- SECCIÓN E: BOREOUT - EAL (q37-q44) ---
    # BOREOUT ALTO (4.1) con diferenciación por seniority y departamento
    
    # Ajustes por departamento (boreout)
    ajustes_boreout = {
        "Desarrollo": 0.3,   # Desarrollo con boreout alto (mantenimiento)
        "Datos": 0.6,        # Datos con boreout MUY alto (análisis repetitivos)
        "Producto": 0.0,
        "RRHH": 0.2,
        "Ventas": -0.5       # Ventas con menos boreout (siempre ocupados)
    }
    
    # Ajustes por seniority (boreout)
    ajustes_seniority_boreout = {
        "Junior": -0.8,      # Juniors con poco boreout (aprenden)
        "Mid": -0.2,
        "Senior": 0.5,       # Seniors con boreout alto
        "Lead": 0.3
    }
    
    for q in range(37, 45):
        base = KPI_OBJETIVO["boreout"]
        ajustes = empleados["departamento"].map(ajustes_boreout) + empleados["seniority"].map(ajustes_seniority_boreout)
        respuestas[f'q{q}'] = np.clip(
            base + ajustes + np.random.normal(0, 0.5, N_EMPLEADOS),
            1, 5
        ).round().astype(int)
    
    # --- SECCIÓN F: BIENESTAR - WHO-5 (q45-q49) ---
    # Bienestar bajo (2.5)
    for q in range(45, 50):
        respuestas[f'q{q}'] = np.clip(
            np.random.normal(KPI_OBJETIVO["bienestar"], 0.7, N_EMPLEADOS),
            1, 5
        ).round().astype(int)
    
    # --- SECCIÓN G: SATISFACCIÓN + AUTOEFICACIA (q50-q56) ---
    # Satisfacción (q50-q53)
    for q in range(50, 54):
        respuestas[f'q{q}'] = np.clip(
            np.random.normal(KPI_OBJETIVO["bienestar"] * 0.95, 0.6, N_EMPLEADOS),
            1, 5
        ).round().astype(int)
    
    # Autoeficacia (q54-q56)
    for q in range(54, 57):
        respuestas[f'q{q}'] = np.clip(
            np.random.normal(3.2, 0.7, N_EMPLEADOS),  # Autoeficacia media-alta
            1, 5
        ).round().astype(int)
    
    # --- SECCIÓN H: ROTACIÓN (q57-q59) ---
    # Rotación alta (3.6)
    for q in range(57, 60):
        respuestas[f'q{q}'] = np.clip(
            np.random.normal(KPI_OBJETIVO["rotacion"], 0.6, N_EMPLEADOS),
            1, 5
        ).round().astype(int)
    
    # --- SECCIÓN I: INFRAOCUPACIÓN (q60-q64) ---
    # Infraocupación alta (parte del boreout)
    for q in range(60, 65):
        base = KPI_OBJETIVO["boreout"] * 0.95
        ajustes = empleados["departamento"].map(ajustes_boreout) + empleados["seniority"].map(ajustes_seniority_boreout)
        respuestas[f'q{q}'] = np.clip(
            base + ajustes + np.random.normal(0, 0.6, N_EMPLEADOS),
            1, 5
        ).round().astype(int)
    
    print(f"   ✅ {len(respuestas.columns)} preguntas generadas")
    
    # =====================================================
    # 3. COMBINAR Y CALCULAR KPIs
    # =====================================================
    
    print("\n📊 Paso 3: Calculando KPIs...")
    
    df_final = pd.concat([empleados, respuestas], axis=1)
    
    # Calcular KPIs
    df_final["kpi_contexto"] = df_final[[f'q{i}' for i in range(1, 16)]].mean(axis=1)
    
    burnout_agotam = df_final[[f'q{i}' for i in range(16, 23)]].mean(axis=1)
    burnout_cinismo = df_final[[f'q{i}' for i in range(23, 30)]].mean(axis=1)
    burnout_ineficacia = 6 - df_final[[f'q{i}' for i in range(30, 37)]].mean(axis=1)
    df_final["kpi_burnout"] = (burnout_agotam + burnout_cinismo + burnout_ineficacia) / 3
    
    boreout_eal = df_final[[f'q{i}' for i in range(37, 45)]].mean(axis=1)
    boreout_infra = df_final[[f'q{i}' for i in range(60, 65)]].mean(axis=1)
    df_final["kpi_boreout"] = (boreout_eal * 8 + boreout_infra * 5) / 13
    
    bienestar_who5 = df_final[[f'q{i}' for i in range(45, 50)]].mean(axis=1)
    satisfaccion = df_final[[f'q{i}' for i in range(50, 54)]].mean(axis=1)
    df_final["kpi_bienestar"] = (bienestar_who5 * 5 + satisfaccion * 4) / 9
    
    df_final["kpi_rotacion"] = df_final[[f'q{i}' for i in range(57, 60)]].mean(axis=1)
    
    # Sub-dimensiones
    df_final["burnout_agotamiento"] = burnout_agotam
    df_final["burnout_cinismo"] = burnout_cinismo
    df_final["burnout_ineficacia"] = burnout_ineficacia
    df_final["boreout_aburrimiento_eal"] = boreout_eal
    df_final["boreout_infraocupacion"] = boreout_infra
    df_final["bienestar_who5"] = bienestar_who5
    df_final["bienestar_satisfaccion"] = satisfaccion
    df_final["bienestar_autoeficacia"] = df_final[[f'q{i}' for i in range(54, 57)]].mean(axis=1)
    
    # Mostrar KPIs medios
    print("\n📈 KPIs medios de la empresa:")
    print(f"   - Burnout: {df_final['kpi_burnout'].mean():.2f}")
    print(f"   - Boreout: {df_final['kpi_boreout'].mean():.2f}")
    print(f"   - Bienestar: {df_final['kpi_bienestar'].mean():.2f}")
    print(f"   - Rotación: {df_final['kpi_rotacion'].mean():.2f}")
    print(f"   - Contexto: {df_final['kpi_contexto'].mean():.2f}")
    
    # =====================================================
    # 4. GUARDAR CSV
    # =====================================================
    
    print("\n💾 Paso 4: Guardando empresa_demo.csv...")
    
    output_path = Path("datasets/empresa_demo.csv")
    df_final.to_csv(output_path, index=False)
    
    print(f"   ✅ Guardado en: {output_path}")
    print(f"   - {len(df_final)} empleados")
    print(f"   - {len(df_final.columns)} columnas")
    
    # =====================================================
    # 5. ANÁLISIS POR DEPARTAMENTO Y SENIORITY
    # =====================================================
    
    print("\n📊 Paso 5: Análisis por departamento y seniority...")
    
    print("\n🏢 Boreout por departamento:")
    for dept in DEPARTAMENTOS.keys():
        boreout_dept = df_final[df_final["departamento"] == dept]["kpi_boreout"].mean()
        print(f"   - {dept:15s}: {boreout_dept:.2f}")
    
    print("\n👤 Boreout por seniority:")
    for sen in SENIORITY.keys():
        boreout_sen = df_final[df_final["seniority"] == sen]["kpi_boreout"].mean()
        print(f"   - {sen:15s}: {boreout_sen:.2f}")
    
    print("\n🔥 Burnout por departamento:")
    for dept in DEPARTAMENTOS.keys():
        burnout_dept = df_final[df_final["departamento"] == dept]["kpi_burnout"].mean()
        print(f"   - {dept:15s}: {burnout_dept:.2f}")
    
    print("\n" + "="*70)
    print("✅ GENERACIÓN COMPLETADA")
    print("="*70)
    print(f"\n📁 Archivo generado: {output_path}")
    print("\n🚀 Siguiente paso: Construir Notebook 5 (Demo del Framework)")
    
    return df_final


# =====================================================
# EJECUCIÓN
# =====================================================

if __name__ == "__main__":
    df_demo = generar_empresa_demo()