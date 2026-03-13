import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import time

# ==========================================
# 1. PAGE CONFIGURATION & CRYSTAL GLASS OS
# ==========================================
st.set_page_config(page_title="⬡ Aether Flight OS", layout="wide", page_icon="⬡")

st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Oxanium:wght@200;300;400;600;700&family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Nunito+Sans:wght@200;300;400&display=swap" rel="stylesheet">

<style>

/* ── KEYFRAMES ── */
@keyframes waterFlow {
  0%   { background-position: 0% 50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
@keyframes morphBlob1 {
  0%,100% { border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; transform: scale(1) rotate(0deg); }
  25%      { border-radius: 30% 60% 70% 40% / 50% 60% 30% 60%; transform: scale(1.05) rotate(15deg); }
  50%      { border-radius: 50% 50% 20% 80% / 25% 80% 20% 75%; transform: scale(0.95) rotate(-10deg); }
  75%      { border-radius: 70% 30% 60% 40% / 40% 40% 60% 60%; transform: scale(1.02) rotate(5deg); }
}
@keyframes morphBlob2 {
  0%,100% { border-radius: 40% 60% 70% 30% / 40% 50% 60% 50%; transform: scale(1) rotate(0deg); }
  33%      { border-radius: 70% 30% 50% 50% / 30% 70% 40% 60%; transform: scale(1.08) rotate(-20deg); }
  66%      { border-radius: 30% 70% 30% 70% / 70% 30% 70% 30%; transform: scale(0.92) rotate(12deg); }
}
@keyframes morphBlob3 {
  0%,100% { border-radius: 50% 50% 50% 50%; transform: scale(1) rotate(0deg); }
  40%      { border-radius: 80% 20% 40% 60% / 30% 70% 40% 60%; transform: scale(1.1) rotate(25deg); }
  70%      { border-radius: 20% 80% 60% 40% / 60% 20% 80% 40%; transform: scale(0.9) rotate(-18deg); }
}
@keyframes rippleWave {
  0%   { transform: scale(0.8); opacity: 0.5; }
  100% { transform: scale(2.2); opacity: 0; }
}
@keyframes flowBorder {
  0%   { background-position: 0% 0%; }
  100% { background-position: 200% 200%; }
}
@keyframes glassShimmer {
  0%   { left: -100%; opacity: 0; }
  20%  { opacity: 0.6; }
  100% { left: 200%; opacity: 0; }
}
@keyframes floatUp {
  0%, 100% { transform: translateY(0px); }
  50%       { transform: translateY(-8px); }
}
@keyframes pulseGlow {
  0%, 100% { box-shadow: 0 0 20px rgba(100, 200, 255, 0.15), 0 0 60px rgba(100, 200, 255, 0.05); }
  50%       { box-shadow: 0 0 40px rgba(100, 200, 255, 0.3), 0 0 100px rgba(100, 200, 255, 0.12); }
}
@keyframes liquidFill {
  0%   { transform: translateY(100%); }
  100% { transform: translateY(0%); }
}
@keyframes scanLine {
  0%   { top: -5%; }
  100% { top: 105%; }
}
@keyframes borderDance {
  0%, 100% { clip-path: inset(0 0 98% 0); }
  25%       { clip-path: inset(0 0 0 98%); }
  50%       { clip-path: inset(98% 0 0 0); }
  75%       { clip-path: inset(0 98% 0 0); }
}
@keyframes fadeSlideIn {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes hueRotate {
  from { filter: hue-rotate(0deg); }
  to   { filter: hue-rotate(360deg); }
}
@keyframes waveShift {
  0%   { d: path("M0,60 C150,100 350,0 500,60 C650,120 850,20 1000,60 L1000,100 L0,100 Z"); }
  50%  { d: path("M0,40 C200,80 300,10 500,40 C700,70 800,0 1000,40 L1000,100 L0,100 Z"); }
  100% { d: path("M0,60 C150,100 350,0 500,60 C650,120 850,20 1000,60 L1000,100 L0,100 Z"); }
}

/* ── ROOT CANVAS ── */
.stApp {
  background: radial-gradient(ellipse at 20% 20%, #0a1628 0%, #060d1f 40%, #020508 100%);
  background-attachment: fixed;
  font-family: 'Nunito Sans', sans-serif;
}

/* ── MORPHING BACKGROUND BLOBS ── */
.stApp::before {
  content: '';
  position: fixed;
  top: -20%;
  left: -15%;
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(14, 80, 160, 0.18) 0%, rgba(0, 120, 200, 0.08) 50%, transparent 70%);
  animation: morphBlob1 18s ease-in-out infinite;
  z-index: 0;
  pointer-events: none;
}
.stApp::after {
  content: '';
  position: fixed;
  bottom: -20%;
  right: -10%;
  width: 700px;
  height: 700px;
  background: radial-gradient(circle, rgba(0, 160, 200, 0.12) 0%, rgba(0, 100, 160, 0.06) 50%, transparent 70%);
  animation: morphBlob2 22s ease-in-out infinite;
  z-index: 0;
  pointer-events: none;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
  background: rgba(255, 255, 255, 0.022) !important;
  backdrop-filter: blur(40px) saturate(180%);
  -webkit-backdrop-filter: blur(40px) saturate(180%);
  border-right: 1px solid rgba(150, 210, 255, 0.12);
  box-shadow: inset -1px 0 0 rgba(255,255,255,0.04), 4px 0 40px rgba(0,0,0,0.4);
}
[data-testid="stSidebar"] > div {
  padding-top: 2rem;
}
[data-testid="stSidebar"] h3 {
  font-family: 'Oxanium', sans-serif !important;
  font-weight: 600;
  letter-spacing: 0.15em;
  color: rgba(160, 210, 255, 0.9) !important;
  font-size: 0.8rem;
  text-transform: uppercase;
  margin-bottom: 1.2rem;
  padding-bottom: 0.6rem;
  border-bottom: 1px solid rgba(150, 210, 255, 0.12);
}

/* ── GLOBAL TYPE ── */
h1, h2, h3, h4 { font-family: 'Oxanium', sans-serif !important; letter-spacing: 0.06em; }
p, span, div, label { font-family: 'Nunito Sans', sans-serif; }
code, .stCode { font-family: 'Space Mono', monospace !important; }

h1 { 
  font-weight: 300 !important; 
  color: rgba(200, 235, 255, 0.95) !important;
  font-size: clamp(1.4rem, 3vw, 2.2rem) !important;
}
h2 { 
  font-weight: 300 !important; 
  color: rgba(160, 210, 255, 0.85) !important;
  font-size: 1.15rem !important;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  margin-bottom: 1.5rem !important;
}
h3 { 
  color: rgba(140, 200, 255, 0.8) !important;
  font-weight: 400 !important;
}
h4 { 
  color: rgba(180, 220, 255, 0.75) !important;
  font-weight: 300 !important;
  font-size: 0.9rem !important;
}

/* ── CRYSTAL GLASS CARD ── */
.glass-card {
  position: relative;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.055) 0%,
    rgba(255, 255, 255, 0.025) 50%,
    rgba(180, 220, 255, 0.035) 100%
  );
  backdrop-filter: blur(60px) saturate(200%) brightness(1.1);
  -webkit-backdrop-filter: blur(60px) saturate(200%) brightness(1.1);
  border-radius: 20px;
  border: 1px solid rgba(200, 230, 255, 0.13);
  padding: 28px 32px;
  margin-bottom: 24px;
  overflow: hidden;
  animation: pulseGlow 6s ease-in-out infinite, fadeSlideIn 0.6s ease-out;
  transition: transform 0.3s ease, border-color 0.3s ease;
}
.glass-card::before {
  content: '';
  position: absolute;
  top: 0; left: -100%;
  width: 60%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.06), transparent);
  animation: glassShimmer 8s ease-in-out infinite;
  pointer-events: none;
}
.glass-card::after {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  border-radius: 20px;
  background: linear-gradient(135deg, rgba(255,255,255,0.04) 0%, transparent 60%);
  pointer-events: none;
}

