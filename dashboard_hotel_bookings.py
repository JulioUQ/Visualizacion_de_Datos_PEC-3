import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "1. Datos" / "hotel_bookings_processed.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

data = load_data()

#-----------------------------
# Título y descripción
#-----------------------------
st.title("Análisis de Reservas de Hoteles en Portugal")
st.markdown("""Este Dashboard explora el conportamiento de las reservas de hoteles en Portugal
            según el tipo de estancia y la nacionalidad de los clientes.""")


#-----------------------------
# Filtros
#-----------------------------
st.sidebar.header("Filtros")
min_year = int(data["arrival_date_year"].min())
max_year = int(data["arrival_date_year"].max())

year_range = st.sidebar.slider(
    "Año de llegada",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
    step=1
)




data_filtered = data[
    (data["arrival_date_year"] >= year_range[0]) &
    (data["arrival_date_year"] <= year_range[1])]


# -----------------------------
# Métricas principales
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Reservas totales", len(data_filtered))

with col2:
    st.metric(
        "Cancelaciones (%)",
        round(data_filtered["is_canceled"].mean() * 100, 2)
    )

with col3:
    st.metric(
        "Precio medio por noche (€)",
        round(data_filtered["adr"].mean(), 2)
    )

st.divider()

#----------------------------
# Pestañas
#---------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "Información general",
    "Evolución temporal",
    "Origen de los turistas",
    "Cancelaciones"
])

#-----------------------------
# Visualizaciones
#-----------------------------
with tab1:
    st.subheader("Número de reservas por tipo de hotel")
    reservas_hotel = (
    data_filtered
    .groupby("hotel")
    .size()
    .reset_index(name="num_reservas")
    )

    fig_reservas = px.bar(
        reservas_hotel,
        x="hotel",
        y="num_reservas",
        text="num_reservas",
        labels={
            "hotel": "Tipo de hotel",
            "num_reservas": "Número de reservas"
        }
    )

    fig_reservas.update_traces(textposition="outside")


    st.plotly_chart(fig_reservas, use_container_width=True)

    st.subheader("Reservas por tipo de estancia y tipo de hotel")
    estancia_hotel = (
    data_filtered
    .groupby(["tipo", "hotel"])
    .size()
    .reset_index(name="num_reservas")
)

    fig_estancia = px.bar(
        estancia_hotel,
        x="tipo",
        y="num_reservas",
        color="hotel",
        barmode="group",
        labels={
            "tipo": "Tipo de estancia",
            "num_reservas": "Número de reservas",
            "hotel": "Tipo de hotel"
        }
    )

    st.plotly_chart(fig_estancia, use_container_width=True)

    st.subheader("Reservas por grupo de clientes y tipo de hotel")
    grupo_hotel = (
    data_filtered
    .groupby(["grupo", "hotel"])
    .size()
    .reset_index(name="num_reservas")
    )

    fig_grupo = px.bar(
        grupo_hotel,
        x="grupo",
        y="num_reservas",
        color="hotel",
        barmode="group",
        labels={
            "grupo": "Grupo de clientes",
            "num_reservas": "Número de reservas",
            "hotel": "Tipo de hotel"
        }
    )
    st.plotly_chart(fig_grupo, use_container_width=True)

    st.subheader("Relación entre tipo de estancia y precio medio por noche (ADR)")

    fig_adr = px.box(
        data_filtered,
        x="tipo",
        y="adr",
        color="hotel",
        labels={
            "tipo": "Tipo de estancia",
            "adr": "Precio medio por noche (€)",
            "hotel": "Tipo de hotel"
        }
    )

    st.plotly_chart(fig_adr, use_container_width=True, key = "fig_adr_tab1")


with tab2:
    st.subheader("Evolución temporal de las reservas por tipo de hotel")

    df_plot = data_filtered.copy()
    df_plot["dia"] = pd.to_datetime(df_plot["dia"])

    # -----------------------------
    # Tipo de hotel
    # -----------------------------
    reservas_hotel_tiempo = (
        df_plot
        .groupby(["dia", "hotel"])
        .size()
        .reset_index(name="num_reservas")
    )

    fig_time_hotel = px.line(
        reservas_hotel_tiempo,
        x="dia",
        y="num_reservas",
        color="hotel",
        labels={
            "dia": "Día de llegada",
            "num_reservas": "Número de reservas",
            "hotel": "Tipo de hotel"
        }
    )

    st.plotly_chart(
        fig_time_hotel,
        use_container_width=True,
        key="fig_time_hotel_tab2"
    )

    # -----------------------------
    # Tipo de estancia
    # -----------------------------
    st.subheader("Evolución temporal de las reservas por tipo de estancia")

    reservas_tipo_tiempo = (
        df_plot
        .groupby(["dia", "tipo"])
        .size()
        .reset_index(name="num_reservas")
    )

    fig_time_tipo = px.line(
        reservas_tipo_tiempo,
        x="dia",
        y="num_reservas",
        color="tipo",
        labels={
            "dia": "Día de llegada",
            "num_reservas": "Número de reservas",
            "tipo": "Tipo de estancia"
        }
    )

    st.plotly_chart(
        fig_time_tipo,
        use_container_width=True,
        key="fig_time_tipo_tab2"
    )

    # -----------------------------
    # Grupo de clientes
    # -----------------------------
    st.subheader("Evolución temporal de las reservas por grupo de clientes")

    reservas_grupo_tiempo = (
        df_plot
        .groupby(["dia", "grupo"])
        .size()
        .reset_index(name="num_reservas")
    )

    fig_time_grupo = px.line(
        reservas_grupo_tiempo,
        x="dia",
        y="num_reservas",
        color="grupo",
        labels={
            "dia": "Día de llegada",
            "num_reservas": "Número de reservas",
            "grupo": "Grupo de clientes"
        }
    )

    st.plotly_chart(
        fig_time_grupo,
        use_container_width=True,
        key="fig_time_grupo_tab2"
    )


