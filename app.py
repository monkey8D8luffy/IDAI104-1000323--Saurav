import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. PAGE CONFIGURATION & GLASS OS CSS
# ==========================================
st.set_page_config(
    page_title="Aerospace Command Center",
    layout="wide",
    page_icon="🛰️",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@200;300;400;500;600&family=Space+Mono:wght@400;700&display=swap');

/* ── ROOT TOKENS ── */
:root {
    --glass-bg:        rgba(255, 255, 255, 0.06);
    --glass-border:    rgba(255, 255, 255, 0.18);
    --glass-shadow:    rgba(0, 0, 0, 0.35);
    --accent-aqua:     #41d9f5;
    --accent-ice:      #a8edea;
    --accent-deep:     #1a6edc;
    --accent-glow:     rgba(65, 217, 245, 0.35);
    --water-1:         #0a1628;
    --water-2:         #0d2444;
    --water-3:         #102a55;
    --text-primary:    #e8f4f8;
    --text-secondary:  rgba(200, 230, 240, 0.65);
    --font-main:       'Outfit', sans-serif;
    --font-mono:       'Space Mono', monospace;
}

/* ── ANIMATED DEEP WATER BACKGROUND ── */
.stApp {
    background: var(--water-1) !important;
    font-family: var(--font-main) !important;
}

.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 60% at 20% 30%, rgba(26,110,220,0.22) 0%, transparent 70%),
        radial-gradient(ellipse 60% 80% at 80% 70%, rgba(65,217,245,0.14) 0%, transparent 65%),
        radial-gradient(ellipse 70% 50% at 50% 100%, rgba(10,22,40,0.9) 0%, transparent 60%);
    animation: waterShift 14s ease-in-out infinite alternate;
    z-index: 0;
    pointer-events: none;
}

@keyframes waterShift {
    0%   { opacity: 1; transform: scale(1) translateY(0px); }
    50%  { opacity: 0.85; transform: scale(1.04) translateY(-12px); }
    100% { opacity: 1; transform: scale(1) translateY(4px); }
}

/* Morphing blob orbs */
.stApp::after {
    content: '';
    position: fixed;
    top: -20%;
    left: -10%;
    width: 65vw;
    height: 65vw;
    background: radial-gradient(circle, rgba(65,217,245,0.07) 0%, transparent 65%);
    border-radius: 60% 40% 55% 45% / 45% 55% 45% 55%;
    animation: morphBlob 18s ease-in-out infinite;
    z-index: 0;
    pointer-events: none;
}

@keyframes morphBlob {
    0%   { border-radius: 60% 40% 55% 45% / 45% 55% 45% 55%; transform: rotate(0deg) scale(1); }
    25%  { border-radius: 40% 60% 35% 65% / 60% 40% 65% 35%; transform: rotate(90deg) scale(1.05); }
    50%  { border-radius: 55% 45% 65% 35% / 35% 65% 40% 60%; transform: rotate(180deg) scale(0.97); }
    75%  { border-radius: 45% 55% 40% 60% / 55% 45% 55% 45%; transform: rotate(270deg) scale(1.03); }
    100% { border-radius: 60% 40% 55% 45% / 45% 55% 45% 55%; transform: rotate(360deg) scale(1); }
}

/* ── TYPOGRAPHY ── */
h1, h2, h3, h4, h5, h6, p, span, div, label, .stMarkdown {
    font-family: var(--font-main) !important;
    color: var(--text-primary) !important;
}

h1 { font-weight: 300 !important; letter-spacing: 0.12em !important; color: var(--accent-aqua) !important; }
h2 { font-weight: 400 !important; letter-spacing: 0.06em !important; color: var(--accent-ice) !important; font-size: 1.25rem !important; }
h3 { font-weight: 400 !important; color: rgba(200,230,240,0.85) !important; }

/* ── GLASS CARD ── */
.glass-card {
    background: var(--glass-bg);
    backdrop-filter: blur(28px) saturate(160%);
    -webkit-backdrop-filter: blur(28px) saturate(160%);
    border-radius: 20px;
    border: 1px solid var(--glass-border);
    padding: 28px 32px;
    margin-bottom: 24px;
    box-shadow:
        0 8px 40px var(--glass-shadow),
        inset 0 1px 0 rgba(255,255,255,0.12),
        inset 0 -1px 0 rgba(0,0,0,0.2);
    position: relative;
    overflow: hidden;
    transition: box-shadow 0.4s ease, transform 0.3s ease;
}

/* Liquid shimmer sweep on glass cards */
.glass-card::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 60%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.06), transparent);
    animation: shimmerSweep 6s ease-in-out infinite;
    pointer-events: none;
}

@keyframes shimmerSweep {
    0%   { left: -100%; opacity: 0; }
    40%  { opacity: 1; }
    60%  { opacity: 1; }
    100% { left: 200%; opacity: 0; }
}

/* ── HEADER CARD ── */
.header-card {
    background: linear-gradient(135deg, rgba(65,217,245,0.08) 0%, rgba(26,110,220,0.08) 100%);
    backdrop-filter: blur(40px) saturate(180%);
    -webkit-backdrop-filter: blur(40px) saturate(180%);
    border-radius: 24px;
    border: 1px solid rgba(65,217,245,0.25);
    padding: 36px 40px;
    margin-bottom: 28px;
    text-align: center;
    box-shadow:
        0 0 60px rgba(65,217,245,0.08),
        0 12px 50px rgba(0,0,0,0.5),
        inset 0 1px 0 rgba(255,255,255,0.15);
    position: relative;
    overflow: hidden;
}

