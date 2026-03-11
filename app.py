import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time

# ==========================================
# 1. PAGE CONFIGURATION & GLASSMORPHISM CSS
# ==========================================
st.set_page_config(page_title="🚀 Advanced Aerospace Analytics", layout="wide", page_icon="🌌")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0b1320, #14213d, #000000); background-attachment: fixed; }
    h1, h2, h3, h4, p, span, div, label { color: #e2e8f0; font-family: 'Inter', 'Segoe UI', sans-serif; }
    [data-testid="stSidebar"] { background: rgba(11, 19, 32, 0.6) !important; backdrop-filter: blur(15px); -webkit-backdrop-filter: blur(15px); border-right: 1px solid rgba(255, 255, 255, 0.05); }
    .glass-card { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1); padding: 25px; margin-bottom: 25px; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5); }
    .stTabs [data-baseweb="tab-list"] { gap: 15px; background: transparent; }
    .stTabs [data-baseweb="tab"] { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 6px; padding: 12px 30px; transition: 0.3s ease; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { background: rgba(88, 166, 255, 0.15); border-color: #58a6ff; }
    hr { border-color: rgba(255, 255, 255, 0.1); margin-top: 40px; margin-bottom: 40px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="glass-card">
    <h1 style='text-align: center; color: #4db8ff !important; margin-bottom: 0; font-weight: 300; letter-spacing: 2px;'>AEROSPACE TELEMETRY & MISSION ANALYTICS</h1>
    <p style='text-align: center; font-size: 1em; opacity: 0.6; text-transform: uppercase; letter-spacing: 1px;'>Advanced Data Science Visualization Terminal</p>
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

# Base Plotly Template for Dark Theme
dark_template = dict(
    layout=go.Layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#a0aec0', family="Inter"),
        title=dict(font=dict(color='#e2e8f0', size=18)),
        legend=dict(font=dict(color='#a0aec0')),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)', zerolinecolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', zerolinecolor='rgba(255,255,255,0.1)')
    )
)

# ==========================================
# 3. TABS
# ==========================================
tab1, tab2 = st.tabs(["📊 Mission Dashboard", "🚀 3D Telemetry & Flight Simulation"])

