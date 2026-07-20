# =====================================================

# Estilos gráficos 
# =====================================================

# ---------- Paleta KPIs ----------

COLORES_EBLET = {
    "Burnout": "#A23B3B",
    "Boreout": "#3E6C8F",
    "Bienestar": "#5B8A72",
    "Rotacion": "#B07D3C"
}

# ---------- Perfiles ----------

COLORES_PERFILES = {
    "🟢 Equilibrio": "#5B8A72",
    "🟡 Estable": "#C6A15B",
    "🟠 Quemado Activo": "#B36A3C",
    "🔵 Aburrido Crónico": "#3E6C8F",
    "🔴 Riesgo Dual": "#8F2D2D",
    "⚫ Desvinculado": "#4A4A4A"
}

# ---------- Culturas ----------

COLORES_CULTURA = {
    "Adhocracia": "#5B8CCB",
    "Clan": "#6FAE6C",
    "Mercado": "#C46A5A",
    "Jerarquica": "#8C8C8C"
}


def aplicar_estilo(fig, titulo=None, ancho=None, alto=None):
    fig.update_layout(
        template="simple_white",

        font=dict(
            family="Arial",
            size=13,
            color="#2F3A44"
        ),

        paper_bgcolor="white",
        plot_bgcolor="white",

        legend_title_text="",

        title=dict(
            text=titulo if titulo is not None else fig.layout.title.text,
            font=dict(
                size=20,
                color="#263645"
            ),
            x=0.02,
            xanchor="left"
        ),

        margin=dict(
            l=60,
            r=40,
            t=100,
            b=60
        ),

        width=ancho,
        height=alto
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor="#BFC5CA"
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#ECEFF1",
        zeroline=False,
        linecolor="#BFC5CA"
    )

    return fig