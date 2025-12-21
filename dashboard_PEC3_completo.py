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
    .chapter-intro {
        font-size: 18px;
        color: #555;
        line-height: 1.8;
        padding: 20px;
        background: #f8f9fa;
        border-left: 5px solid #1f77b4;
        border-radius: 5px;
        margin: 20px 0;
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
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        padding: 10px 20px;
        background-color: #f0f2f6;
        border-radius: 10px 10px 0 0;
        font-size: 16px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
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
# SIDEBAR - FILTROS
# ============================================
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
# HEADER PRINCIPAL
# ============================================
st.markdown('<div class="big-title">🏨 El Enigma de las Cancelaciones</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Un Viaje por los Datos Hoteleros de Portugal (2015-2017)</div>', unsafe_allow_html=True)

st.markdown("---")

# ============================================
# TABS - CAPÍTULOS
# ============================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏁 Bienvenida al Problema",
    "📊 Radiografía del Dataset", 
    "⏰ El Factor Tiempo",
    "📱 Canales y Comportamiento",
    "🎯 Conclusiones"
])

# ============================================
# TAB 1: BIENVENIDA AL PROBLEMA
# ============================================
with tab1:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        cancelation_rate = data_filtered["is_canceled"].mean() * 100
        st.markdown(f"""
        <div style="text-align: center; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); margin-top: 30px;">
            <div style="font-size: 80px; font-weight: bold; color: white;">{cancelation_rate:.1f}%</div>
            <div style="font-size: 28px; color: #f0f0f0; margin-top: 10px;">DE CANCELACIONES</div>
            <div style="font-size: 18px; color: #e0e0e0; margin-top: 20px; font-style: italic;">
            4 de cada 10 clientes no llegan al hotel
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="chapter-intro">
    <strong>Imagina que eres director de un hotel en Lisboa.</strong> Cada mañana, al revisar las reservas del día, 
    descubres que 4 de cada 10 clientes han cancelado. <strong>¿Frustración? Absolutamente.</strong> 
    Pero, ¿y si pudiéramos entender el porqué?<br><br>
    
    He analizado <strong>119,390 reservas hoteleras</strong> realizadas entre 2015 y 2017 
    en dos hoteles portugueses: un <strong>City Hotel en Lisboa</strong> y un <strong>Resort Hotel en el Algarve</strong>. 
    <br><br>
    
    <strong>Nuestro objetivo:</strong> Desentrañar los patrones ocultos detrás de ese 37% de cancelaciones 
    que amenaza la rentabilidad del sector hotelero.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🔍 ¿Qué encontraremos?")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 20px; background: #e3f2fd; border-radius: 10px;">
            <div style="font-size: 40px;">⏰</div>
            <div style="font-size: 14px; margin-top: 10px; color: #555;">
            <strong>Patrones temporales</strong><br>
            ¿Cuándo se cancela más?
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 20px; background: #f3e5f5; border-radius: 10px;">
            <div style="font-size: 40px;">📱</div>
            <div style="font-size: 14px; margin-top: 10px; color: #555;">
            <strong>Canales críticos</strong><br>
            El rol de las OTAs
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 20px; background: #fff3e0; border-radius: 10px;">
            <div style="font-size: 40px;">💰</div>
            <div style="font-size: 14px; margin-top: 10px; color: #555;">
            <strong>Políticas flexibles</strong><br>
            Depósitos y riesgo
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align: center; padding: 20px; background: #e8f5e9; border-radius: 10px;">
            <div style="font-size: 40px;">🎯</div>
            <div style="font-size: 14px; margin-top: 10px; color: #555;">
            <strong>Soluciones</strong><br>
            Estrategias accionables
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# TAB 2: RADIOGRAFÍA DEL DATASET
# ============================================
with tab2:
    st.markdown("""
    <div class="chapter-intro">
    Comencemos por entender la magnitud de los datos. Este análisis abarca <strong>tres años de 
    operaciones hoteleras</strong> con información detallada de cada reserva: desde cuándo se realizó, 
    cuántas noches se quedó el huésped, qué tipo de habitación eligió, hasta si finalmente se presentó o canceló.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📈 Métricas Clave")
    
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
    
    # Gráficos de distribución
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏨 Distribución por Tipo de Hotel")
        hotel_dist = data_filtered.groupby("hotel").size().reset_index(name="count")
        fig_hotel = px.pie(
            hotel_dist,
            values="count",
            names="hotel",
            color_discrete_sequence=["#1f77b4", "#ff7f0e"],
            hole=0.4
        )
        fig_hotel.update_traces(textposition='inside', textinfo='percent+label', textfont_size=14)
        fig_hotel.update_layout(height=400, showlegend=True)
        st.plotly_chart(fig_hotel, use_container_width=True, key="fig_hotel_tab2")
    
    with col2:
        st.markdown("### 📋 Estado de las Reservas")
        status_map = {1: "Cancelada", 0: "Completada"}
        data_filtered_status = data_filtered.copy()
        data_filtered_status["status"] = data_filtered_status["is_canceled"].map(status_map)
        
        status_dist = data_filtered_status.groupby("status").size().reset_index(name="count")
        fig_status = px.pie(
            status_dist,
            values="count",
            names="status",
            color_discrete_sequence=["#2ca02c", "#d62728"],
            hole=0.4
        )
        fig_status.update_traces(textposition='inside', textinfo='percent+label', textfont_size=14)
        fig_status.update_layout(height=400, showlegend=True)
        st.plotly_chart(fig_status, use_container_width=True, key="fig_status_tab2")
    
    st.markdown("### 🏷️ Tipo de Comida y Clientes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'meal' in data_filtered.columns:
            meal_dist = data_filtered.groupby('meal').size().reset_index(name='count')
            meal_dist = meal_dist.sort_values('count', ascending=False)
            
            fig_meal = px.bar(
                meal_dist,
                x='meal',
                y='count',
                title='Distribución por Tipo de Comida',
                labels={'meal': 'Tipo de Comida', 'count': 'Número de Reservas'},
                color='count',
                color_continuous_scale='Blues'
            )
            fig_meal.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_meal, use_container_width=True, key="fig_meal_tab2")
    
    with col2:
        if 'customer_type' in data_filtered.columns:
            customer_dist = data_filtered.groupby('customer_type').size().reset_index(name='count')
            
            fig_customer = px.bar(
                customer_dist,
                x='customer_type',
                y='count',
                title='Distribución por Tipo de Cliente',
                labels={'customer_type': 'Tipo de Cliente', 'count': 'Número de Reservas'},
                color='count',
                color_continuous_scale='Purples'
            )
            fig_customer.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_customer, use_container_width=True, key="fig_customer_tab2")
    
    st.markdown("""
    <div class="insight-box">
        <strong>💡 Insight Clave:</strong> El City Hotel domina con el 66.5% de las reservas, 
        mientras que el 77% de los clientes eligen solo desayuno (BB). 
        El perfil típico: cliente individual (Transient) sin historial previo.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 👥 Composición de Huéspedes y Duración de Estancias")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'total_guests' in data_filtered.columns:
            # Distribución de huéspedes
            guests_dist = data_filtered['total_guests'].value_counts().sort_index().reset_index()
            guests_dist.columns = ['num_guests', 'count']
            guests_dist = guests_dist[guests_dist['num_guests'] <= 8]  # Limitar para mejor visualización
            
            fig_guests = px.bar(
                guests_dist,
                x='num_guests',
                y='count',
                title='Distribución por Número de Huéspedes',
                labels={'num_guests': 'Número de Huéspedes', 'count': 'Número de Reservas'},
                color='count',
                color_continuous_scale='Teal',
                text='count'
            )
            fig_guests.update_traces(texttemplate='%{text:,}', textposition='outside')
            fig_guests.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_guests, use_container_width=True, key="fig_guests_tab2")
    
    with col2:
        if 'total_nights' in data_filtered.columns:
            # Distribución de noches
            nights_dist = data_filtered[data_filtered['total_nights'] <= 14].copy()  # Limitar outliers
            nights_counts = nights_dist['total_nights'].value_counts().sort_index().reset_index()
            nights_counts.columns = ['num_nights', 'count']
            
            fig_nights = px.bar(
                nights_counts,
                x='num_nights',
                y='count',
                title='Distribución por Duración de Estancia (Noches)',
                labels={'num_nights': 'Número de Noches', 'count': 'Número de Reservas'},
                color='count',
                color_continuous_scale='Magma',
                text='count'
            )
            fig_nights.update_traces(texttemplate='%{text:,}', textposition='outside')
            fig_nights.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_nights, use_container_width=True, key="fig_nights_tab2")

# ============================================
# TAB 3: EL FACTOR TIEMPO
# ============================================
with tab3:
    st.markdown("""
    <div class="chapter-intro">
    El tiempo es el protagonista silencioso de las cancelaciones. <strong>¿Cuándo se reserva? 
    ¿Cuándo se cancela?</strong> Estas respuestas revelan patrones críticos para la gestión hotelera.
    <br><br>
    La anticipación (lead time) y la estacionalidad son dos factores que pueden predecir el comportamiento de cancelación.
    </div>
    """, unsafe_allow_html=True)
    
    # Evolución temporal de reservas por hotel
    st.markdown("### 📅 Evolución Temporal de Reservas por Hotel")
    
    if 'dia' in data_filtered.columns:
        df_time = data_filtered.dropna(subset=['dia']).copy()
        df_time['year_month'] = df_time['dia'].dt.to_period('M').astype(str)
        
        monthly = df_time.groupby(['year_month', 'hotel']).size().reset_index(name='reservas')
        
        fig_time_hotel = px.line(
            monthly,
            x='year_month',
            y='reservas',
            color='hotel',
            title='Evolución Temporal de Reservas por Tipo de Hotel',
            labels={'year_month': 'Mes', 'reservas': 'Número de Reservas', 'hotel': 'Tipo de Hotel'},
            color_discrete_sequence=['#1f77b4', '#ff7f0e'],
            markers=True
        )
        fig_time_hotel.update_layout(height=450, hovermode='x unified')
        fig_time_hotel.update_xaxes(tickangle=45)
        st.plotly_chart(fig_time_hotel, use_container_width=True, key="fig_time_hotel_tab3")
    
    # Evolución de cancelaciones por temporada
    st.markdown("### 📊 Comparativa por Temporada: Completadas vs Canceladas")
    
    if 'season' in data_filtered.columns:
        season_order = ['Primavera', 'Verano', 'Otoño', 'Invierno']
        season_cancellations = data_filtered.groupby(['season', 'is_canceled']).size().reset_index(name='count')
        season_cancellations['status'] = season_cancellations['is_canceled'].map({0: 'Completadas', 1: 'Canceladas'})
        
        # Ordenar por temporada
        season_cancellations['season'] = pd.Categorical(season_cancellations['season'], categories=season_order, ordered=True)
        season_cancellations = season_cancellations.sort_values('season')
        
        fig_season = px.bar(
            season_cancellations,
            x='season',
            y='count',
            color='status',
            barmode='group',
            title='Reservas Completadas vs Canceladas por Temporada',
            labels={'season': 'Temporada', 'count': 'Número de Reservas', 'status': 'Estado'},
            color_discrete_map={'Completadas': '#2ca02c', 'Canceladas': '#d62728'}
        )
        fig_season.update_layout(height=450)
        st.plotly_chart(fig_season, use_container_width=True, key="fig_season_tab3")
    
    st.markdown("""
    <div class="insight-box">
        <strong>💡 Insight Clave:</strong> Los picos de cancelaciones coinciden con la temporada alta (verano). 
        Mayor demanda = mayor flexibilidad percibida para cancelar.
    </div>
    """, unsafe_allow_html=True)
    
    # Lead Time vs Cancelaciones
    st.markdown("### ⏳ Lead Time: El Factor Predictivo")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if 'lead_time_category' in data_filtered.columns:
            # Ordenar categorías
            category_order = ['Mismo día', '1 semana', '1 mes', '3 meses', '6 meses', 'Más de 6 meses']
            
            lead_cancel = data_filtered.groupby('lead_time_category')['is_canceled'].agg(['sum', 'count']).reset_index()
            lead_cancel['cancel_rate'] = (lead_cancel['sum'] / lead_cancel['count'] * 100).round(2)
            
            # Ordenar
            lead_cancel['lead_time_category'] = pd.Categorical(lead_cancel['lead_time_category'], categories=category_order, ordered=True)
            lead_cancel = lead_cancel.sort_values('lead_time_category')
            
            fig_lead = px.bar(
                lead_cancel,
                x='lead_time_category',
                y='cancel_rate',
                title='Tasa de Cancelación según Anticipación de la Reserva',
                labels={'lead_time_category': 'Anticipación (Lead Time)', 'cancel_rate': 'Tasa de Cancelación (%)'},
                color='cancel_rate',
                color_continuous_scale='Reds',
                text='cancel_rate'
            )
            fig_lead.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig_lead.update_layout(height=450, showlegend=False)
            fig_lead.update_xaxes(tickangle=45)
            st.plotly_chart(fig_lead, use_container_width=True, key="fig_lead_tab3")
    
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        ### 🎯 Patrón Revelador
        
        **A mayor anticipación, mayor riesgo:**
        
        - **< 30 días**: Compromiso alto, cancelación baja
        - **30-90 días**: Zona intermedia
        - **> 180 días**: Alto riesgo de cancelación
        
        **¿Por qué?** 
        
        Más tiempo entre reserva y llegada significa:
        - Mayor probabilidad de cambio de planes
        - Menos compromiso emocional
        - Búsqueda de mejores ofertas
        """)
    
    # Distribución de lead time
    st.markdown("### 📊 Distribución de Reservas por Categoría de Lead Time")
    
    if 'lead_time_category' in data_filtered.columns:
        category_order = ['Mismo día', '1 semana', '1 mes', '3 meses', '6 meses', 'Más de 6 meses']
        
        lead_dist = data_filtered['lead_time_category'].value_counts().reset_index()
        lead_dist.columns = ['lead_time_category', 'count']
        
        # Ordenar
        lead_dist['lead_time_category'] = pd.Categorical(lead_dist['lead_time_category'], categories=category_order, ordered=True)
        lead_dist = lead_dist.sort_values('lead_time_category')
        
        fig_lead_dist = px.bar(
            lead_dist,
            x='lead_time_category',
            y='count',
            title='Número de Reservas por Categoría de Anticipación',
            labels={'lead_time_category': 'Categoría de Lead Time', 'count': 'Número de Reservas'},
            color='count',
            color_continuous_scale='Blues',
            text='count'
        )
        fig_lead_dist.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig_lead_dist.update_layout(height=400, showlegend=False)
        fig_lead_dist.update_xaxes(tickangle=45)
        st.plotly_chart(fig_lead_dist, use_container_width=True, key="fig_lead_dist_tab3")
    
    # Relación Lead Time y Duración de Estancia
    st.markdown("### 🔄 Lead Time vs Duración de Estancia")
    
    if 'lead_time_category' in data_filtered.columns and 'total_nights' in data_filtered.columns:
        category_order = ['Mismo día', '1 semana', '1 mes', '3 meses', '6 meses', 'Más de 6 meses']
        
        # Filtrar outliers en noches
        lead_nights = data_filtered[data_filtered['total_nights'] <= 20].copy()
        
        lead_nights_avg = lead_nights.groupby('lead_time_category')['total_nights'].agg(['mean', 'median', 'count']).reset_index()
        lead_nights_avg.columns = ['lead_time_category', 'promedio_noches', 'mediana_noches', 'num_reservas']
        
        # Ordenar
        lead_nights_avg['lead_time_category'] = pd.Categorical(lead_nights_avg['lead_time_category'], categories=category_order, ordered=True)
        lead_nights_avg = lead_nights_avg.sort_values('lead_time_category')
        
        fig_lead_nights = go.Figure()
        
        fig_lead_nights.add_trace(go.Bar(
            name='Promedio de Noches',
            x=lead_nights_avg['lead_time_category'],
            y=lead_nights_avg['promedio_noches'],
            marker_color='#1f77b4',
            text=lead_nights_avg['promedio_noches'].round(1),
            texttemplate='%{text:.1f}',
            textposition='outside'
        ))
        
        fig_lead_nights.add_trace(go.Scatter(
            name='Mediana de Noches',
            x=lead_nights_avg['lead_time_category'],
            y=lead_nights_avg['mediana_noches'],
            mode='lines+markers',
            marker=dict(color='#ff7f0e', size=10),
            line=dict(color='#ff7f0e', width=3)
        ))
        
        fig_lead_nights.update_layout(
            title='Duración Promedio de Estancia según Anticipación de Reserva',
            xaxis_title='Categoría de Lead Time',
            yaxis_title='Número de Noches',
            height=450,
            hovermode='x unified',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
        )
        fig_lead_nights.update_xaxes(tickangle=45)
        
        st.plotly_chart(fig_lead_nights, use_container_width=True, key="fig_lead_nights_tab3")
        
        st.markdown("""
        <div class="insight-box">
            <strong>💡 Insight Clave:</strong> Las reservas con mayor anticipación (lead time) tienden a tener 
            estancias ligeramente más largas, lo que sugiere que los clientes que planifican con más antelación 
            buscan experiencias más prolongadas. Sin embargo, también presentan mayor riesgo de cancelación.
        </div>
        """, unsafe_allow_html=True)