/* ── HERO HEADER CARD ── */
.hero-glass {
  position: relative;
  background: linear-gradient(
    160deg,
    rgba(15, 50, 100, 0.45) 0%,
    rgba(8, 30, 65, 0.55) 40%,
    rgba(5, 20, 50, 0.6) 100%
  );
  backdrop-filter: blur(80px) saturate(250%);
  -webkit-backdrop-filter: blur(80px) saturate(250%);
  border-radius: 24px;
  border-top: 1px solid rgba(200, 230, 255, 0.2);
  border-left: 1px solid rgba(200, 230, 255, 0.12);
  border-right: 1px solid rgba(80, 140, 200, 0.08);
  border-bottom: 1px solid rgba(80, 140, 200, 0.08);
  padding: 36px 40px 32px;
  margin-bottom: 28px;
  overflow: hidden;
  box-shadow:
    0 32px 80px rgba(0, 0, 0, 0.5),
    0 2px 0 rgba(255,255,255,0.08) inset,
    0 -1px 0 rgba(0,0,0,0.3) inset;
}
.hero-glass .water-wave {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 60px;
  overflow: hidden;
}
.hero-glass .water-wave svg {
  width: 200%;
  animation: waterFlow 6s linear infinite;
  background-size: 200% 200%;
}
.hero-title {
  font-family: 'Oxanium', sans-serif !important;
  font-weight: 200;
  font-size: clamp(1.6rem, 4vw, 2.8rem) !important;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: rgba(220, 240, 255, 0.95) !important;
  text-shadow: 0 0 40px rgba(100, 180, 255, 0.4), 0 2px 4px rgba(0,0,0,0.5);
  margin: 0 0 6px 0;
}
.hero-sub {
  font-family: 'Space Mono', monospace;
  font-size: 0.7rem;
  letter-spacing: 0.3em;
  color: rgba(120, 180, 230, 0.6);
  text-transform: uppercase;
}
.hero-accent-line {
  width: 60px;
  height: 1px;
  background: linear-gradient(90deg, rgba(100,180,255,0.8), transparent);
  margin: 14px 0;
}

/* ── WATER BLOB (decorative blobs inside hero) ── */
.morph-orb {
  position: absolute;
  border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
  opacity: 0.12;
  animation: morphBlob1 14s ease-in-out infinite;
  pointer-events: none;
}
.morph-orb-1 {
  top: -30px; right: -30px;
  width: 200px; height: 200px;
  background: radial-gradient(circle, rgba(0, 160, 255, 0.8), rgba(0, 100, 200, 0.4));
  animation: morphBlob1 14s ease-in-out infinite;
}
.morph-orb-2 {
  bottom: -40px; left: 10%;
  width: 150px; height: 150px;
  background: radial-gradient(circle, rgba(0, 200, 240, 0.6), rgba(0, 120, 180, 0.3));
  animation: morphBlob3 18s ease-in-out infinite;
  opacity: 0.08;
}

