import numpy as np
import pandas as pd
import random

from config import PERFILES


def generar_encuestas(empleados, n=2500):

    registros = []

    empleados_list = empleados.to_dict("records")

    for i in range(n):

        emp = random.choice(empleados_list)

        # =========================
        # PERFIL OCULTO
        # =========================
        perfil = random.choices(
            list(PERFILES.keys()),
            weights=list(PERFILES.values())
        )[0]

        ruido = lambda: np.random.normal(0, 0.35)

        # =========================
        # FACTORES BASE PSICOLÓGICOS
        # =========================
        base = {
            "Burnout": {"presion": 4.5, "autonomia": 2.5, "satisfaccion": 2.3},
            "Boreout": {"presion": 2.0, "autonomia": 2.8, "satisfaccion": 2.4},
            "Engaged": {"presion": 4.2, "autonomia": 4.3, "satisfaccion": 4.6},
            "Healthy": {"presion": 3.0, "autonomia": 3.5, "satisfaccion": 3.8},
        }[perfil]

        presion = base["presion"] + ruido()
        autonomia = base["autonomia"] + ruido()
        satisfaccion = base["satisfaccion"] + ruido()

        def clip(x):
            return float(np.clip(round(x, 2), 1, 5))

        # =========================
        # Q1–Q5 (VARIABLES REALES)
        # =========================
        q1 = np.random.normal(7, 1.5)     # horas sueño
        q2 = np.random.randint(0, 7)      # ejercicio
        q3 = np.random.randint(0, 30)     # vacaciones
        q4 = np.random.choice([0, 1])     # apoyo psicológico empresa
        q5 = np.random.choice([0, 1])     # uso apoyo psicológico

        # =========================
        # Q6–Q20 (ORGANIZACIÓN - LIKERT)
        # =========================
        q6_20 = {f"Q{i}": clip(np.random.uniform(1, 5)) for i in range(6, 21)}

        # =========================
        # Q21–Q29 BURNOUT
        # =========================
        q21 = clip(presion + ruido())
        q22 = clip(presion + ruido())
        q23 = clip(presion + ruido())

        q24 = clip((5 - autonomia) + ruido())
        q25 = clip((5 - autonomia) + ruido())
        q26 = clip((5 - autonomia) + ruido())

        q27 = clip((5 - satisfaccion) + ruido())

        q28 = clip(presion + ruido())
        q29 = clip((5 - autonomia) + ruido())

        # =========================
        # Q30–Q38 BOREOUT
        # =========================
        q30 = clip((5 - presion) + ruido())
        q31 = clip((5 - presion) + ruido())
        q32 = clip((5 - satisfaccion) + ruido())

        q33 = clip((5 - autonomia) + ruido())
        q34 = clip((5 - autonomia) + ruido())
        q35 = clip((5 - autonomia) + ruido())

        q36 = clip((5 - presion) + ruido())
        q37 = clip((5 - presion) + ruido())
        q38 = clip((5 - autonomia) + ruido())

        # =========================
        # Q39–Q45 BIENESTAR
        # =========================
        q39 = clip(satisfaccion + ruido())
        q40 = clip(satisfaccion + ruido())
        q41 = clip(satisfaccion + ruido())
        q42 = clip(satisfaccion + ruido())

        q43 = clip(autonomia + ruido())
        q44 = clip(satisfaccion + ruido())
        q45 = clip(autonomia + ruido())

        # =========================
        # Q46–Q48 ROTACIÓN
        # =========================
        q46 = clip((5 - satisfaccion) + ruido())
        q47 = clip((5 - satisfaccion) + ruido())
        q48 = clip((5 - satisfaccion) + ruido())

        # =========================
        # REGISTRO FINAL
        # =========================
        registro = {

            "encuesta_id": f"ENC_{i:05d}",
            "empleado_id": emp["empleado_id"],

            # Q1–Q5 reales
            "Q1": round(q1, 1),
            "Q2": q2,
            "Q3": q3,
            "Q4": q4,
            "Q5": q5,

            # Q6–Q20
            **q6_20,

            # Q21–Q29
            "Q21": q21, "Q22": q22, "Q23": q23,
            "Q24": q24, "Q25": q25, "Q26": q26,
            "Q27": q27, "Q28": q28, "Q29": q29,

            # Q30–Q38
            "Q30": q30, "Q31": q31, "Q32": q32,
            "Q33": q33, "Q34": q34, "Q35": q35,
            "Q36": q36, "Q37": q37, "Q38": q38,

            # Q39–Q45
            "Q39": q39, "Q40": q40, "Q41": q41,
            "Q42": q42, "Q43": q43, "Q44": q44, "Q45": q45,

            # Q46–Q48
            "Q46": q46, "Q47": q47, "Q48": q48
        }

        registros.append(registro)

    return pd.DataFrame(registros)