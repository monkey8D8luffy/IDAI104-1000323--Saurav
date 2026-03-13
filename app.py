import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import time

# ==========================================
# 1. PAGE CONFIGURATION & GLASS OS THEME
# ==========================================
st.set_page_config(page_title="⬡ ASTRA // Orbital Intelligence", layout="wide", page_icon="⬡")

# --- LOAD GOOGLE FONTS ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=Syne+Mono&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# --- MASTER CSS: GLASS OS + WATER FLOW + MORPH ---
st.markdown("""
<style>
/* ============================================
ROOT TOKENS & BASE
============================================ */
:root {
--glass-bg:        rgba(6, 26, 46, 0.55);
--glass-border:    rgba(0, 210, 255, 0.18);
--glass-glow:      rgba(0, 210, 255, 0.08);
--water-primary:   #00d4ff;
--water-deep:      #0063a6;
--water-surface:   rgba(0, 180, 230, 0.12);
--ocean-dark:      #010c18;
--ocean-mid:       #021a2e;
--ocean-light:     #03283f;
--text-primary:    #e8f4f8;
--text-secondary:  rgba(180, 220, 240, 0.65);
--text-accent:     #00d4ff;
--success:         #00ffb3;
--danger:          #ff3b6b;
--font-display:    'Syne', sans-serif;
--font-mono:       'DM Mono', monospace;
--blur-amount:     22px;
--radius-lg:       20px;
--radius-md:       14px;
--radius-sm:       8px;
}

/* ============================================
ANIMATED DEEP OCEAN BACKGROUND
============================================ */
.stApp {
background: var(--ocean-dark);
background-image:
radial-gradient(ellipse 80% 60% at 10% 20%, rgba(0, 80, 140, 0.35) 0%, transparent 60%),
radial-gradient(ellipse 60% 80% at 90% 80%, rgba(0, 50, 110, 0.3) 0%, transparent 60%),
radial-gradient(ellipse 100% 50% at 50% 50%, rgba(0, 30, 60, 0.8) 0%, transparent 100%);
min-height: 100vh;
font-family: var(--font-display);
overflow-x: hidden;
}

/* Ambient light blobs – morphing slowly */
.stApp::before {
content: '';
position: fixed;
top: -20%;
left: -15%;
width: 55%;
height: 65%;
background: radial-gradient(circle, rgba(0, 140, 210, 0.12) 0%, transparent 70%);
border-radius: 60% 40% 70% 30% / 50% 60% 40% 50%;
animation: morphBlob1 14s ease-in-out infinite alternate;
pointer-events: none;
z-index: 0;
}
.stApp::after {
content: '';
position: fixed;
bottom: -15%;
right: -10%;
width: 50%;
height: 60%;
background: radial-gradient(circle, rgba(0, 80, 160, 0.1) 0%, transparent 70%);
border-radius: 40% 60% 30% 70% / 60% 40% 60% 40%;
animation: morphBlob2 18s ease-in-out infinite alternate;
pointer-events: none;
z-index: 0;
}

/* ============================================
MORPH KEYFRAMES
============================================ */
@keyframes morphBlob1 {
0%   { border-radius: 60% 40% 70% 30% / 50% 60% 40% 50%; transform: translate(0,0) scale(1); }
33%  { border-radius: 30% 70% 40% 60% / 40% 50% 60% 40%; transform: translate(3%,2%) scale(1.05); }
66%  { border-radius: 50% 50% 60% 40% / 60% 30% 70% 40%; transform: translate(-2%,4%) scale(0.97); }
100% { border-radius: 70% 30% 50% 50% / 30% 70% 30% 70%; transform: translate(1%,-2%) scale(1.03); }
}
@keyframes morphBlob2 {
0%   { border-radius: 40% 60% 30% 70% / 60% 40% 60% 40%; transform: translate(0,0) scale(1); }
33%  { border-radius: 70% 30% 60% 40% / 40% 60% 40% 60%; transform: translate(-3%,-2%) scale(1.07); }
66%  { border-radius: 50% 50% 40% 60% / 50% 50% 50% 50%; transform: translate(2%,-4%) scale(0.95); }
100% { border-radius: 30% 70% 70% 30% / 70% 30% 70% 30%; transform: translate(-1%,2%) scale(1.04); }
}
@keyframes waterFlow {
0%   { transform: translateX(-100%) skewX(-10deg); opacity: 0; }
20%  { opacity: 1; }
80%  { opacity: 0.7; }
100% { transform: translateX(110%) skewX(-10deg); opacity: 0; }
}
@keyframes waveRise {
0%, 100% { transform: translateY(0) scaleY(1); }
50%       { transform: translateY(-6px) scaleY(1.08); }
}
@keyframes ripplePulse {
0%   { transform: scale(1); opacity: 0.6; }
100% { transform: scale(2.8); opacity: 0; }
}
@keyframes shimmer {
0%   { background-position: -200% center; }
100% { background-position: 200% center; }
}
@keyframes glowPulse {
0%, 100% { box-shadow: 0 0 20px rgba(0,212,255,0.15), 0 0 60px rgba(0,212,255,0.05); }
50%       { box-shadow: 0 0 35px rgba(0,212,255,0.28), 0 0 80px rgba(0,212,255,0.10); }
}
@keyframes floatUp {
0%, 100% { transform: translateY(0px); }
50%       { transform: translateY(-5px); }
}
@keyframes scanLine {
0%   { top: -2px; opacity: 0.4; }
100% { top: 100%; opacity: 0; }
}
@keyframes liquidMorph {
0%,100% { border-radius: 50% 60% 40% 70% / 60% 40% 70% 40%; }
25%      { border-radius: 70% 40% 60% 50% / 40% 70% 40% 60%; }
50%      { border-radius: 40% 70% 50% 60% / 70% 40% 60% 50%; }
75%      { border-radius: 60% 50% 70% 40% / 50% 60% 50% 70%; }
}
@keyframes dropletFall {
0%   { transform: translateY(-10px) scale(0.8); opacity: 0; }
30%  { opacity: 1; }
100% { transform: translateY(300px) scale(1.1); opacity: 0; }
}

/* ============================================
WATER FLOW STRIP (decorative horizontal)
============================================ */
.water-flow-strip {
position: relative;
height: 3px;
background: linear-gradient(90deg, transparent, rgba(0,212,255,0.3), rgba(0,212,255,0.8), rgba(0,212,255,0.3), transparent);
margin: 30px 0;
overflow: hidden;
border-radius: 2px;
}
.water-flow-strip::after {
content: '';
position: absolute;
top: 0; left: 0; right: 0; bottom: 0;
background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.8) 50%, transparent 100%);
background-size: 200% 100%;
animation: shimmer 2.5s linear infinite;
}

/* ============================================
GLASS CARD SYSTEM
============================================ */
.glass-card {
background: var(--glass-bg);
backdrop-filter: blur(var(--blur-amount)) saturate(1.4);
-webkit-backdrop-filter: blur(var(--blur-amount)) saturate(1.4);
border: 1px solid var(--glass-border);
border-radius: var(--radius-lg);
padding: 28px 32px;
margin-bottom: 22px;
position: relative;
overflow: hidden;
animation: glowPulse 6s ease-in-out infinite;
transition: border-color 0.4s ease, transform 0.3s ease;
}
.glass-card::before {
content: '';
position: absolute;
top: 0; left: 0; right: 0;
height: 1px;
background: linear-gradient(90deg, transparent, rgba(0,212,255,0.6), transparent);
}
/* Subtle scan-line effect */
.glass-card::after {
content: '';
position: absolute;
left: 0; right: 0;
height: 80px;
background: linear-gradient(to bottom, transparent, rgba(0,212,255,0.03), transparent);
animation: scanLine 8s linear infinite;
pointer-events: none;
}
.glass-card:hover {
border-color: rgba(0,212,255,0.35);
transform: translateY(-2px);
}

/* Elevated card variant */
.glass-card-elevated {
background: linear-gradient(145deg, rgba(0,60,100,0.45), rgba(0,20,50,0.60));
backdrop-filter: blur(30px);
-webkit-backdrop-filter: blur(30px);
border: 1px solid rgba(0,212,255,0.25);
border-radius: var(--radius-lg);
padding: 32px 36px;
margin-bottom: 24px;
position: relative;
overflow: hidden;
box-shadow: 0 20px 60px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.05);
}

/* ============================================
HERO HEADER – WATER MORPHING TITLE
============================================ */
.hero-container {
position: relative;
text-align: center;
padding: 52px 20px 44px;
overflow: hidden;
}
.hero-bg-morph {
position: absolute;
top: 50%; left: 50%;
transform: translate(-50%, -50%);
width: 600px;
height: 200px;
background: radial-gradient(ellipse, rgba(0,140,200,0.18) 0%, transparent 70%);
animation: liquidMorph 10s ease-in-out infinite;
pointer-events: none;
}
.hero-eyebrow {
font-family: var(--font-mono);
font-size: 0.72rem;
letter-spacing: 0.35em;
color: var(--water-primary);
text-transform: uppercase;
opacity: 0.75;
margin-bottom: 14px;
}
.hero-title {
font-family: var(--font-display);
font-size: clamp(2.2rem, 5vw, 3.6rem);
font-weight: 800;
letter-spacing: -0.01em;
background: linear-gradient(135deg, #ffffff 0%, #a8dcf0 40%, #00d4ff 70%, #0090cc 100%);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
background-clip: text;
background-size: 200% 200%;
animation: shimmer 5s linear infinite;
margin-bottom: 10px;
line-height: 1.1;
}
.hero-subtitle {
font-family: var(--font-mono);
font-size: 0.82rem;
letter-spacing: 0.2em;
color: var(--text-secondary);
text-transform: uppercase;
}
/* Water droplets floating behind hero */
.droplet {
position: absolute;
width: 6px;
height: 9px;
background: radial-gradient(ellipse at 35% 30%, rgba(0,212,255,0.7), rgba(0,100,180,0.3));
border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
animation: dropletFall linear infinite;
pointer-events: none;
}

/* ============================================
TELEMETRY LIVE BOX
============================================ */
.telemetry-box {
background: linear-gradient(135deg, rgba(0,30,55,0.9), rgba(0,50,80,0.7));
backdrop-filter: blur(18px);
-webkit-backdrop-filter: blur(18px);
border: 1px solid rgba(0,212,255,0.22);
border-left: 3px solid var(--water-primary);
padding: 18px 22px;
border-radius: var(--radius-md);
font-family: var(--font-mono);
font-size: 0.82rem;
line-height: 1.7;
margin-bottom: 18px;
color: #b0ddf0;
position: relative;
overflow: hidden;
transition: border-color 0.3s;
}
.telemetry-box::after {
content: '';
position: absolute;
left: 0; right: 0; top: 0;
height: 40px;
background: linear-gradient(to bottom, rgba(0,212,255,0.04), transparent);
animation: scanLine 5s linear infinite;
pointer-events: none;
}

/* ============================================
SECTION HEADINGS
============================================ */
h1, h2, h3, h4 {
font-family: var(--font-display) !important;
color: var(--text-primary) !important;
}
h2 {
font-size: 1.35rem !important;
font-weight: 700 !important;
letter-spacing: 0.04em !important;
margin-bottom: 18px !important;
position: relative;
display: inline-block;
}
h2::after {
content: '';
display: block;
height: 2px;
width: 100%;
background: linear-gradient(90deg, var(--water-primary), transparent);
margin-top: 5px;
border-radius: 1px;
animation: waveRise 3s ease-in-out infinite;
}
h3 { font-size: 1.1rem !important; color: rgba(180,220,240,0.9) !important; }

/* ============================================
SIDEBAR – FROSTED GLASS PANEL
============================================ */
[data-testid="stSidebar"] {
background: linear-gradient(180deg, rgba(2,16,30,0.85) 0%, rgba(1,12,25,0.95) 100%) !important;
backdrop-filter: blur(30px) !important;
-webkit-backdrop-filter: blur(30px) !important;
border-right: 1px solid rgba(0,212,255,0.12) !important;
}
[data-testid="stSidebar"]::before {
content: '';
position: absolute;
top: 0; left: 0; right: 0;
height: 180px;
background: radial-gradient(ellipse at 50% 0%, rgba(0,120,200,0.12), transparent);
pointer-events: none;
}

/* ============================================
TABS – WATER SURFACE STYLE
============================================ */
.stTabs [data-baseweb="tab-list"] {
gap: 8px;
background: rgba(0,20,40,0.5);
border-radius: 14px;
padding: 6px;
border: 1px solid rgba(0,212,255,0.1);
backdrop-filter: blur(16px);
}
.stTabs [data-baseweb="tab"] {
background: transparent;
border: none !important;
border-radius: 10px !important;
padding: 10px 28px;
font-family: var(--font-display);
font-size: 0.88rem;
letter-spacing: 0.04em;
color: var(--text-secondary) !important;
transition: all 0.35s ease;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
background: linear-gradient(135deg, rgba(0,140,210,0.28), rgba(0,80,140,0.35)) !important;
border: 1px solid rgba(0,212,255,0.35) !important;
color: #ffffff !important;
box-shadow: 0 0 20px rgba(0,212,255,0.18), inset 0 1px 0 rgba(255,255,255,0.08);
}

/* ============================================
METRIC TILES – LIQUID GLASS
============================================ */
[data-testid="stMetric"] {
background: linear-gradient(145deg, rgba(0,50,90,0.45), rgba(0,25,55,0.6));
border: 1px solid rgba(0,212,255,0.18);
border-radius: var(--radius-md);
padding: 18px 20px;
transition: all 0.3s ease;
position: relative;
overflow: hidden;
animation: floatUp 5s ease-in-out infinite;
}
[data-testid="stMetric"]:nth-child(2) { animation-delay: 0.5s; }
[data-testid="stMetric"]:nth-child(3) { animation-delay: 1s; }
[data-testid="stMetric"]:nth-child(4) { animation-delay: 1.5s; }
[data-testid="stMetric"]::before {
content: '';
position: absolute;
top: 0; left: 0; right: 0;
height: 1px;
background: linear-gradient(90deg, transparent, rgba(0,212,255,0.5), transparent);
}
[data-testid="stMetric"]:hover {
border-color: rgba(0,212,255,0.4);
box-shadow: 0 8px 30px rgba(0,212,255,0.12);
transform: translateY(-2px);
}
[data-testid="stMetricLabel"] { color: var(--text-secondary) !important; font-family: var(--font-mono) !important; font-size: 0.72rem !important; letter-spacing: 0.12em !important; }
[data-testid="stMetricValue"] { color: var(--text-accent) !important; font-family: var(--font-display) !important; font-weight: 700 !important; }

/* ============================================
BUTTONS
============================================ */
.stButton > button {
background: linear-gradient(135deg, rgba(0,100,180,0.5), rgba(0,50,110,0.7)) !important;
color: #ffffff !important;
border: 1px solid rgba(0,212,255,0.4) !important;
border-radius: 12px !important;
font-family: var(--font-display) !important;
font-weight: 600 !important;
letter-spacing: 0.12em !important;
font-size: 0.85rem !important;
padding: 14px 28px !important;
transition: all 0.35s cubic-bezier(0.23,1,0.32,1) !important;
position: relative;
overflow: hidden;
backdrop-filter: blur(12px);
}
.stButton > button::after {
content: '';
position: absolute;
top: 0; left: -100%;
width: 100%; height: 100%;
background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
transition: left 0.5s ease;
}
.stButton > button:hover::after { left: 100%; }
.stButton > button:hover {
background: linear-gradient(135deg, rgba(0,140,220,0.6), rgba(0,80,160,0.8)) !important;
border-color: rgba(0,212,255,0.7) !important;
box-shadow: 0 0 30px rgba(0,212,255,0.3), 0 8px 24px rgba(0,0,0,0.4) !important;
transform: translateY(-2px) !important;
}
.stButton > button:active { transform: translateY(0px) !important; }

/* ============================================
SELECT / SLIDER / RADIO / INPUT CONTROLS
============================================ */
.stSelectbox > div > div,
.stNumberInput > div > div {
background: rgba(0,25,50,0.7) !important;
border: 1px solid rgba(0,212,255,0.2) !important;
border-radius: var(--radius-sm) !important;
color: var(--text-primary) !important;
font-family: var(--font-mono) !important;
backdrop-filter: blur(12px) !important;
transition: border-color 0.3s !important;
}
.stSelectbox > div > div:hover,
.stNumberInput > div > div:hover {
border-color: rgba(0,212,255,0.45) !important;
}
.stSlider [data-baseweb="slider"] {
margin-top: 8px;
}
.stRadio > div {
background: rgba(0,20,45,0.5);
border: 1px solid rgba(0,212,255,0.12);
border-radius: 10px;
padding: 8px 12px;
backdrop-filter: blur(10px);
}

/* ============================================
PROGRESS BAR
============================================ */
.stProgress > div > div > div {
background: linear-gradient(90deg, var(--water-deep), var(--water-primary)) !important;
border-radius: 4px;
animation: shimmer 2s linear infinite;
background-size: 200% 100%;
}
.stProgress > div > div {
background: rgba(0,30,60,0.6) !important;
border-radius: 4px;
}

/* ============================================
ALERT / SUCCESS / ERROR BOXES
============================================ */
.stSuccess, [data-testid="stAlertContainer"][data-type="success"] {
background: rgba(0,255,179,0.07) !important;
border: 1px solid rgba(0,255,179,0.3) !important;
border-radius: var(--radius-md) !important;
font-family: var(--font-mono) !important;
color: #00ffb3 !important;
}
.stError, [data-testid="stAlertContainer"][data-type="error"] {
background: rgba(255,59,107,0.07) !important;
border: 1px solid rgba(255,59,107,0.3) !important;
border-radius: var(--radius-md) !important;
font-family: var(--font-mono) !important;
color: #ff5580 !important;
}

/* ============================================
DIVIDER / HR
============================================ */
hr {
border: none !important;
height: 1px !important;
background: linear-gradient(90deg, transparent, rgba(0,212,255,0.25) 30%, rgba(0,212,255,0.5) 50%, rgba(0,212,255,0.25) 70%, transparent) !important;
margin: 40px 0 !important;
position: relative;
}

/* ============================================
GENERAL TEXT
============================================ */
p, span, div, label { color: var(--text-primary); font-family: var(--font-display); }
.stMarkdown p { color: var(--text-secondary) !important; line-height: 1.7; }

/* ============================================
SCROLLBAR
============================================ */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: rgba(0,10,25,0.8); }
::-webkit-scrollbar-thumb {
background: linear-gradient(var(--water-deep), var(--water-primary));
border-radius: 3px;
}

/* ============================================
STATUS BADGE UTILITY
============================================ */
.status-nominal {
display: inline-block;
background: rgba(0,255,179,0.12);
color: #00ffb3;
border: 1px solid rgba(0,255,179,0.35);
border-radius: 20px;
padding: 2px 12px;
font-family: var(--font-mono);
font-size: 0.78rem;
letter-spacing: 0.08em;
}
.status-anomaly {
display: inline-block;
background: rgba(255,59,107,0.12);
color: #ff5580;
border: 1px solid rgba(255,59,107,0.35);
border-radius: 20px;
padding: 2px 12px;
font-family: var(--font-mono);
font-size: 0.78rem;
letter-spacing: 0.08em;
}
/* Pulsing dot for live telemetry */
.live-dot {
display: inline-block;
width: 8px; height: 8px;
background: #00ffb3;
border-radius: 50%;
margin-right: 8px;
box-shadow: 0 0 8px #00ffb3;
animation: ripplePulse 1.8s ease-out infinite;
}

/* ============================================
WATER FLOW ANIMATION ELEMENT
============================================ */
.water-flow-anim {
position: relative;
height: 2px;
margin: 24px 0;
overflow: hidden;
border-radius: 2px;
background: rgba(0,212,255,0.06);
}
.water-flow-anim span {
position: absolute;
top: 0; left: 0;
height: 100%;
width: 60%;
background: linear-gradient(90deg, transparent, rgba(0,212,255,0.6), rgba(180,240,255,0.9), rgba(0,212,255,0.6), transparent);
border-radius: 2px;
animation: waterFlow 2.8s ease-in-out infinite;
}
.water-flow-anim span:nth-child(2) { animation-delay: 0.9s; opacity: 0.6; }
.water-flow-anim span:nth-child(3) { animation-delay: 1.8s; opacity: 0.4; }

/* ============================================
MORPH DECORATION BLOB (inline HTML usage)
============================================ */
.morph-blob {
display: inline-block;
width: 180px; height: 180px;
background: radial-gradient(circle at 40% 35%, rgba(0,180,230,0.18), rgba(0,50,120,0.08) 70%);
border: 1px solid rgba(0,212,255,0.14);
animation: liquidMorph 9s ease-in-out infinite;
pointer-events: none;
position: absolute;
}

/* ============================================
SECTION LABEL CHIP
============================================ */
.section-chip {
display: inline-block;
font-family: var(--font-mono);
font-size: 0.68rem;
letter-spacing: 0.25em;
color: var(--water-primary);
background: rgba(0,212,255,0.08);
border: 1px solid rgba(0,212,255,0.2);
border-radius: 20px;
padding: 3px 14px;
margin-bottom: 10px;
text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# HERO HEADER
# ==========================================
st.markdown("""
<div class="glass-card-elevated hero-container">
<div class="hero-bg-morph"></div>


<div class="droplet" style="left:8%;  top:10%; animation-duration:5.5s; animation-delay:0s;   opacity:0.6;"></div>
<div class="droplet" style="left:18%; top:5%;  animation-duration:7s;   animation-delay:1.2s; opacity:0.4;"></div>
<div class="droplet" style="left:75%; top:8%;  animation-duration:6.2s; animation-delay:0.6s; opacity:0.5;"></div>
<div class="droplet" style="left:88%; top:15%; animation-duration:4.8s; animation-delay:2s;   opacity:0.35;"></div>
<div class="droplet" style="left:55%; top:3%;  animation-duration:8s;   animation-delay:0.3s; opacity:0.3;"></div>

<div class="hero-eyebrow">⬡ &nbsp; ASTRA ORBITAL SYSTEMS &nbsp; ⬡</div>
<div class="hero-title">AEROSPACE COMMAND TERMINAL</div>
<div class="hero-subtitle">Orbital Telemetry &nbsp;·&nbsp; Predictive Analytics &nbsp;·&nbsp; Flight Simulation</div>

<div class="water-flow-anim" style="width:55%; margin:22px auto 0;">
<span></span><span></span><span></span>
</div>
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
    numeric_cols = ['Mission Cost (billion USD)', 'Payload Weight (tons)',
                    'Fuel Consumption (tons)', 'Mission Duration (years)',
                    'Distance from Earth (light-years)', 'Crew Size',
                    'Mission Success (%)', 'Scientific Yield (points)']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=['Payload Weight (tons)', 'Fuel Consumption (tons)'])
    df['Outcome Status'] = np.where(df['Mission Success (%)'] >= 80, 'Nominal (Success)', 'Anomaly (Failure)')
    return df

