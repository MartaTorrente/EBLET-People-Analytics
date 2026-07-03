import pandas as pd
import numpy as np
import random
from config import CITIES, SPECIALTIES
def generate_companies(n=25):
    companies = []
    city_names = list(CITIES.keys())
    for i in range(n):
        company = {
            "company_id": f"CMP_{i:03d}",
            "company_name": f"Tech{random.choice(['Nova','Data','Cloud','AI','Digital','Labs'])}{i}",
            "city": random.choices(city_names, weights=list(CITIES.values()))[0],
            "specialty": random.choice(SPECIALTIES),
            "size": random.choice(["Small", "Medium", "Large"])
        }
        companies.append(company)
    return pd.DataFrame(companies)

from config import ROLES, SENIORITY, PROFILES
# ---------------------------
# GENERAR EMPLEADOS
# ---------------------------
def generar_empleados(empresas_df, n_empleados=2500):
    empleados = []
    empresas = empresas_df.to_dict("records")
    lista_roles = list(ROLES.keys())
    lista_seniority = list(SENIORITY.keys())
    lista_perfiles = list(PROFILES.keys())
    for i in range(n_empleados):
        empresa = random.choice(empresas)
        # ---------------------------
        # PERFIL PSICOLÓGICO OCULTO
        # ---------------------------
        perfil = random.choices(
            lista_perfiles,
            weights=list(PROFILES.values())
        )[0]
        # ---------------------------
        # SENIORITY
        # ---------------------------
        seniority = random.choices(
            lista_seniority,
            weights=list(SENIORITY.values())
        )[0]
        # ---------------------------
        # ROL (ligado a empresa)
        # ---------------------------
        rol = random.choice(lista_roles)
        empleado = {
            "id_empleado": f"EMP_{i:05d}",
            "id_empresa": empresa["company_id"],
            "ciudad": empresa["city"],
            "especialidad_empresa": empresa["specialty"],
            "rol": rol,
            "seniority": seniority,
            "perfil_oculto": perfil,
            # variables base
            "edad": None,
            "experiencia": None,
            "antiguedad_empresa": None,
            "horas_semana": None
        }
        empleados.append(empleado)
    return pd.DataFrame(empleados)

def asignar_variables_base(df):
    edades = []
    experiencia = []
    antiguedad = []
    horas = []
    for _, row in df.iterrows():
        # ---------------------------
        # EDAD SEGÚN SENIORITY
        # ---------------------------
        if row["seniority"] == "Junior":
            edad = np.random.normal(25, 2)
        elif row["seniority"] == "Mid":
            edad = np.random.normal(30, 3)
        elif row["seniority"] == "Senior":
            edad = np.random.normal(38, 4)
        else:  # Lead
            edad = np.random.normal(45, 5)
        edad = int(np.clip(edad, 22, 60))
        edades.append(edad)
        # ---------------------------
        # EXPERIENCIA REALISTA
        # ---------------------------
        exp = max(0, edad - 22 + np.random.normal(0, 2))
        experiencia.append(round(exp, 1))
        # ---------------------------
        # ANTIGÜEDAD EMPRESA
        # ---------------------------
        antig = min(exp, abs(np.random.normal(3, 2)))
        antiguedad.append(round(antig, 1))
        # ---------------------------
        # HORAS SEMANALES BASE
        # ---------------------------
        base = 40
        if row["perfil_oculto"] == "Burnout":
            base += np.random.normal(10, 3)
        elif row["perfil_oculto"] == "Boreout":
            base -= np.random.normal(5, 2)
        elif row["perfil_oculto"] == "Engaged":
            base += np.random.normal(2, 2)
        else:  # Healthy
            base += np.random.normal(0, 2)
        horas.append(round(np.clip(base, 25, 65), 1))
    df["edad"] = edades
    df["experiencia"] = experiencia
    df["antiguedad_empresa"] = antiguedad
    df["horas_semana"] = horas
    return df

def generar_variables_psicologicas(df):
    presion = []
    autonomia = []
    apoyo_manager = []
    apoyo_social = []
    equilibrio_vt = []
    satisfaccion = []
    for _, row in df.iterrows():
        perfil = row["perfil_oculto"]
        rol = row["rol"]
        # ---------------------------
        # BASES POR PERFIL
        # ---------------------------
        if perfil == "Burnout":
            base_presion = np.random.normal(4.5, 0.5)
            base_autonomia = np.random.normal(2.5, 0.7)
            base_apoyo_manager = np.random.normal(2.5, 0.7)
            base_apoyo_social = np.random.normal(3.0, 0.6)
            base_equilibrio = np.random.normal(2.5, 0.7)
            base_satisfaccion = np.random.normal(2.5, 0.8)
        elif perfil == "Boreout":
            base_presion = np.random.normal(2.0, 0.6)
            base_autonomia = np.random.normal(2.8, 0.7)
            base_apoyo_manager = np.random.normal(3.0, 0.6)
            base_apoyo_social = np.random.normal(3.2, 0.6)
            base_equilibrio = np.random.normal(3.5, 0.6)
            base_satisfaccion = np.random.normal(2.3, 0.7)
        elif perfil == "Engaged":
            base_presion = np.random.normal(4.0, 0.6)
            base_autonomia = np.random.normal(4.2, 0.5)
            base_apoyo_manager = np.random.normal(4.2, 0.5)
            base_apoyo_social = np.random.normal(4.3, 0.4)
            base_equilibrio = np.random.normal(4.0, 0.5)
            base_satisfaccion = np.random.normal(4.5, 0.4)
        else:  # Healthy
            base_presion = np.random.normal(3.0, 0.6)
            base_autonomia = np.random.normal(3.5, 0.6)
            base_apoyo_manager = np.random.normal(3.5, 0.6)
            base_apoyo_social = np.random.normal(3.5, 0.6)
            base_equilibrio = np.random.normal(3.8, 0.5)
            base_satisfaccion = np.random.normal(3.8, 0.5)
        # ---------------------------
        # EFECTO DEL ROL (AJUSTE REALISTA)
        # ---------------------------
        if rol == "DEVOPS":
            base_presion += 0.5
        if rol == "QA":
            base_boreout_bonus = 0.4 if perfil == "Boreout" else 0
        if rol == "PM":
            base_presion += 0.4
            base_autonomia += 0.3
        if rol == "DA":
            base_autonomia += 0.2
        # ---------------------------
        # CLIP FINAL (ESCALA 1-5)
        # ---------------------------
        presion.append(np.clip(base_presion, 1, 5))
        autonomia.append(np.clip(base_autonomia, 1, 5))
        apoyo_manager.append(np.clip(base_apoyo_manager, 1, 5))
        apoyo_social.append(np.clip(base_apoyo_social, 1, 5))
        equilibrio_vt.append(np.clip(base_equilibrio, 1, 5))
        satisfaccion.append(np.clip(base_satisfaccion, 1, 5))
    df["presion"] = presion
    df["autonomia"] = autonomia
    df["apoyo_manager"] = apoyo_manager
    df["apoyo_social"] = apoyo_social
    df["equilibrio_vida_trabajo"] = equilibrio_vt
    df["satisfaccion"] = satisfaccion
    return df

