import streamlit as st

# --------------------------------------------------
# Configuración de la página
# --------------------------------------------------

st.set_page_config(
    page_title="EBLET",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# Cabecera
# --------------------------------------------------

st.title("📊 EBLET")

st.subheader("Evaluación de Bienestar Laboral y Entorno de Trabajo")

st.markdown(
    """
Framework de **People Analytics** para evaluar el bienestar laboral,
el burnout, el boreout, la cultura organizacional y el riesgo de rotación
mediante instrumentos psicométricos validados.
"""
)

st.divider()

# --------------------------------------------------
# Selección
# --------------------------------------------------

st.markdown("## ¿Qué deseas evaluar?")

col1, col2 = st.columns(2)

with col1:
    if st.button("👤 Persona", use_container_width=True):
        st.success("Próximamente: Evaluación Individual")

with col2:
    if st.button("🏢 Organización", use_container_width=True):
        st.success("Próximamente: Evaluación Organizacional")

st.divider()

st.caption("EBLET · People Analytics Framework")