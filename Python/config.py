import numpy as np
np.random.seed(42)

# =========================
# CONFIG GENERAL
# =========================
N_EMPRESAS = 50
N_ENCUESTAS = 2500

# =========================
# VARIABLES EMPRESAS
# =========================
CIUDADES = {
    "Madrid": 0.35,
    "Barcelona": 0.25,
    "Valencia": 0.15,
    "Málaga": 0.15,
    "Bilbao": 0.10
}

SECTORES = [
    "Tecnología", "Finanzas", "Retail", "Industria", "Consultoría"
]

TAMANOS_EMPRESA = {
    "Micro": 0.10,
    "Pequeña": 0.30,
    "Mediana": 0.40,
    "Grande": 0.20
}

CULTURAS = {
    "Innovadora": 0.30,
    "Tradicional": 0.20,
    "Orientada a Resultados": 0.30,
    "Orientada a las Personas": 0.20
}

# =========================
# EMPLEADOS
# =========================
DEPARTAMENTOS = [
    "Desarrollo", "Data & IA", "Producto", "QA", "DevOps",
    "UX/UI", "Marketing", "Ventas", "RRHH", "Administración", "Finanzas"
]

SENIORITY = {
    "Junior": 0.30,
    "Mid": 0.40,
    "Senior": 0.22,
    "Lead": 0.08
}

PERFILES = {
    "Healthy": 0.40,
    "Engaged": 0.20,
    "Burnout": 0.25,
    "Boreout": 0.15
}

MODALIDAD = {
    "Presencial": 0.20,
    "Híbrido": 0.60,
    "Remoto": 0.20
}

SALARIOS = {
    "Junior": "<30k",
    "Mid": "30k-45k",
    "Senior": "45k-60k",
    "Lead": ">60k"
}