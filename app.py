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
    h1, h2, h3, h4, p, span, div { color: #e2e8f0; font-family: 'Inter', 'Segoe UI', sans-serif; }
    [data-testid="stSidebar"] { background: rgba(11, 19, 32, 0.6) !important; backdrop-filter: blur(15px); -webkit-backdrop-filter: blur(15px); border-right: 1px solid rgba(255, 255, 255, 0.05); }
    .glass-card { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1); padding: 25px; margin-bottom: 25px; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5); }
    .stTabs [data-baseweb="tab-list"] { gap: 15px; background: transparent; }
    .stTabs [data-baseweb="tab"] { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 6px; padding: 12px 30px; transition: 0.3s ease; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { background: rgba(88, 166, 255, 0.15); border-color: #58a6ff; }
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

# ==========================================
# 3. SIDEBAR CONTROLS
# ==========================================
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
# 4. TABS: ADVANCED ANALYTICS vs SIMULATION
# ==========================================
tab1, tab2 = st.tabs(["🔬 Deep Orbital Analytics", "🚀 Telemetry & Flight Simulation"])

with tab1:
    st.markdown(f"<div class='glass-card'><h4>Dataset Array: {len(filtered_data)} Records Filtered</h4></div>", unsafe_allow_html=True)
    
    # 1. 3D PARAMETER SPACE MAP (High Detail)
    st.markdown("### 🌐 3D Mission Parameter Space")
    st.markdown("Analyze the multidimensional relationship between deep-space distance, required fuel, and payload limits.")
    fig_3d = px.scatter_3d(filtered_data, x='Distance from Earth (light-years)', y='Fuel Consumption (tons)', z='Payload Weight (tons)',
                           color='Mission Success (%)', size='Mission Cost (billion USD)', 
                           hover_name='Mission Name', hover_data=['Launch Vehicle', 'Target Name'],
                           color_continuous_scale=px.colors.sequential.Plasma, opacity=0.8)
    fig_3d.update_layout(template=dark_template, height=600, scene=dict(
        xaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.1)"),
        yaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.1)"),
        zaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.1)")
    ))
    st.plotly_chart(fig_3d, use_container_width=True)

    col_a, col_b = st.columns(2)
    
    # 2. PEARSON CORRELATION MATRIX
    with col_a:
        st.markdown("### 📊 Metric Correlation Matrix")
        num_df = filtered_data[['Mission Cost (billion USD)', 'Scientific Yield (points)', 'Crew Size', 
                                'Mission Success (%)', 'Fuel Consumption (tons)', 'Payload Weight (tons)', 
                                'Distance from Earth (light-years)']]
        corr_matrix = num_df.corr()
        fig_corr = px.imshow(corr_matrix, text_auto=".2f", aspect="auto", color_continuous_scale='RdBu_r', origin='lower')
        fig_corr.update_layout(template=dark_template, height=500)
        st.plotly_chart(fig_corr, use_container_width=True)

    # 3. HIERARCHICAL SUNBURST CHART
    with col_b:
        st.markdown("### 🪐 Mission Taxonomy Architecture")
        fig_sun = px.sunburst(filtered_data, path=['Launch Vehicle', 'Target Type', 'Mission Type'], 
                              values='Mission Cost (billion USD)', color='Mission Success (%)', 
                              color_continuous_scale='viridis')
        fig_sun.update_layout(template=dark_template, height=500, margin=dict(t=0, l=0, r=0, b=0))
        st.plotly_chart(fig_sun, use_container_width=True)

    # 4. VIOLIN & SWARM PLOT FOR STATISTICAL DISTRIBUTION
    st.markdown("### 📈 Scientific Yield Distribution Analysis")
    fig_violin = px.violin(filtered_data, x='Mission Type', y='Scientific Yield (points)', color='Mission Type', 
                           box=True, points="all", hover_data=['Mission Name', 'Launch Vehicle'])
    fig_violin.update_layout(template=dark_template, height=500, showlegend=False)
    st.plotly_chart(fig_violin, use_container_width=True)

    # 5. MARGINAL SCATTER PLOT (Efficiency Matrix)
    st.markdown("### 🎯 Resource Efficiency & Outcome Marginal Distributions")
    fig_marg = px.scatter(filtered_data, x='Mission Cost (billion USD)', y='Scientific Yield (points)', 
                          color='Outcome Status', marginal_x="histogram", marginal_y="rug", 
                          hover_name='Mission Name', size='Crew Size',
                          color_discrete_map={"Nominal (Success)": "#00ff88", "Anomaly (Failure)": "#ff3366"})
    fig_marg.update_layout(template=dark_template, height=600)
    st.plotly_chart(fig_marg, use_container_width=True)

with tab2:
    st.markdown("<div class='glass-card'><h3>⚙️ Dynamic 2D Flight Simulation Engine</h3><p>Select a specific mission trajectory. The physics engine interprets Payload, Fuel, and Vehicle telemetry to simulate aerodynamic flight profiles.</p></div>", unsafe_allow_html=True)
    
    mission_names = filtered_data['Mission Name'].tolist()
    selected_mission = st.selectbox("Select Mission Telemetry Profile:", mission_names)
    
    if selected_mission:
        m_data = filtered_data[filtered_data['Mission Name'] == selected_mission].iloc[0]
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
        col4.metric("Success Prob.", f"{success_chance}%")

        if st.button("🚀 INITIATE IGNITION SEQUENCE", use_container_width=True):
            dt = 0.5
            time_steps = 300
            burn_rate = fuel_kg / 100 
            gravity = 9.81
            
            will_fail = success_chance < np.random.uniform(50, 100)
            failure_time = np.random.randint(40, 90) if will_fail else 999
            
            time_list, alt_list, status_list = [], [], []
            current_mass = init_mass + fuel_kg + payload_kg
            velocity = 0.0
            altitude = 0.0
            status = "Nominal"
            
            progress_bar = st.progress(0)
            
            for t_step in range(time_steps):
                t = t_step * dt
                if t >= failure_time and will_fail and status == "Nominal":
                    status = "ANOMALY - THRUST LOSS"
                    thrust = 0 
                
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
                        status = "CATASTROPHIC IMPACT"
                    break
                    
                time_list.append(t)
                alt_list.append(altitude / 1000) 
                status_list.append(status)
                
            progress_bar.empty()
            
            if will_fail:
                st.error(f"💥 {status_list[-1]} at T+{failure_time}s")
            else:
                st.success("✨ ORBITAL INSERTION CONFIRMED")
            
            sim_df = pd.DataFrame({"Time (s)": time_list, "Altitude (km)": alt_list, "Status": status_list})
            sim_df = sim_df.iloc[::2, :].copy() 
            
            fig_anim = px.scatter(sim_df, x="Time (s)", y="Altitude (km)", animation_frame="Time (s)", 
                                  range_x=[0, sim_df['Time (s)'].max() + 10], range_y=[0, sim_df['Altitude (km)'].max() * 1.2])
            
            fig_anim.update_traces(marker=dict(size=20, symbol="triangle-up", 
                                   color=np.where(sim_df['Status'] == "Nominal", "#00ff88", "#ff3366"),
                                   line=dict(width=2, color="white")))
            
            fig_anim.add_trace(go.Scatter(x=sim_df["Time (s)"], y=sim_df["Altitude (km)"],
                                          mode="lines", line=dict(color="rgba(255, 255, 255, 0.2)", width=2), name="Flight Path"))
            
            fig_anim.update_layout(template=dark_template, updatemenus=[dict(type="buttons", showactive=False)])
            st.plotly_chart(fig_anim, use_container_width=True)