/* ── TELEMETRY BOX ── */
.telemetry-box {
  position: relative;
  background: linear-gradient(135deg, rgba(0, 30, 60, 0.7) 0%, rgba(0, 20, 45, 0.8) 100%);
  backdrop-filter: blur(30px);
  -webkit-backdrop-filter: blur(30px);
  border: 1px solid rgba(100, 180, 255, 0.2);
  border-left: 3px solid rgba(100, 200, 255, 0.6);
  padding: 18px 22px;
  border-radius: 10px;
  font-family: 'Space Mono', monospace;
  font-size: 0.78rem;
  color: rgba(180, 220, 255, 0.9);
  margin-bottom: 20px;
  overflow: hidden;
  line-height: 1.8;
}
.telemetry-box::before {
  content: '';
  position: absolute;
  top: 0; left: -100%;
  width: 50%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(100,200,255,0.04), transparent);
  animation: glassShimmer 4s linear infinite;
}
.scan-line {
  position: absolute;
  left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, rgba(100,200,255,0.4), transparent);
  animation: scanLine 3s linear infinite;
  pointer-events: none;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
  gap: 6px;
  background: rgba(255,255,255,0.018);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 14px 14px 0 0;
  padding: 8px 8px 0;
  border: 1px solid rgba(200,230,255,0.08);
  border-bottom: none;
}
.stTabs [data-baseweb="tab"] {
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(200,230,255,0.06);
  border-radius: 10px 10px 0 0;
  padding: 12px 28px;
  font-family: 'Oxanium', sans-serif;
  font-size: 0.78rem;
  font-weight: 400;
  letter-spacing: 0.12em;
  color: rgba(150, 200, 240, 0.6);
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}
.stTabs [data-baseweb="tab"]:hover {
  background: rgba(100, 180, 255, 0.06);
  border-color: rgba(100, 180, 255, 0.15);
  color: rgba(180, 220, 255, 0.9);
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
  background: linear-gradient(180deg, rgba(50, 120, 200, 0.18) 0%, rgba(30, 80, 150, 0.12) 100%);
  border-color: rgba(100, 180, 255, 0.25);
  border-bottom: 2px solid rgba(120, 200, 255, 0.7);
  color: rgba(200, 235, 255, 0.95);
  text-shadow: 0 0 20px rgba(100, 200, 255, 0.5);
}
.stTabs [data-baseweb="tab-panel"] {
  background: rgba(255,255,255,0.012);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(200,230,255,0.07);
  border-top: none;
  border-radius: 0 0 16px 16px;
  padding: 20px;
}

/* ── METRICS ── */
[data-testid="stMetric"] {
  background: linear-gradient(135deg, rgba(255,255,255,0.04) 0%, rgba(100,180,255,0.03) 100%);
  backdrop-filter: blur(30px);
  -webkit-backdrop-filter: blur(30px);
  border: 1px solid rgba(200,230,255,0.1);
  border-top: 1px solid rgba(200,230,255,0.18);
  border-radius: 14px;
  padding: 18px 22px !important;
  transition: transform 0.2s ease, border-color 0.2s ease;
  animation: floatUp 5s ease-in-out infinite;
}
[data-testid="stMetric"]:nth-child(2) { animation-delay: 0.8s; }
[data-testid="stMetric"]:nth-child(3) { animation-delay: 1.6s; }
[data-testid="stMetric"]:nth-child(4) { animation-delay: 2.4s; }
[data-testid="stMetric"]:hover {
  transform: translateY(-4px) !important;
  border-color: rgba(100, 200, 255, 0.25);
}
[data-testid="stMetricLabel"] {
  font-family: 'Oxanium', sans-serif !important;
  font-size: 0.65rem !important;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: rgba(130, 190, 230, 0.65) !important;
}
[data-testid="stMetricValue"] {
  font-family: 'Oxanium', sans-serif !important;
  font-weight: 300 !important;
  font-size: 1.4rem !important;
  color: rgba(210, 240, 255, 0.95) !important;
  letter-spacing: 0.04em;
}

/* ── SELECTBOX & SLIDER ── */
[data-testid="stSelectbox"] > div > div,
[data-testid="stSlider"] {
  background: rgba(255,255,255,0.025) !important;
  border-radius: 10px;
}
.stSelectbox [data-baseweb="select"] > div {
  background: rgba(10, 30, 60, 0.5) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(100, 180, 255, 0.18) !important;
  border-radius: 10px !important;
  color: rgba(180, 220, 255, 0.9) !important;
  font-family: 'Oxanium', sans-serif;
  font-size: 0.82rem;
  letter-spacing: 0.06em;
  transition: border-color 0.2s ease;
}
.stSelectbox [data-baseweb="select"] > div:hover {
  border-color: rgba(100, 200, 255, 0.35) !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
  background: rgba(100, 200, 255, 0.9) !important;
  box-shadow: 0 0 12px rgba(100,200,255,0.5) !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] div[style*="background"] {
  background: linear-gradient(90deg, rgba(50,120,200,0.6), rgba(100,200,255,0.8)) !important;
}

/* ── BUTTONS ── */
.stButton > button {
  background: linear-gradient(
    135deg,
    rgba(20, 70, 140, 0.6) 0%,
    rgba(10, 45, 100, 0.8) 50%,
    rgba(15, 60, 130, 0.6) 100%
  );
  background-size: 200% 200%;
  animation: waterFlow 4s ease-in-out infinite;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(100, 180, 255, 0.3);
  border-top: 1px solid rgba(200, 230, 255, 0.25);
  border-radius: 12px;
  color: rgba(210, 240, 255, 0.95) !important;
  font-family: 'Oxanium', sans-serif !important;
  font-weight: 600;
  font-size: 0.82rem;
  letter-spacing: 0.2em;
  padding: 14px 28px;
  text-transform: uppercase;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}
.stButton > button::before {
  content: '';
  position: absolute;
  top: 0; left: -100%;
  width: 60%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
  animation: glassShimmer 3s ease-in-out infinite;
}
.stButton > button:hover {
  background: linear-gradient(
    135deg,
    rgba(30, 100, 180, 0.7) 0%,
    rgba(20, 70, 140, 0.85) 50%,
    rgba(25, 90, 160, 0.7) 100%
  ) !important;
  border-color: rgba(120, 200, 255, 0.5) !important;
  box-shadow: 0 8px 30px rgba(60, 140, 255, 0.3), 0 0 0 1px rgba(100,200,255,0.15);
  transform: translateY(-2px);
  color: white !important;
}
.stButton > button:active {
  transform: translateY(0px);
  box-shadow: 0 4px 15px rgba(60, 140, 255, 0.2);
}

/* ── PROGRESS BAR ── */
[data-testid="stProgressBar"] > div > div {
  background: linear-gradient(90deg, rgba(30,100,200,0.7), rgba(100,200,255,0.9)) !important;
  background-size: 200% 100% !important;
  animation: waterFlow 2s ease-in-out infinite;
  border-radius: 4px;
  box-shadow: 0 0 10px rgba(100,200,255,0.4);
}
[data-testid="stProgressBar"] > div {
  background: rgba(255,255,255,0.04) !important;
  border-radius: 4px;
  border: 1px solid rgba(100,180,255,0.1);
}

