"""
EBLET v2.0 - Generador de Empleados Sintéticos

Genera perfiles demográficos y organizacionales realistas
para los empleados de las empresas sintéticas.
"""

import pandas as pd
import numpy as np

from config import N_EMPLEADOS_DEFAULT


def generar_empleados(empresas: pd.DataFrame, n_empleados: int = N_EMPLEADOS_DEFAULT):
    """
    Genera empleados asignados a empresas ya creadas por escenario.
    """
    
    n_empresas = len(empresas)
    
    # =====================================================
    # 1. ASIGNACIÓN EMPLEADO → EMPRESA
    # =====================================================
    
    empresa_asignada = np.random.choice(
        empresas["empresa_id"],
        size=n_empleados
    )
    
    df = pd.DataFrame({
        "empleado_id": [f"EMP_{i:05d}" for i in range(n_empleados)],
        "empresa_id": empresa_asignada
    })
    
    # =====================================================
    # 2. JOIN CON EMPRESA (CONTEXTO ORGANIZACIONAL)
    # =====================================================
    
    df = df.merge(empresas, on="empresa_id", how="left")
    
    # =====================================================
    # 3. VARIABLES SOCIODEMOGRÁFICAS
    # =====================================================
    
    # Edad (distribución laboral realista)
    df["edad"] = np.random.normal(34, 8, n_empleados).clip(22, 60).astype(int)
    
    # Experiencia profesional
    edad_inicio = np.random.uniform(18, 25, n_empleados)
    df["experiencia"] = (
        df["edad"] - edad_inicio + np.random.normal(0, 1.2, n_empleados)
    ).clip(0).round(1)
    
    # Antigüedad en empresa (depende de estabilidad del escenario)
    estabilidad_factor = np.where(
        df["escenario"] == "saludable", 0.9,
        np.where(df["escenario"] == "critico", 0.3, 0.6)
    )
    
    df["antiguedad"] = (
        df["experiencia"] * np.random.uniform(0.2, estabilidad_factor)
    ).clip(0).round(1)
    
    # =====================================================
    # 4. VARIABLES ORGANIZACIONALES
    # =====================================================
    
    df["departamento"] = np.random.choice(
        ["Desarrollo", "Datos", "Producto", "RRHH", "Ventas"],
        n_empleados
    )
    
    df["seniority"] = np.where(
        df["experiencia"] < 2, "Junior",
        np.where(df["experiencia"] < 5, "Mid",
        np.where(df["experiencia"] < 10, "Senior", "Lead"))
    )
    
    df["modalidad"] = np.random.choice(
        ["Presencial", "Híbrido", "Remoto"],
        n_empleados,
        p=[0.30, 0.45, 0.25]
    )
    
    df["genero"] = np.random.choice(
        ["Hombre", "Mujer", "No binario"],
        n_empleados,
        p=[0.55, 0.40, 0.05]
    )
    
    # =====================================================
    # 5. SALARIO (COHERENTE CON SENIORITY)
    # =====================================================
    
    def salario(seniority):
        rangos = {
            "Junior": (22000, 35000),
            "Mid": (30000, 50000),
            "Senior": (45000, 70000),
            "Lead": (60000, 95000)
        }
        
        min_s, max_s = rangos[seniority]
        return int(np.random.normal((min_s + max_s) / 2, (max_s - min_s) / 6))
    
    df["salario"] = df["seniority"].apply(salario)
    
    # =====================================================
    # 6. FEATURE ENGINEERING BASE
    # =====================================================
    
    df["empresa_size"] = df["tamano"]
    df["sector"] = df["sector"]
    
    return df