import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_lottie import st_lottie
import requests
import time

# ==========================================
# 1. PAGE CONFIGURATION & THEME
# ==========================================
st.set_page_config(page_title="🚀 Aerospace Data Insights", layout="wide", page_icon="🌌")

# Custom CSS for Rocket Theme
st.markdown("""
    <style>
    .main {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    h1, h2, h3 {
        color: #58a6ff;
        font-family: 'Courier New', Courier, monospace;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #161b22;
        border-radius: 4px;
        padding: 10px 20px;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Lottie Animation Function (Rocket Loading)
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

lottie_rocket = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_jzzvxt.json")

# Display Loading Animation 
with st.spinner("Igniting Engines & Loading Dashboard..."):
    time.sleep(1) # Simulated load time
    
# Title
col1, col2 = st.columns([1, 4])
with col1:
    if lottie_rocket:
        st_lottie(lottie_rocket, height=120, key="rocket")
with col2:
    st.title("🚀 Space Rocket Paths & Mission Data Dashboard")
    st.markdown("*Aerospace Data Insights Project*")

# ==========================================
# 2. DATA LOADING & PREPROCESSING
# ==========================================
@st.cache_data
def load_and_clean_data():
    # Load dataset
    df = pd.read_csv("space_missions_dataset.csv")
    
    # Preprocessing
    df['Launch Date'] = pd.to_datetime(df['Launch Date'], errors='coerce')
    df['Launch Year'] = df['Launch Date'].dt.year
    
    # Ensure numeric columns
    numeric_cols = ['Mission Cost (billion USD)', 'Payload Weight (tons)', 
                    'Fuel Consumption (tons)', 'Mission Duration (years)', 
                    'Distance from Earth (light-years)', 'Crew Size', 
                    'Mission Success (%)', 'Scientific Yield (points)']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    # Drop rows with critical missing values
    df = df.dropna(subset=['Payload Weight (tons)', 'Fuel Consumption (tons)'])
    
    # Create Success/Failure Categorization based on threshold (e.g., >80% = Success)
    df['Outcome Status'] = np.where(df['Mission Success (%)'] >= 80, 'Success', 'Failure')
    
    return df

try:
    data = load_and_clean_data()
except FileNotFoundError:
    st.error("⚠️ 'space_missions_dataset.csv' not found. Please ensure the dataset is in the same directory as app.py.")
    st.stop()

# ==========================================
# 3. SIDEBAR CONTROLS & FILTERS
# ==========================================
st.sidebar.header("🎛️ Mission Filters")

# Selectboxes
selected_mission_type = st.sidebar.selectbox("Mission Type", options=["All"] + list(data['Mission Type'].unique()))
selected_vehicle = st.sidebar.selectbox("Launch Vehicle", options=["All"] + list(data['Launch Vehicle'].unique()))

# Slider 
min_year, max_year = int(data['Launch Year'].min()), int(data['Launch Year'].max())
selected_year_range = st.sidebar.slider("Launch Year Range", min_value=min_year, max_value=max_year, value=(min_year, max_year))

# Filter Data
filtered_data = data.copy()
if selected_mission_type != "All":
    filtered_data = filtered_data[filtered_data['Mission Type'] == selected_mission_type]
if selected_vehicle != "All":
    filtered_data = filtered_data[filtered_data['Launch Vehicle'] == selected_vehicle]
filtered_data = filtered_data[(filtered_data['Launch Year'] >= selected_year_range[0]) & (filtered_data['Launch Year'] <= selected_year_range[1])]

# ==========================================
# 4. TABS: DASHBOARD vs SIMULATION
# ==========================================
tab1, tab2 = st.tabs(["📊 Mission Dashboard", "🚀 Rocket Physics Simulation"])

with tab1:
    st.subheader(f"Analyzing {len(filtered_data)} Missions")
    
    col_a, col_b = st.columns(2)
    
    # 1. Scatter Plot: Payload vs Fuel (Plotly)
    with col_a:
        st.markdown("### Payload Weight vs Fuel Consumption")
        fig1 = px.scatter(filtered_data, x='Payload Weight (tons)', y='Fuel Consumption (tons)',
                          color='Outcome Status', size='Mission Cost (billion USD)',
                          hover_data=['Mission Name', 'Launch Vehicle'],
                          color_discrete_map={"Success": "#00CC96", "Failure": "#EF553B"})
        fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
        st.plotly_chart(fig1, use_container_width=True)

    # 2. Bar Chart: Mission Cost: Success vs Failure (Plotly)
    with col_b:
        st.markdown("### Total Mission Cost (Success vs Failure)")
        cost_df = filtered_data.groupby('Outcome Status')['Mission Cost (billion USD)'].sum().reset_index()
        fig2 = px.bar(cost_df, x='Outcome Status', y='Mission Cost (billion USD)', 
                      color='Outcome Status', color_discrete_map={"Success": "#00CC96", "Failure": "#EF553B"})
        fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
        st.plotly_chart(fig2, use_container_width=True)

    col_c, col_d = st.columns(2)
    
    # 3. Line Chart: Mission Duration vs Distance (Now Plotly!)
    with col_c:
        st.markdown("### Mission Duration vs Distance from Earth")
        # Sorting is important for line charts so the line flows correctly
        line_data = filtered_data.sort_values(by='Distance from Earth (light-years)')
        fig3 = px.line(line_data, x='Distance from Earth (light-years)', y='Mission Duration (years)', markers=True)
        fig3.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
        fig3.update_traces(line_color='#636EFA', line_width=2)
        st.plotly_chart(fig3, use_container_width=True)

    # 4. Box Plot: Crew Size vs Mission Success % (Now Plotly!)
    with col_d:
        st.markdown("### Crew Size Distribution per Outcome")
        fig4 = px.box(filtered_data, x='Outcome Status', y='Crew Size', 
                      color='Outcome Status', color_discrete_map={"Success": "#00CC96", "Failure": "#EF553B"})
        fig4.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
        st.plotly_chart(fig4, use_container_width=True)

    # 5. Scatter Plot: Scientific Yield vs Mission Cost
    st.markdown("### Scientific Yield vs Mission Cost")
    fig5 = px.scatter(filtered_data, x='Mission Cost (billion USD)', y='Scientific Yield (points)',
                      color='Mission Type', hover_data=['Target Name'])
    fig5.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
    st.plotly_chart(fig5, use_container_width=True)

with tab2:
    st.subheader("⚙️ Rocket Launch Differential Equation Simulation")
    st.markdown("Simulate how thrust, mass, gravity, and drag affect altitude over time.")
    
    sim_col1, sim_col2 = st.columns([1, 2])
    
    with sim_col1:
        st.markdown("#### Initial Conditions")
        init_mass = st.number_input("Empty Rocket Mass (kg)", value=25000)
        fuel_mass = st.number_input("Fuel Mass (kg)", value=100000)
        payload = st.number_input("Payload Weight (kg)", value=5000)
        thrust = st.number_input("Engine Thrust (N)", value=1500000)
        drag_coeff = st.number_input("Drag Factor", value=0.5)
        burn_rate = st.slider("Fuel Burn Rate (kg/s)", 100, 1000, 500)
        time_steps = st.slider("Simulation Time (seconds)", 50, 300, 150)
        
    with sim_col2:
        # Simulation Logic
        dt = 1.0 # 1 second per step
        gravity = 9.81
        
        time_list = []
        alt_list = []
        vel_list = []
        
        current_mass = init_mass + fuel_mass + payload
        velocity = 0.0
        altitude = 0.0
        
        for t in range(time_steps):
            if fuel_mass > 0:
                current_thrust = thrust
                fuel_mass -= burn_rate * dt
                current_mass -= burn_rate * dt
            else:
                current_thrust = 0  # Engine stops when out of fuel
            
            # Density drops as altitude increases (simple exponential decay model)
            air_density = max(0, 1.225 * np.exp(-altitude / 8000))
            
            # Drag Force: 0.5 * drag_coeff * density * v^2
            drag_force = 0.5 * drag_coeff * air_density * (velocity ** 2) * np.sign(velocity)
            
            # Gravity Force: m * g
            gravity_force = current_mass * gravity
            
            # Net Force and Acceleration
            net_force = current_thrust - gravity_force - drag_force
            acceleration = net_force / current_mass
            
            # Update Velocity and Altitude
            velocity += acceleration * dt
            altitude += velocity * dt
            
            # Don't let rocket fall through the ground
            if altitude < 0:
                altitude = 0
                velocity = 0
                
            time_list.append(t)
            alt_list.append(altitude)
            vel_list.append(velocity)
            
        sim_df = pd.DataFrame({"Time (s)": time_list, "Altitude (m)": alt_list, "Velocity (m/s)": vel_list})
        
        st.markdown("#### Altitude Over Time")
        fig_sim = px.line(sim_df, x="Time (s)", y="Altitude (m)", title="Rocket Trajectory")
        fig_sim.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
        fig_sim.update_traces(line_color='#FF4B4B', line_width=3)
        st.plotly_chart(fig_sim, use_container_width=True)

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Designed by Aerospace Data Insights Project Team</p>", unsafe_allow_html=True)
