import pandas as pd

from generador_empresas import generar_empresas
from generador_empleados import generar_empleados
from generador_encuestas import generar_encuestas

from scoring import *
from validacion import validar_dataset

# =========================
# PIPELINE
# =========================

empresas = generar_empresas(50)

empleados = generar_empleados(empresas, 2500)

encuestas = generar_encuestas(empleados, 2500)

# =========================
# EXPORT RAW
# =========================

empresas.to_csv("empresas.csv", index=False)
empleados.to_csv("empleados.csv", index=False)
encuestas.to_csv("encuestas.csv", index=False)

# =========================
# SCORES (CORRECTO)
# =========================

scores = pd.DataFrame({
    "encuesta_id": encuestas["encuesta_id"],
    "empleado_id": encuestas["empleado_id"],

    # BURNOUT
    "burnout_exhaustion": burnout_exhaustion(encuestas),
    "burnout_cynicism": burnout_cynicism(encuestas),
    "burnout_efficacy": burnout_efficacy(encuestas),
    "burnout_global": burnout_global(encuestas),

    # BOREOUT
    "boreout_disinterest": boreout_disinterest(encuestas),
    "boreout_lack_challenge": boreout_lack_challenge(encuestas),
    "boreout_underload": boreout_underload(encuestas),
    "boreout_global": boreout_global(encuestas),

    # WELLBEING
    "wellbeing_satisfaction": wellbeing_satisfaction(encuestas),
    "wellbeing_efficacy": wellbeing_efficacy(encuestas),
    "wellbeing_global": wellbeing_global(encuestas),

    # ROTATION
    "rotation_global": rotation_global(encuestas)
})

scores.to_csv("scores.csv", index=False)

# =========================
# VALIDACIÓN
# =========================

validar_dataset(encuestas)

print("OK ✔")