/* ── RADIO ── */
[data-testid="stRadio"] > div {
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(100,180,255,0.1);
  border-radius: 12px;
  padding: 8px 12px;
}
[data-testid="stRadio"] label {
  font-family: 'Oxanium', sans-serif !important;
  font-size: 0.8rem !important;
  letter-spacing: 0.06em;
  color: rgba(160, 210, 255, 0.8) !important;
}

/* ── NUMBER INPUT ── */
[data-testid="stNumberInput"] input {
  background: rgba(10, 30, 60, 0.5) !important;
  border: 1px solid rgba(100, 180, 255, 0.18) !important;
  border-radius: 10px !important;
  color: rgba(180, 220, 255, 0.9) !important;
  font-family: 'Space Mono', monospace !important;
  font-size: 0.85rem;
}

/* ── STATUS BADGE ── */
.status-nominal {
  display: inline-block;
  background: rgba(0, 200, 150, 0.12);
  border: 1px solid rgba(0, 200, 150, 0.3);
  border-radius: 6px;
  padding: 2px 10px;
  color: rgba(0, 220, 160, 0.9);
  font-family: 'Space Mono', monospace;
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}
.status-anomaly {
  display: inline-block;
  background: rgba(255, 50, 100, 0.12);
  border: 1px solid rgba(255, 50, 100, 0.3);
  border-radius: 6px;
  padding: 2px 10px;
  color: rgba(255, 80, 120, 0.9);
  font-family: 'Space Mono', monospace;
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

/* ── SECTION DIVIDER ── */
.liquid-divider {
  position: relative;
  height: 1px;
  margin: 40px 0;
  overflow: visible;
}
.liquid-divider::before {
  content: '';
  position: absolute;
  left: 0; right: 0; top: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent 0%, rgba(100,180,255,0.3) 20%, rgba(100,200,255,0.6) 50%, rgba(100,180,255,0.3) 80%, transparent 100%);
  background-size: 200% 100%;
  animation: waterFlow 3s ease-in-out infinite;
}
.liquid-divider::after {
  content: '◈';
  position: absolute;
  top: -8px;
  left: 50%;
  transform: translateX(-50%);
  color: rgba(100, 200, 255, 0.4);
  font-size: 0.7rem;
  background: #060d1f;
  padding: 0 8px;
}

/* ── SECTION LABEL ── */
.section-label {
  font-family: 'Space Mono', monospace;
  font-size: 0.6rem;
  letter-spacing: 0.35em;
  color: rgba(100, 180, 255, 0.4);
  text-transform: uppercase;
  margin-bottom: 6px;
}

/* ── UPLINK BADGE ── */
.uplink-badge {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: rgba(0, 30, 60, 0.6);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(100,180,255,0.15);
  border-radius: 50px;
  padding: 8px 20px 8px 14px;
  font-family: 'Space Mono', monospace;
  font-size: 0.72rem;
  color: rgba(150, 210, 255, 0.8);
  letter-spacing: 0.1em;
  animation: fadeSlideIn 0.5s ease-out;
}
.uplink-dot {
  width: 8px; height: 8px;
  background: rgba(0, 220, 160, 0.9);
  border-radius: 50%;
  box-shadow: 0 0 10px rgba(0,220,160,0.6);
  animation: pulseGlow 2s ease-in-out infinite;
}

/* ── PLOTLY OVERRIDES ── */
.js-plotly-plot .plotly {
  border-radius: 12px;
  overflow: hidden;
}

/* ── ALERTS ── */
[data-testid="stAlert"] {
  backdrop-filter: blur(30px);
  border-radius: 12px;
  border-left-width: 3px;
  font-family: 'Oxanium', sans-serif;
  letter-spacing: 0.04em;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,0.02); }
::-webkit-scrollbar-thumb { background: rgba(100,180,255,0.2); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: rgba(100,200,255,0.35); }

/* ── FADE IN ANIMATION FOR SECTIONS ── */
[data-testid="stHorizontalBlock"] {
  animation: fadeSlideIn 0.5s ease-out;
}

</style>
""", unsafe_allow_html=True)

# ── HERO HEADER ──
st.markdown("""
<div class="hero-glass">
  <div class="morph-orb morph-orb-1"></div>
  <div class="morph-orb morph-orb-2"></div>
  <div class="section-label">Orbital Telemetry & Predictive Analytics Software</div>
  <div class="hero-accent-line"></div>
  <h1 class="hero-title">Aether Flight OS</h1>
  <p class="hero-sub">Mission Control &nbsp;·&nbsp; Aerospace Command Terminal &nbsp;·&nbsp; Build 4.7.1</p>
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
    "SLS": {"mass_kg": 1000000, "thrust_N": 39000000, "drag": 0.4},
    "Starship": {"mass_kg": 1200000, "thrust_N": 74000000, "drag": 0.3},
    "Falcon Heavy": {"mass_kg": 1420000, "thrust_N": 22000000, "drag": 0.35},
    "Ariane 6": {"mass_kg": 800000, "thrust_N": 10000000, "drag": 0.45}
}

# ── CRYSTAL PLOTLY THEME ──
crystal_template = dict(
    layout=go.Layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='rgba(180,220,255,0.8)', family="Nunito Sans"),
        title=dict(font=dict(color='rgba(200,235,255,0.9)', size=14, family="Oxanium"), x=0.02),
        legend=dict(
            font=dict(color='rgba(160,210,255,0.7)', size=11, family="Nunito Sans"),
            bgcolor='rgba(5,15,35,0.7)',
            bordercolor='rgba(100,180,255,0.15)',
            borderwidth=1
        ),
        xaxis=dict(
            gridcolor='rgba(100,180,255,0.06)',
            zerolinecolor='rgba(100,180,255,0.15)',
            tickfont=dict(color='rgba(130,190,230,0.6)', size=10),
            linecolor='rgba(100,180,255,0.1)'
        ),
        yaxis=dict(
            gridcolor='rgba(100,180,255,0.06)',
            zerolinecolor='rgba(100,180,255,0.15)',
            tickfont=dict(color='rgba(130,190,230,0.6)', size=10),
            linecolor='rgba(100,180,255,0.1)'
        ),
        margin=dict(l=16, r=16, t=50, b=16),
    )
)