try:
    data = load_and_clean_data()
except FileNotFoundError:
    st.error("⚠️ 'space_missions_dataset.csv' not found.")
    st.stop()

VEHICLE_STATS = {
    "SLS":           {"mass_kg": 1000000, "thrust_N": 39000000, "drag": 0.4},
    "Starship":      {"mass_kg": 1200000, "thrust_N": 74000000, "drag": 0.3},
    "Falcon Heavy":  {"mass_kg": 1420000, "thrust_N": 22000000, "drag": 0.35},
    "Ariane 6":      {"mass_kg": 800000,  "thrust_N": 10000000, "drag": 0.45}
}

# ==========================================
# CHART THEME
# ==========================================
cyber_template = dict(
    layout=go.Layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#a8cfe0', family="DM Mono, monospace"),
        title=dict(font=dict(color='#00d4ff', size=14, family="Syne, sans-serif")),
        legend=dict(font=dict(color='#a8cfe0'), bgcolor='rgba(0,0,0,0)'),
        xaxis=dict(gridcolor='rgba(0,212,255,0.06)', zerolinecolor='rgba(0,212,255,0.15)',
                   linecolor='rgba(0,212,255,0.1)'),
        yaxis=dict(gridcolor='rgba(0,212,255,0.06)', zerolinecolor='rgba(0,212,255,0.15)',
                   linecolor='rgba(0,212,255,0.1)')
    )
)