with tab1:
    st.sidebar.markdown("<h3 style='color: #4db8ff;'>⎈ Telemetry Filters</h3>", unsafe_allow_html=True)
    selected_mission_type = st.sidebar.selectbox("Mission Architecture", options=["All"] + list(data['Mission Type'].unique()))
    selected_vehicle = st.sidebar.selectbox("Launch Platform", options=["All"] + list(data['Launch Vehicle'].unique()))

    min_year, max_year = int(data['Launch Year'].min()), int(data['Launch Year'].max())
    selected_year_range = st.sidebar.slider("Operational Window (Years)", min_year, max_year, (min_year, max_year))

    filtered_data = data.copy()
    if selected_mission_type != "All":
        filtered_data = filtered_data[filtered_data['Mission Type'] == selected_mission_type]
    if selected_vehicle != "All":
        filtered_data = filtered_data[filtered_data['Launch Vehicle'] == selected_vehicle]
    filtered_data = filtered_data[(filtered_data['Launch Year'] >= selected_year_range[0]) & (filtered_data['Launch Year'] <= selected_year_range[1])]

    st.markdown(f"<div class='glass-card'><h4>Dataset Array: {len(filtered_data)} Records Filtered</h4></div>", unsafe_allow_html=True)
    
    # --- PART A: EXECUTIVE SUMMARY ---
    st.markdown("<h2 style='color: #4db8ff;'>Executive Summary: Key Mission Metrics</h2>", unsafe_allow_html=True)
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        fig1 = px.scatter(filtered_data, x='Payload Weight (tons)', y='Fuel Consumption (tons)', color='Outcome Status', size='Mission Cost (billion USD)', hover_data=['Mission Name', 'Launch Vehicle'], title="Payload vs Fuel Consumption", color_discrete_map={"Nominal (Success)": "#00e676", "Anomaly (Failure)": "#ff1744"})
        fig1.update_layout(template=dark_template)
        st.plotly_chart(fig1, use_container_width=True)

    with col_a2:
        cost_df = filtered_data.groupby('Outcome Status')['Mission Cost (billion USD)'].sum().reset_index()
        fig2 = px.bar(cost_df, x='Outcome Status', y='Mission Cost (billion USD)', color='Outcome Status', title="Total Mission Cost by Outcome", color_discrete_map={"Nominal (Success)": "#00e676", "Anomaly (Failure)": "#ff1744"})
        fig2.update_layout(template=dark_template)
        st.plotly_chart(fig2, use_container_width=True)

    col_a3, col_a4 = st.columns(2)
    with col_a3:
        line_data = filtered_data.sort_values(by='Distance from Earth (light-years)')
        fig3 = px.line(line_data, x='Distance from Earth (light-years)', y='Mission Duration (years)', markers=True, title="Mission Duration vs Distance")
        fig3.update_layout(template=dark_template)
        fig3.update_traces(line_color='#29b6f6', line_width=2)
        st.plotly_chart(fig3, use_container_width=True)

    with col_a4:
        fig4 = px.box(filtered_data, x='Outcome Status', y='Crew Size', color='Outcome Status', title="Crew Size Distribution", color_discrete_map={"Nominal (Success)": "#00e676", "Anomaly (Failure)": "#ff1744"})
        fig4.update_layout(template=dark_template)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # --- PART B: DEEP ORBITAL ANALYTICS ---
    st.markdown("<h2 style='color: #4db8ff;'>Deep Orbital Analytics: Advanced Telemetry</h2>", unsafe_allow_html=True)
    fig_3d = px.scatter_3d(filtered_data, x='Distance from Earth (light-years)', y='Fuel Consumption (tons)', z='Payload Weight (tons)', color='Mission Success (%)', size='Mission Cost (billion USD)', hover_name='Mission Name', hover_data=['Launch Vehicle', 'Target Name'], color_continuous_scale=px.colors.sequential.Plasma, opacity=0.8)
    fig_3d.update_layout(template=dark_template, height=600, scene=dict(xaxis=dict(backgroundcolor="rgba(0,0,0,0)"), yaxis=dict(backgroundcolor="rgba(0,0,0,0)"), zaxis=dict(backgroundcolor="rgba(0,0,0,0)")))
    st.plotly_chart(fig_3d, use_container_width=True)

    col_b1, col_b2 = st.columns(2)
    with col_b1:
        num_df = filtered_data[['Mission Cost (billion USD)', 'Scientific Yield (points)', 'Crew Size', 'Mission Success (%)', 'Fuel Consumption (tons)', 'Payload Weight (tons)', 'Distance from Earth (light-years)']]
        fig_corr = px.imshow(num_df.corr(), text_auto=".2f", aspect="auto", color_continuous_scale='RdBu_r', origin='lower', title="Metric Correlation Matrix")
        fig_corr.update_layout(template=dark_template, height=500)
        st.plotly_chart(fig_corr, use_container_width=True)

    with col_b2:
        fig_sun = px.sunburst(filtered_data, path=['Launch Vehicle', 'Target Type', 'Mission Type'], values='Mission Cost (billion USD)', color='Mission Success (%)', color_continuous_scale='viridis', title="Mission Taxonomy Architecture")
        fig_sun.update_layout(template=dark_template, height=500, margin=dict(t=30, l=0, r=0, b=0))
        st.plotly_chart(fig_sun, use_container_width=True)

    fig_violin = px.violin(filtered_data, x='Mission Type', y='Scientific Yield (points)', color='Mission Type', box=True, points="all", hover_data=['Mission Name', 'Launch Vehicle'], title="Scientific Yield Distribution Analysis")
    fig_violin.update_layout(template=dark_template, height=500, showlegend=False)
    st.plotly_chart(fig_violin, use_container_width=True)