.header-card::after {
    content: '';
    position: absolute;
    bottom: -50%;
    left: 50%;
    transform: translateX(-50%);
    width: 80%;
    height: 100%;
    background: radial-gradient(ellipse, rgba(65,217,245,0.06) 0%, transparent 70%);
    animation: headerPulse 5s ease-in-out infinite;
    pointer-events: none;
}

@keyframes headerPulse {
    0%, 100% { transform: translateX(-50%) scale(1); opacity: 0.7; }
    50% { transform: translateX(-50%) scale(1.15); opacity: 1; }
}

.app-title {
    font-family: var(--font-main) !important;
    font-size: clamp(1.6rem, 3.5vw, 2.6rem) !important;
    font-weight: 200 !important;
    letter-spacing: 0.22em !important;
    color: var(--accent-aqua) !important;
    text-shadow: 0 0 30px rgba(65,217,245,0.5), 0 0 60px rgba(65,217,245,0.2) !important;
    margin: 0 0 8px 0 !important;
    text-transform: uppercase !important;
}

.app-subtitle {
    font-family: var(--font-mono) !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.3em !important;
    color: var(--text-secondary) !important;
    text-transform: uppercase !important;
    margin: 0 !important;
}

/* ── TELEMETRY BOX ── */
.telemetry-box {
    background: rgba(65, 217, 245, 0.04);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-left: 3px solid var(--accent-aqua);
    border-radius: 0 12px 12px 0;
    padding: 16px 20px;
    font-family: var(--font-mono) !important;
    font-size: 0.8rem;
    margin-bottom: 20px;
    color: var(--accent-ice) !important;
    position: relative;
    overflow: hidden;
    box-shadow: inset 0 0 30px rgba(65,217,245,0.03);
    animation: telePulse 2s ease-in-out infinite;
}

@keyframes telePulse {
    0%, 100% { border-left-color: var(--accent-aqua); box-shadow: inset 0 0 30px rgba(65,217,245,0.03); }
    50% { border-left-color: var(--accent-ice); box-shadow: inset 0 0 40px rgba(168,237,234,0.06); }
}

/* ── FILTER BADGE ── */
.filter-badge {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    background: rgba(65, 217, 245, 0.08);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(65, 217, 245, 0.2);
    border-radius: 50px;
    padding: 10px 22px;
    font-family: var(--font-mono);
    font-size: 0.75rem;
    color: var(--accent-aqua) !important;
    letter-spacing: 0.1em;
    margin-bottom: 20px;
}

.pulse-dot {
    width: 8px; height: 8px;
    background: var(--accent-aqua);
    border-radius: 50%;
    animation: pulseDot 1.8s ease-in-out infinite;
    flex-shrink: 0;
    box-shadow: 0 0 8px var(--accent-aqua);
}

@keyframes pulseDot {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.6); opacity: 0.5; }
}

/* ── SECTION LABEL ── */
.section-label {
    display: flex;
    align-items: center;
    gap: 14px;
    margin: 32px 0 20px 0;
}

.section-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(65,217,245,0.4) 0%, transparent 100%);
}

.section-line-right {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, rgba(65,217,245,0.15) 100%);
}

.section-title-text {
    font-family: var(--font-mono) !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.25em !important;
    color: var(--accent-aqua) !important;
    text-transform: uppercase !important;
    white-space: nowrap !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: rgba(10, 18, 35, 0.75) !important;
    backdrop-filter: blur(30px) saturate(150%) !important;
    -webkit-backdrop-filter: blur(30px) saturate(150%) !important;
    border-right: 1px solid rgba(65, 217, 245, 0.12) !important;
}

[data-testid="stSidebar"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent, var(--accent-aqua), transparent);
    animation: topBeam 4s ease-in-out infinite;
}

@keyframes topBeam {
    0%, 100% { opacity: 0.4; }
    50% { opacity: 1; }
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px !important;
    background: transparent !important;
    border-bottom: 1px solid rgba(65, 217, 245, 0.12) !important;
    padding-bottom: 0 !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
    padding: 14px 28px !important;
    font-family: var(--font-mono) !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: var(--text-secondary) !important;
    transition: all 0.3s ease !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: var(--accent-aqua) !important;
    background: rgba(65, 217, 245, 0.04) !important;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: transparent !important;
    border-bottom: 2px solid var(--accent-aqua) !important;
    color: var(--accent-aqua) !important;
    text-shadow: 0 0 12px rgba(65,217,245,0.5) !important;
}

/* ── METRICS ── */
[data-testid="stMetric"] {
    background: var(--glass-bg) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 16px !important;
    padding: 20px !important;
    box-shadow: 0 4px 20px var(--glass-shadow), inset 0 1px 0 rgba(255,255,255,0.08) !important;
    transition: transform 0.25s ease, box-shadow 0.25s ease !important;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 30px rgba(65,217,245,0.12), inset 0 1px 0 rgba(255,255,255,0.1) !important;
}

