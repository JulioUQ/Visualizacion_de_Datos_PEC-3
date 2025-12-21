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
    initial_sidebar_state="collapsed"  # Ocultar sidebar por defecto
)

# CSS personalizado - Diseño optimizado para presentación
st.markdown("""
<style>
    /* Ocultar elementos de Streamlit para presentación limpia */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Estilos principales */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    .big-number {
        font-size: 120px;
        font-weight: bold;
        text-align: center;
        color: #dc3545;
        margin: 60px 0;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.2);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .hero-title {
        font-size: 64px;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin: 40px 0 20px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .subtitle {
        font-size: 28px;
        text-align: center;
        color: #666;
        margin-bottom: 50px;
        font-style: italic;
    }
    
    .section-title {
        font-size: 48px;
        font-weight: bold;
        color: #dc3545;
        margin: 50px 0 30px 0;
        padding-left: 20px;
        border-left: 8px solid #dc3545;
    }
    
    .narrative-text {
        font-size: 24px;
        line-height: 1.8;
        color: #333;
        padding: 30px;
        background: #f8f9fa;
        border-radius: 10px;
        margin: 30px 0;
    }
    
    .impact-number {
        font-size: 72px;
        font-weight: bold;
        text-align: center;
        color: #28a745;
        margin: 30px 0;
    }
    
    .metric-card-large {
        background: white;
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.15);
        text-align: center;
        margin: 20px 0;
    }
    
    .metric-value-large {
        font-size: 72px;
        font-weight: bold;
        color: #1f77b4;
    }
    
    .metric-label-large {
        font-size: 24px;
        color: #666;
        margin-top: 15px;
    }
    
    .culprit-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 40px;
        border-radius: 15px;
        margin: 30px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .culprit-title {
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    
    .culprit-text {
        font-size: 22px;
        line-height: 1.6;
    }
    
    .solution-box {
        background: #d4edda;
        border-left: 8px solid #28a745;
        padding: 30px;
        margin: 20px 0;
        border-radius: 10px;
    }
    
    .solution-title {
        font-size: 28px;
        font-weight: bold;
        color: #28a745;
        margin-bottom: 15px;
    }
    
    .solution-text {
        font-size: 20px;
        line-height: 1.6;
        color: #333;
    }
    
    .calculator-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 40px;
        border-radius: 15px;
        color: white;
        margin: 30px 0;
    }
    
    /* Hacer tabs más visibles */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 70px;
        padding: 15px 30px;
        background-color: #f0f2f6;
        border-radius: 15px 15px 0 0;
        font-size: 20px;
        font-weight: 700;
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
# ESTRUCTURA DE TABS PARA PRESENTACIÓN
# ============================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎬 EL PROBLEMA",
    "📊 ESTABLECER MAGNITUD", 
    "⏰ CULPABLE #1: TIEMPO",
    "📱 CULPABLES #2 Y #3",
    "💡 LA SOLUCIÓN"
])

# ============================================
# TAB 1: EL PROBLEMA - HOOK EMOCIONAL
# ============================================
with tab1:
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Número impactante
    cancelation_rate = data["is_canceled"].mean() * 100
    st.markdown(f'<div class="big-number">{cancelation_rate:.0f}%</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="narrative-text" style="text-align: center; font-size: 28px;">
    <strong>44.224 habitaciones vacías.</strong><br>
    44.224 oportunidades perdidas.<br>
    44.224 razones por las que los hoteles en Portugal perdieron millones de euros.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="narrative-text">
        <p style="margin: 10px 0; font-size: 24px;">
        <strong>Imagina:</strong> Eres director de un hotel en Lisboa. Es lunes por la mañana. 
        Revisas las reservas de hoy... y <strong>4 de cada 10 clientes han cancelado</strong>.
        </p>
        <br>
        <p style="margin: 10px 0; font-size: 24px;">
        No es un mal día. Es <strong>TODOS LOS DÍAS</strong>.
        </p>
        <br>
        <p style="margin: 10px 0; font-size: 24px;">
        119.390 reservas reales. 3 años completos. Dos hoteles portugueses.
        </p>
        <p style="margin: 10px 0; font-size: 24px;">
        Y descubrí algo que cambiará cómo ves las cancelaciones.
        </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Pregunta central
    st.markdown("""
    <div style="text-align: center; font-size: 42px; font-weight: bold; color: #dc3545; margin: 50px 0;">
    La pregunta no es <em>por qué</em> cancelan.<br>
    La pregunta es: ¿<strong>cuándo podemos predecirlo</strong>?
    </div>
    """, unsafe_allow_html=True)

# ============================================
# TAB 2: ESTABLECER MAGNITUD
# ============================================
with tab2:
    st.markdown('<div class="hero-title">119.390 Reservas Analizadas</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Dos hoteles • Tres años • Un patrón revelador</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # KPIs grandes y visibles
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total = len(data)
        st.markdown(f"""
        <div class="metric-card-large">
            <div class="metric-value-large" style="color: #1f77b4;">{total:,}</div>
            <div class="metric-label-large">Reservas Totales</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        completed = len(data[data["is_canceled"] == 0])
        st.markdown(f"""
        <div class="metric-card-large">
            <div class="metric-value-large" style="color: #28a745;">{completed:,}</div>
            <div class="metric-label-large">Completadas</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        canceled = data["is_canceled"].sum()
        st.markdown(f"""
        <div class="metric-card-large">
            <div class="metric-value-large" style="color: #dc3545;">{canceled:,}</div>
            <div class="metric-label-large">Canceladas</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_adr = data["adr"].mean()
        st.markdown(f"""
        <div class="metric-card-large">
            <div class="metric-value-large" style="color: #ff7f0e;">€{avg_adr:.0f}</div>
            <div class="metric-label-large">ADR Promedio</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Visualización de completadas vs canceladas - MUY GRANDE
    col1, col2 = st.columns(2)
    
    with col1:
        status_map = {1: "Canceladas", 0: "Completadas"}
        data_status = data.copy()
        data_status["status"] = data_status["is_canceled"].map(status_map)
        
        status_dist = data_status.groupby("status").size().reset_index(name="count")
        
        fig_status = px.pie(
            status_dist,
            values="count",
            names="status",
            color_discrete_map={"Completadas": "#28a745", "Canceladas": "#dc3545"},
            hole=0.5
        )
        fig_status.update_traces(
            textposition='inside', 
            textinfo='percent+label', 
            textfont_size=28,
            marker=dict(line=dict(color='white', width=4))
        )
        fig_status.update_layout(
            height=600, 
            showlegend=False,
            title={
                'text': "Estado de las Reservas",
                'font': {'size': 32, 'color': '#333'},
                'x': 0.5,
                'xanchor': 'center'
            }
        )
        st.plotly_chart(fig_status, use_container_width=True, key="fig_status_main")
    
    with col2:
        st.markdown(f"""
        <div class="narrative-text" style="margin-top: 100px;">
        <p style="font-size: 32px; font-weight: bold; color: #dc3545; margin: 0 0 20px 0;">
        Este caos tiene patrones perfectos.
        </p>
        <p style="font-size: 26px; margin: 0;">
        Tres patrones que, si los entiendes, puedes convertir ese 37% en dinero real.
        </p>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# TAB 3: CULPABLE #1 - EL TIEMPO
# ============================================
with tab3:
    st.markdown('<div class="section-title">CULPABLE #1: El Tiempo es tu Enemigo</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Gráfico ESTRELLA - Lead Time vs Cancelaciones
    if 'lead_time_category' in data.columns:
        category_order = ['Mismo día', '1 semana', '1 mes', '3 meses', '6 meses', 'Más de 6 meses']
        
        lead_cancel = data.groupby('lead_time_category')['is_canceled'].agg(['sum', 'count']).reset_index()
        lead_cancel['cancel_rate'] = (lead_cancel['sum'] / lead_cancel['count'] * 100).round(1)
        
        lead_cancel['lead_time_category'] = pd.Categorical(
            lead_cancel['lead_time_category'], 
            categories=category_order, 
            ordered=True
        )
        lead_cancel = lead_cancel.sort_values('lead_time_category')
        
        fig_lead = px.bar(
            lead_cancel,
            x='lead_time_category',
            y='cancel_rate',
            title='',
            labels={'lead_time_category': 'Anticipación de la Reserva', 'cancel_rate': 'Tasa de Cancelación (%)'},
            color='cancel_rate',
            color_continuous_scale='Reds',
            text='cancel_rate'
        )
        fig_lead.update_traces(
            texttemplate='%{text:.1f}%', 
            textposition='outside',
            textfont_size=24,
            marker_line_color='white',
            marker_line_width=2
        )
        fig_lead.update_layout(
            height=650,
            showlegend=False,
            font=dict(size=20),
            yaxis=dict(range=[0, 60]),
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_lead, use_container_width=True, key="fig_lead_main")
    
    # Narrativa explicativa
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="culprit-box">
            <div class="culprit-title">18% vs 56%</div>
            <p style="font-size: 22px; line-height: 1.6; margin: 20px 0;">
            Si un cliente reserva con <strong>menos de 7 días</strong> de anticipación: 
            solo el <strong>18% cancela</strong>. Tiene prisa, tiene compromiso.
            </p>
            <p style="font-size: 22px; line-height: 1.6; margin: 20px 0;">
            Pero si reserva con <strong>más de 6 meses</strong>: <strong>56% de cancelaciones</strong>. 
            Más de la mitad.
            </p>
            <p style="font-size: 22px; line-height: 1.6; margin: 20px 0;">
            ¿Por qué? Porque el tiempo diluye el compromiso.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Distribución de reservas por lead time
        lead_dist = data['lead_time_category'].value_counts().reset_index()
        lead_dist.columns = ['lead_time_category', 'count']
        lead_dist['lead_time_category'] = pd.Categorical(
            lead_dist['lead_time_category'], 
            categories=category_order, 
            ordered=True
        )
        lead_dist = lead_dist.sort_values('lead_time_category')
        
        fig_lead_dist = px.bar(
            lead_dist,
            x='lead_time_category',
            y='count',
            title='¿Dónde se concentran las reservas?',
            labels={'lead_time_category': 'Anticipación', 'count': 'Número de Reservas'},
            color='count',
            color_continuous_scale='Blues',
            text='count'
        )
        fig_lead_dist.update_traces(
            texttemplate='%{text:,}', 
            textposition='outside',
            textfont_size=18
        )
        fig_lead_dist.update_layout(
            height=400,
            showlegend=False,
            font=dict(size=16),
            xaxis_tickangle=-45,
            title_font_size=22
        )
        st.plotly_chart(fig_lead_dist, use_container_width=True, key="fig_lead_dist_main")
    
    st.markdown("""
    <div class="narrative-text" style="background: #fff3cd; border-left: 8px solid #ffc107;">
    <p style="font-size: 28px; font-weight: bold; margin: 0 0 15px 0;">El insight de oro:</p>
    <p style="font-size: 24px; margin: 0;">
    La mayoría de reservas se concentran entre <strong>1 y 3 meses</strong>. 
    Esta es tu <strong>zona de batalla</strong>. No son los extremos, es el centro donde se juega el partido.
    </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# TAB 4: CULPABLES #2 Y #3
# ============================================
with tab4:
    st.markdown('<div class="section-title">CULPABLE #2: Vendiste tu Alma a las OTAs</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Gráfico de canales de distribución
        if 'distribution_channel' in data.columns:
            channel_dist = data.groupby('distribution_channel').size().reset_index(name='count')
            channel_dist = channel_dist.sort_values('count', ascending=True)
            
            fig_channel = px.bar(
                channel_dist,
                x='count',
                y='distribution_channel',
                orientation='h',
                title='',
                labels={'distribution_channel': 'Canal de Distribución', 'count': 'Número de Reservas'},
                color='count',
                color_continuous_scale='Oranges',
                text='count'
            )
            fig_channel.update_traces(
                texttemplate='%{text:,}', 
                textposition='outside',
                textfont_size=22
            )
            fig_channel.update_layout(
                height=500,
                showlegend=False,
                font=dict(size=20)
            )
            st.plotly_chart(fig_channel, use_container_width=True, key="fig_channel_main")
    
    with col2:
        # Cálculo del porcentaje de OTAs
        if 'distribution_channel' in data.columns:
            ota_pct = (data['distribution_channel'] == 'TA/TO').sum() / len(data) * 100
            
            st.markdown(f"""
            <div class="metric-card-large" style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%); color: white;">
                <div class="metric-value-large" style="color: white; font-size: 96px;">{ota_pct:.0f}%</div>
                <div class="metric-label-large" style="color: white; font-size: 28px;">De reservas via OTAs</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="narrative-text" style="background: #ffe5e5;">
            <p style="font-size: 24px; font-weight: bold; margin: 0 0 15px 0;">Cancelar en una OTA es ridículamente fácil.</p>
            <p style="font-size: 20px; margin: 0;">Tres clics. Sin llamar. Sin culpa. Sin conexión humana.</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Huéspedes repetidos
    col1, col2 = st.columns([2, 3])
    
    with col1:
        if 'is_repeated_guest' in data.columns:
            repeated_pct = (data['is_repeated_guest'] == 1).sum() / len(data) * 100
            
            st.markdown(f"""
            <div class="metric-card-large" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                <div class="metric-value-large" style="color: white; font-size: 96px;">{repeated_pct:.0f}%</div>
                <div class="metric-label-large" style="color: white; font-size: 28px;">Clientes que Repiten</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="narrative-text" style="background: #e3f2fd;">
            <p style="font-size: 24px; font-weight: bold; margin: 0 0 15px 0;">97% son desconocidos.</p>
            <p style="font-size: 20px; margin: 0;">
            Llegaron por una OTA, no tienen lealtad, no te conocen. 
            Son <strong>fantasmas digitales</strong> que pueden desaparecer con un clic.
            </p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if 'is_repeated_guest' in data.columns:
            repeated_dist = data.groupby('is_repeated_guest').size().reset_index(name='count')
            repeated_dist['type'] = repeated_dist['is_repeated_guest'].map({0: 'Nuevos (97%)', 1: 'Repetidos (3%)'})
            
            fig_repeated = px.pie(
                repeated_dist,
                values='count',
                names='type',
                title='Distribución de Huéspedes',
                color_discrete_sequence=['#ff7f0e', '#2ca02c'],
                hole=0.5
            )
            fig_repeated.update_traces(
                textposition='inside', 
                textinfo='label', 
                textfont_size=24,
                marker=dict(line=dict(color='white', width=4))
            )
            fig_repeated.update_layout(
                height=500,
                title_font_size=28
            )
            st.plotly_chart(fig_repeated, use_container_width=True, key="fig_repeated_main")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">CULPABLE #3: Tu Generosidad te está Arruinando</div>', unsafe_allow_html=True)
    
    # Gráfico de depósitos - MUY DESTACADO
    if 'deposit_type' in data.columns:
        deposit_cancel = data.groupby('deposit_type').agg({
            'is_canceled': ['sum', 'count']
        }).reset_index()
        deposit_cancel.columns = ['deposit_type', 'canceled', 'total']
        deposit_cancel['cancel_rate'] = (deposit_cancel['canceled'] / deposit_cancel['total'] * 100).round(1)
        deposit_cancel['completed_rate'] = (100 - deposit_cancel['cancel_rate']).round(1)
        
        fig_deposit = go.Figure()
        fig_deposit.add_trace(go.Bar(
            name='Completadas',
            x=deposit_cancel['deposit_type'],
            y=deposit_cancel['completed_rate'],
            marker_color='#28a745',
            text=deposit_cancel['completed_rate'],
            texttemplate='%{text:.1f}%',
            textposition='inside',
            textfont_size=22
        ))
        fig_deposit.add_trace(go.Bar(
            name='Canceladas',
            x=deposit_cancel['deposit_type'],
            y=deposit_cancel['cancel_rate'],
            marker_color='#dc3545',
            text=deposit_cancel['cancel_rate'],
            texttemplate='%{text:.1f}%',
            textposition='inside',
            textfont_size=22
        ))
        
        fig_deposit.update_layout(
            title='',
            xaxis_title='Tipo de Depósito',
            yaxis_title='Porcentaje (%)',
            barmode='stack',
            height=600,
            font=dict(size=20),
            legend=dict(font=dict(size=22))
        )
        st.plotly_chart(fig_deposit, use_container_width=True, key="fig_deposit_main")
    
    st.markdown("""
    <div class="culprit-box">
        <div class="culprit-title">15% vs 43%</div>
        <p style="font-size: 22px; line-height: 1.6; margin: 20px 0;">
        Reservas <strong>con depósito</strong>: 15% de cancelaciones.
        </p>
        <p style="font-size: 22px; line-height: 1.6; margin: 20px 0;">
        Reservas <strong>sin depósito</strong>: 43% de cancelaciones.
        </p>
        <p style="font-size: 22px; line-height: 1.6; margin: 20px 0;">
        No hace falta un doctorado en psicología:
        </p>
        <p style="font-size: 22px; line-height: 1.6; margin: 20px 0;">
        <strong>Dinero en juego = Compromiso</strong>
        </p>
        <p style="font-size: 22px; line-height: 1.6; margin: 20px 0;">
        Sin dinero en juego = 'Ya veré si voy'
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# TAB 5: LA SOLUCIÓN
# ============================================
with tab5:
    st.markdown('<div class="hero-title" style="color: #28a745;">Plan de Acción: 3 Pasos</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Las 3 soluciones
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="solution-box">
            <div class="solution-title">PASO 1: Depósitos Escalonados</div>
            <p style="font-size: 20px; line-height: 1.6; margin: 15px 0;">
            <strong>&lt; 30 días:</strong> 0% depósito
            </p>
            <p style="font-size: 20px; line-height: 1.6; margin: 15px 0;">
            <strong>30-90 días:</strong> 10% depósito
            </p>
            <p style="font-size: 20px; line-height: 1.6; margin: 15px 0;">
            <strong>&gt; 90 días:</strong> 20% depósito
            </p>
            <p style="font-size: 18px; line-height: 1.6; margin: 20px 0; font-style: italic;">
            Suficiente para pensárselo dos veces.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="solution-box">
            <div class="solution-title">PASO 2: Rescata tu Canal Directo</div>
            <p style="font-size: 20px; line-height: 1.6; margin: 15px 0;">
            • 7% descuento directo
            </p>
            <p style="font-size: 20px; line-height: 1.6; margin: 15px 0;">
            • Programa de puntos
            </p>
            <p style="font-size: 20px; line-height: 1.6; margin: 15px 0;">
            • Upgrades gratis
            </p>
            <p style="font-size: 18px; line-height: 1.6; margin: 20px 0; font-style: italic;">
            Meta: del 18% al 35% en un año
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="solution-box">
            <div class="solution-title">PASO 3: Convierte Desconocidos en Familia</div>
            <p style="font-size: 20px; line-height: 1.6; margin: 15px 0;">
            • Email 48h post-reserva
            </p>
            <p style="font-size: 20px; line-height: 1.6; margin: 15px 0;">
            • Tips locales 7 días antes
            </p>
            <p style="font-size: 20px; line-height: 1.6; margin: 15px 0;">
            • Follow-up post-estancia
            </p>
            <p style="font-size: 18px; line-height: 1.6; margin: 20px 0; font-style: italic;">
            Meta: triplicar el 3% actual
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # CALCULADORA DE IMPACTO - ELEMENTO CLAVE
    st.markdown('<div class="section-title" style="color: #28a745;">¿Cuánto Vale Todo Esto?</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="narrative-text" style="font-size: 26px; text-align: center;">
    Hagamos las cuentas <strong>EN VIVO</strong>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # CALCULADORA INTERACTIVA
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.markdown("""
        <div class="calculator-box">
            <h2 style="margin-top: 0; font-size: 32px;">📊 Calculadora de Impacto</h2>
            <p style="font-size: 20px;">Mueve el slider para ver cuánto dinero recuperas:</p>
        </div>
        """, unsafe_allow_html=True)
        
        reduccion_objetivo = st.slider(
            "Reducción objetivo en cancelaciones (puntos porcentuales)",
            min_value=5,
            max_value=20,
            value=10,
            step=1,
            key="reduccion_slider_main"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Cálculos
        total_reservas = len(data)
        canceladas = data['is_canceled'].sum()
        tasa_actual = (canceladas / total_reservas * 100)
        nueva_tasa = tasa_actual - reduccion_objetivo
        reservas_salvadas = int(total_reservas * (reduccion_objetivo / 100))
        avg_adr = data["adr"].mean()
        noches_promedio = 2.5
        ingresos_recuperados = reservas_salvadas * avg_adr * noches_promedio
        
        st.markdown(f"""
        <div style="background: white; padding: 30px; border-radius: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.2);">
            <h3 style="color: #1f77b4; font-size: 28px; margin-bottom: 20px;">📈 Proyección de Impacto</h3>
            <table style="width: 100%; font-size: 20px; line-height: 2;">
                <tr>
                    <td><strong>Tasa actual:</strong></td>
                    <td style="text-align: right; color: #dc3545;"><strong>{tasa_actual:.1f}%</strong></td>
                </tr>
                <tr>
                    <td><strong>Tasa objetivo:</strong></td>
                    <td style="text-align: right; color: #28a745;"><strong>{nueva_tasa:.1f}%</strong></td>
                </tr>
                <tr>
                    <td><strong>Reservas salvadas:</strong></td>
                    <td style="text-align: right;"><strong>{reservas_salvadas:,}</strong></td>
                </tr>
                <tr>
                    <td><strong>Noches promedio:</strong></td>
                    <td style="text-align: right;">{noches_promedio}</td>
                </tr>
                <tr>
                    <td><strong>ADR promedio:</strong></td>
                    <td style="text-align: right;">€{avg_adr:.2f}</td>
                </tr>
                <tr style="border-top: 3px solid #28a745;">
                    <td><strong style="font-size: 24px;">💰 INGRESOS RECUPERADOS:</strong></td>
                    <td style="text-align: right; color: #28a745; font-size: 32px;">
                        <strong>€{ingresos_recuperados:,.0f}</strong>
                    </td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Gráfico de impacto visual
        impacto_data = pd.DataFrame({
            'Escenario': ['Situación Actual', 'Con Estrategias'],
            'Cancelaciones': [tasa_actual, nueva_tasa],
            'Completadas': [100 - tasa_actual, 100 - nueva_tasa]
        })
        
        fig_impacto = go.Figure()
        
        fig_impacto.add_trace(go.Bar(
            name='Completadas',
            x=impacto_data['Escenario'],
            y=impacto_data['Completadas'],
            marker_color='#28a745',
            text=impacto_data['Completadas'].round(1),
            texttemplate='%{text:.1f}%',
            textposition='inside',
            textfont_size=28
        ))
        
        fig_impacto.add_trace(go.Bar(
            name='Cancelaciones',
            x=impacto_data['Escenario'],
            y=impacto_data['Cancelaciones'],
            marker_color='#dc3545',
            text=impacto_data['Cancelaciones'].round(1),
            texttemplate='%{text:.1f}%',
            textposition='inside',
            textfont_size=28
        ))
        
        fig_impacto.update_layout(
            title='Impacto Visual de las Estrategias',
            barmode='stack',
            height=600,
            font=dict(size=20),
            legend=dict(font=dict(size=22)),
            yaxis=dict(title='Porcentaje (%)', range=[0, 100]),
            title_font_size=28
        )
        
        st.plotly_chart(fig_impacto, use_container_width=True, key="fig_impacto_main")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # IMPACTO DESTACADO
    st.markdown(f"""
    <div class="impact-number" style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
         color: white; padding: 50px; border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.3);">
        💰 €{ingresos_recuperados:,.0f}
        <div style="font-size: 32px; margin-top: 20px; font-weight: normal;">
        Recuperados con solo {reduccion_objetivo}% de reducción en cancelaciones
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    # CIERRE PODEROSO - Todo en un solo bloque centrado
    st.markdown("""
    <div style="max-width: 1200px; margin: 0 auto;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
             padding: 50px 60px; border-radius: 20px; color: white; box-shadow: 0 10px 40px rgba(0,0,0,0.3);">
            
            <h2 style="color: white; text-align: center; font-size: 42px; margin: 0 0 40px 0;">
                El Enigma Está Resuelto
            </h2>
            
            <p style="font-size: 32px; font-weight: bold; margin: 0 0 30px 0; text-align: center;">
                Tres culpables. Tres soluciones.
            </p>
            
            <p style="font-size: 26px; margin: 20px 0; line-height: 1.6;">
                ⏰ <strong>Tiempo:</strong> Depósitos escalonados según anticipación
            </p>
            
            <p style="font-size: 26px; margin: 20px 0; line-height: 1.6;">
                📱 <strong>OTAs:</strong> Rescata tu canal directo con incentivos
            </p>
            
            <p style="font-size: 26px; margin: 20px 0; line-height: 1.6;">
                💰 <strong>Políticas:</strong> Dinero en juego = Compromiso real
            </p>
            
            <div style="text-align: center; font-size: 32px; margin-top: 50px; background: rgba(255,255,255,0.2); padding: 35px; border-radius: 15px;">
                <p style="margin: 0 0 20px 0;">119.390 reservas nos contaron su historia.</p>
                <p style="margin: 0; font-weight: bold;">Ahora depende de ti escribir el siguiente capítulo.</p>
            </div>
            
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Mensaje final
    st.markdown("""
    <div style="text-align: center; font-size: 28px; color: #333; margin: 50px 0;">
    ¿37% de cancelaciones?<br>
    <strong style="font-size: 36px; color: #28a745;">No tiene por qué ser tu realidad.</strong>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# FOOTER MINIMALISTA
# ============================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; padding: 20px;">
    <p style="font-size: 16px;"><strong>Dashboard Storytelling - PEC 3 Visualización de Datos</strong></p>
    <p style="font-size: 14px;">Máster en Ciencia de Datos | UOC | 2025</p>
</div>
""", unsafe_allow_html=True)