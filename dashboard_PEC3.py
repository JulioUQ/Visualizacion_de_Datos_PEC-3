import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="El Enigma de las Cancelaciones",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado mejorado
st.markdown("""
<style>
    /* Estilos generales */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Títulos principales */
    .big-title {
        font-size: 64px;
        font-weight: 900;
        text-align: center;
        color: #1f77b4;
        margin: 40px 0 15px 0;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.2);
        letter-spacing: -1px;
    }
    
    .subtitle {
        font-size: 26px;
        text-align: center;
        color: #666;
        margin-bottom: 50px;
        font-style: italic;
        font-weight: 300;
    }
    
    /* Capítulos */
    .chapter-title {
        font-size: 42px;
        font-weight: 700;
        color: #1f77b4;
        margin: 50px 0 20px 0;
        border-left: 6px solid #1f77b4;
        padding-left: 20px;
    }
    
    .chapter-intro {
        font-size: 19px;
        color: #444;
        line-height: 1.9;
        padding: 25px;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-left: 6px solid #1f77b4;
        border-radius: 8px;
        margin: 25px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    /* Tarjetas métricas */
    .metric-card {
        background: white;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.12);
        text-align: center;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.18);
    }
    
    .metric-value {
        font-size: 52px;
        font-weight: 900;
        color: #1f77b4;
        margin: 10px 0;
    }
    
    .metric-label {
        font-size: 17px;
        color: #666;
        margin-top: 10px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Cajas de insights */
    .insight-box {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border-left: 6px solid #ffc107;
        padding: 20px;
        margin: 30px 0;
        border-radius: 8px;
        box-shadow: 0 3px 10px rgba(255,193,7,0.2);
    }
    
    .insight-box strong {
        color: #856404;
        font-size: 19px;
    }
    
    /* Cajas de recomendaciones */
    .recommendation-box {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 6px solid #28a745;
        padding: 18px;
        margin: 15px 0;
        border-radius: 8px;
        box-shadow: 0 3px 10px rgba(40,167,69,0.2);
    }
    
    .recommendation-box strong {
        color: #155724;
        font-size: 18px;
    }
    
    /* Tarjetas de pilares */
    .pillar-card {
        background: rgba(255,255,255,0.15);
        padding: 20px;
        border-radius: 12px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        height: 100%;
    }
    
    /* Iconos grandes */
    .icon-card {
        text-align: center;
        padding: 25px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .icon-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }
    
    .icon-large {
        font-size: 48px;
        margin-bottom: 15px;
    }
    
    /* Hero section */
    .hero-metric {
        text-align: center;
        padding: 50px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        margin: 40px auto;
        max-width: 800px;
    }
    
    .hero-number {
        font-size: 96px;
        font-weight: 900;
        color: white;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
        margin: 0;
    }
    
    .hero-label {
        font-size: 32px;
        color: #f0f0f0;
        margin: 15px 0;
        font-weight: 600;
        letter-spacing: 2px;
    }
    
    .hero-subtitle {
        font-size: 20px;
        color: #e0e0e0;
        margin-top: 25px;
        font-style: italic;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 65px;
        padding: 15px 25px;
        background-color: white;
        border-radius: 10px;
        font-size: 17px;
        font-weight: 700;
        border: 2px solid #e9ecef;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #f8f9fa;
        border-color: #667eea;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border-color: #667eea;
    }
    
    /* Secciones numeradas */
    .section-number {
        display: inline-block;
        width: 40px;
        height: 40px;
        background: #1f77b4;
        color: white;
        border-radius: 50%;
        text-align: center;
        line-height: 40px;
        font-weight: 700;
        margin-right: 15px;
        font-size: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Cargar datos
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "1. Datos" / "hotel_bookings_processed.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    
    # Crear columna de fecha de llegada
    if 'arrival_date_year' in df.columns and 'arrival_date_month' in df.columns and 'arrival_date_day_of_month' in df.columns:
        month_map = {
            'January': 1, 'February': 2, 'March': 3, 'April': 4,
            'May': 5, 'June': 6, 'July': 7, 'August': 8,
            'September': 9, 'October': 10, 'November': 11, 'December': 12
        }
        df['month_num'] = df['arrival_date_month'].map(month_map)
        df['dia'] = pd.to_datetime(df[['arrival_date_year', 'month_num', 'arrival_date_day_of_month']].rename(
            columns={'arrival_date_year': 'year', 'month_num': 'month', 'arrival_date_day_of_month': 'day'}
        ))
    
    # Total de noches
    if 'stays_in_weekend_nights' in df.columns and 'stays_in_week_nights' in df.columns:
        df['total_nights'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']
    
    # Total de huéspedes
    if 'adults' in df.columns and 'children' in df.columns and 'babies' in df.columns:
        df['total_guests'] = df['adults'] + df['children'] + df['babies']
    
    # Temporada
    if 'arrival_date_month' in df.columns:
        df['season'] = df['arrival_date_month'].map({
            'December': 'Invierno', 'January': 'Invierno', 'February': 'Invierno',
            'March': 'Primavera', 'April': 'Primavera', 'May': 'Primavera',
            'June': 'Verano', 'July': 'Verano', 'August': 'Verano',
            'September': 'Otoño', 'October': 'Otoño', 'November': 'Otoño'
        })
    
    # Categoría de lead time
    if 'lead_time' in df.columns:
        df['lead_time_category'] = pd.cut(
            df['lead_time'],
            bins=[-1, 0, 7, 30, 90, 180, df['lead_time'].max()],
            labels=['Mismo día', '1 semana', '1 mes', '3 meses', '6 meses', 'Más de 6 meses']
        )
    
    return df

data = load_data()

# ============================================
# SIDEBAR - FILTROS INTERACTIVOS
# ============================================
st.sidebar.markdown("## 🎯 Filtros Interactivos")
st.sidebar.markdown("*Personaliza tu exploración de datos*")
st.sidebar.markdown("---")

# Filtro de hotel
hotel_options = ["Todos"] + sorted(list(data["hotel"].unique()))
selected_hotel = st.sidebar.selectbox("🏨 Tipo de Hotel", hotel_options)

# Filtro de año
min_year = int(data["arrival_date_year"].min())
max_year = int(data["arrival_date_year"].max())
year_range = st.sidebar.slider(
    "📅 Año de Llegada",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
    step=1
)

# Filtro de tipo de cliente
if 'customer_type' in data.columns:
    customer_options = ["Todos"] + sorted(list(data["customer_type"].unique()))
    selected_customer = st.sidebar.selectbox("👤 Tipo de Cliente", customer_options)
else:
    selected_customer = "Todos"

# Aplicar filtros
data_filtered = data[
    (data["arrival_date_year"] >= year_range[0]) &
    (data["arrival_date_year"] <= year_range[1])
]

if selected_hotel != "Todos":
    data_filtered = data_filtered[data_filtered["hotel"] == selected_hotel]

if selected_customer != "Todos" and 'customer_type' in data.columns:
    data_filtered = data_filtered[data_filtered["customer_type"] == selected_customer]

st.sidebar.markdown("---")
st.sidebar.success(f"**📊 Registros filtrados:** {len(data_filtered):,}")

st.sidebar.markdown("---")
st.sidebar.info("""
**💡 Tip de Navegación**

Explora cada capítulo secuencialmente para seguir la narrativa de datos. Usa los filtros para descubrir patrones específicos.
""")

# ============================================
# HEADER PRINCIPAL - PORTADA IMPACTANTE
# ============================================
st.markdown('<div class="big-title">🏨 El Enigma de las Cancelaciones</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Un Viaje por los Datos Hoteleros de Portugal (2015-2017)</div>', unsafe_allow_html=True)

# Hero metric
cancelation_rate = data_filtered["is_canceled"].mean() * 100
st.markdown(f"""
<div class="hero-metric">
    <div class="hero-number">{cancelation_rate:.1f}%</div>
    <div class="hero-label">DE CANCELACIONES</div>
    <div class="hero-subtitle">
        4 de cada 10 clientes no llegan al hotel<br>
        ¿Frustración? Absolutamente. ¿Solución? Exploremos los datos.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================
# CAPÍTULO 1: BIENVENIDA AL PROBLEMA
# ============================================
st.markdown('<div class="chapter-title">📖 Capítulo 1: Bienvenida al Problema</div>', unsafe_allow_html=True)

st.markdown("""
<div class="chapter-intro">
<strong>Imagina que eres director de un hotel en Lisboa.</strong> Cada mañana, al revisar las reservas del día, 
descubres que 4 de cada 10 clientes han cancelado. <strong>¿Frustración? Absolutamente.</strong> 
Pero, ¿y si pudiéramos entender el porqué?<br><br>

Esta visualización explora <strong>119,390 reservas hoteleras</strong> realizadas entre 2015 y 2017 
en dos hoteles portugueses: un <strong>City Hotel en Lisboa</strong> y un <strong>Resort Hotel en el Algarve</strong>.<br><br>

<strong>Nuestro objetivo:</strong> Desentrañar los patrones ocultos detrás de ese 37% de cancelaciones 
que amenaza la rentabilidad del sector hotelero.
</div>
""", unsafe_allow_html=True)

st.markdown("### 🔍 Los 4 Pilares de Nuestra Historia")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="icon-card">
        <div class="icon-large">⏰</div>
        <strong>Factor Temporal</strong><br>
        <span style="color: #666;">Lead time y estacionalidad</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="icon-card">
        <div class="icon-large">📱</div>
        <strong>Dependencia Digital</strong><br>
        <span style="color: #666;">82% vía OTAs</span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="icon-card">
        <div class="icon-large">💰</div>
        <strong>Políticas Flexibles</strong><br>
        <span style="color: #666;">87% sin depósito</span>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="icon-card">
        <div class="icon-large">🔄</div>
        <strong>Baja Fidelización</strong><br>
        <span style="color: #666;">97% clientes nuevos</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================
# CAPÍTULO 2: RADIOGRAFÍA DEL DATASET
# ============================================
st.markdown('<div class="chapter-title">📊 Capítulo 2: Radiografía del Dataset</div>', unsafe_allow_html=True)

st.markdown("""
<div class="chapter-intro">
Comencemos por entender la magnitud de los datos. Este análisis abarca <strong>tres años de 
operaciones hoteleras</strong> con 32 variables que describen cada aspecto de una reserva: 
desde cuándo se realizó, cuántas noches se quedó el huésped, qué tipo de habitación eligió, 
hasta si finalmente se presentó o canceló.
</div>
""", unsafe_allow_html=True)

st.markdown("### 📈 Métricas Clave del Negocio")

# Métricas principales en KPI cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{len(data_filtered):,}</div>
        <div class="metric-label">Reservas Totales</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    canceled = data_filtered["is_canceled"].sum()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color: #d62728;">{canceled:,}</div>
        <div class="metric-label">Cancelaciones</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    avg_adr = data_filtered["adr"].mean()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color: #28a745;">€{avg_adr:.2f}</div>
        <div class="metric-label">ADR Promedio</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    avg_lead = data_filtered["lead_time"].mean()
    median_lead = data_filtered["lead_time"].median()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color: #ff7f0e;">{int(median_lead)}</div>
        <div class="metric-label">Mediana Lead Time</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Insights clave del dataset
st.markdown("""
<div class="insight-box">
<strong>💡 Hallazgo #1: La Magnitud del Problema</strong><br>
44,224 reservas canceladas de 119,390 totales. Un 37% que representa pérdidas millonarias 
en ingresos potenciales. La mediana de lead time es de 69 días, pero encontramos reservas 
hechas con hasta 2 años de anticipación.
</div>
""", unsafe_allow_html=True)

# Gráficos de distribución
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🏨 Distribución por Tipo de Hotel")
    hotel_dist = data_filtered.groupby("hotel").size().reset_index(name="count")
    fig_hotel = px.pie(
        hotel_dist,
        values="count",
        names="hotel",
        color_discrete_sequence=["#1f77b4", "#ff7f0e"],
        hole=0.45
    )
    fig_hotel.update_traces(
        textposition='inside', 
        textinfo='percent+label', 
        textfont_size=16,
        marker=dict(line=dict(color='white', width=3))
    )
    fig_hotel.update_layout(
        height=420, 
        showlegend=True,
        font=dict(size=14)
    )
    st.plotly_chart(fig_hotel, use_container_width=True, key="fig_hotel_ch2")

with col2:
    st.markdown("#### 📋 Estado de las Reservas")
    status_map = {1: "Cancelada", 0: "Completada"}
    data_filtered_status = data_filtered.copy()
    data_filtered_status["status"] = data_filtered_status["is_canceled"].map(status_map)
    
    status_dist = data_filtered_status.groupby("status").size().reset_index(name="count")
    fig_status = px.pie(
        status_dist,
        values="count",
        names="status",
        color_discrete_sequence=["#2ca02c", "#d62728"],
        hole=0.45
    )
    fig_status.update_traces(
        textposition='inside', 
        textinfo='percent+label', 
        textfont_size=16,
        marker=dict(line=dict(color='white', width=3))
    )
    fig_status.update_layout(
        height=420, 
        showlegend=True,
        font=dict(size=14)
    )
    st.plotly_chart(fig_status, use_container_width=True, key="fig_status_ch2")

st.markdown("### 👥 Composición de Huéspedes y Duración")

col1, col2 = st.columns(2)

with col1:
    if 'total_guests' in data_filtered.columns:
        guests_dist = data_filtered['total_guests'].value_counts().sort_index().reset_index()
        guests_dist.columns = ['num_guests', 'count']
        guests_dist = guests_dist[guests_dist['num_guests'] <= 8]
        
        fig_guests = px.bar(
            guests_dist,
            x='num_guests',
            y='count',
            title='Distribución por Número de Huéspedes',
            labels={'num_guests': 'Huéspedes', 'count': 'Reservas'},
            color='count',
            color_continuous_scale='Teal'
        )
        fig_guests.update_traces(
            text=guests_dist['count'],
            texttemplate='%{text:,}',
            textposition='outside',
            marker_line_color='white',
            marker_line_width=2
        )
        fig_guests.update_layout(height=400, showlegend=False, font=dict(size=13))
        st.plotly_chart(fig_guests, use_container_width=True, key="fig_guests_ch2")

with col2:
    if 'total_nights' in data_filtered.columns:
        nights_dist = data_filtered[data_filtered['total_nights'] <= 14].copy()
        nights_counts = nights_dist['total_nights'].value_counts().sort_index().reset_index()
        nights_counts.columns = ['num_nights', 'count']
        
        fig_nights = px.bar(
            nights_counts,
            x='num_nights',
            y='count',
            title='Distribución por Duración de Estancia',
            labels={'num_nights': 'Noches', 'count': 'Reservas'},
            color='count',
            color_continuous_scale='Magma'
        )
        fig_nights.update_traces(
            text=nights_counts['count'],
            texttemplate='%{text:,}',
            textposition='outside',
            marker_line_color='white',
            marker_line_width=2
        )
        fig_nights.update_layout(height=400, showlegend=False, font=dict(size=13))
        st.plotly_chart(fig_nights, use_container_width=True, key="fig_nights_ch2")

st.markdown("---")

# ============================================
# CAPÍTULO 3: EL FACTOR TIEMPO
# ============================================
st.markdown('<div class="chapter-title">⏰ Capítulo 3: El Factor Tiempo</div>', unsafe_allow_html=True)

st.markdown("""
<div class="chapter-intro">
El tiempo es el protagonista silencioso de las cancelaciones. <strong>¿Cuándo se reserva? ¿Cuándo se cancela?</strong> 
Estas respuestas revelan patrones críticos para la gestión hotelera.<br><br>

<strong>Hallazgo #2: El Patrón Temporal Alarmante.</strong> La anticipación (lead time) muestra una historia 
fascinante: mientras la mediana es de 69 días, encontramos reservas con hasta 2 años de anticipación. 
¿La correlación? Las reservas con más anticipación tienen mayor probabilidad de cancelación.
</div>
""", unsafe_allow_html=True)

# Evolución temporal
st.markdown("### 📅 Evolución Temporal: El Ritmo de las Cancelaciones")

if 'dia' in data_filtered.columns:
    df_time = data_filtered.dropna(subset=['dia']).copy()
    df_time['year_month'] = df_time['dia'].dt.to_period('M').astype(str)
    
    monthly = df_time.groupby(['year_month', 'hotel']).size().reset_index(name='reservas')
    
    fig_time_hotel = px.line(
        monthly,
        x='year_month',
        y='reservas',
        color='hotel',
        title='Reservas Mensuales por Tipo de Hotel',
        labels={'year_month': 'Mes', 'reservas': 'Número de Reservas', 'hotel': 'Hotel'},
        color_discrete_sequence=['#1f77b4', '#ff7f0e'],
        markers=True
    )
    fig_time_hotel.update_traces(line=dict(width=3), marker=dict(size=8))
    fig_time_hotel.update_layout(
        height=480, 
        hovermode='x unified',
        font=dict(size=13),
        title_font_size=18
    )
    fig_time_hotel.update_xaxes(tickangle=45)
    st.plotly_chart(fig_time_hotel, use_container_width=True, key="fig_time_hotel_ch3")

# Comparativa por temporada
st.markdown("### 🌤️ Estacionalidad: El Patrón Oculto")

if 'season' in data_filtered.columns:
    season_order = ['Primavera', 'Verano', 'Otoño', 'Invierno']
    season_cancellations = data_filtered.groupby(['season', 'is_canceled']).size().reset_index(name='count')
    season_cancellations['status'] = season_cancellations['is_canceled'].map({0: 'Completadas', 1: 'Canceladas'})
    
    season_cancellations['season'] = pd.Categorical(season_cancellations['season'], categories=season_order, ordered=True)
    season_cancellations = season_cancellations.sort_values('season')
    
    fig_season = px.bar(
        season_cancellations,
        x='season',
        y='count',
        color='status',
        barmode='group',
        title='Reservas por Temporada: Completadas vs Canceladas',
        labels={'season': 'Temporada', 'count': 'Número de Reservas', 'status': 'Estado'},
        color_discrete_map={'Completadas': '#2ca02c', 'Canceladas': '#d62728'}
    )
    fig_season.update_traces(marker_line_color='white', marker_line_width=2)
    fig_season.update_layout(
        height=480, 
        font=dict(size=13),
        title_font_size=18,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    st.plotly_chart(fig_season, use_container_width=True, key="fig_season_ch3")

st.markdown("""
<div class="insight-box">
<strong>💡 Insight Crítico:</strong> Los picos de cancelaciones coinciden con la temporada alta (verano). 
Mayor demanda = mayor flexibilidad percibida para cancelar. Es la paradoja del éxito: 
cuando más se llena el hotel, más cancelaciones recibe.
</div>
""", unsafe_allow_html=True)

# Lead Time - El Factor Predictivo
st.markdown("### ⏳ Lead Time: El Factor Predictivo Definitivo")

col1, col2 = st.columns([2, 1])

with col1:
    if 'lead_time_category' in data_filtered.columns:
        category_order = ['Mismo día', '1 semana', '1 mes', '3 meses', '6 meses', 'Más de 6 meses']
        
        lead_cancel = data_filtered.groupby('lead_time_category')['is_canceled'].agg(['sum', 'count']).reset_index()
        lead_cancel['cancel_rate'] = (lead_cancel['sum'] / lead_cancel['count'] * 100).round(2)
        
        lead_cancel['lead_time_category'] = pd.Categorical(lead_cancel['lead_time_category'], categories=category_order, ordered=True)
        lead_cancel = lead_cancel.sort_values('lead_time_category')
        
        fig_lead = px.bar(
            lead_cancel,
            x='lead_time_category',
            y='cancel_rate',
            title='Tasa de Cancelación según Anticipación',
            labels={'lead_time_category': 'Lead Time', 'cancel_rate': 'Tasa Cancelación (%)'},
            color='cancel_rate',
            color_continuous_scale='Reds'
        )
        fig_lead.update_traces(
            text=lead_cancel['cancel_rate'],
            texttemplate='%{text:.1f}%',
            textposition='outside',
            marker_line_color='white',
            marker_line_width=2
        )
        fig_lead.update_layout(height=480, showlegend=False, font=dict(size=13), title_font_size=18)
        fig_lead.update_xaxes(tickangle=45)
        st.plotly_chart(fig_lead, use_container_width=True, key="fig_lead_ch3")

with col2:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    ### 🎯 El Patrón Revelador
    
    **A mayor anticipación, mayor riesgo:**
    
    - **< 1 mes**: Compromiso alto ✅
    - **1-3 meses**: Zona de riesgo medio ⚠️
    - **> 6 meses**: Alto riesgo ❌
    
    **¿Por qué?**
    
    Más tiempo = más oportunidades para:
    - Cambiar de planes
    - Encontrar mejores ofertas
    - Perder compromiso emocional
    """)

# Lead Time vs Duración
st.markdown("### 🔄 Lead Time vs Duración de Estancia")

if 'lead_time_category' in data_filtered.columns and 'total_nights' in data_filtered.columns:
    category_order = ['Mismo día', '1 semana', '1 mes', '3 meses', '6 meses', 'Más de 6 meses']
    
    lead_nights = data_filtered[data_filtered['total_nights'] <= 20].copy()
    lead_nights_avg = lead_nights.groupby('lead_time_category')['total_nights'].agg(['mean', 'median', 'count']).reset_index()
    lead_nights_avg.columns = ['lead_time_category', 'promedio_noches', 'mediana_noches', 'num_reservas']
    
    lead_nights_avg['lead_time_category'] = pd.Categorical(lead_nights_avg['lead_time_category'], categories=category_order, ordered=True)
    lead_nights_avg = lead_nights_avg.sort_values('lead_time_category')
    
    fig_lead_nights = go.Figure()
    
    fig_lead_nights.add_trace(go.Bar(
        name='Promedio de Noches',
        x=lead_nights_avg['lead_time_category'],
        y=lead_nights_avg['promedio_noches'],
        marker_color='#1f77b4',
        marker_line_color='white',
        marker_line_width=2,
        text=lead_nights_avg['promedio_noches'].round(1),
        texttemplate='%{text:.1f}',
        textposition='outside'
    ))
    
    fig_lead_nights.add_trace(go.Scatter(
        name='Mediana de Noches',
        x=lead_nights_avg['lead_time_category'],
        y=lead_nights_avg['mediana_noches'],
        mode='lines+markers',
        marker=dict(color='#ff7f0e', size=12, line=dict(color='white', width=2)),
        line=dict(color='#ff7f0e', width=4)
    ))
    
    fig_lead_nights.update_layout(
        title='¿Reservas anticipadas = Estancias más largas?',
        xaxis_title='Categoría de Lead Time',
        yaxis_title='Número de Noches',
        height=480,
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        font=dict(size=13),
        title_font_size=18
    )
    fig_lead_nights.update_xaxes(tickangle=45)
    
    st.plotly_chart(fig_lead_nights, use_container_width=True, key="fig_lead_nights_ch3")
    
    st.markdown("""
    <div class="insight-box">
        <strong>💡 Patrón Interesante:</strong> Las reservas con mayor anticipación tienden a tener 
        estancias ligeramente más largas. Los clientes que planifican con antelación buscan experiencias 
        más prolongadas, pero también son los que más cancelan. Es el dilema del hotelero.
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================
# CAPÍTULO 4: CANALES Y COMPORTAMIENTO
# ============================================
st.markdown('<div class="chapter-title">📱 Capítulo 4: Los Canales y el Comportamiento</div>', unsafe_allow_html=True)

st.markdown("""
<div class="chapter-intro">
¿Cómo llegan los clientes al hotel? ¿Quiénes son? La distribución y tipología de clientes 
revelan dependencias críticas del negocio.<br><br>

<strong>Hallazgo #3: La Dependencia Tecnológica.</strong> El 82% de las reservas llegan a través de 
agencias de viajes online (OTAs). Esta intermediación digital amplifica el alcance de mercado, 
pero también facilita las cancelaciones con un simple clic.
</div>
""", unsafe_allow_html=True)

st.markdown("### 📊 Canales de Distribución")

col1, col2 = st.columns(2)

with col1:
    if 'distribution_channel' in data_filtered.columns:
        channel_dist = data_filtered.groupby('distribution_channel').size().reset_index(name='count')
        channel_dist = channel_dist.sort_values('count', ascending=False)
        
        fig_channel = px.bar(
            channel_dist,
            x='count',
            y='distribution_channel',
            orientation='h',
            title='Reservas por Canal de Distribución',
            labels={'distribution_channel': 'Canal', 'count': 'Reservas'},
            color='count',
            color_continuous_scale='Blues'
        )
        fig_channel.update_traces(
            text=channel_dist['count'],
            texttemplate='%{text:,}',
            textposition='outside',
            marker_line_color='white',
            marker_line_width=2
        )
        fig_channel.update_layout(height=420, showlegend=False, font=dict(size=13), title_font_size=18)
        st.plotly_chart(fig_channel, use_container_width=True, key="fig_channel_ch4")

with col2:
    if 'market_segment' in data_filtered.columns:
        market_dist = data_filtered.groupby('market_segment').size().reset_index(name='count')
        market_dist = market_dist.sort_values('count', ascending=False)
        
        fig_market_dist = px.pie(
            market_dist,
            values='count',
            names='market_segment',
            title='Segmento de Mercado',
            hole=0.45
        )
        fig_market_dist.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            marker=dict(line=dict(color='white', width=3))
        )
        fig_market_dist.update_layout(height=420, font=dict(size=13), title_font_size=18)
        st.plotly_chart(fig_market_dist, use_container_width=True, key="fig_market_dist_ch4")

st.markdown("""
<div class="insight-box">
    <strong>💡 El Doble Filo Digital:</strong> La dependencia de OTAs supera el 82% de las reservas. 
    Amplifica alcance pero facilita cancelaciones. Es la trampa de la conveniencia moderna.
</div>
""", unsafe_allow_html=True)

st.markdown("### 🔄 Crisis de Fidelización")

col1, col2 = st.columns(2)

with col1:
    if 'is_repeated_guest' in data_filtered.columns:
        repeated_dist = data_filtered.groupby('is_repeated_guest').size().reset_index(name='count')
        repeated_dist['type'] = repeated_dist['is_repeated_guest'].map({0: 'Nuevos', 1: 'Repetidos'})
        
        fig_repeated = px.pie(
            repeated_dist,
            values='count',
            names='type',
            title='Huéspedes: Nuevos vs Repetidos',
            color_discrete_sequence=['#ff7f0e', '#2ca02c'],
            hole=0.45
        )
        fig_repeated.update_traces(
            textposition='inside', 
            textinfo='percent+label', 
            textfont_size=18,
            marker=dict(line=dict(color='white', width=3))
        )
        fig_repeated.update_layout(height=420, font=dict(size=14), title_font_size=18)
        st.plotly_chart(fig_repeated, use_container_width=True, key="fig_repeated_ch4")

with col2:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("""
    ### 📉 El Talón de Aquiles
    
    **Solo el 3% son huéspedes repetidos**
    
    Esto significa:
    - 💸 **97% clientes nuevos** cada vez
    - 📈 Alto costo de adquisición constante
    - ⚠️ Sin ventaja de lealtad
    - 🎯 Mayor vulnerabilidad a competencia
    
    **Oportunidad**: Programas de fidelización urgentes
    """)

st.markdown("""
<div class="insight-box">
    <strong>💡 Hallazgo #4: Baja Fidelización.</strong> Solo el 3% son huéspedes repetidos. 
    Esto implica costos constantes de adquisición y vulnerabilidad ante la competencia. 
    Sin ventaja de lealtad, cada reserva es una batalla nueva.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================
# CAPÍTULO 5: CONCLUSIONES Y ACCIÓN
# ============================================
st.markdown('<div class="chapter-title">🎯 Capítulo 5: De los Datos a la Acción</div>', unsafe_allow_html=True)

st.markdown("""
<div class="chapter-intro">
Hemos descubierto los patrones. Ahora, <strong>transformemos datos en estrategia</strong>. 
Basándonos en los 4 pilares identificados, proponemos un plan de acción con impacto medible 
que puede reducir las cancelaciones del 37% actual a menos del 27% en 12 meses.
</div>
""", unsafe_allow_html=True)

st.markdown("### 🛡️ Estrategias de Mitigación Accionables")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="recommendation-box">
    <span class="section-number">1</span><strong>Política de Depósitos Escalonada</strong><br><br>
    • Lead time &lt; 30 días: <strong>Sin depósito</strong> (confianza alta)<br>
    • Lead time 30-90 días: <strong>Depósito 10%</strong> (riesgo medio)<br>
    • Lead time &gt; 90 días: <strong>Depósito 15-20%</strong> (riesgo alto)<br><br>
    <em>📊 Impacto esperado: Reducción 12-15% en cancelaciones anticipadas</em>
    </div>
    
    <div class="recommendation-box">
    <span class="section-number">2</span><strong>Incentivos por Booking Directo</strong><br><br>
    • Descuento <strong>5-10%</strong> en canal directo<br>
    • Programa de fidelización con <strong>puntos acumulables</strong><br>
    • Upgrades gratuitos para <strong>clientes recurrentes</strong><br><br>
    <em>📊 Impacto esperado: Reducir dependencia OTAs del 82% al 65%</em>
    </div>
    
    <div class="recommendation-box">
    <span class="section-number">3</span><strong>Precios Dinámicos Anti-Cancelación</strong><br><br>
    • Tarifas <strong>flexibles</strong> para reservas &lt; 30 días<br>
    • Penalización <strong>gradual</strong> por cancelación según lead time<br>
    • Opciones de <strong>reprogramación sin costo</strong> (1 vez)<br><br>
    <em>📊 Impacto esperado: Reducción 8-10% manteniendo flexibilidad</em>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("#### 📊 Calculadora de Impacto Financiero")
    
    total_reservas = len(data_filtered)
    canceladas = data_filtered['is_canceled'].sum()
    tasa_actual = (canceladas / total_reservas * 100)
    
    reduccion_objetivo = st.slider(
        "**Reducción objetivo en puntos porcentuales**",
        min_value=5,
        max_value=20,
        value=10,
        step=1,
        help="Desliza para ver el impacto financiero de diferentes reducciones",
        key="reduccion_slider"
    )
    
    nueva_tasa = tasa_actual - reduccion_objetivo
    reservas_salvadas = int(total_reservas * (reduccion_objetivo / 100))
    avg_adr = data_filtered["adr"].mean()
    noches_promedio = data_filtered["total_nights"].mean() if "total_nights" in data_filtered.columns else 2.5
    ingresos_recuperados = reservas_salvadas * avg_adr * noches_promedio
    
    st.markdown(f"""
    <div style="background: white; padding: 30px; border-radius: 15px; box-shadow: 0 8px 20px rgba(0,0,0,0.15);">
    <h4 style="color: #1f77b4; margin-top: 0;">💰 Proyección de Impacto</h4>
    <table style="width: 100%; font-size: 16px; line-height: 2.5;">
    <tr>
        <td><strong>Tasa actual:</strong></td>
        <td style="text-align: right; font-size: 20px;">{tasa_actual:.1f}%</td>
    </tr>
    <tr>
        <td><strong>Tasa objetivo:</strong></td>
        <td style="text-align: right; font-size: 20px; color: #28a745;"><strong>{nueva_tasa:.1f}%</strong></td>
    </tr>
    <tr>
        <td><strong>Reservas salvadas:</strong></td>
        <td style="text-align: right; font-size: 20px;">{reservas_salvadas:,}</td>
    </tr>
    <tr>
        <td><strong>Noches promedio:</strong></td>
        <td style="text-align: right; font-size: 20px;">{noches_promedio:.1f}</td>
    </tr>
    <tr style="border-top: 3px solid #1f77b4;">
        <td style="padding-top: 15px;"><strong>💵 Ingresos recuperados:</strong></td>
        <td style="text-align: right; color: #28a745; font-size: 28px; font-weight: 900; padding-top: 15px;">
            €{ingresos_recuperados:,.0f}
        </td>
    </tr>
    </table>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if reduccion_objetivo >= 15:
        st.success("🎯 **Meta ambiciosa pero alcanzable** con implementación completa de las 3 estrategias")
    elif reduccion_objetivo >= 10:
        st.info("✅ **Meta realista** aplicando estrategias de depósito y precios dinámicos")
    else:
        st.warning("⚠️ **Meta conservadora**. Considera ser más agresivo en la implementación")

# Impacto de políticas de depósito
st.markdown("### 💳 Evidencia: Impacto de la Política de Depósito")

if 'deposit_type' in data_filtered.columns:
    deposit_cancel = data_filtered.groupby('deposit_type').agg({
        'is_canceled': ['sum', 'count']
    }).reset_index()
    deposit_cancel.columns = ['deposit_type', 'canceled', 'total']
    deposit_cancel['cancel_rate'] = (deposit_cancel['canceled'] / deposit_cancel['total'] * 100).round(2)
    deposit_cancel['completed_rate'] = 100 - deposit_cancel['cancel_rate']
    
    fig_deposit = go.Figure()
    fig_deposit.add_trace(go.Bar(
        name='✅ Completadas',
        x=deposit_cancel['deposit_type'],
        y=deposit_cancel['completed_rate'],
        marker_color='#2ca02c',
        marker_line_color='white',
        marker_line_width=2,
        text=deposit_cancel['completed_rate'].round(1),
        texttemplate='%{text}%',
        textposition='inside',
        textfont=dict(size=14, color='white')
    ))
    fig_deposit.add_trace(go.Bar(
        name='❌ Canceladas',
        x=deposit_cancel['deposit_type'],
        y=deposit_cancel['cancel_rate'],
        marker_color='#d62728',
        marker_line_color='white',
        marker_line_width=2,
        text=deposit_cancel['cancel_rate'].round(1),
        texttemplate='%{text}%',
        textposition='inside',
        textfont=dict(size=14, color='white')
    ))
    
    fig_deposit.update_layout(
        title='Depósitos: La Diferencia es Abismal',
        xaxis_title='Tipo de Depósito',
        yaxis_title='Porcentaje (%)',
        barmode='stack',
        height=480,
        font=dict(size=13),
        title_font_size=18,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    st.plotly_chart(fig_deposit, use_container_width=True, key="fig_deposit_ch5")

st.markdown("""
<div class="insight-box">
    <strong>💡 La Evidencia es Clara:</strong> Las reservas sin depósito tienen tasas de cancelación 
    significativamente mayores. La implementación de depósitos escalonados puede reducir cancelaciones 
    sin impactar negativamente la conversión. Es el equilibrio perfecto entre flexibilidad y compromiso.
</div>
""", unsafe_allow_html=True)

# Resumen Ejecutivo Final
st.markdown("### 🎯 Resumen Ejecutivo: Los 4 Pilares del Problema")

st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px; border-radius: 20px; color: white; box-shadow: 0 15px 35px rgba(0,0,0,0.3);">
<h3 style="color: white; margin-top: 0; text-align: center; font-size: 32px;">📚 La Historia Completa en 4 Actos</h3>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin-top: 30px;">
    <div class="pillar-card">
        <div style="font-size: 48px; margin-bottom: 15px;">⏰</div>
        <strong style="font-size: 20px;">Factor Temporal</strong><br><br>
        Lead time &gt; 180 días = Alto riesgo<br>
        Temporada alta = Más cancelaciones<br>
        <strong>Solución:</strong> Depósitos escalonados
    </div>
    <div class="pillar-card">
        <div style="font-size: 48px; margin-bottom: 15px;">📱</div>
        <strong style="font-size: 20px;">Dependencia Digital</strong><br><br>
        82% vía OTAs<br>
        Facilita cancelaciones con 1 clic<br>
        <strong>Solución:</strong> Incentivos canal directo
    </div>
    <div class="pillar-card">
        <div style="font-size: 48px; margin-bottom: 15px;">💰</div>
        <strong style="font-size: 20px;">Políticas Flexibles</strong><br><br>
        87% sin depósito<br>
        Cero penalización = Cero compromiso<br>
        <strong>Solución:</strong> Precios dinámicos
    </div>
    <div class="pillar-card">
        <div style="font-size: 48px; margin-bottom: 15px;">🔄</div>
        <strong style="font-size: 20px;">Baja Fidelización</strong><br><br>
        97% clientes nuevos<br>
        Sin ventaja de lealtad<br>
        <strong>Solución:</strong> Programa de fidelización
    </div>
</div>

<div style="margin-top: 40px; padding: 30px; background: rgba(255,255,255,0.95); border-radius: 15px; color: #333; box-shadow: 0 5px 15px rgba(0,0,0,0.2);">
    <strong style="color: #1f77b4; font-size: 22px;">🚀 Próximos Pasos Recomendados</strong><br><br>
    <div style="font-size: 16px; line-height: 2;">
    <strong>1.</strong> <strong>Implementar depósitos escalonados</strong> según lead time en próximo trimestre (Q1 2024)<br>
    <strong>2.</strong> <strong>Lanzar campaña de booking directo</strong> con descuentos del 7% y programa de puntos<br>
    <strong>3.</strong> <strong>Crear programa de fidelización</strong> para convertir el 3% actual en 15% en 12 meses<br>
    <strong>4.</strong> <strong>Monitorear KPIs semanalmente</strong>: tasa de cancelación, ADR, % canal directo, ROI
    </div>
</div>

<div style="text-align: center; margin-top: 30px; font-size: 18px; font-style: italic;">
    "Los datos revelan problemas. Las estrategias crean soluciones. La acción genera resultados."
</div>
</div>
""", unsafe_allow_html=True)

# ============================================
# FOOTER - CIERRE NARRATIVO
# ============================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 40px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 15px; margin-top: 50px;">
    <h3 style="color: #1f77b4; margin-top: 0;">🎬 Fin del Viaje</h3>
    <p style="font-size: 18px; color: #555; line-height: 1.8; max-width: 800px; margin: 20px auto;">
    Hemos transformado <strong>119,390 reservas</strong> en una narrativa comprensible. 
    Hemos convertido datos complejos en <strong>estrategias accionables</strong>. 
    Y hemos demostrado que cada cancelación cuenta una historia.<br><br>
    <strong>Esta no es solo una visualización de datos.</strong><br>
    Es una conversación guiada donde tú eres el protagonista de tu descubrimiento.
    </p>
    
    <div style="margin-top: 30px; padding: 20px; background: white; border-radius: 10px; display: inline-block;">
        <p style="margin: 0; color: #666;"><strong>Dashboard creado para PEC 3 - Visualización de Datos</strong></p>
        <p style="margin: 5px 0; color: #888;">Máster Universitario en Ciencia de Datos | UOC</p>
        <p style="margin: 5px 0; color: #888;">Dataset: Hotel Bookings (119,390 reservas | 2015-2017 | Portugal)</p>
        <p style="margin: 15px 0 0 0; color: #1f77b4; font-weight: 600;">
            Herramientas: Streamlit 🎈 | Plotly 📊 | Pandas 🐼
        </p>
    </div>
</div>
""", unsafe_allow_html=True)