[data-testid="stMetricLabel"] {
    font-family: var(--font-mono) !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    color: var(--text-secondary) !important;
}

[data-testid="stMetricValue"] {
    font-family: var(--font-main) !important;
    font-weight: 300 !important;
    color: var(--accent-aqua) !important;
    font-size: 1.4rem !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, rgba(65,217,245,0.12), rgba(26,110,220,0.12)) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(65, 217, 245, 0.35) !important;
    border-radius: 12px !important;
    color: var(--accent-aqua) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.15em !important;
    padding: 14px 28px !important;
    text-transform: uppercase !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 0 0 transparent !important;
    position: relative !important;
    overflow: hidden !important;
}

.stButton > button::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(65,217,245,0.1), transparent);
    opacity: 0;
    transition: opacity 0.3s ease;
}

.stButton > button:hover {
    background: linear-gradient(135deg, rgba(65,217,245,0.22), rgba(26,110,220,0.22)) !important;
    border-color: rgba(65, 217, 245, 0.65) !important;
    box-shadow: 0 0 30px rgba(65,217,245,0.2), 0 4px 20px rgba(0,0,0,0.3) !important;
    transform: translateY(-2px) !important;
    color: #ffffff !important;
}

.stButton > button:active {
    transform: translateY(0px) !important;
}

/* ── SELECTBOX & INPUTS ── */
[data-baseweb="select"] > div,
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {
    background: rgba(255, 255, 255, 0.04) !important;
    backdrop-filter: blur(15px) !important;
    border: 1px solid rgba(65, 217, 245, 0.18) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-family: var(--font-main) !important;
    transition: border-color 0.3s ease !important;
}

[data-baseweb="select"] > div:focus-within,
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextInput"] input:focus {
    border-color: rgba(65, 217, 245, 0.5) !important;
    box-shadow: 0 0 0 3px rgba(65, 217, 245, 0.08) !important;
}

/* ── SLIDER ── */
[data-testid="stSlider"] [role="slider"] {
    background: var(--accent-aqua) !important;
    box-shadow: 0 0 10px rgba(65,217,245,0.6) !important;
}

/* ── RADIO ── */
[data-testid="stRadio"] label {
    background: var(--glass-bg) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 10px !important;
    padding: 10px 18px !important;
    transition: all 0.25s ease !important;
    font-family: var(--font-mono) !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em !important;
}

[data-testid="stRadio"] label:hover {
    border-color: rgba(65,217,245,0.4) !important;
    background: rgba(65,217,245,0.06) !important;
}

/* ── PROGRESS BAR ── */
[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, var(--accent-deep), var(--accent-aqua)) !important;
    border-radius: 4px !important;
    box-shadow: 0 0 12px rgba(65,217,245,0.4) !important;
}

/* ── HR ── */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(65,217,245,0.2), transparent) !important;
    margin: 36px 0 !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(65,217,245,0.25); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(65,217,245,0.45); }

/* ── SUCCESS / ERROR ALERTS ── */
[data-testid="stAlert"] {
    background: var(--glass-bg) !important;
    backdrop-filter: blur(20px) !important;
    border-radius: 12px !important;
    border: 1px solid var(--glass-border) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.8rem !important;
}

/* ── WATER RIPPLE DECORATION ── */
.water-ripple {
    position: relative;
    display: inline-block;
}

.water-ripple::before,
.water-ripple::after {
    content: '';
    position: absolute;
    inset: -2px;
    border-radius: inherit;
    border: 1px solid rgba(65,217,245,0.3);
    animation: rippleOut 3s ease-out infinite;
}

.water-ripple::after {
    animation-delay: 1.5s;
}

@keyframes rippleOut {
    0% { transform: scale(1); opacity: 0.5; }
    100% { transform: scale(1.08); opacity: 0; }
}

/* ── PLOTLY CHART CONTAINERS ── */
[data-testid="stPlotlyChart"] {
    border-radius: 16px !important;
    overflow: hidden !important;
}

/* ── MATPLOTLIB IMAGES ── */
[data-testid="stImage"] {
    border-radius: 14px !important;
    overflow: hidden !important;
}

/* Fix Streamlit default white backgrounds */
.element-container { background: transparent !important; }
.block-container { padding-top: 2rem !important; }
</style>
""", unsafe_allow_html=True)


# ── HEADER ──────────────────────────────────────────────
st.markdown("""
<div class="header-card">
    <p class="app-title">Aerospace Command Center</p>
    <p class="app-subtitle">Orbital Telemetry &nbsp;·&nbsp; Predictive Analytics &nbsp;·&nbsp; Flight Physics</p>