color_map_status = {"Nominal (Success)": "#00ffb3", "Anomaly (Failure)": "#ff3b6b"}

plt.style.use('dark_background')
fig_rc = {
    'figure.facecolor': '#010c18',
    'axes.facecolor':   (0.0, 0.078, 0.176, 0.7),   # rgba(0,20,45,0.7)
    'axes.edgecolor':   (0.0, 0.831, 1.0,   0.2),   # rgba(0,212,255,0.2)
    'text.color':       '#a8cfe0',
    'xtick.color':      '#00d4ff',
    'ytick.color':      '#00d4ff',
    'grid.color':       (0.0, 0.831, 1.0,   0.05),  # rgba(0,212,255,0.05)
}
sns.set_theme(style="darkgrid", rc=fig_rc)


# ==========================================
# 3. TABS
# ==========================================
tab1, tab2 = st.tabs(["  📊  Mission Data Intelligence  ", "  🚀  Flight Physics Simulator  "])


# ==========================================
# TAB 1 – MISSION INTELLIGENCE
# ==========================================
with tab1:

    # Sidebar
    st.sidebar.markdown("""
<div style="text-align:center; padding: 18px 0 10px;">
<div class="section-chip">⎈ TELEMETRY FILTERS</div>
</div>
""", unsafe_allow_html=True)

    selected_mission_type = st.sidebar.selectbox("Mission Architecture", options=["All"] + list(data['Mission Type'].unique()))
    selected_vehicle      = st.sidebar.selectbox("Launch Platform",      options=["All"] + list(data['Launch Vehicle'].unique()))
    min_year, max_year    = int(data['Launch Year'].min()), int(data['Launch Year'].max())
    selected_year_range   = st.sidebar.slider("Operational Window (Years)", min_year, max_year, (min_year, max_year))

    st.sidebar.markdown("""
<div class="water-flow-anim" style="margin-top:18px;">
<span></span><span></span><span></span>
</div>
""", unsafe_allow_html=True)

    filtered_data = data.copy()
    if selected_mission_type != "All":
        filtered_data = filtered_data[filtered_data['Mission Type'] == selected_mission_type]
    if selected_vehicle != "All":
        filtered_data = filtered_data[filtered_data['Launch Vehicle'] == selected_vehicle]
    filtered_data = filtered_data[
        (filtered_data['Launch Year'] >= selected_year_range[0]) &
        (filtered_data['Launch Year'] <= selected_year_range[1])
    ]

    # Uplink status
    st.markdown(f"""
<div class="glass-card" style="padding: 16px 24px; display: flex; align-items: center; gap: 12px;">
<span class="live-dot"></span>
<span style="font-family:var(--font-mono); font-size:0.82rem; color:#a8cfe0;">
UPLINK ACTIVE &nbsp;·&nbsp; <strong style="color:#00d4ff;">{len(filtered_data)}</strong> TELEMETRY RECORDS FILTERED
</span>
</div>
""", unsafe_allow_html=True)

    # --- SECTION A: MACRO METRICS ---
    st.markdown('<div class="section-chip">01 / MACRO-LEVEL ANALYTICS</div>', unsafe_allow_html=True)
    st.markdown("<h2>Launch Performance Overview</h2>", unsafe_allow_html=True)

    col_a1, col_a2 = st.columns(2)
    with col_a1:
        fig1 = px.scatter(
            filtered_data, x='Payload Weight (tons)', y='Fuel Consumption (tons)',
            color='Outcome Status', size='Mission Cost (billion USD)',
            hover_data=['Mission Name', 'Launch Vehicle'],
            title="Mass-to-Propellant Ratio & Mission Viability",
            color_discrete_map=color_map_status
        )
        fig1.update_layout(template=cyber_template)
        st.plotly_chart(fig1, use_container_width=True)

    with col_a2:
        cost_df = filtered_data.groupby('Outcome Status')['Mission Cost (billion USD)'].sum().reset_index()
        fig2 = px.bar(
            cost_df, x='Outcome Status', y='Mission Cost (billion USD)',
            color='Outcome Status',
            title="Aggregate Financial Expenditure by Outcome",
            color_discrete_map=color_map_status
        )
        fig2.update_layout(template=cyber_template)
        st.plotly_chart(fig2, use_container_width=True)

    col_a3, col_a4 = st.columns(2)
    with col_a3:
        line_data = filtered_data.sort_values(by='Distance from Earth (light-years)')
        fig3 = px.line(
            line_data, x='Distance from Earth (light-years)', y='Mission Duration (years)',
            markers=True, title="Orbital Reach: Distance vs. Operational Duration"
        )
        fig3.update_layout(template=cyber_template)
        fig3.update_traces(line_color='#00d4ff', line_width=2.5, marker=dict(size=6, color="#ff3b6b"))
        st.plotly_chart(fig3, use_container_width=True)

    with col_a4:
        fig4 = px.box(
            filtered_data, x='Outcome Status', y='Crew Size', color='Outcome Status',
            title="Personnel Capacity Distribution by Mission Status",
            color_discrete_map=color_map_status
        )
        fig4.update_layout(template=cyber_template)
        st.plotly_chart(fig4, use_container_width=True)

    # Water-flow divider
    st.markdown("""
<div class="water-flow-anim"><span></span><span></span><span></span></div>
""", unsafe_allow_html=True)

    # --- SECTION B: STATISTICAL DISTRIBUTIONS ---
    st.markdown('<div class="section-chip">02 / STATISTICAL DISTRIBUTIONS</div>', unsafe_allow_html=True)
    st.markdown("<h2>Core Statistical Analysis (Matplotlib & Seaborn)</h2>", unsafe_allow_html=True)

    col_s1, col_s2, col_s3 = st.columns(3)

    with col_s1:
        fig_m1, ax_m1 = plt.subplots(figsize=(5, 4))
        cost_agg = filtered_data.groupby('Outcome Status')['Mission Cost (billion USD)'].mean()
        bars = ax_m1.bar(cost_agg.index, cost_agg.values, color=['#ff3b6b', '#00ffb3'], edgecolor='none', width=0.5)
        ax_m1.set_ylabel("Avg Cost (B USD)", fontsize=9)
        ax_m1.set_title("Mean Capital Expenditure per Status", fontsize=9, pad=10)
        ax_m1.spines['top'].set_visible(False)
        ax_m1.spines['right'].set_visible(False)
        fig_m1.tight_layout()
        st.pyplot(fig_m1)
        plt.close(fig_m1)

    with col_s2:
        fig_s1, ax_s1 = plt.subplots(figsize=(5, 4))
        sns.boxplot(
            data=filtered_data, x='Outcome Status', y='Crew Size',
            palette={"Nominal (Success)": "#00ffb3", "Anomaly (Failure)": "#ff3b6b"},
            ax=ax_s1, linewidth=1.2
        )
        ax_s1.set_title("Crew Configuration Dispersion", fontsize=9, pad=10)
        ax_s1.spines['top'].set_visible(False)
        ax_s1.spines['right'].set_visible(False)
        fig_s1.tight_layout()
        st.pyplot(fig_s1)
        plt.close(fig_s1)

    with col_s3:
        fig_s2, ax_s2 = plt.subplots(figsize=(5, 4))
        sns.scatterplot(
            data=filtered_data, x='Payload Weight (tons)', y='Fuel Consumption (tons)',
            hue='Outcome Status',
            palette={"Nominal (Success)": "#00ffb3", "Anomaly (Failure)": "#ff3b6b"},
            ax=ax_s2, s=40, alpha=0.8
        )
        ax_s2.set_title("Propellant vs. Payload Mass", fontsize=9, pad=10)
        ax_s2.spines['top'].set_visible(False)
        ax_s2.spines['right'].set_visible(False)
        fig_s2.tight_layout()
        st.pyplot(fig_s2)
        plt.close(fig_s2)

    # Water-flow divider
    st.markdown("""
<div class="water-flow-anim"><span></span><span></span><span></span></div>
""", unsafe_allow_html=True)

    # --- SECTION C: DEEP ORBITAL ANALYTICS ---
    st.markdown('<div class="section-chip">03 / DEEP ORBITAL ANALYTICS</div>', unsafe_allow_html=True)
    st.markdown("<h2>Multi-Dimensional Systems Analytics</h2>", unsafe_allow_html=True)

    fig_3d = px.scatter_3d(
        filtered_data,
        x='Distance from Earth (light-years)', y='Fuel Consumption (tons)', z='Payload Weight (tons)',
        color='Mission Success (%)',
        size='Mission Cost (billion USD)',
        hover_name='Mission Name',
        hover_data=['Launch Vehicle', 'Target Name'],
        title="3D Parameter Space: Interstellar Distance, Fuel Mass & Payload",
        color_continuous_scale=px.colors.sequential.Sunsetdark,
        opacity=0.88
    )
    fig_3d.update_layout(template=cyber_template, height=680, scene=dict(
        xaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(0,212,255,0.08)"),
        yaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(0,212,255,0.08)"),
        zaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(0,212,255,0.08)")
    ))
    st.plotly_chart(fig_3d, use_container_width=True)

    col_b1, col_b2 = st.columns(2)
    with col_b1:
        num_df = filtered_data[[
            'Mission Cost (billion USD)', 'Scientific Yield (points)', 'Crew Size',
            'Mission Success (%)', 'Fuel Consumption (tons)', 'Payload Weight (tons)',
            'Distance from Earth (light-years)'
        ]]
        fig_corr = px.imshow(
            num_df.corr(), text_auto=".2f", aspect="auto",
            color_continuous_scale='Picnic', origin='lower',
            title="Pearson Correlation Matrix of Mission Telemetry"
        )
        fig_corr.update_layout(template=cyber_template, height=480)
        st.plotly_chart(fig_corr, use_container_width=True)

    with col_b2:
        fig_sun = px.sunburst(
            filtered_data, path=['Launch Vehicle', 'Target Type', 'Mission Type'],
            values='Mission Cost (billion USD)', color='Mission Success (%)',
            color_continuous_scale='Plotly3',
            title="Hierarchical Architecture: Vehicle → Target → Mission"
        )
        fig_sun.update_layout(template=cyber_template, height=480, margin=dict(t=40, l=0, r=0, b=0))
        st.plotly_chart(fig_sun, use_container_width=True)


