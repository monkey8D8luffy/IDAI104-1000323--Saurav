import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time

# ==========================================
# 1. PAGE CONFIGURATION & GLASSMORPHISM CSS
# ==========================================
st.set_page_config(page_title="🚀 Aerospace Data Insights", layout="wide", page_icon="🌌")

# Glassmorphism & Custom Theming
st.markdown("""
    <style>
    /* Main Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        background-attachment: fixed;
    }
    
    /* Typography */
    h1, h2, h3, h4, p, span {
        color: #e2e8f0 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Glassmorphism for Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(15, 32, 39, 0.4) !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Glassmorphism for Data Cards/Containers */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    
    /* Styling Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        padding: 10px 25px;
        transition: 0.3s ease;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: rgba(88, 166, 255, 0.2);
        border-color: #58a6ff;
    }
    </style>
""", unsafe_allow_html=True)

# Title Header with Glass Effect
st.markdown("""
<div class="glass-card">
    <h1 style='text-align: center; color: #58a6ff !important; margin-bottom: 0;'>🚀 Space Rocket Paths & Mission Data Dashboard</h1>
    <p style='text-align: center; font-size: 1.1em; opacity: 0.8;'>Aerospace Data Insights Project</p>
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
    df['Outcome Status'] = np.where(df['Mission Success (%)'] >= 80, 'Success', 'Failure')
    return df

try:
    data = load_and_clean_data()
except FileNotFoundError:
    st.error("⚠️ 'space_missions_dataset.csv' not found.")
    st.stop()

# Dictionary to estimate rocket base stats for simulation
VEHICLE_STATS = {
    "SLS": {"mass_kg": 1000000, "thrust_N": 39000000, "drag": 0.4},
    "Starship": {"mass_kg": 1200000, "thrust_N": 74000000, "drag": 0.3},
    "Falcon Heavy": {"mass_kg": 1420000, "thrust_N": 22000000, "drag": 0.35},
    "Ariane 6": {"mass_kg": 800000, "thrust_N": 10000000, "drag": 0.45}
}

# ==========================================
# 3. SIDEBAR CONTROLS
# ==========================================
st.sidebar.markdown("### 🎛️ Mission Filters")
selected_mission_type = st.sidebar.selectbox("Mission Type", options=["All"] + list(data['Mission Type'].unique()))
selected_vehicle = st.sidebar.selectbox("Launch Vehicle", options=["All"] + list(data['Launch Vehicle'].unique()))

min_year, max_year = int(data['Launch Year'].min()), int(data['Launch Year'].max())
selected_year_range = st.sidebar.slider("Launch Year Range", min_year, max_year, (min_year, max_year))

filtered_data = data.copy()
if selected_mission_type != "All":
    filtered_data = filtered_data[filtered_data['Mission Type'] == selected_mission_type]
if selected_vehicle != "All":
    filtered_data = filtered_data[filtered_data['Launch Vehicle'] == selected_vehicle]
filtered_data = filtered_data[(filtered_data['Launch Year'] >= selected_year_range[0]) & (filtered_data['Launch Year'] <= selected_year_range[1])]

# ==========================================
# 4. TABS: DASHBOARD vs SIMULATION
# ==========================================
tab1, tab2 = st.tabs(["📊 Mission Dashboard", "🚀 Data-Driven Flight Simulation"])

with tab1:
    st.markdown(f"<div class='glass-card'><h3>Analyzing {len(filtered_data)} Space Missions</h3></div>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        fig1 = px.scatter(filtered_data, x='Payload Weight (tons)', y='Fuel Consumption (tons)',
                          color='Outcome Status', size='Mission Cost (billion USD)',
                          hover_data=['Mission Name', 'Launch Vehicle'], title="Payload vs Fuel Consumption",
                          color_discrete_map={"Success": "#00e676", "Failure": "#ff1744"})
        fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        cost_df = filtered_data.groupby('Outcome Status')['Mission Cost (billion USD)'].sum().reset_index()
        fig2 = px.bar(cost_df, x='Outcome Status', y='Mission Cost (billion USD)', 
                      color='Outcome Status', title="Total Mission Cost by Outcome",
                      color_discrete_map={"Success": "#00e676", "Failure": "#ff1744"})
        fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
        st.plotly_chart(fig2, use_container_width=True)

    col_c, col_d = st.columns(2)
    with col_c:
        line_data = filtered_data.sort_values(by='Distance from Earth (light-years)')
        fig3 = px.line(line_data, x='Distance from Earth (light-years)', y='Mission Duration (years)', 
                       markers=True, title="Duration vs Distance")
        fig3.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
        fig3.update_traces(line_color='#29b6f6', line_width=2)
        st.plotly_chart(fig3, use_container_width=True)

    with col_d:
        fig4 = px.box(filtered_data, x='Outcome Status', y='Crew Size', 
                      color='Outcome Status', title="Crew Size Distribution",
                      color_discrete_map={"Success": "#00e676", "Failure": "#ff1744"})
        fig4.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
        st.plotly_chart(fig4, use_container_width=True)

with tab2:
    st.markdown("<div class='glass-card'><h3>⚙️ Dynamic 2D Flight Simulation</h3><p>Select a specific mission from the dataset. The physics engine will use its real Payload, Fuel, and Vehicle parameters to simulate the launch. If the Mission Success % is low, watch out for a mid-air anomaly!</p></div>", unsafe_allow_html=True)
    
    # Mission Selector
    mission_names = filtered_data['Mission Name'].tolist()
    selected_mission = st.selectbox("Select a Mission to Simulate:", mission_names)
    
    if selected_mission:
        m_data = filtered_data[filtered_data['Mission Name'] == selected_mission].iloc[0]
        vehicle = m_data['Launch Vehicle']
        
        # Fallback stats if vehicle not in dictionary
        v_stats = VEHICLE_STATS.get(vehicle, {"mass_kg": 1000000, "thrust_N": 30000000, "drag": 0.4})
        
        # Map Dataset to Physics Variables
        init_mass = v_stats["mass_kg"]
        thrust = v_stats["thrust_N"]
        drag_coeff = v_stats["drag"]
        payload_kg = m_data['Payload Weight (tons)'] * 1000
        fuel_kg = m_data['Fuel Consumption (tons)'] * 1000
        success_chance = m_data['Mission Success (%)']
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Vehicle", vehicle)
        col2.metric("Payload", f"{payload_kg:,.0f} kg")
        col3.metric("Fuel", f"{fuel_kg:,.0f} kg")
        col4.metric("Historical Success", f"{success_chance}%")

        if st.button("🚀 INITIATE LAUNCH SEQUENCE", use_container_width=True):
            # Physics Engine Setup
            dt = 0.5
            time_steps = 300
            burn_rate = fuel_kg / 100  # Assume 100 sec burn time
            gravity = 9.81
            
            # Determine if this specific flight will fail
            will_fail = success_chance < np.random.uniform(50, 100)
            failure_time = np.random.randint(40, 90) if will_fail else 999
            
            time_list, alt_list, status_list = [], [], []
            current_mass = init_mass + fuel_kg + payload_kg
            velocity = 0.0
            altitude = 0.0
            status = "Nominal"
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for t_step in range(time_steps):
                t = t_step * dt
                
                # Trigger Failure
                if t >= failure_time and will_fail and status == "Nominal":
                    status = "ANOMALY DETECTED - ENGINE FAILURE"
                    thrust = 0  # Complete loss of thrust
                
                if fuel_kg > 0 and status == "Nominal":
                    current_thrust = thrust
                    fuel_spent = min(burn_rate * dt, fuel_kg)
                    fuel_kg -= fuel_spent
                    current_mass -= fuel_spent
                else:
                    current_thrust = 0
                
                air_density = max(0, 1.225 * np.exp(-altitude / 8000))
                drag_force = 0.5 * drag_coeff * air_density * (velocity ** 2) * np.sign(velocity)
                gravity_force = current_mass * gravity
                
                net_force = current_thrust - gravity_force - drag_force
                acceleration = net_force / current_mass
                
                velocity += acceleration * dt
                altitude += velocity * dt
                
                if altitude <= 0 and t > 5:
                    altitude = 0
                    velocity = 0
                    if status != "Nominal":
                        status = "CRITICAL IMPACT - ROCKET DESTROYED"
                    break
                    
                time_list.append(t)
                alt_list.append(altitude / 1000) # Convert to km for viz
                status_list.append(status)
                
            progress_bar.empty()
            
            if will_fail:
                st.error(f"💥 {status_list[-1]} at T+{failure_time}s!")
            else:
                st.success("✨ ORBIT REACHED SUCCESSFULLY!")
            
            # Create 2D Animation with Plotly
            sim_df = pd.DataFrame({"Time (s)": time_list, "Altitude (km)": alt_list, "Status": status_list})
            
            # Downsample for smoother Streamlit rendering
            sim_df = sim_df.iloc[::2, :].copy() 
            
            fig_anim = px.scatter(sim_df, x="Time (s)", y="Altitude (km)", 
                                  animation_frame="Time (s)", 
                                  range_x=[0, sim_df['Time (s)'].max() + 10], 
                                  range_y=[0, sim_df['Altitude (km)'].max() * 1.2],
                                  title="2D Flight Path Simulation")
            
            # Styling the Rocket Marker
            fig_anim.update_traces(marker=dict(size=20, symbol="triangle-up", 
                                   color=np.where(sim_df['Status'] == "Nominal", "#00e676", "#ff1744"),
                                   line=dict(width=2, color="white")))
            
            # Add trajectory trail
            fig_anim.add_trace(go.Scatter(x=sim_df["Time (s)"], y=sim_df["Altitude (km)"],
                                          mode="lines", line=dict(color="rgba(255, 255, 255, 0.3)", width=2),
                                          name="Trajectory"))
            
            fig_anim.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                                   font=dict(color='white'), updatemenus=[dict(type="buttons", showactive=False)])
            
            st.plotly_chart(fig_anim, use_container_width=True)