</div>
""", unsafe_allow_html=True)


# ==========================================
# 2. DATA LOADING & PREPROCESSING
# ==========================================
@st.cache_data
def load_and_clean_data():
    df = pd.read_csv("space_missions_dataset.csv")
    df['Launch Date'] = pd.to_datetime(df['Launch Date'], errors='coerce')
    df['Launch Year'] = df['Launch Date'].dt.year
    numeric_cols = [
        'Mission Cost (billion USD)', 'Payload Weight (tons)',
        'Fuel Consumption (tons)', 'Mission Duration (years)',
        'Distance from Earth (light-years)', 'Crew Size',
        'Mission Success (%)', 'Scientific Yield (points)'
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=['Payload Weight (tons)', 'Fuel Consumption (tons)'])
    df['Outcome Status'] = np.where(
        df['Mission Success (%)'] >= 80, 'Nominal (Success)', 'Anomaly (Failure)'
    )
    return df

try:
    data = load_and_clean_data()
except FileNotFoundError:
    st.error("⚠️  'space_missions_dataset.csv' not found. Please upload the dataset.")
    st.stop()


VEHICLE_STATS = {
    "SLS":          {"mass_kg": 1000000, "thrust_N": 39000000, "drag": 0.4},
    "Starship":     {"mass_kg": 1200000, "thrust_N": 74000000, "drag": 0.3},
    "Falcon Heavy": {"mass_kg": 1420000, "thrust_N": 22000000, "drag": 0.35},
    "Ariane 6":     {"mass_kg": 800000,  "thrust_N": 10000000, "drag": 0.45}
}


# ── CHART THEME ─────────────────────────────────────────
aqua_template = dict(
    layout=go.Layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='rgba(200,230,240,0.8)', family='Outfit, sans-serif', size=12),
        title=dict(font=dict(color='#41d9f5', size=14, family='Space Mono'), x=0.02),
        legend=dict(
            font=dict(color='rgba(200,230,240,0.7)', size=11),
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(65,217,245,0.15)',
            borderwidth=1
        ),
        xaxis=dict(
            gridcolor='rgba(65,217,245,0.07)',
            zerolinecolor='rgba(65,217,245,0.15)',
            tickfont=dict(color='rgba(200,230,240,0.6)'),
        ),
        yaxis=dict(
            gridcolor='rgba(65,217,245,0.07)',
            zerolinecolor='rgba(65,217,245,0.15)',
            tickfont=dict(color='rgba(200,230,240,0.6)'),
        ),
        margin=dict(l=0, r=0, t=40, b=0),
    )
)

color_map_status = {
    "Nominal (Success)": "#41d9f5",
    "Anomaly (Failure)": "#f55241"
}

plt.style.use('dark_background')
fig_rc = {
    'figure.facecolor': '#0a1628',
    'axes.facecolor':   'none',
    'axes.edgecolor':   'rgba(65,217,245,0.2)',
    'text.color':       '#c8e6f0',
    'xtick.color':      '#41d9f5',
    'ytick.color':      '#41d9f5',
    'axes.spines.top':  False,
    'axes.spines.right':False,
}
sns.set_theme(style="darkgrid", rc=fig_rc)


# ==========================================
# 3. TABS
# ==========================================
tab1, tab2 = st.tabs([
    "📊  Mission Data Intelligence",
    "🚀  Advanced Flight Physics Simulator"
])


# ─────────────────────────────────────────
# TAB 1 ── MISSION DATA INTELLIGENCE
# ─────────────────────────────────────────
with tab1:

    # SIDEBAR FILTERS
    with st.sidebar:
        st.markdown("""
        <div style="margin-bottom:20px;">
            <p style="font-family:'Space Mono',monospace; font-size:0.65rem; letter-spacing:0.25em;
               color:rgba(65,217,245,0.7); text-transform:uppercase; margin-bottom:4px;">
               ⎈ Telemetry Filters
            </p>
            <div style="height:1px; background:linear-gradient(90deg,rgba(65,217,245,0.4),transparent);"></div>
        </div>
        """, unsafe_allow_html=True)

        selected_mission_type = st.selectbox(
            "Mission Architecture",
            options=["All"] + list(data['Mission Type'].unique())
        )
        selected_vehicle = st.selectbox(
            "Launch Platform",
            options=["All"] + list(data['Launch Vehicle'].unique())
        )
        min_year = int(data['Launch Year'].min())
        max_year = int(data['Launch Year'].max())
        selected_year_range = st.slider(
            "Operational Window",
            min_year, max_year, (min_year, max_year)
        )

    # Apply filters
    filtered_data = data.copy()
    if selected_mission_type != "All":
        filtered_data = filtered_data[filtered_data['Mission Type'] == selected_mission_type]
    if selected_vehicle != "All":
        filtered_data = filtered_data[filtered_data['Launch Vehicle'] == selected_vehicle]
    filtered_data = filtered_data[
        (filtered_data['Launch Year'] >= selected_year_range[0]) &
        (filtered_data['Launch Year'] <= selected_year_range[1])
    ]

    # Live record badge
    st.markdown(f"""
    <div class="filter-badge">
        <div class="pulse-dot"></div>
        Uplink Active &nbsp;—&nbsp; {len(filtered_data):,} Records Acquired
    </div>
    """, unsafe_allow_html=True)

    # ── SECTION A: MACRO METRICS ──────────────────────────
    st.markdown("""
    <div class="section-label">
        <div class="section-line"></div>
        <span class="section-title-text">01 &nbsp; Macro Launch Metrics</span>
        <div class="section-line-right"></div>
    </div>
    """, unsafe_allow_html=True)

    col_a1, col_a2 = st.columns(2, gap="medium")

    with col_a1:
        fig1 = px.scatter(
            filtered_data,
            x='Payload Weight (tons)', y='Fuel Consumption (tons)',
            color='Outcome Status',
            size='Mission Cost (billion USD)',
            hover_data=['Mission Name', 'Launch Vehicle'],
            title="Mass-to-Propellant Ratio & Mission Viability",
            color_discrete_map=color_map_status
        )
        fig1.update_layout(template=aqua_template)
        st.plotly_chart(fig1, use_container_width=True)

    with col_a2:
        cost_df = (
            filtered_data
            .groupby('Outcome Status')['Mission Cost (billion USD)']
            .sum()
            .reset_index()
        )
        fig2 = px.bar(
            cost_df,
            x='Outcome Status', y='Mission Cost (billion USD)',
            color='Outcome Status',
            title="Aggregate Financial Expenditure by Mission Outcome",
            color_discrete_map=color_map_status
        )
        fig2.update_traces(marker_line_color='rgba(255,255,255,0.1)', marker_line_width=1)
        fig2.update_layout(template=aqua_template)
        st.plotly_chart(fig2, use_container_width=True)

    col_a3, col_a4 = st.columns(2, gap="medium")

    with col_a3:
        line_data = filtered_data.sort_values(by='Distance from Earth (light-years)')
        fig3 = px.line(
            line_data,
            x='Distance from Earth (light-years)', y='Mission Duration (years)',
            markers=True,
            title="Orbital Reach: Distance Traveled vs. Operational Duration"
        )
        fig3.update_layout(template=aqua_template)
        fig3.update_traces(
            line_color='#41d9f5', line_width=2.5,
            marker=dict(size=6, color="#a8edea", line=dict(color="#41d9f5", width=1.5))
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col_a4:
        fig4 = px.box(
            filtered_data,
            x='Outcome Status', y='Crew Size',
            color='Outcome Status',
            title="Personnel Capacity Distribution Across Mission Status",
            color_discrete_map=color_map_status
        )
        fig4.update_layout(template=aqua_template)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── SECTION B: STATISTICAL DISTRIBUTIONS ──────────────
    st.markdown("""
    <div class="section-label">
        <div class="section-line"></div>
        <span class="section-title-text">02 &nbsp; Statistical Distributions</span>
        <div class="section-line-right"></div>
    </div>
    """, unsafe_allow_html=True)

    col_s1, col_s2, col_s3 = st.columns(3, gap="medium")

    mpl_face = '#0a1628'
    palette_map = {
        "Nominal (Success)": "#41d9f5",
        "Anomaly (Failure)": "#f55241"
    }

    with col_s1:
        fig_m1, ax_m1 = plt.subplots(figsize=(5, 4), facecolor=mpl_face)
        ax_m1.set_facecolor('none')
        cost_agg = filtered_data.groupby('Outcome Status')['Mission Cost (billion USD)'].mean()
        bars = ax_m1.bar(
            cost_agg.index, cost_agg.values,
            color=[palette_map.get(k, '#41d9f5') for k in cost_agg.index],
            edgecolor='rgba(255,255,255,0.1)', linewidth=0.8, width=0.5
        )
        ax_m1.set_ylabel("Avg Cost (Billion USD)", fontsize=9, color='rgba(200,230,240,0.7)')
        ax_m1.set_title("Mean Capital Expenditure", fontsize=10, color='#41d9f5', pad=10)
        ax_m1.tick_params(colors='rgba(200,230,240,0.6)', labelsize=8)
        for spine in ax_m1.spines.values():
            spine.set_edgecolor('rgba(65,217,245,0.15)')
        fig_m1.tight_layout(pad=1.5)
        st.pyplot(fig_m1)
        plt.close(fig_m1)

    with col_s2:
        fig_s1, ax_s1 = plt.subplots(figsize=(5, 4), facecolor=mpl_face)
        ax_s1.set_facecolor('none')
        sns.boxplot(
            data=filtered_data, x='Outcome Status', y='Crew Size',
            palette=palette_map, ax=ax_s1,
            linewidth=1.2, flierprops=dict(marker='o', markersize=4, alpha=0.6)
        )
        ax_s1.set_title("Crew Configuration Dispersion", fontsize=10, color='#41d9f5', pad=10)
        ax_s1.tick_params(colors='rgba(200,230,240,0.6)', labelsize=8)
        for spine in ax_s1.spines.values():
            spine.set_edgecolor('rgba(65,217,245,0.15)')
        fig_s1.tight_layout(pad=1.5)
        st.pyplot(fig_s1)
        plt.close(fig_s1)

    with col_s3:
        fig_s2, ax_s2 = plt.subplots(figsize=(5, 4), facecolor=mpl_face)
        ax_s2.set_facecolor('none')
        sns.scatterplot(
            data=filtered_data,
            x='Payload Weight (tons)', y='Fuel Consumption (tons)',
            hue='Outcome Status', palette=palette_map, ax=ax_s2,
            s=55, alpha=0.8, edgecolor='rgba(255,255,255,0.15)', linewidth=0.5
        )
        ax_s2.set_title("Propellant vs. Payload Mass", fontsize=10, color='#41d9f5', pad=10)
        ax_s2.tick_params(colors='rgba(200,230,240,0.6)', labelsize=8)
        for spine in ax_s2.spines.values():
            spine.set_edgecolor('rgba(65,217,245,0.15)')
        fig_s2.tight_layout(pad=1.5)
        st.pyplot(fig_s2)
        plt.close(fig_s2)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── SECTION C: MULTI-DIMENSIONAL ANALYTICS ────────────
    st.markdown("""
    <div class="section-label">
        <div class="section-line"></div>
        <span class="section-title-text">03 &nbsp; Multi-Dimensional Systems Analytics</span>
        <div class="section-line-right"></div>
    </div>
    """, unsafe_allow_html=True)

    fig_3d = px.scatter_3d(
        filtered_data,
        x='Distance from Earth (light-years)', y='Fuel Consumption (tons)',
        z='Payload Weight (tons)', color='Mission Success (%)',
        size='Mission Cost (billion USD)',
        hover_name='Mission Name',
        hover_data=['Launch Vehicle', 'Target Name'],
        title="3D Parameter Space: Interstellar Distance, Fuel Mass & Payload Limits",
        color_continuous_scale='Turbo',
        opacity=0.88
    )
    fig_3d.update_layout(
        template=aqua_template, height=680,
        scene=dict(
            xaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(65,217,245,0.08)"),
            yaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(65,217,245,0.08)"),
            zaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(65,217,245,0.08)")
        )
    )
    st.plotly_chart(fig_3d, use_container_width=True)

    col_b1, col_b2 = st.columns(2, gap="medium")

    with col_b1:
        num_df = filtered_data[[
            'Mission Cost (billion USD)', 'Scientific Yield (points)',
            'Crew Size', 'Mission Success (%)',
            'Fuel Consumption (tons)', 'Payload Weight (tons)',
            'Distance from Earth (light-years)'
        ]]
        fig_corr = px.imshow(
            num_df.corr(), text_auto=".2f", aspect="auto",
            color_continuous_scale='RdBu_r', origin='lower',
            title="Pearson Correlation Matrix — Mission Telemetry"
        )
        fig_corr.update_layout(template=aqua_template, height=480)
        st.plotly_chart(fig_corr, use_container_width=True)

    with col_b2:
        fig_sun = px.sunburst(
            filtered_data,
            path=['Launch Vehicle', 'Target Type', 'Mission Type'],
            values='Mission Cost (billion USD)',
            color='Mission Success (%)',
            color_continuous_scale='Teal',
            title="Hierarchical Architecture: Vehicle → Target → Mission Type"
        )
        fig_sun.update_layout(
            template=aqua_template, height=480,
            margin=dict(t=40, l=0, r=0, b=0)
        )
        st.plotly_chart(fig_sun, use_container_width=True)


# ─────────────────────────────────────────
# TAB 2 ── FLIGHT PHYSICS SIMULATOR
# ─────────────────────────────────────────
with tab2:

    st.markdown("""
    <div class="glass-card" style="border-color:rgba(65,217,245,0.2);">
        <h3 style="margin:0 0 8px 0; font-weight:300; letter-spacing:0.08em;">
            ⚙️ &nbsp; Advanced 3D Flight Physics Simulator
        </h3>
        <p style="font-family:'Space Mono',monospace; font-size:0.72rem; color:rgba(200,230,240,0.55);
           letter-spacing:0.05em; margin:0; line-height:1.7;">
            Integrates the Tsiolkovsky rocket equation · dynamic pressure (Max-Q) modelling ·
            Mach calculations for orbital trajectory generation
        </p>
    </div>
    """, unsafe_allow_html=True)

    mode = st.radio(
        "Simulation Mode",
        ["Dataset Telemetry Profiles", "Manual Engineering Override"],
        horizontal=True
    )
    st.markdown("<hr style='margin:10px 0 24px 0;'>", unsafe_allow_html=True)

    # ── MODE A: DATASET PROFILES ──────────────────────────
    if mode == "Dataset Telemetry Profiles":
        mission_names = data['Mission Name'].tolist()
        selected_mission = st.selectbox("Select Mission Telemetry Profile:", mission_names)

        m_data        = data[data['Mission Name'] == selected_mission].iloc[0]
        vehicle       = m_data['Launch Vehicle']
        v_stats       = VEHICLE_STATS.get(vehicle, {"mass_kg": 1000000, "thrust_N": 30000000, "drag": 0.4})
        init_mass     = v_stats["mass_kg"]
        thrust        = v_stats["thrust_N"]
        drag_coeff    = v_stats["drag"]
        payload_kg    = m_data['Payload Weight (tons)']  * 1000
        fuel_kg       = m_data['Fuel Consumption (tons)'] * 1000
        success_chance= m_data['Mission Success (%)']

    # ── MODE B: MANUAL OVERRIDE ───────────────────────────
    else:
        st.markdown("""
        <p style="font-family:'Space Mono',monospace; font-size:0.72rem;
           letter-spacing:0.15em; color:rgba(65,217,245,0.7); text-transform:uppercase;
           margin-bottom:16px;">
            🔧 &nbsp; Vehicle Engineering Configuration
        </p>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2, gap="medium")
        init_mass  = col1.number_input("Dry Rocket Mass (kg)",  value=1_000_000, step=50_000)
        thrust     = col2.number_input("Engine Thrust (N)",     value=35_000_000, step=1_000_000)

        col3, col4 = st.columns(2, gap="medium")
        payload_kg = col3.number_input("Payload Weight (kg)",   value=25_000,   step=1_000)
        fuel_kg    = col4.number_input("Propellant Mass (kg)",  value=2_000_000, step=100_000)

        col5, col6 = st.columns(2, gap="medium")
        drag_coeff     = col5.slider("Aerodynamic Drag Factor (Cd)", 0.1, 1.0, 0.4)
        success_chance = col6.slider("System Reliability Prob. (%)",  10,  100, 90)
        vehicle        = "Custom Prototype"

    # ── PRE-LAUNCH CALCULATIONS ───────────────────────────
    total_initial_mass = init_mass + payload_kg + fuel_kg
    initial_twr        = thrust / (total_initial_mass * 9.81)
    burn_time_est      = 120
    mass_flow_rate     = fuel_kg / burn_time_est if burn_time_est > 0 else 1
    exhaust_velocity   = thrust / mass_flow_rate if mass_flow_rate > 0 else 0
    delta_v            = (
        exhaust_velocity * np.log(total_initial_mass / (init_mass + payload_kg))
        if exhaust_velocity > 0 and (init_mass + payload_kg) > 0 else 0
    )

    col_m1, col_m2, col_m3, col_m4 = st.columns(4, gap="small")
    col_m1.metric("Launch Platform",     vehicle)
    col_m2.metric("Total Lift-off Mass", f"{total_initial_mass:,.0f} kg")
    col_m3.metric("Initial TWR",         f"{initial_twr:.2f}")
    col_m4.metric("Est. Delta-V",        f"{delta_v/1000:.2f} km/s")

    st.markdown("<br>", unsafe_allow_html=True)

    live_telemetry = st.empty()

    if st.button("🚀  INITIATE IGNITION SEQUENCE", use_container_width=True):

        dt           = 0.5
        time_steps   = 400
        gravity      = 9.81
        speed_of_sound = 343.0

        will_fail    = success_chance < np.random.uniform(0, 100)
        failure_time = np.random.randint(40, 100) if will_fail else 9999

        time_list, x_list, y_list, z_list = [], [], [], []
        status_list, mach_list, q_list    = [], [], []

        current_mass = total_initial_mass
        x, y, z      = 0.0, 0.0, 0.0
        vx, vy, vz   = 0.0, 0.0, 0.0
        status       = "Nominal"
        pitch_angle  = np.pi / 2
        azimuth_angle= np.pi / 4
        max_q        = 0.0

        progress_bar = st.progress(0)
        fuel_remaining = fuel_kg

        for t_step in range(time_steps):
            t = t_step * dt

            if t >= failure_time and will_fail and status == "Nominal":
                status = "ANOMALY — CRITICAL ENGINE FAILURE"
                thrust = 0

            if t > 10 and status == "Nominal":
                pitch_angle = max(0.1, pitch_angle - 0.006 * dt)

            if fuel_remaining > 0 and status == "Nominal":
                current_thrust = thrust
                fuel_spent     = min(mass_flow_rate * dt, fuel_remaining)
                fuel_remaining -= fuel_spent
                current_mass   -= fuel_spent
            else:
                current_thrust = 0

            air_density      = max(0.0, 1.225 * np.exp(-z / 8000))
            v_mag            = np.sqrt(vx**2 + vy**2 + vz**2)
            mach             = v_mag / speed_of_sound
            dynamic_pressure = 0.5 * air_density * v_mag**2
            if dynamic_pressure > max_q:
                max_q = dynamic_pressure

            drag_force = 0.5 * drag_coeff * air_density * v_mag**2
            dx = drag_force * (vx / v_mag) if v_mag > 0 else 0.0
            dy = drag_force * (vy / v_mag) if v_mag > 0 else 0.0
            dz = drag_force * (vz / v_mag) if v_mag > 0 else 0.0

            tx = current_thrust * np.cos(pitch_angle) * np.cos(azimuth_angle)
            ty = current_thrust * np.cos(pitch_angle) * np.sin(azimuth_angle)
            tz = current_thrust * np.sin(pitch_angle)

            if current_mass > 0:
                ax_ = (tx - dx) / current_mass
                ay_ = (ty - dy) / current_mass
                az_ = (tz - dz - current_mass * gravity) / current_mass
            else:
                ax_ = ay_ = az_ = 0.0

            vx += ax_ * dt
            vy += ay_ * dt
            vz += az_ * dt
            x  += vx  * dt
            y  += vy  * dt
            z  += vz  * dt

            current_twr = current_thrust / (current_mass * gravity) if current_mass > 0 else 0

            if t_step % 5 == 0:
                ok = status == "Nominal"
                status_color = "#41d9f5" if ok else "#f55241"
                live_telemetry.markdown(f"""
                <div class="telemetry-box">
                    <b>LIVE TELEMETRY</b> &nbsp; T+{t:.1f}s &nbsp;|&nbsp;
                    <b>Status:</b> <span style="color:{status_color}">{status}</span><br>
                    <b>ALT:</b> {z/1000:.2f} km &nbsp;·&nbsp;
                    <b>VEL:</b> {v_mag:.1f} m/s &nbsp;·&nbsp;
                    <b>MACH:</b> {mach:.2f} &nbsp;·&nbsp;
                    <b>TWR:</b> {current_twr:.2f} &nbsp;·&nbsp;
                    <b>Q:</b> {dynamic_pressure/1000:.1f} kPa
                </div>
                """, unsafe_allow_html=True)

            progress_bar.progress(min(int((t_step / time_steps) * 100), 100))

            if z <= 0 and t > 5:
                z = 0.0; vz = 0.0; vx = 0.0; vy = 0.0
                if status != "Nominal":
                    status = "CATASTROPHIC SURFACE IMPACT"
                break

            time_list.append(t)
            x_list.append(x / 1000)
            y_list.append(y / 1000)
            z_list.append(z / 1000)
            status_list.append(status)
            mach_list.append(mach)
            q_list.append(dynamic_pressure)

        progress_bar.empty()

        if will_fail:
            st.error(f"💥  {status_list[-1]} at T+{failure_time}s  ·  Max-Q: {max_q/1000:.1f} kPa")
        else:
            st.success(f"✨  ORBITAL INSERTION CONFIRMED  ·  Apogee: {z_list[-1]:.2f} km  ·  Max-Q: {max_q/1000:.1f} kPa")

        sim_df = pd.DataFrame({
            "Time (s)":       time_list,
            "Downrange (km)": x_list,
            "Crossrange (km)":y_list,
            "Altitude (km)":  z_list,
            "Status":         status_list,
            "Mach":           mach_list
        })

        # ── 3D TRAJECTORY ──────────────────────────────────
        st.markdown("""
        <div class="section-label" style="margin-top:28px;">
            <div class="section-line"></div>
            <span class="section-title-text">3D Kinematic Spatial Trajectory</span>
            <div class="section-line-right"></div>
        </div>
        """, unsafe_allow_html=True)

        fig_3d_traj = go.Figure()

        if x_list and y_list:
            gx = np.linspace(0, max(x_list) * 1.2, 5)
            gy = np.linspace(0, max(y_list) * 1.2, 5)
            fig_3d_traj.add_trace(go.Surface(
                z=np.zeros((5, 5)), x=gx, y=gy,
                colorscale='Teal', opacity=0.08,
                showscale=False, name="Ground Plane"
            ))

        fig_3d_traj.add_trace(go.Scatter3d(
            x=sim_df["Downrange (km)"],
            y=sim_df["Crossrange (km)"],
            z=sim_df["Altitude (km)"],
            mode='lines',
            line=dict(
                color=sim_df['Mach'], colorscale='Plasma', width=5,
                showscale=True,
                colorbar=dict(
                    title="Mach",
                    tickfont=dict(color='rgba(200,230,240,0.7)', size=10),
                    titlefont=dict(color='rgba(200,230,240,0.7)', size=11)
                )
            ),
            name="Flight Path"
        ))

        end_color = "#f55241" if will_fail else "#41d9f5"
        fig_3d_traj.add_trace(go.Scatter3d(
            x=[sim_df["Downrange (km)"].iloc[-1]],
            y=[sim_df["Crossrange (km)"].iloc[-1]],
            z=[sim_df["Altitude (km)"].iloc[-1]],
            mode='markers+text',
            marker=dict(size=9, color=end_color, symbol='diamond',
                        line=dict(color='white', width=1.5)),
            text=[status_list[-1]],
            textposition="top center",
            name="Terminal State"
        ))

        fig_3d_traj.update_layout(
            template=aqua_template, height=680,
            scene=dict(
                xaxis_title="Downrange (km)",
                yaxis_title="Crossrange (km)",
                zaxis_title="Altitude (km)",
                xaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(65,217,245,0.07)"),
                yaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(65,217,245,0.07)"),
                zaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(65,217,245,0.07)")
            )
        )
        st.plotly_chart(fig_3d_traj, use_container_width=True)

        # ── 2D ASCENT PROFILE ──────────────────────────────
        st.markdown("""
        <div class="section-label">
            <div class="section-line"></div>
            <span class="section-title-text">2D Ascent Profile — Altitude vs Downrange</span>
            <div class="section-line-right"></div>
        </div>
        """, unsafe_allow_html=True)

        sub_df = sim_df.iloc[::2, :].copy().reset_index(drop=True)

        fig_anim = px.scatter(
            sub_df,
            x="Downrange (km)", y="Altitude (km)",
            animation_frame="Time (s)",
            range_x=[0, sim_df['Downrange (km)'].max() + 10],
            range_y=[0, sim_df['Altitude (km)'].max() * 1.2],
            title="Cross-sectional Ascent Trajectory"
        )
        marker_colors = np.where(sub_df['Status'] == "Nominal", "#41d9f5", "#f55241")
        fig_anim.update_traces(marker=dict(
            size=14, symbol="triangle-up",
            color=marker_colors,
            line=dict(width=1.5, color="white")
        ))
        fig_anim.add_trace(go.Scatter(
            x=sim_df["Downrange (km)"], y=sim_df["Altitude (km)"],
            mode="lines",
            line=dict(color="rgba(65,217,245,0.3)", width=2, dash='dot'),
            name="Projected Path"
        ))
        fig_anim.update_layout(
            template=aqua_template,
            updatemenus=[dict(type="buttons", showactive=False)]
        )
        st.plotly_chart(fig_anim, use_container_width=True)