# ==========================================
# TAB 2 – FLIGHT PHYSICS SIMULATOR
# ==========================================
with tab2:

    st.markdown("""
<div class="glass-card-elevated">
<div class="section-chip">FLIGHT SIMULATION ENGINE</div>
<h3 style="margin-top:10px; margin-bottom:6px;">⚙️ Advanced 3D Flight Physics Simulator</h3>
<p style="font-family:var(--font-mono); font-size:0.8rem; color:rgba(160,210,230,0.7); line-height:1.7;">
Integrates the <strong style="color:#00d4ff;">Tsiolkovsky rocket equation</strong>,
dynamic pressure (Max-Q) modelling, and Mach calculations
for true-to-life orbital trajectory generation.
</p>
<div class="water-flow-anim" style="margin-top:16px;"><span></span><span></span><span></span></div>
</div>
""", unsafe_allow_html=True)

    mode = st.radio(
        "⚙️ Simulation Mode:",
        ["Dataset Telemetry Profiles", "Manual Engineering Override"],
        horizontal=True
    )

    st.markdown("""
<div class="water-flow-anim"><span></span><span></span><span></span></div>
""", unsafe_allow_html=True)

    # --- DATASET PROFILE MODE ---
    if mode == "Dataset Telemetry Profiles":
        mission_names    = data['Mission Name'].tolist()
        selected_mission = st.selectbox("Select Mission Telemetry Profile:", mission_names)

        m_data      = data[data['Mission Name'] == selected_mission].iloc[0]
        vehicle     = m_data['Launch Vehicle']
        v_stats     = VEHICLE_STATS.get(vehicle, {"mass_kg": 1000000, "thrust_N": 30000000, "drag": 0.4})

        init_mass      = v_stats["mass_kg"]
        thrust         = v_stats["thrust_N"]
        drag_coeff     = v_stats["drag"]
        payload_kg     = m_data['Payload Weight (tons)'] * 1000
        fuel_kg        = m_data['Fuel Consumption (tons)'] * 1000
        success_chance = m_data['Mission Success (%)']

    # --- MANUAL OVERRIDE MODE ---
    else:
        st.markdown('<div class="section-chip">🔧 ENGINEERING CONFIGURATION</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        init_mass  = col1.number_input("Dry Rocket Mass (kg)",  value=1000000, step=50000)
        thrust     = col2.number_input("Engine Thrust (N)",     value=35000000, step=1000000)
        col3, col4 = st.columns(2)
        payload_kg = col3.number_input("Payload Weight (kg)",   value=25000,   step=1000)
        fuel_kg    = col4.number_input("Propellant Mass (kg)",  value=2000000, step=100000)
        col5, col6 = st.columns(2)
        drag_coeff     = col5.slider("Aerodynamic Drag Factor (Cd)",     0.1, 1.0, 0.4)
        success_chance = col6.slider("System Reliability Prob. (%)",      10, 100,  90)
        vehicle        = "Custom Prototype"

    # Pre-launch calculations
    total_initial_mass = init_mass + payload_kg + fuel_kg
    initial_twr        = thrust / (total_initial_mass * 9.81)
    burn_time_est      = 120
    mass_flow_rate     = fuel_kg / burn_time_est
    exhaust_velocity   = thrust / mass_flow_rate if mass_flow_rate > 0 else 0
    delta_v            = exhaust_velocity * np.log(total_initial_mass / (init_mass + payload_kg)) if exhaust_velocity > 0 else 0

    # Metrics row
    st.markdown("""
<div class="water-flow-anim"><span></span><span></span><span></span></div>
""", unsafe_allow_html=True)
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("Launch Platform",       vehicle)
    col_m2.metric("Total Lift-off Mass",   f"{total_initial_mass:,.0f} kg")
    col_m3.metric("Initial TWR",           f"{initial_twr:.2f}")
    col_m4.metric("Est. Delta-V (Δv)",     f"{delta_v/1000:.2f} km/s")

    st.markdown("<br>", unsafe_allow_html=True)
    live_telemetry = st.empty()

    # --- IGNITION BUTTON ---
    if st.button("🚀  INITIATE IGNITION SEQUENCE", use_container_width=True):

        dt         = 0.5
        time_steps = 400
        gravity    = 9.81
        speed_of_sound = 343

        will_fail    = success_chance < np.random.uniform(0, 100)
        failure_time = np.random.randint(40, 100) if will_fail else 999

        time_list, x_list, y_list, z_list, status_list, mach_list, q_list = [], [], [], [], [], [], []
        current_mass = total_initial_mass

        x, y, z    = 0.0, 0.0, 0.0
        vx, vy, vz = 0.0, 0.0, 0.0
        status     = "Nominal"

        pitch_angle  = np.pi / 2
        azimuth_angle = np.pi / 4

        progress_bar = st.progress(0)
        max_q = 0

        for t_step in range(time_steps):
            t = t_step * dt

            if t >= failure_time and will_fail and status == "Nominal":
                status = "ANOMALY - CRITICAL ENGINE FAILURE"
                thrust = 0

            if t > 10 and status == "Nominal":
                pitch_angle = max(0.1, pitch_angle - 0.006 * dt)

            if fuel_kg > 0 and status == "Nominal":
                current_thrust = thrust
                fuel_spent     = min(mass_flow_rate * dt, fuel_kg)
                fuel_kg       -= fuel_spent
                current_mass  -= fuel_spent
            else:
                current_thrust = 0

            air_density      = max(0, 1.225 * np.exp(-z / 8000))
            v_mag            = np.sqrt(vx**2 + vy**2 + vz**2)
            mach             = v_mag / speed_of_sound
            dynamic_pressure = 0.5 * air_density * (v_mag ** 2)
            if dynamic_pressure > max_q:
                max_q = dynamic_pressure

            drag_force = 0.5 * drag_coeff * air_density * (v_mag ** 2)
            dx = drag_force * (vx / v_mag) if v_mag > 0 else 0
            dy = drag_force * (vy / v_mag) if v_mag > 0 else 0
            dz = drag_force * (vz / v_mag) if v_mag > 0 else 0

            tx = current_thrust * np.cos(pitch_angle) * np.cos(azimuth_angle)
            ty = current_thrust * np.cos(pitch_angle) * np.sin(azimuth_angle)
            tz = current_thrust * np.sin(pitch_angle)

            ax_ = (tx - dx) / current_mass
            ay_ = (ty - dy) / current_mass
            az_ = (tz - dz - current_mass * gravity) / current_mass

            vx += ax_ * dt; vy += ay_ * dt; vz += az_ * dt
            x  += vx * dt;  y  += vy * dt;  z  += vz * dt

            current_twr = current_thrust / (current_mass * gravity) if current_mass > 0 else 0

            if t_step % 5 == 0:
                is_nominal   = status == "Nominal"
                status_color = "#00ffb3" if is_nominal else "#ff3b6b"
                status_class = "status-nominal" if is_nominal else "status-anomaly"
                live_telemetry.markdown(f"""
                <div class="telemetry-box">
                    <span class="live-dot" style="background:{'#00ffb3' if is_nominal else '#ff3b6b'}; box-shadow:0 0 8px {'#00ffb3' if is_nominal else '#ff3b6b'};"></span>
                    <strong style="font-size:0.85rem; color:#00d4ff; letter-spacing:0.12em;">T +{t:.1f}s</strong>
                    &nbsp;&nbsp;
                    <span class="{status_class}">{status}</span>
                    <br><br>
                    <span style="color:#4a9abb;">ALT</span>&nbsp;&nbsp;<strong style="color:#e8f4f8;">{z/1000:.2f} km</strong>
                    &nbsp;&nbsp;|&nbsp;&nbsp;
                    <span style="color:#4a9abb;">VEL</span>&nbsp;&nbsp;<strong style="color:#e8f4f8;">{v_mag:.1f} m/s</strong>
                    &nbsp;&nbsp;|&nbsp;&nbsp;
                    <span style="color:#4a9abb;">MACH</span>&nbsp;&nbsp;<strong style="color:#e8f4f8;">{mach:.2f}</strong>
                    &nbsp;&nbsp;|&nbsp;&nbsp;
                    <span style="color:#4a9abb;">TWR</span>&nbsp;&nbsp;<strong style="color:#e8f4f8;">{current_twr:.2f}</strong>
                    &nbsp;&nbsp;|&nbsp;&nbsp;
                    <span style="color:#4a9abb;">Q</span>&nbsp;&nbsp;<strong style="color:#e8f4f8;">{dynamic_pressure/1000:.1f} kPa</strong>
                </div>
                """, unsafe_allow_html=True)

            if z <= 0 and t > 5:
                z = 0; vz = 0; vx = 0; vy = 0
                if status != "Nominal":
                    status = "CATASTROPHIC SURFACE IMPACT"
                break

            time_list.append(t)
            x_list.append(x / 1000);  y_list.append(y / 1000);  z_list.append(z / 1000)
            status_list.append(status);  mach_list.append(mach);  q_list.append(dynamic_pressure)

        progress_bar.empty()

        if will_fail:
            st.error(f"💥  {status_list[-1]} at T+{failure_time}s  —  Max-Q reached: {max_q/1000:.1f} kPa")
        else:
            st.success(f"✨  ORBITAL INSERTION CONFIRMED  —  Apogee: {z_list[-1]:.2f} km  ·  Max-Q: {max_q/1000:.1f} kPa")

        sim_df = pd.DataFrame({
            "Time (s)":       time_list,
            "Downrange (km)": x_list,
            "Crossrange (km)": y_list,
            "Altitude (km)":  z_list,
            "Status":         status_list,
            "Mach":           mach_list
        })

        # --- 3D TRAJECTORY ---
        st.markdown("""
<div class="section-chip" style="margin-top:24px;">🛰️ 3D KINEMATIC TRAJECTORY</div>
""", unsafe_allow_html=True)
        st.markdown("<h2>Spatial Flight Path Visualisation</h2>", unsafe_allow_html=True)

        fig_3d_traj = go.Figure()
        fig_3d_traj.add_trace(go.Surface(
            z=np.zeros((5, 5)),
            x=np.linspace(0, max(x_list) * 1.2, 5),
            y=np.linspace(0, max(y_list) * 1.2, 5),
            colorscale='Greens', opacity=0.08, showscale=False, name="Ground Plane"
        ))
        mach_vals = sim_df['Mach'].tolist()
        # Solid path line (single colour, always compatible)
        fig_3d_traj.add_trace(go.Scatter3d(
            x=sim_df["Downrange (km)"].tolist(),
            y=sim_df["Crossrange (km)"].tolist(),
            z=sim_df["Altitude (km)"].tolist(),
            mode='lines',
            line=dict(color='rgba(0,212,255,0.5)', width=4),
            name="Flight Path",
            showlegend=True
        ))
        # Invisible markers carrying the Mach colour + colorbar
        fig_3d_traj.add_trace(go.Scatter3d(
            x=sim_df["Downrange (km)"].tolist(),
            y=sim_df["Crossrange (km)"].tolist(),
            z=sim_df["Altitude (km)"].tolist(),
            mode='markers',
            marker=dict(
                size=3,
                color=mach_vals,
                colorscale='Plasma',
                showscale=True,
                colorbar=dict(
                    title=dict(text="Mach", font=dict(color='#00d4ff')),
                    tickfont=dict(color='#a8cfe0'),
                    x=1.02
                ),
                opacity=0.85
            ),
            name="Mach Profile",
            showlegend=False
        ))
        end_color = "#ff3b6b" if will_fail else "#00ffb3"
        fig_3d_traj.add_trace(go.Scatter3d(
            x=[sim_df["Downrange (km)"].iloc[-1]],
            y=[sim_df["Crossrange (km)"].iloc[-1]],
            z=[sim_df["Altitude (km)"].iloc[-1]],
            mode='markers+text',
            marker=dict(size=9, color=end_color, symbol='diamond',
                        line=dict(width=2, color='white')),
            text=[status_list[-1]], textposition="top center", name="Terminal State"
        ))
        fig_3d_traj.update_layout(
            template=cyber_template, height=680,
            scene=dict(
                xaxis_title="Downrange (km)", yaxis_title="Crossrange (km)", zaxis_title="Altitude (km)",
                xaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(0,212,255,0.07)"),
                yaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(0,212,255,0.07)"),
                zaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(0,212,255,0.07)")
            )
        )
        st.plotly_chart(fig_3d_traj, use_container_width=True)

        # --- 2D ASCENT PROFILE ---
        st.markdown("""
<div class="section-chip">📺 2D ASCENT PROFILE</div>
""", unsafe_allow_html=True)
        st.markdown("<h2>Cross-Sectional Trajectory Animation</h2>", unsafe_allow_html=True)

        sub_df     = sim_df.iloc[::2, :].copy()
        marker_clr = np.where(sub_df['Status'] == "Nominal", "#00ffb3", "#ff3b6b")
        fig_anim   = px.scatter(
            sub_df, x="Downrange (km)", y="Altitude (km)", animation_frame="Time (s)",
            range_x=[0, sim_df['Downrange (km)'].max() + 10],
            range_y=[0, sim_df['Altitude (km)'].max() * 1.2],
            title="Ascent Trajectory (Animated)"
        )
        fig_anim.update_traces(
            marker=dict(size=14, symbol="triangle-up", color=marker_clr.tolist(),
                        line=dict(width=2, color="rgba(255,255,255,0.5)"))
        )
        fig_anim.add_trace(go.Scatter(
            x=sim_df["Downrange (km)"], y=sim_df["Altitude (km)"],
            mode="lines",
            line=dict(color="rgba(0,212,255,0.35)", width=2, dash="dot"),
            name="Projected Path"
        ))
        fig_anim.update_layout(
            template=cyber_template,
            updatemenus=[dict(type="buttons", showactive=False)]
        )
        st.plotly_chart(fig_anim, use_container_width=True)