def generar_encuesta(df):
    respuestas = []
    for _, row in df.iterrows():
        perfil = row["perfil_oculto"]
        # ---------------------------
        # FACTORES BASE
        # ---------------------------
        presion = row["presion"]
        autonomia = row["autonomia"]
        apoyo_manager = row["apoyo_manager"]
        apoyo_social = row["apoyo_social"]
        equilibrio = row["equilibrio_vida_trabajo"]
        satisfaccion = row["satisfaccion"]
        # ---------------------------
        # RUIDO CONTROLADO
        # ---------------------------
        ruido = lambda: np.random.normal(0, 0.4)
        # ===========================
        # SECCIÓN 4 - BURNOUT (Q21-Q29)
        # ===========================
        q21 = presion + ruido()
        q22 = presion + (5 - equilibrio) * 0.3 + ruido()
        q23 = (5 - equilibrio) + ruido()
        q24 = (5 - apoyo_manager) + ruido()
        q25 = (5 - apoyo_social) + ruido()
        q26 = (5 - autonomia) + ruido()
        q27 = (5 - satisfaccion) + ruido()
        q28 = presion * 0.7 + (5 - autonomia) * 0.3 + ruido()
        q29 = (5 - autonomia) + ruido()
        burnout_items = [q21,q22,q23,q24,q25,q26,q27,q28,q29]
        # ===========================
        # SECCIÓN 5 - BOREOUT (Q30-Q38)
        # ===========================
        q30 = (5 - presion) + ruido()
        q31 = (5 - presion) + ruido()
        q32 = (5 - satisfaccion) + ruido()
        q33 = (5 - autonomia) + ruido()
        q34 = (5 - autonomia) + ruido()
        q35 = (5 - autonomia) + ruido()
        q36 = (5 - presion) + ruido()
        q37 = (5 - presion) + ruido()
        q38 = (5 - autonomia) + ruido()
        boreout_items = [q30,q31,q32,q33,q34,q35,q36,q37,q38]
        # ===========================
        # SECCIÓN 6 - BIENESTAR (Q39-Q45)
        # ===========================
        q39 = satisfaccion + ruido()
        q40 = satisfaccion + ruido()
        q41 = (apoyo_manager + apoyo_social) / 2 + ruido()
        q42 = equilibrio + ruido()
        q43 = autonomia + ruido()
        q44 = equilibrio + ruido()
        q45 = autonomia + ruido()
        bienestar_items = [q39,q40,q41,q42,q43,q44,q45]
        # ===========================
        # SECCIÓN 7 - INTENCIÓN CAMBIO (Q46-Q48)
        # ===========================
        base_rotacion = (5 - satisfaccion) * 0.6 + presion * 0.4
        q46 = base_rotacion + ruido()
        q47 = base_rotacion + ruido()
        q48 = base_rotacion + ruido()
        rotacion_items = [q46,q47,q48]
        # ---------------------------
        # CLIP ESCALA LIKERT 1-5
        # ---------------------------
        def clip(x):
            return float(np.clip(round(x,2), 1, 5))
        respuestas.append({
            "Q21": clip(q21), "Q22": clip(q22), "Q23": clip(q23),
            "Q24": clip(q24), "Q25": clip(q25), "Q26": clip(q26),
            "Q27": clip(q27), "Q28": clip(q28), "Q29": clip(q29),
            "Q30": clip(q30), "Q31": clip(q31), "Q32": clip(q32),
            "Q33": clip(q33), "Q34": clip(q34), "Q35": clip(q35),
            "Q36": clip(q36), "Q37": clip(q37), "Q38": clip(q38),
            "Q39": clip(q39), "Q40": clip(q40), "Q41": clip(q41),
            "Q42": clip(q42), "Q43": clip(q43), "Q44": clip(q44),
            "Q45": clip(q45),
            "Q46": clip(q46), "Q47": clip(q47), "Q48": clip(q48)
        })
    return pd.DataFrame(respuestas)