color_map_status = {"Nominal (Success)": "#00DDA3", "Anomaly (Failure)": "#FF4878"}

plt.style.use('dark_background')
fig_rc = {
    'figure.facecolor': '#050e1e',
    'axes.facecolor': '#050e1e',
    'axes.edgecolor': 'rgba(100,180,255,0.2)',
    'text.color': 'rgba(180,220,255,0.7)',
    'xtick.color': 'rgba(130,190,230,0.5)',
    'ytick.color': 'rgba(130,190,230,0.5)',
    'axes.labelcolor': 'rgba(160,210,255,0.7)',
    'grid.color': 'rgba(100,180,255,0.06)',
}
sns.set_theme(style="darkgrid", rc=fig_rc)

# ==========================================
# 3. TABS & SIDEBAR
# ==========================================
tab1, tab2 = st.tabs(["  📊  Mission Data Intelligence  ", "  🚀  Advanced Flight Physics Simulator  "])

with tab1:
    st.sidebar.markdown("""
    <div style="margin-bottom: 8px;">
      <div class="section-label" style="margin-bottom: 12px;">⎈ &nbsp; Telemetry Filters</div>
    </div>
    """, unsafe_allow_html=True)

    selected_mission_type = st.sidebar.selectbox("Mission Architecture", options=["All"] + list(data['Mission Type'].unique()))
    selected_vehicle = st.sidebar.selectbox("Launch Platform", options=["All"] + list(data['Launch Vehicle'].unique()))
    min_year, max_year = int(data['Launch Year'].min()), int(data['Launch Year'].max())
    selected_year_range = st.sidebar.slider("Operational Window (Years)", min_year, max_year, (min_year, max_year))

    filtered_data = data.copy()
    if selected_mission_type != "All": filtered_data = filtered_data[filtered_data['Mission Type'] == selected_mission_type]
    if selected_vehicle != "All": filtered_data = filtered_data[filtered_data['Launch Vehicle'] == selected_vehicle]
    filtered_data = filtered_data[
        (filtered_data['Launch Year'] >= selected_year_range[0]) &
        (filtered_data['Launch Year'] <= selected_year_range[1])
    ]

    # Uplink badge
    st.markdown(f"""
    <div style="margin-bottom: 24px;">
      <div class="uplink-badge">
        <span class="uplink-dot"></span>
        Uplink Active &nbsp;·&nbsp; <strong>{len(filtered_data)}</strong> &nbsp;Records Filtered
      </div>
    </div>
    """, unsafe_allow_html=True)

    # --- PART A: EXECUTIVE SUMMARY ---
    st.markdown('<div class="section-label">Section 01</div>', unsafe_allow_html=True)
    st.markdown("<h2>Macro-Level Launch Metrics</h2>", unsafe_allow_html=True)

    col_a1, col_a2 = st.columns(2, gap="medium")
    with col_a1:
        fig1 = px.scatter(
            filtered_data, x='Payload Weight (tons)', y='Fuel Consumption (tons)',
            color='Outcome Status', size='Mission Cost (billion USD)',
            hover_data=['Mission Name', 'Launch Vehicle'],
            title="Mass-to-Propellant Ratio & Mission Viability",
            color_discrete_map=color_map_status
        )
        fig1.update_layout(template=crystal_template)
        st.plotly_chart(fig1, use_container_width=True)

    with col_a2:
        cost_df = filtered_data.groupby('Outcome Status')['Mission Cost (billion USD)'].sum().reset_index()
        fig2 = px.bar(
            cost_df, x='Outcome Status', y='Mission Cost (billion USD)',
            color='Outcome Status', title="Aggregate Financial Expenditure by Outcome",
            color_discrete_map=color_map_status
        )
        fig2.update_layout(template=crystal_template)
        st.plotly_chart(fig2, use_container_width=True)

    col_a3, col_a4 = st.columns(2, gap="medium")
    with col_a3:
        line_data = filtered_data.sort_values(by='Distance from Earth (light-years)')
        fig3 = px.line(
            line_data, x='Distance from Earth (light-years)', y='Mission Duration (years)',
            markers=True, title="Orbital Reach: Distance vs. Operational Duration"
        )
        fig3.update_layout(template=crystal_template)
        fig3.update_traces(line_color='rgba(80,170,255,0.8)', line_width=2.5,
                           marker=dict(size=6, color="rgba(100,200,255,0.9)",
                                       line=dict(width=1, color='rgba(255,255,255,0.2)')))
        st.plotly_chart(fig3, use_container_width=True)

    with col_a4:
        fig4 = px.box(
            filtered_data, x='Outcome Status', y='Crew Size',
            color='Outcome Status', title="Personnel Capacity Distribution",
            color_discrete_map=color_map_status
        )
        fig4.update_layout(template=crystal_template)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown('<div class="liquid-divider"></div>', unsafe_allow_html=True)

    # --- PART B: CORE STATISTICAL ANALYSIS ---
    st.markdown('<div class="section-label">Section 02</div>', unsafe_allow_html=True)
    st.markdown("<h2>Core Statistical Distributions</h2>", unsafe_allow_html=True)

    col_s1, col_s2, col_s3 = st.columns(3, gap="medium")
    plt_bg = '#050e1e'

    with col_s1:
        fig_m1, ax_m1 = plt.subplots(figsize=(5, 4), facecolor=plt_bg)
        ax_m1.set_facecolor(plt_bg)
        cost_agg = filtered_data.groupby('Outcome Status')['Mission Cost (billion USD)'].mean()
        bars = ax_m1.bar(
            cost_agg.index, cost_agg.values,
            color=['rgba(255,72,120,0.7)', 'rgba(0,221,163,0.7)'],
            edgecolor=['rgba(255,72,120,0.4)', 'rgba(0,221,163,0.4)'],
            linewidth=1.5, width=0.5
        )
        ax_m1.set_ylabel("Avg Cost (Billion USD)", fontsize=9, color='rgba(160,210,255,0.6)')
        ax_m1.set_title("Mean Capital Expenditure", fontsize=10, color='rgba(200,235,255,0.8)', pad=12)
        ax_m1.spines[:].set_color('rgba(100,180,255,0.1)')
        plt.tight_layout()
        st.pyplot(fig_m1)

    with col_s2:
        fig_s1, ax_s1 = plt.subplots(figsize=(5, 4), facecolor=plt_bg)
        ax_s1.set_facecolor(plt_bg)
        sns.boxplot(
            data=filtered_data, x='Outcome Status', y='Crew Size',
            palette={"Nominal (Success)": "#00DDA3", "Anomaly (Failure)": "#FF4878"},
            ax=ax_s1, linewidth=1.2
        )
        ax_s1.set_title("Crew Configuration Dispersion", fontsize=10, color='rgba(200,235,255,0.8)', pad=12)
        ax_s1.spines[:].set_color('rgba(100,180,255,0.1)')
        plt.tight_layout()
        st.pyplot(fig_s1)

    with col_s3:
        fig_s2, ax_s2 = plt.subplots(figsize=(5, 4), facecolor=plt_bg)
        ax_s2.set_facecolor(plt_bg)
        sns.scatterplot(
            data=filtered_data, x='Payload Weight (tons)', y='Fuel Consumption (tons)',
            hue='Outcome Status',
            palette={"Nominal (Success)": "#00DDA3", "Anomaly (Failure)": "#FF4878"},
            ax=ax_s2, alpha=0.8, s=40, linewidth=0
        )
        ax_s2.set_title("Propellant vs. Payload Mass", fontsize=10, color='rgba(200,235,255,0.8)', pad=12)
        ax_s2.spines[:].set_color('rgba(100,180,255,0.1)')
        ax_s2.legend(fontsize=8, framealpha=0.2, edgecolor='rgba(100,180,255,0.2)')
        plt.tight_layout()
        st.pyplot(fig_s2)

    st.markdown('<div class="liquid-divider"></div>', unsafe_allow_html=True)

    # --- PART C: DEEP ORBITAL ANALYTICS ---
    st.markdown('<div class="section-label">Section 03</div>', unsafe_allow_html=True)
    st.markdown("<h2>Multi-Dimensional Systems Analytics</h2>", unsafe_allow_html=True)

    fig_3d = px.scatter_3d(
        filtered_data,
        x='Distance from Earth (light-years)', y='Fuel Consumption (tons)', z='Payload Weight (tons)',
        color='Mission Success (%)', size='Mission Cost (billion USD)',
        hover_name='Mission Name', hover_data=['Launch Vehicle', 'Target Name'],
        title="3D Parameter Space: Interstellar Distance, Fuel Mass & Payload",
        color_continuous_scale=[[0, "#FF4878"], [0.5, "#4B8FFF"], [1, "#00DDA3"]],
        opacity=0.85
    )
    fig_3d.update_layout(
        template=crystal_template, height=680,
        scene=dict(
            xaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(100,180,255,0.07)", showbackground=True),
            yaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(100,180,255,0.07)", showbackground=True),
            zaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(100,180,255,0.07)", showbackground=True),
            bgcolor="rgba(4,10,25,0.0)"
        )
    )
    st.plotly_chart(fig_3d, use_container_width=True)

    col_b1, col_b2 = st.columns(2, gap="medium")
    with col_b1:
        num_df = filtered_data[[
            'Mission Cost (billion USD)', 'Scientific Yield (points)', 'Crew Size',
            'Mission Success (%)', 'Fuel Consumption (tons)', 'Payload Weight (tons)',
            'Distance from Earth (light-years)'
        ]]
        fig_corr = px.imshow(
            num_df.corr(), text_auto=".2f", aspect="auto",
            color_continuous_scale=[[0, "#FF4878"], [0.5, "#0A1628"], [1, "#00DDA3"]],
            origin='lower', title="Pearson Correlation Matrix"
        )
        fig_corr.update_layout(template=crystal_template, height=480)
        st.plotly_chart(fig_corr, use_container_width=True)

    with col_b2:
        fig_sun = px.sunburst(
            filtered_data,
            path=['Launch Vehicle', 'Target Type', 'Mission Type'],
            values='Mission Cost (billion USD)',
            color='Mission Success (%)',
            color_continuous_scale=[[0, "#FF4878"], [0.5, "#4B8FFF"], [1, "#00DDA3"]],
            title="Hierarchical Mission Architecture"
        )
        fig_sun.update_layout(
            template=crystal_template, height=480,
            margin=dict(t=50, l=0, r=0, b=0)
        )
        st.plotly_chart(fig_sun, use_container_width=True)