with tab2:
    st.markdown("<div class='glass-card'><h3>⚙️ Dynamic 3D Flight Simulation Engine</h3><p>Choose between utilizing real dataset telemetry or engaging the Manual Override to build your own aerodynamic profile.</p></div>", unsafe_allow_html=True)
    
    # Toggle for Manual vs Dataset
    mode = st.radio("⚙️ Simulation Mode:", ["Dataset Telemetry Profiles", "Manual Engineering Override"], horizontal=True)
    
    st.markdown("<hr style='margin-top: 10px; margin-bottom: 20px;'>", unsafe_allow_html=True)

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
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Platform", vehicle)
        col2.metric("Payload (kg)", f"{payload_kg:,.0f}")
        col3.metric("Propellant (kg)", f"{fuel_kg:,.0f}")
        col4.metric("Historical Success", f"{success_chance}%")
        
    else:
        st.markdown("#### 🔧 Custom Vehicle Configuration")
        col1, col2 = st.columns(2)
        init_mass = col1.number_input("Dry Rocket Mass (kg)", value=1000000, step=50000)
        thrust = col2.number_input("Engine Thrust (N)", value=35000000, step=1000000)
        
        col3, col4 = st.columns(2)
        payload_kg = col3.number_input("Payload Weight (kg)", value=25000, step=1000)
        fuel_kg = col4.number_input("Propellant Mass (kg)", value=2000000, step=100000)
        
        col5, col6 = st.columns(2)
        drag_coeff = col5.slider("Aerodynamic Drag Factor", 0.1, 1.0, 0.4)
        success_chance = col6.slider("System Reliability Prob. (%)", 10, 100, 90)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 INITIATE 3D IGNITION SEQUENCE", use_container_width=True):
        # 3D Physics Engine Setup
        dt = 0.5
        time_steps = 400
        burn_rate = fuel_kg / 120  # Approx 120s burn
        gravity = 9.81
        
        # Determine failure timing
        will_fail = success_chance < np.random.uniform(0, 100)
        failure_time = np.random.randint(30, 90) if will_fail else 999
        
        time_list, x_list, y_list, z_list, status_list = [], [], [], [], []
        current_mass = init_mass + fuel_kg + payload_kg
        
        # Initial 3D Variables
        x, y, z = 0.0, 0.0, 0.0
        vx, vy, vz = 0.0, 0.0, 0.0
        status = "Nominal"
        
        # Angles for Gravity Turn
        pitch_angle = np.pi / 2 # 90 degrees (straight up)
        azimuth_angle = np.pi / 4 # 45 degree inclination for 3D depth
        
        progress_bar = st.progress(0)
        
        for t_step in range(time_steps):
            t = t_step * dt
            
            # Anomaly Trigger
            if t >= failure_time and will_fail and status == "Nominal":
                status = "ANOMALY - THRUST LOSS"
                thrust = 0 
            
            # Gravity Turn Pitch Control
            if t > 10 and status == "Nominal":
                pitch_angle = max(0.1, pitch_angle - 0.005 * dt) # Gradually tilt horizontal
            
            # Fuel Burn
            if fuel_kg > 0 and status == "Nominal":
                current_thrust = thrust
                fuel_spent = min(burn_rate * dt, fuel_kg)
                fuel_kg -= fuel_spent
                current_mass -= fuel_spent
            else:
                current_thrust = 0
            
            # Forces
            air_density = max(0, 1.225 * np.exp(-z / 8000))
            v_mag = np.sqrt(vx**2 + vy**2 + vz**2)
            drag_force = 0.5 * drag_coeff * air_density * (v_mag ** 2)
            
            dx = drag_force * (vx / v_mag) if v_mag > 0 else 0
            dy = drag_force * (vy / v_mag) if v_mag > 0 else 0
            dz = drag_force * (vz / v_mag) if v_mag > 0 else 0
            
            tx = current_thrust * np.cos(pitch_angle) * np.cos(azimuth_angle)
            ty = current_thrust * np.cos(pitch_angle) * np.sin(azimuth_angle)
            tz = current_thrust * np.sin(pitch_angle)
            
            ax = (tx - dx) / current_mass
            ay = (ty - dy) / current_mass
            az = (tz - dz - current_mass * gravity) / current_mass
            
            # Integration
            vx += ax * dt
            vy += ay * dt
            vz += az * dt
            
            x += vx * dt
            y += vy * dt
            z += vz * dt
            
            # Ground Collision
            if z <= 0 and t > 5:
                z = 0
                vz = 0
                if status != "Nominal":
                    status = "CATASTROPHIC IMPACT"
                break
                
            time_list.append(t)
            x_list.append(x / 1000) # Convert to km
            y_list.append(y / 1000) 
            z_list.append(z / 1000) 
            status_list.append(status)
            
        progress_bar.empty()
        
        if will_fail:
            st.error(f"💥 {status_list[-1]} at T+{failure_time}s")
        else:
            st.success("✨ ORBITAL INSERTION CONFIRMED")
        
        # Combine Data for Plotting
        sim_df = pd.DataFrame({"Time (s)": time_list, "Downrange (km)": x_list, "Crossrange (km)": y_list, "Altitude (km)": z_list, "Status": status_list})
        
        # --- 3D Orbital Trajectory Map ---
        st.markdown("### 🛰️ 3D Orbital Trajectory")
        fig_3d_traj = px.scatter_3d(sim_df, x="Downrange (km)", y="Crossrange (km)", z="Altitude (km)", 
                                    color="Status", title="Spatial Telemetry Breadcrumb Trail",
                                    color_discrete_map={"Nominal": "#00ff88", "ANOMALY - THRUST LOSS": "#ff9900", "CATASTROPHIC IMPACT": "#ff3366"})
        fig_3d_traj.update_traces(marker=dict(size=4))
        fig_3d_traj.update_layout(template=dark_template, height=600, scene=dict(
            xaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.1)"),
            yaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.1)"),
            zaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.1)")
        ))
        st.plotly_chart(fig_3d_traj, use_container_width=True)

        # --- 2D Animated Flight Path ---
        st.markdown("### 📺 2D Temporal Animation")
        sim_df_anim = sim_df.iloc[::2, :].copy() 
        fig_anim = px.scatter(sim_df_anim, x="Time (s)", y="Altitude (km)", animation_frame="Time (s)", 
                              range_x=[0, sim_df_anim['Time (s)'].max() + 10], range_y=[0, sim_df_anim['Altitude (km)'].max() * 1.2])
        fig_anim.update_traces(marker=dict(size=20, symbol="triangle-up", 
                               color=np.where(sim_df_anim['Status'] == "Nominal", "#00ff88", "#ff3366"),
                               line=dict(width=2, color="white")))
        fig_anim.add_trace(go.Scatter(x=sim_df_anim["Time (s)"], y=sim_df_anim["Altitude (km)"],
                                      mode="lines", line=dict(color="rgba(255, 255, 255, 0.2)", width=2), name="Flight Path"))
        fig_anim.update_layout(template=dark_template, updatemenus=[dict(type="buttons", showactive=False)])
        st.plotly_chart(fig_anim, use_container_width=True)