# ============================================
# TAB 4: CANALES Y COMPORTAMIENTO
# ============================================
with tab4:
    st.markdown("""
    <div class="chapter-intro">
    ¿Cómo llegan los clientes al hotel? ¿Quiénes son? La <strong>distribución y tipología de clientes</strong> 
    revelan dependencias críticas del negocio. La dependencia de OTAs supera el 80%, 
    lo que facilita las cancelaciones pero amplifica el alcance de mercado.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📱 Canales de Distribución")
    
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
                color_continuous_scale='Blues',
                text='count'
            )
            fig_channel.update_traces(texttemplate='%{text:,}', textposition='outside')
            fig_channel.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_channel, use_container_width=True, key="fig_channel_tab4")
    
    with col2:
        # Segmento de mercado
        if 'market_segment' in data_filtered.columns:
            market_dist = data_filtered.groupby('market_segment').size().reset_index(name='count')
            market_dist = market_dist.sort_values('count', ascending=False)
            
            fig_market_dist = px.pie(
                market_dist,
                values='count',
                names='market_segment',
                title='Distribución por Segmento de Mercado',
                hole=0.4
            )
            fig_market_dist.update_traces(textposition='inside', textinfo='percent+label')
            fig_market_dist.update_layout(height=400)
            st.plotly_chart(fig_market_dist, use_container_width=True, key="fig_market_dist_tab4")
    
    st.markdown("""
    <div class="insight-box">
        <strong>💡 Insight Clave:</strong> La dependencia de OTAs (TA/TO) supera el 82% de las reservas. 
        Esta intermediación digital facilita las cancelaciones con un simple clic pero amplifica el alcance de mercado.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📊 Comportamiento por Canal y Segmento")
    
    # Tasa de cancelación por segmento de mercado
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
            color_continuous_scale='Oranges',
            text='cancel_rate'
        )
        fig_market.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_market.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_market, use_container_width=True, key="fig_market_tab4")
    
    # Huéspedes repetidos vs nuevos
    st.markdown("### 🔄 Fidelización: El Talón de Aquiles")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'is_repeated_guest' in data_filtered.columns:
            repeated_dist = data_filtered.groupby('is_repeated_guest').size().reset_index(name='count')
            repeated_dist['type'] = repeated_dist['is_repeated_guest'].map({0: 'Nuevos', 1: 'Repetidos'})
            
            fig_repeated = px.pie(
                repeated_dist,
                values='count',
                names='type',
                title='Distribución de Huéspedes: Nuevos vs Repetidos',
                color_discrete_sequence=['#ff7f0e', '#2ca02c'],
                hole=0.4
            )
            fig_repeated.update_traces(textposition='inside', textinfo='percent+label', textfont_size=14)
            fig_repeated.update_layout(height=400)
            st.plotly_chart(fig_repeated, use_container_width=True, key="fig_repeated_tab4")
    
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        ### 📉 Crisis de Fidelización
        
        **Solo el 3% son huéspedes repetidos**
        
        Esto significa:
        - **97% de clientes nuevos** cada vez
        - Alto costo de adquisición constante
        - Sin ventaja de lealtad
        - Mayor vulnerabilidad a competencia
        
        **Oportunidad:** Implementar programas de fidelización
        """)
    
    # Top países
    st.markdown("### 🌍 Origen Geográfico de los Clientes")
    
    if 'country' in data_filtered.columns:
        top_countries = data_filtered['country'].value_counts().head(10).index
        country_data = data_filtered[data_filtered['country'].isin(top_countries)]
        country_dist = country_data.groupby('country').size().reset_index(name='count')
        country_dist = country_dist.sort_values('count', ascending=False)
        
        fig_country_dist = px.bar(
            country_dist,
            x='country',
            y='count',
            title='Top 10 Países por Número de Reservas',
            labels={'country': 'País', 'count': 'Número de Reservas'},
            color='count',
            color_continuous_scale='Viridis',
            text='count'
        )
        fig_country_dist.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig_country_dist.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_country_dist, use_container_width=True, key="fig_country_dist_tab4")

# ============================================
# TAB 5: CONCLUSIONES Y RECOMENDACIONES
# ============================================
with tab5:
    st.markdown("""
    <div class="chapter-intro">
    De los datos a la acción: estrategias concretas para <strong>reducir cancelaciones y optimizar la rentabilidad</strong>. 
    Basándonos en los patrones identificados, proponemos un plan de acción con impacto medible.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🛡️ Estrategias de Mitigación")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="recommendation-box">
        <strong>1. Política de Depósitos Escalonada</strong><br>
        • Lead time &lt; 30 días: Sin depósito<br>
        • Lead time 30-90 días: Depósito 10%<br>
        • Lead time &gt; 90 días: Depósito 15-20%<br>
        <em>Impacto esperado: Reducción 12-15% en cancelaciones anticipadas</em>
        </div>
        
        <div class="recommendation-box">
        <strong>2. Incentivos por Booking Directo</strong><br>
        • Descuento 5-10% en canal directo<br>
        • Programa de fidelización con puntos<br>
        • Upgrades gratuitos para clientes recurrentes<br>
        <em>Impacto esperado: Reducir dependencia de OTAs del 82% al 65%</em>
        </div>
        
        <div class="recommendation-box">
        <strong>3. Precios Dinámicos Anti-Cancelación</strong><br>
        • Tarifas flexibles para reservas &lt; 30 días<br>
        • Penalización gradual por cancelación según lead time<br>
        • Opciones de reprogramación sin costo<br>
        <em>Impacto esperado: Mantener flexibilidad reduciendo cancelaciones 8-10%</em>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📊 Calculadora de Impacto")
        
        # Cálculo de impacto
        total_reservas = len(data_filtered)
        canceladas = data_filtered['is_canceled'].sum()
        tasa_actual = (canceladas / total_reservas * 100)
        
        reduccion_objetivo = st.slider(
            "Reducción objetivo (puntos porcentuales)",
            min_value=5,
            max_value=20,
            value=10,
            step=1,
            key="reduccion_slider"
        )
        
        nueva_tasa = tasa_actual - reduccion_objetivo
        reservas_salvadas = int(total_reservas * (reduccion_objetivo / 100))
        avg_adr = data_filtered["adr"].mean()
        noches_promedio = 2.5
        ingresos_recuperados = reservas_salvadas * avg_adr * noches_promedio
        
        st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h4 style="color: #1f77b4;">Proyección de Impacto</h4>
        <table style="width: 100%; font-size: 15px;">
        <tr><td><strong>Tasa actual:</strong></td><td style="text-align: right;">{tasa_actual:.1f}%</td></tr>
        <tr><td><strong>Tasa objetivo:</strong></td><td style="text-align: right; color: #28a745;"><strong>{nueva_tasa:.1f}%</strong></td></tr>
        <tr><td><strong>Reservas salvadas:</strong></td><td style="text-align: right;">{reservas_salvadas:,}</td></tr>
        <tr><td><strong>Noches promedio:</strong></td><td style="text-align: right;">{noches_promedio}</td></tr>
        <tr style="border-top: 2px solid #ddd;"><td><strong>Ingresos recuperados:</strong></td><td style="text-align: right; color: #28a745; font-size: 18px;"><strong>€{ingresos_recuperados:,.0f}</strong></td></tr>
        </table>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Políticas de depósito y su impacto
    st.markdown("### 💳 Análisis: Política de Depósito")
    
    col1, col2 = st.columns(2)
    
    with col1:
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
                marker_color='#2ca02c',
                text=deposit_cancel['completed_rate'].round(1),
                texttemplate='%{text}%',
                textposition='inside'
            ))
            fig_deposit.add_trace(go.Bar(
                name='Canceladas',
                x=deposit_cancel['deposit_type'],
                y=deposit_cancel['cancel_rate'],
                marker_color='#d62728',
                text=deposit_cancel['cancel_rate'].round(1),
                texttemplate='%{text}%',
                textposition='inside'
            ))
            
            fig_deposit.update_layout(
                title='Impacto de la Política de Depósito en Cancelaciones',
                xaxis_title='Tipo de Depósito',
                yaxis_title='Porcentaje (%)',
                barmode='stack',
                height=400
            )
            st.plotly_chart(fig_deposit, use_container_width=True, key="fig_deposit_tab5")
    
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
        fig_adr.update_traces(line_color='#ff7f0e', line_width=3, marker_size=12)
        fig_adr.update_layout(height=400)
        st.plotly_chart(fig_adr, use_container_width=True, key="fig_adr_tab5")
    
    st.markdown("""
    <div class="insight-box">
        <strong>💡 Insight Clave:</strong> Las reservas sin depósito tienen una tasa de cancelación 
        significativamente mayor. La implementación de depósitos escalonados puede reducir cancelaciones 
        sin afectar negativamente la conversión de reservas.
    </div>
    """, unsafe_allow_html=True)
    
    # Top países con mayor cancelación
    st.markdown("### 🌍 Mercados con Mayor Riesgo de Cancelación")
    
    if 'country' in data_filtered.columns:
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
            title='Tasa de Cancelación por País de Origen (Top 10)',
            labels={'country': 'País', 'cancel_rate': 'Tasa de Cancelación (%)'},
            color='cancel_rate',
            color_continuous_scale='RdYlGn_r',
            text='cancel_rate'
        )
        fig_country.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_country.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig_country, use_container_width=True, key="fig_country_tab5")
    
    # Resumen final
    st.markdown("### 🎯 Resumen Ejecutivo")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 15px; color: white;">
    <h3 style="color: white; margin-top: 0;">Los 4 Pilares del Problema</h3>
    
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;">
        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
            <strong>⏰ Factor Temporal</strong><br>
            Lead time &gt; 180 días = Alto riesgo<br>
            Temporada alta = Más cancelaciones
        </div>
        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
            <strong>📱 Dependencia Digital</strong><br>
            82% via OTAs<br>
            Facilita cancelaciones con 1 clic
        </div>
        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
            <strong>💰 Políticas Flexibles</strong><br>
            87% sin depósito<br>
            Cero penalización = Cero compromiso
        </div>
        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
            <strong>🔄 Baja Fidelización</strong><br>
            97% clientes nuevos<br>
            Sin ventaja de lealtad
        </div>
    </div>
    
    <div style="margin-top: 30px; padding: 20px; background: rgba(255,255,255,0.9); border-radius: 10px; color: #333;">
        <strong style="color: #1f77b4; font-size: 18px;">🚀 Próximos Pasos Recomendados:</strong><br><br>
        1. <strong>Implementar depósitos escalonados</strong> según lead time en próximo trimestre<br>
        2. <strong>Lanzar campaña de booking directo</strong> con descuentos del 7%<br>
        3. <strong>Crear programa de fidelización</strong> para convertir el 3% actual en 15% en 12 meses<br>
        4. <strong>Monitorear KPIs semanalmente</strong>: tasa de cancelación, ADR, % canal directo
    </div>
    </div>
    """, unsafe_allow_html=True)

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