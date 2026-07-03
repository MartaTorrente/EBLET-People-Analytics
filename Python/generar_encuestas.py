# =========================
# PERFIL PSICOLÓGICO
# =========================

        if perfil == "Burnout":

            presion = np.random.normal(4.6, 0.4)
            autonomia = np.random.normal(2.5, 0.6)
            apoyo_manager = np.random.normal(2.4, 0.6)
            apoyo_social = np.random.normal(3.0, 0.6)
            satisfaccion = np.random.normal(2.3, 0.7)
            equilibrio = np.random.normal(2.5, 0.7)

        elif perfil == "Boreout":

            presion = np.random.normal(2.0, 0.6)
            autonomia = np.random.normal(2.8, 0.6)
            apoyo_manager = np.random.normal(3.2, 0.5)
            apoyo_social = np.random.normal(3.3, 0.5)
            satisfaccion = np.random.normal(2.4, 0.6)
            equilibrio = np.random.normal(3.5, 0.5)

        elif perfil == "Engaged":

            presion = np.random.normal(4.2, 0.5)
            autonomia = np.random.normal(4.3, 0.4)
            apoyo_manager = np.random.normal(4.3, 0.4)
            apoyo_social = np.random.normal(4.4, 0.4)
            satisfaccion = np.random.normal(4.6, 0.3)
            equilibrio = np.random.normal(4.1, 0.4)

        else:  # Healthy

            presion = np.random.normal(3.0, 0.5)
            autonomia = np.random.normal(3.5, 0.5)
            apoyo_manager = np.random.normal(3.5, 0.5)
            apoyo_social = np.random.normal(3.5, 0.5)
            satisfaccion = np.random.normal(3.8, 0.4)
            equilibrio = np.random.normal(3.8, 0.4)

        # =========================
        # EFECTO DEPARTAMENTO
        # =========================

        if departamento in ["IT", "DevOps", "Ciberseguridad"]:

            presion += 0.4

        if departamento in ["QA", "Administración"]:

            autonomia -= 0.3

        if departamento == "Producto":

            autonomia += 0.2
            satisfaccion += 0.2

        if departamento == "RRHH":

            apoyo_social += 0.3

        # =========================
        # CULTURA ORGANIZACIONAL
        # =========================

        cultura = empresa["cultura"]

        if cultura == "Jerárquica":

            autonomia -= 0.5
            apoyo_manager -= 0.2

        elif cultura == "Innovadora":

            autonomia += 0.4
            satisfaccion += 0.3

        elif cultura == "Colaborativa":

            apoyo_social += 0.5
            equilibrio += 0.2

        elif cultura == "Orientada a resultados":

            presion += 0.4

        presion = np.clip(presion, 1, 5)
        autonomia = np.clip(autonomia, 1, 5)
        apoyo_manager = np.clip(apoyo_manager, 1, 5)
        apoyo_social = np.clip(apoyo_social, 1, 5)
        satisfaccion = np.clip(satisfaccion, 1, 5)
        equilibrio = np.clip(equilibrio, 1, 5)

        ruido = lambda: np.random.normal(0, 0.35)

# BURNOUT (Q21–Q29)

        q21 = presion + ruido()
        q22 = presion + (5 - equilibrio)*0.4 + ruido()
        q23 = (5 - equilibrio) + ruido()

        q24 = (5 - apoyo_manager) + ruido()
        q25 = (5 - apoyo_social) + ruido()
        q26 = (5 - autonomia) + ruido()

        q27 = (5 - satisfaccion) + ruido()
        q28 = presion*0.6 + (5 - autonomia)*0.4 + ruido()
        q29 = (5 - autonomia) + ruido()

# BOREOUT (Q30–Q38)

        q30 = (5 - presion) + ruido()
        q31 = (5 - presion) + ruido()
        q32 = (5 - satisfaccion) + ruido()

        q33 = (5 - autonomia) + ruido()
        q34 = (5 - autonomia) + ruido()
        q35 = (5 - autonomia) + ruido()

        q36 = (5 - presion) + ruido()
        q37 = (5 - presion) + ruido()
        q38 = (5 - autonomia) + ruido()

# BIENESTAR (Q39–Q45)
        q39 = satisfaccion + ruido()
        q40 = satisfaccion + ruido()
        q41 = (apoyo_manager + apoyo_social)/2 + ruido()
        q42 = equilibrio + ruido()
        q43 = autonomia + ruido()
        q44 = equilibrio + ruido()
        q45 = autonomia + ruido()

# ROTACIÓN (Q46–Q48)

        base_rotacion = (5 - satisfaccion)*0.7 + presion*0.3

        q46 = base_rotacion + ruido()
        q47 = base_rotacion + ruido()
        q48 = base_rotacion + ruido()

        def clip(x):
            return float(np.clip(round(x, 2), 1, 5))

# GUARDAR RESPUESTAS

        registros.append({
            "empresa_id": empresa["empresa_id"],
            "departamento": departamento,
            "rol": rol,
            "seniority": seniority,
            "perfil_oculto": perfil,

            "edad": edad,
            "experiencia": experiencia,
            "antiguedad": antiguedad,
            "horas_semana": horas,

            "presion": presion,
            "autonomia": autonomia,
            "apoyo_manager": apoyo_manager,
            "apoyo_social": apoyo_social,
            "satisfaccion": satisfaccion,
            "equilibrio": equilibrio,

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
    return pd.DataFrame(registros)