with tab3:
    st.subheader("Evolución temporal de las reservas por país de origen (Top 5)")

    df_plot = data_filtered.copy()
    df_plot["dia"] = pd.to_datetime(df_plot["dia"])

    # -----------------------------
    # Selección Top 5 países
    # -----------------------------
    top_countries = (
        df_plot["country"]
        .value_counts()
        .head(5)
        .index
    )

    df_top = df_plot[df_plot["country"].isin(top_countries)]

    # -----------------------------
    # Evolución temporal por país
    # -----------------------------
    reservas_pais_tiempo = (
        df_top
        .groupby(["dia", "country"])
        .size()
        .reset_index(name="num_reservas")
    )

    fig_country_time = px.line(
        reservas_pais_tiempo,
        x="dia",
        y="num_reservas",
        color="country",
        labels={
            "dia": "Día de llegada",
            "num_reservas": "Número de reservas",
            "country": "País de origen"
        }
    )

    st.plotly_chart(
        fig_country_time,
        use_container_width=True,
        key="fig_country_time_tab3"
    )

    # -----------------------------
    # Reservas por tipo de estancia y país
    # -----------------------------
    st.subheader("Reservas por tipo de estancia según país de origen (Top 5)")

    estancia_pais = (
        df_top
        .groupby(["country", "tipo"])
        .size()
        .reset_index(name="num_reservas")
    )

    fig_estancia_pais = px.bar(
        estancia_pais,
        x="country",
        y="num_reservas",
        color="tipo",
        barmode="group",
        labels={
            "country": "País de origen",
            "tipo": "Tipo de estancia",
            "num_reservas": "Número de reservas"
        }
    )

    st.plotly_chart(
        fig_estancia_pais,
        use_container_width=True,
        key="fig_estancia_pais_tab3"
    )

    # -----------------------------
    # Reservas por grupo de clientes y país
    # -----------------------------
    st.subheader("Reservas por grupo de clientes según país de origen (Top 5)")

    grupo_pais = (
        df_top
        .groupby(["country", "grupo"])
        .size()
        .reset_index(name="num_reservas")
    )

    fig_grupo_pais = px.bar(
        grupo_pais,
        x="country",
        y="num_reservas",
        color="grupo",
        barmode="group",
        labels={
            "country": "País de origen",
            "grupo": "Grupo de clientes",
            "num_reservas": "Número de reservas"
        }
    )

    st.plotly_chart(
        fig_grupo_pais,
        use_container_width=True,
        key="fig_grupo_pais_tab3"
    )



with tab4:
    st.subheader("Tasa de cancelación por grupo de clientes y tipo de hotel")

    cancel_group = (
        data_filtered
        .groupby(["grupo", "hotel"])["is_canceled"]
        .mean()
        .reset_index()
    )

    cancel_group["cancel_rate"] = cancel_group["is_canceled"] * 100

    fig_cancel_group = px.bar(
        cancel_group,
        x="grupo",
        y="cancel_rate",
        color="hotel",
        barmode="group",
        labels={
            "grupo": "Grupo de clientes",
            "cancel_rate": "Tasa de cancelación (%)",
            "hotel": "Tipo de hotel"
        }
    )
    st.plotly_chart(fig_cancel_group, use_container_width=True)

    st.subheader("Tasa de cancelación por tipo de estancia")

    cancel_tipo = (
        data_filtered
        .groupby(["tipo", "hotel"])["is_canceled"]
        .mean()
        .reset_index()
    )

    cancel_tipo["cancel_rate"] = cancel_tipo["is_canceled"] * 100

    fig_cancel_tipo = px.bar(
        cancel_tipo,
        x="tipo",
        y="cancel_rate",
        color="hotel",
        barmode="group"
    )

    st.plotly_chart(fig_cancel_tipo, use_container_width=True)

    st.subheader("Tasa de cancelación por nacionalidad (Top 10)")

    # Seleccionar países con más reservas
    top_countries = (
        data_filtered["country"]
        .value_counts()
        .head(10)
        .index
    )

    df_country = data_filtered[data_filtered["country"].isin(top_countries)]

    cancel_country = (
        df_country
        .groupby("country")["is_canceled"]
        .mean()
        .reset_index()
    )

    cancel_country["cancel_rate"] = cancel_country["is_canceled"] * 100

    fig_cancel_country = px.bar(
        cancel_country,
        x="country",
        y="cancel_rate",
        labels={
            "country": "País de origen",
            "cancel_rate": "Tasa de cancelación (%)"
        }
    )

    st.plotly_chart(
        fig_cancel_country,
        use_container_width=True,
        key="fig_cancel_country_tab4"
    )