# ==========================================
# TAB 2: FLIGHT SIMULATOR
# ==========================================
with tab2:
    st.markdown("""
    <div class="glass-card" style="margin-bottom: 28px;">
      <div class="morph-orb" style="top:-60px; right:-40px; width:180px; height:180px; background:radial-gradient(circle, rgba(0,120,255,0.15), transparent); animation:morphBlob2 16s ease-in-out infinite; opacity:1;"></div>
      <div class="section-label">Advanced Simulation Module</div>
      <h3 style="margin: 8px 0 6px; font-size:1.1rem;">⚙️ &nbsp; Flight Physics Simulator</h3>
      <p style="font-size:0.82rem; color:rgba(150,200,240,0.6); font-family:'Nunito Sans',sans-serif; line-height:1.6; margin:0;">
        Integrates the Tsiolkovsky rocket equation, dynamic pressure (Max-Q) modeling,
        and Mach calculations for true-to-life orbital trajectory generation.
      </p>
    </div>
    """, unsafe_allow_html=True)

    mode = st.radio("⚙️  Simulation Mode:", ["Dataset Telemetry Profiles", "Manual Engineering Override"], horizontal=True)
    st.markdown('<div class="liquid-divider" style="margin: 16px 0 24px;"></div>', unsafe_allow_html=True)

    if mode == "Dataset Telemetry Profiles":
        mission_names = data['Mission Name'].tolist()
        selected_mission = st.selectbox("Select Mission Telemetry Profile:", mission_names)

        m_data = data[data['Mission Name'] == selected_mission].iloc[0]
        vehicle = m_data['Launch Vehicle']
        v_stats = VEHICLE_STATS.get(vehicle, {"mass_kg": 1000000, "thrust_N": 30000000, "drag": 0.4})

        init_mass = v_stats["mass_kg"]
        thrust = v_stats["thrust_N"]
        drag_coeff = v_stats["drag"]
        payload_kg = m_data['Payload Weight (tons)'] * 1000
        fuel_kg = m_data['Fuel Consumption (tons)'] * 1000
        success_chance = m_data['Mission Success (%)']

    else:
        st.markdown("""
        <div class="glass-card" style="padding: 20px 24px; margin-bottom: 20px;">
          <div class="section-label" style="margin-bottom:12px;">Vehicle Engineering Configuration</div>
        </div>
        """, unsafe_allow_html=True)
        col1, col2 = st.columns(2, gap="medium")
        init_mass = col1.number_input("Dry Rocket Mass (kg)", value=1000000, step=50000)
        thrust = col2.number_input("Engine Thrust (N)", value=35000000, step=1000000)
        col3, col4 = st.columns(2, gap="medium")
        payload_kg = col3.number_input("Payload Weight (kg)", value=25000, step=1000)
        fuel_kg = col4.number_input("Propellant Mass (kg)", value=2000000, step=100000)
        col5, col6 = st.columns(2, gap="medium")
        drag_coeff = col5.slider("Aerodynamic Drag Factor (Cd)", 0.1, 1.0, 0.4)
        success_chance = col6.slider("System Reliability Prob. (%)", 10, 100, 90)
        vehicle = "Custom Prototype"

    # Pre-Launch Calculations
    total_initial_mass = init_mass + payload_kg + fuel_kg
    initial_twr = thrust / (total_initial_mass * 9.81)
    burn_time_est = 120
    mass_flow_rate = fuel_kg / burn_time_est
    exhaust_velocity = thrust / mass_flow_rate if mass_flow_rate > 0 else 0
    delta_v = exhaust_velocity * np.log(total_initial_mass / (init_mass + payload_kg)) if exhaust_velocity > 0 else 0

    st.markdown('<div class="section-label" style="margin-bottom:10px;">Pre-Launch Orbital Mechanics</div>', unsafe_allow_html=True)
    col_m1, col_m2, col_m3, col_m4 = st.columns(4, gap="medium")
    col_m1.metric("Launch Platform", vehicle)
    col_m2.metric("Total Lift-off Mass", f"{total_initial_mass:,.0f} kg")
    col_m3.metric("Initial TWR", f"{initial_twr:.2f}")
    col_m4.metric("Est. Delta-V (Δv)", f"{delta_v/1000:.2f} km/s")

    st.markdown("<br>", unsafe_allow_html=True)
    live_telemetry = st.empty()

    if st.button("⬡  INITIATE IGNITION SEQUENCE", use_container_width=True):
        dt = 0.5
        time_steps = 400
        gravity = 9.81
        speed_of_sound = 343

        will_fail = success_chance < np.random.uniform(0, 100)
        failure_time = np.random.randint(40, 100) if will_fail else 999

        time_list, x_list, y_list, z_list, status_list, mach_list, q_list = [], [], [], [], [], [], []
        current_mass = total_initial_mass

        x, y, z = 0.0, 0.0, 0.0
        vx, vy, vz = 0.0, 0.0, 0.0
        status = "Nominal"

        pitch_angle = np.pi / 2
        azimuth_angle = np.pi / 4

        progress_bar = st.progress(0)
        max_q = 0

        for t_step in range(time_steps):
            t = t_step * dt

            if t >= failure_time and will_fail and status == "Nominal":
                status = "ANOMALY — CRITICAL ENGINE FAILURE"
                thrust = 0

            if t > 10 and status == "Nominal":
                pitch_angle = max(0.1, pitch_angle - 0.006 * dt)

            if fuel_kg > 0 and status == "Nominal":
                current_thrust = thrust
                fuel_spent = min(mass_flow_rate * dt, fuel_kg)
                fuel_kg -= fuel_spent
                current_mass -= fuel_spent
            else:
                current_thrust = 0

            air_density = max(0, 1.225 * np.exp(-z / 8000))
            v_mag = np.sqrt(vx**2 + vy**2 + vz**2)
            mach = v_mag / speed_of_sound
            dynamic_pressure = 0.5 * air_density * (v_mag ** 2)
            if dynamic_pressure > max_q: max_q = dynamic_pressure

            drag_force = 0.5 * drag_coeff * air_density * (v_mag ** 2)
            dx = drag_force * (vx / v_mag) if v_mag > 0 else 0
            dy = drag_force * (vy / v_mag) if v_mag > 0 else 0
            dz = drag_force * (vz / v_mag) if v_mag > 0 else 0

            tx = current_thrust * np.cos(pitch_angle) * np.cos(azimuth_angle)
            ty = current_thrust * np.cos(pitch_angle) * np.sin(azimuth_angle)
            tz = current_thrust * np.sin(pitch_angle)

            ax_val = (tx - dx) / current_mass
            ay_val = (ty - dy) / current_mass
            az_val = (tz - dz - current_mass * gravity) / current_mass

            vx += ax_val * dt
            vy += ay_val * dt
            vz += az_val * dt
            x += vx * dt
            y += vy * dt
            z += vz * dt

            current_twr = current_thrust / (current_mass * gravity) if current_mass > 0 else 0

            if t_step % 5 == 0:
                status_color = "#00DDA3" if status == "Nominal" else "#FF4878"
                status_class = "nominal" if status == "Nominal" else "anomaly"
                live_telemetry.markdown(f"""
                <div class="telemetry-box">
                  <div class="scan-line"></div>
                  <span style="color:rgba(100,180,255,0.5); font-size:0.65rem; letter-spacing:0.2em;">LIVE TELEMETRY</span>
                  &nbsp; T+{t:.1f}s &nbsp;
                  <span class="status-{status_class}">{status}</span>
                  <br>
                  <span style="color:rgba(130,190,230,0.5);">ALT</span> {z/1000:.2f} km &nbsp;|&nbsp;
                  <span style="color:rgba(130,190,230,0.5);">VEL</span> {v_mag:.1f} m/s &nbsp;|&nbsp;
                  <span style="color:rgba(130,190,230,0.5);">MACH</span> {mach:.2f} &nbsp;|&nbsp;
                  <span style="color:rgba(130,190,230,0.5);">TWR</span> {current_twr:.2f} &nbsp;|&nbsp;
                  <span style="color:rgba(130,190,230,0.5);">DYN-Q</span> {dynamic_pressure/1000:.1f} kPa
                </div>
                """, unsafe_allow_html=True)

            progress_bar.progress(min(t_step / time_steps, 1.0))

            if z <= 0 and t > 5:
                z = 0; vz = 0; vx = 0; vy = 0
                if status != "Nominal": status = "CATASTROPHIC SURFACE IMPACT"
                break

            time_list.append(t); x_list.append(x / 1000); y_list.append(y / 1000); z_list.append(z / 1000)
            status_list.append(status); mach_list.append(mach); q_list.append(dynamic_pressure)

        progress_bar.empty()
        if will_fail:
            st.error(f"💥  {status_list[-1]}  ·  T+{failure_time}s  ·  Max-Q: {max_q/1000:.1f} kPa")
        else:
            st.success(f"⬡  ORBITAL INSERTION CONFIRMED  ·  Apogee: {z_list[-1]:.2f} km  ·  Max-Q: {max_q/1000:.1f} kPa")

        sim_df = pd.DataFrame({
            "Time (s)": time_list, "Downrange (km)": x_list,
            "Crossrange (km)": y_list, "Altitude (km)": z_list,
            "Status": status_list, "Mach": mach_list
        })

        # --- 3D Trajectory ---
        st.markdown('<div class="section-label" style="margin: 28px 0 8px;">3D Kinematic Spatial Trajectory</div>', unsafe_allow_html=True)
        st.markdown("<h3>🛰️ &nbsp; Orbital Flight Path Visualization</h3>", unsafe_allow_html=True)

        fig_3d_traj = go.Figure()
        fig_3d_traj.add_trace(go.Surface(
            z=np.zeros((5, 5)),
            x=np.linspace(0, max(x_list) * 1.2, 5),
            y=np.linspace(0, max(y_list) * 1.2, 5),
            colorscale=[[0, 'rgba(0,60,30,0.15)'], [1, 'rgba(0,100,50,0.08)']],
            opacity=0.15, showscale=False, name="Ground Plane"
        ))
        fig_3d_traj.add_trace(go.Scatter3d(
            x=sim_df["Downrange (km)"], y=sim_df["Crossrange (km)"], z=sim_df["Altitude (km)"],
            mode='lines',
            line=dict(color=sim_df['Mach'], colorscale='Plasma', width=5,
                      showscale=True, colorbar=dict(title="Mach", thickness=12,
                      tickfont=dict(color='rgba(160,210,255,0.7)', size=9),
                      titlefont=dict(color='rgba(160,210,255,0.7)', size=10))),
            name="Flight Path"
        ))
        end_color = "#FF4878" if will_fail else "#00DDA3"
        fig_3d_traj.add_trace(go.Scatter3d(
            x=[sim_df["Downrange (km)"].iloc[-1]],
            y=[sim_df["Crossrange (km)"].iloc[-1]],
            z=[sim_df["Altitude (km)"].iloc[-1]],
            mode='markers+text',
            marker=dict(size=8, color=end_color, symbol='diamond',
                        line=dict(width=2, color='rgba(255,255,255,0.4)')),
            text=[status_list[-1]], textposition="top center",
            textfont=dict(color=end_color, size=10, family="Oxanium"),
            name="Terminal State"
        ))
        fig_3d_traj.update_layout(
            template=crystal_template, height=680,
            scene=dict(
                xaxis_title="Downrange (km)", yaxis_title="Crossrange (km)", zaxis_title="Altitude (km)",
                xaxis=dict(backgroundcolor="rgba(0,5,20,0.0)", gridcolor="rgba(100,180,255,0.08)", showbackground=True),
                yaxis=dict(backgroundcolor="rgba(0,5,20,0.0)", gridcolor="rgba(100,180,255,0.08)", showbackground=True),
                zaxis=dict(backgroundcolor="rgba(0,5,20,0.0)", gridcolor="rgba(100,180,255,0.08)", showbackground=True),
                bgcolor="rgba(0,0,0,0)"
            )
        )
        st.plotly_chart(fig_3d_traj, use_container_width=True)

        # --- 2D Ascent Profile ---
        st.markdown('<div class="section-label" style="margin: 28px 0 8px;">2D Ascent Profile</div>', unsafe_allow_html=True)
        st.markdown("<h3>📺 &nbsp; Altitude vs. Downrange — Animated Trajectory</h3>", unsafe_allow_html=True)

        fig_anim = px.scatter(
            sim_df.iloc[::2, :].copy(),
            x="Downrange (km)", y="Altitude (km)",
            animation_frame="Time (s)",
            range_x=[0, sim_df['Downrange (km)'].max() + 10],
            range_y=[0, sim_df['Altitude (km)'].max() * 1.2],
            title="Cross-sectional Ascent Trajectory"
        )
        fig_anim.update_traces(marker=dict(
            size=14, symbol="triangle-up",
            color=np.where(sim_df.iloc[::2, :]['Status'] == "Nominal", "#00DDA3", "#FF4878"),
            line=dict(width=1.5, color="rgba(255,255,255,0.3)")
        ))
        fig_anim.add_trace(go.Scatter(
            x=sim_df["Downrange (km)"], y=sim_df["Altitude (km)"],
            mode="lines",
            line=dict(color="rgba(80,170,255,0.3)", width=1.5, dash="dot"),
            name="Projected Path"
        ))
        fig_anim.update_layout(
            template=crystal_template,
            updatemenus=[dict(type="buttons", showactive=False,
                              buttons=[dict(label="▶", method="animate")])]
        )
        st.plotly_chart(fig_anim, use_container_width=True)
