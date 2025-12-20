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

# CSS personalizado
st.markdown("""
<style>
    .big-title {
        font-size: 56px;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin: 30px 0 10px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .subtitle {
        font-size: 24px;
        text-align: center;
        color: #666;
        margin-bottom: 40px;
        font-style: italic;
    }
    .chapter-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        margin: 30px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .chapter-title {
        font-size: 32px;
        font-weight: bold;
        color: white;
        margin-bottom: 15px;
    }
    .chapter-content {
        font-size: 18px;
        color: #f0f0f0;
        line-height: 1.6;
    }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 48px;
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-label {
        font-size: 16px;
        color: #666;
        margin-top: 10px;
    }
    .insight-box {
        background: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 15px;
        margin: 20px 0;
        border-radius: 5px;
    }
    .recommendation-box {
        background: #d4edda;
        border-left: 5px solid #28a745;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Cargar datos
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "1. Datos" / "hotel_bookings.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    if 'dia' in df.columns:
        df['dia'] = pd.to_datetime(df['dia'])
    return df

data = load_data()

# ============================================
# SIDEBAR - FILTROS
# ============================================
st.sidebar.image("https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/hotel.svg", width=100)
st.sidebar.title("🎯 Filtros de Exploración")

# Filtro de hotel
hotel_options = ["Todos"] + list(data["hotel"].unique())
selected_hotel = st.sidebar.selectbox("Tipo de Hotel", hotel_options)

# Filtro de año
min_year = int(data["arrival_date_year"].min())
max_year = int(data["arrival_date_year"].max())
year_range = st.sidebar.slider(
    "Año de llegada",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
    step=1
)

# Filtro de tipo de cliente
if 'customer_type' in data.columns:
    customer_options = ["Todos"] + list(data["customer_type"].unique())
    selected_customer = st.sidebar.selectbox("Tipo de Cliente", customer_options)
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
st.sidebar.info(f"📊 **Registros filtrados:** {len(data_filtered):,}")

# ============================================
# CAPÍTULO 1: BIENVENIDA AL PROBLEMA
# ============================================
st.markdown('<div class="big-title">🏨 El Enigma de las Cancelaciones</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Un Viaje por los Datos Hoteleros de Portugal (2015-2017)</div>', unsafe_allow_html=True)

st.markdown("---")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    cancelation_rate = data_filtered["is_canceled"].mean() * 100
    st.markdown(f"""
    <div style="text-align: center; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
        <div style="font-size: 80px; font-weight: bold; color: white;">{cancelation_rate:.1f}%</div>
        <div style="font-size: 28px; color: #f0f0f0; margin-top: 10px;">DE CANCELACIONES</div>
        <div style="font-size: 18px; color: #e0e0e0; margin-top: 20px; font-style: italic;">
        4 de cada 10 clientes no llegan al hotel
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; font-size: 18px; color: #555; max-width: 900px; margin: 0 auto; line-height: 1.8;">
Imagina que eres director de un hotel en Lisboa. Cada mañana, al revisar las reservas del día, 
descubres que 4 de cada 10 clientes han cancelado. <strong>¿Frustración? Absolutamente.</strong> 
Pero, ¿y si pudiéramos entender el porqué?<br><br>
Esta visualización explora <strong>119,390 reservas hoteleras</strong> en dos hoteles portugueses 
para desentrañar los patrones ocultos detrás de las cancelaciones.
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ============================================
# CAPÍTULO 2: RADIOGRAFÍA DEL DATASET
# ============================================
st.markdown("""
<div class="chapter-card">
    <div class="chapter-title">📊 CAPÍTULO 1: Radiografía del Dataset</div>
    <div class="chapter-content">
    Comencemos por entender la magnitud de los datos. Este análisis abarca tres años de 
    operaciones hoteleras con información detallada de cada reserva.
    </div>
</div>
""", unsafe_allow_html=True)

# Métricas principales
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
        <div class="metric-value" style="color: #dc3545;">{canceled:,}</div>
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
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color: #ff7f0e;">{avg_lead:.0f}</div>
        <div class="metric-label">Lead Time (días)</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Distribución por hotel
col1, col2 = st.columns(2)

with col1:
    hotel_dist = data_filtered.groupby("hotel").size().reset_index(name="count")
    fig_hotel = px.pie(
        hotel_dist,
        values="count",
        names="hotel",
        title="Distribución por Tipo de Hotel",
        color_discrete_sequence=["#1f77b4", "#ff7f0e"],
        hole=0.4
    )
    fig_hotel.update_traces(textposition='inside', textinfo='percent+label')
    fig_hotel.update_layout(height=400)
    st.plotly_chart(fig_hotel, use_container_width=True)

with col2:
    # Estado de reservas
    status_map = {1: "Cancelada", 0: "Completada"}
    data_filtered_status = data_filtered.copy()
    data_filtered_status["status"] = data_filtered_status["is_canceled"].map(status_map)
    
    status_dist = data_filtered_status.groupby("status").size().reset_index(name="count")
    fig_status = px.pie(
        status_dist,
        values="count",
        names="status",
        title="Estado de las Reservas",
        color_discrete_sequence=["#2ca02c", "#d62728"],
        hole=0.4
    )
    fig_status.update_traces(textposition='inside', textinfo='percent+label')
    fig_status.update_layout(height=400)
    st.plotly_chart(fig_status, use_container_width=True)

# ============================================
# CAPÍTULO 3: EL FACTOR TIEMPO
# ============================================
st.markdown("""
<div class="chapter-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
    <div class="chapter-title">⏰ CAPÍTULO 2: El Factor Tiempo</div>
    <div class="chapter-content">
    El tiempo es el protagonista silencioso de las cancelaciones. ¿Cuándo se reserva? 
    ¿Cuándo se cancela? Estas respuestas revelan patrones críticos.
    </div>
</div>
""", unsafe_allow_html=True)

# Evolución temporal de cancelaciones
if 'dia' in data_filtered.columns:
    df_time = data_filtered.copy()
    df_time['year_month'] = df_time['dia'].dt.to_period('M').astype(str)
    
    monthly_cancellations = df_time.groupby(['year_month', 'is_canceled']).size().reset_index(name='count')
    monthly_cancellations['status'] = monthly_cancellations['is_canceled'].map({0: 'Completadas', 1: 'Canceladas'})
    
    fig_time = px.line(
        monthly_cancellations,
        x='year_month',
        y='count',
        color='status',
        title='Evolución Mensual de Reservas: Completadas vs Canceladas',
        labels={'year_month': 'Mes', 'count': 'Número de Reservas', 'status': 'Estado'},
        color_discrete_map={'Completadas': '#2ca02c', 'Canceladas': '#d62728'}
    )
    fig_time.update_layout(height=450, hovermode='x unified')
    st.plotly_chart(fig_time, use_container_width=True)

st.markdown("""
<div class="insight-box">
    <strong>💡 Insight Clave:</strong> Los picos de cancelaciones coinciden con la temporada alta. 
    Mayor demanda = mayor flexibilidad percibida para cancelar.
</div>
""", unsafe_allow_html=True)

# Lead Time vs Cancelaciones
col1, col2 = st.columns([2, 1])

with col1:
    # Crear bins de lead time
    data_lead = data_filtered.copy()
    data_lead['lead_time_bin'] = pd.cut(
        data_lead['lead_time'],
        bins=[0, 30, 60, 90, 180, 365, 800],
        labels=['0-30 días', '31-60 días', '61-90 días', '91-180 días', '181-365 días', '>365 días']
    )
    
    lead_cancel = data_lead.groupby('lead_time_bin')['is_canceled'].agg(['sum', 'count']).reset_index()
    lead_cancel['cancel_rate'] = (lead_cancel['sum'] / lead_cancel['count'] * 100).round(2)
    
    fig_lead = px.bar(
        lead_cancel,
        x='lead_time_bin',
        y='cancel_rate',
        title='Tasa de Cancelación según Anticipación de la Reserva',
        labels={'lead_time_bin': 'Anticipación (Lead Time)', 'cancel_rate': 'Tasa de Cancelación (%)'},
        color='cancel_rate',
        color_continuous_scale='Reds'
    )
    fig_lead.update_layout(height=450, showlegend=False)
    st.plotly_chart(fig_lead, use_container_width=True)

with col2:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("""
    ### 🎯 Patrón Revelador
    
    **A mayor anticipación, mayor riesgo:**
    
    - Reservas de último momento (< 30 días): Menor cancelación
    - Reservas anticipadas (> 180 días): Mayor cancelación
    
    **¿Por qué?** Más tiempo = más cambios en planes personales
    """)

# ============================================
# CAPÍTULO 4: LOS CANALES Y EL COMPORTAMIENTO
# ============================================
st.markdown("""
<div class="chapter-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
    <div class="chapter-title">📱 CAPÍTULO 3: Los Canales y el Comportamiento</div>
    <div class="chapter-content">
    ¿Cómo llegan los clientes al hotel? ¿Quiénes son? La distribución y tipología de clientes 
    revelan dependencias críticas del negocio.
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Canal de distribución
    if 'distribution_channel' in data_filtered.columns:
        channel_dist = data_filtered.groupby('distribution_channel').size().reset_index(name='count')
        channel_dist = channel_dist.sort_values('count', ascending=False)
        
        fig_channel = px.bar(
            channel_dist,
            x='count',
            y='distribution_channel',
            orientation='h',
            title='Reservas por Canal de Distribución',
            labels={'distribution_channel': 'Canal', 'count': 'Número de Reservas'},
            color='count',
            color_continuous_scale='Blues'
        )
        fig_channel.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_channel, use_container_width=True)

with col2:
    # Tipo de cliente
    if 'customer_type' in data_filtered.columns:
        customer_dist = data_filtered.groupby('customer_type').size().reset_index(name='count')
        
        fig_customer = px.pie(
            customer_dist,
            values='count',
            names='customer_type',
            title='Distribución por Tipo de Cliente',
            hole=0.4
        )
        fig_customer.update_layout(height=400)
        st.plotly_chart(fig_customer, use_container_width=True)

# Segmento de mercado
if 'market_segment' in data_filtered.columns:
    market_cancel = data_filtered.groupby('market_segment').agg({
        'is_canceled': ['sum', 'count']
    }).reset_index()
    market_cancel.columns = ['market_segment', 'canceled', 'total']
    market_cancel['cancel_rate'] = (market_cancel['canceled'] / market_cancel['total'] * 100).round(2)
    market_cancel = market_cancel.sort_values('cancel_rate', ascending=False)
    
    fig_market = px.bar(
        market_cancel,
        x='market_segment',
        y='cancel_rate',
        title='Tasa de Cancelación por Segmento de Mercado',
        labels={'market_segment': 'Segmento de Mercado', 'cancel_rate': 'Tasa de Cancelación (%)'},
        color='cancel_rate',
        color_continuous_scale='Oranges'
    )
    fig_market.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_market, use_container_width=True)

st.markdown("""
<div class="insight-box">
    <strong>💡 Insight Clave:</strong> La dependencia de OTAs (Agencias Online) supera el 80%. 
    Esta intermediación facilita las cancelaciones pero amplifica el alcance de mercado.
</div>
""", unsafe_allow_html=True)

# ============================================
# CAPÍTULO 5: POLÍTICAS Y PRECIOS
# ============================================
st.markdown("""
<div class="chapter-card" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
    <div class="chapter-title">💰 CAPÍTULO 4: Políticas y Precios</div>
    <div class="chapter-content">
    Las políticas de depósito y pricing tienen un impacto directo en el comportamiento 
    de cancelación. Exploremos esta relación crítica.
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Política de depósito vs cancelaciones
    if 'deposit_type' in data_filtered.columns:
        deposit_cancel = data_filtered.groupby('deposit_type').agg({
            'is_canceled': ['sum', 'count']
        }).reset_index()
        deposit_cancel.columns = ['deposit_type', 'canceled', 'total']
        deposit_cancel['cancel_rate'] = (deposit_cancel['canceled'] / deposit_cancel['total'] * 100).round(2)
        deposit_cancel['completed_rate'] = 100 - deposit_cancel['cancel_rate']
        
        fig_deposit = go.Figure()
        fig_deposit.add_trace(go.Bar(
            name='Completadas',
            x=deposit_cancel['deposit_type'],
            y=deposit_cancel['completed_rate'],
            marker_color='#2ca02c'
        ))
        fig_deposit.add_trace(go.Bar(
            name='Canceladas',
            x=deposit_cancel['deposit_type'],
            y=deposit_cancel['cancel_rate'],
            marker_color='#d62728'
        ))
        
        fig_deposit.update_layout(
            title='Impacto de la Política de Depósito',
            xaxis_title='Tipo de Depósito',
            yaxis_title='Porcentaje (%)',
            barmode='stack',
            height=400
        )
        st.plotly_chart(fig_deposit, use_container_width=True)

with col2:
    # ADR vs Cancelaciones
    data_adr = data_filtered[data_filtered['adr'] > 0].copy()
    data_adr['adr_bin'] = pd.cut(
        data_adr['adr'],
        bins=[0, 50, 100, 150, 200, 500],
        labels=['€0-50', '€51-100', '€101-150', '€151-200', '>€200']
    )
    
    adr_cancel = data_adr.groupby('adr_bin')['is_canceled'].agg(['sum', 'count']).reset_index()
    adr_cancel['cancel_rate'] = (adr_cancel['sum'] / adr_cancel['count'] * 100).round(2)
    
    fig_adr = px.line(
        adr_cancel,
        x='adr_bin',
        y='cancel_rate',
        title='Tasa de Cancelación según Rango de Precio (ADR)',
        labels={'adr_bin': 'Rango de Precio por Noche', 'cancel_rate': 'Tasa de Cancelación (%)'},
        markers=True
    )
    fig_adr.update_traces(line_color='#ff7f0e', line_width=3, marker_size=10)
    fig_adr.update_layout(height=400)
    st.plotly_chart(fig_adr, use_container_width=True)

st.markdown("""
<div class="insight-box">
    <strong>💡 Insight Clave:</strong> El 87% de reservas sin depósito correlaciona directamente 
    con la alta tasa de cancelación. Flexibilidad = Riesgo.
</div>
""", unsafe_allow_html=True)

# ============================================
# CAPÍTULO 6: CONCLUSIONES ACCIONABLES
# ============================================
st.markdown("""
<div class="chapter-card" style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);">
    <div class="chapter-title">🎯 CAPÍTULO 5: Conclusiones Accionables</div>
    <div class="chapter-content">
    De los datos a la acción: estrategias concretas para reducir cancelaciones y optimizar la rentabilidad.
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🛡️ Estrategias de Mitigación
    
    <div class="recommendation-box">
    <strong>1. Política de Depósitos Escalonada</strong><br>
    Implementar depósitos parciales (10-20%) para reservas con lead time > 90 días
    </div>
    
    <div class="recommendation-box">
    <strong>2. Incentivos por Booking Directo</strong><br>
    Reducir dependencia de OTAs ofreciendo 5-10% descuento en canal directo
    </div>
    
    <div class="recommendation-box">
    <strong>3. Precios Dinámicos Anti-Cancelación</strong><br>
    Tarifas más flexibles para reservas de último momento (< 30 días)
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    ### 📊 Impacto Potencial
    """)
    
    # Cálculo de impacto
    total_reservas = len(data_filtered)
    canceladas = data_filtered['is_canceled'].sum()
    tasa_actual = (canceladas / total_reservas * 100)
    
    reduccion_objetivo = 10  # 10 puntos porcentuales
    nueva_tasa = tasa_actual - reduccion_objetivo
    reservas_salvadas = int(total_reservas * (reduccion_objetivo / 100))
    ingresos_recuperados = reservas_salvadas * avg_adr * 2.5  # asumiendo 2.5 noches promedio
    
    st.markdown(f"""
    <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    <h4 style="color: #1f77b4;">Reducción objetivo: {reduccion_objetivo} puntos porcentuales</h4>
    <ul style="font-size: 16px; line-height: 2;">
        <li><strong>Tasa actual:</strong> {tasa_actual:.1f}%</li>
        <li><strong>Tasa objetivo:</strong> {nueva_tasa:.1f}%</li>
        <li><strong>Reservas salvadas:</strong> {reservas_salvadas:,}</li>
        <li><strong>Ingresos recuperados:</strong> €{ingresos_recuperados:,.0f}</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Top países con mayor cancelación
if 'country' in data_filtered.columns:
    st.markdown("### 🌍 Países con Mayor Tasa de Cancelación (Top 10)")
    
    top_countries = data_filtered['country'].value_counts().head(10).index
    country_data = data_filtered[data_filtered['country'].isin(top_countries)]
    
    country_cancel = country_data.groupby('country').agg({
        'is_canceled': ['sum', 'count']
    }).reset_index()
    country_cancel.columns = ['country', 'canceled', 'total']
    country_cancel['cancel_rate'] = (country_cancel['canceled'] / country_cancel['total'] * 100).round(2)
    country_cancel = country_cancel.sort_values('cancel_rate', ascending=False)
    
    fig_country = px.bar(
        country_cancel,
        y='country',
        x='cancel_rate',
        orientation='h',
        title='Tasa de Cancelación por País de Origen',
        labels={'country': 'País', 'cancel_rate': 'Tasa de Cancelación (%)'},
        color='cancel_rate',
        color_continuous_scale='RdYlGn_r'
    )
    fig_country.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig_country, use_container_width=True)

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; padding: 20px;">
    <p><strong>Dashboard creado para PEC 3 - Visualización de Datos</strong></p>
    <p>Máster Universitario en Ciencia de Datos | UOC</p>
    <p>Dataset: Hotel Bookings (119,390 reservas | 2015-2017 | Portugal)</p>
</div>
""", unsafe_allow_html=True)