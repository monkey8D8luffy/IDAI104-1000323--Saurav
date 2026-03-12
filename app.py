import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import time

# ==========================================
# 1. PAGE CONFIGURATION & DEEP SPACE CSS
# ==========================================
st.set_page_config(page_title="🚀 Aerospace Command Center", layout="wide", page_icon="🌌")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #05050f 100%); background-attachment: fixed; }
    h1, h2, h3, h4, p, span, div, label { color: #f8f9fa; font-family: 'Inter', 'Segoe UI', sans-serif; }
    h1 { text-shadow: 0 0 10px rgba(0, 242, 254, 0.5); color: #00f2fe !important; }
    h2, h3 { color: #4facfe !important; }
    [data-testid="stSidebar"] { background: rgba(15, 12, 41, 0.6) !important; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border-right: 1px solid rgba(0, 242, 254, 0.2); }
    .glass-card { background: rgba(255, 255, 255, 0.02); backdrop-filter: blur(25px); -webkit-backdrop-filter: blur(25px); border-radius: 16px; border: 1px solid rgba(0, 242, 254, 0.15); padding: 25px; margin-bottom: 25px; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.6), inset 0 0 20px rgba(0, 242, 254, 0.02); }
    .telemetry-box { background: rgba(0, 242, 254, 0.05); border-left: 4px solid #00f2fe; padding: 15px; border-radius: 5px; font-family: 'Courier New', Courier, monospace; margin-bottom: 20px;}
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background: transparent; }
    .stTabs [data-baseweb="tab"] { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 8px 8px 0 0; padding: 12px 30px; transition: 0.3s ease; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { background: rgba(0, 242, 254, 0.1); border-bottom: 3px solid #00f2fe; border-top: 1px solid rgba(0, 242, 254, 0.3); border-left: 1px solid rgba(0, 242, 254, 0.3); border-right: 1px solid rgba(0, 242, 254, 0.3); color: #00f2fe; text-shadow: 0 0 8px rgba(0, 242, 254, 0.4); }
    hr { border-color: rgba(0, 242, 254, 0.15); margin-top: 40px; margin-bottom: 40px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="glass-card">
    <h1 style='text-align: center; margin-bottom: 5px; font-weight: 400; letter-spacing: 3px;'>AEROSPACE COMMAND TERMINAL</h1>
    <p style='text-align: center; font-size: 1.1em; opacity: 0.7; text-transform: uppercase; letter-spacing: 2px; color: #a0aec0;'>Orbital Telemetry & Predictive Analytics Software</p>
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

cyber_template = dict(
    layout=go.Layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#cfd8dc', family="Inter"),
        title=dict(font=dict(color='#00f2fe', size=16)),
        legend=dict(font=dict(color='#cfd8dc'), bgcolor='rgba(0,0,0,0)'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)', zerolinecolor='rgba(0,242,254,0.2)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', zerolinecolor='rgba(0,242,254,0.2)')
    )
)

color_map_status = {"Nominal (Success)": "#00FFA3", "Anomaly (Failure)": "#FF3366"}

plt.style.use('dark_background')
fig_rc = {'figure.facecolor': '#0f0c29', 'axes.facecolor': '#0f0c29', 
          'axes.edgecolor': '#00f2fe', 'text.color': '#cfd8dc', 
          'xtick.color': '#00f2fe', 'ytick.color': '#00f2fe'}
sns.set_theme(style="darkgrid", rc=fig_rc)

# ==========================================
# 3. TABS & SIDEBAR
# ==========================================
tab1, tab2 = st.tabs(["📊 Mission Data Intelligence", "🚀 Advanced Flight Physics Simulator"])

with tab1:
    st.sidebar.markdown("<h3>⎈ Telemetry Filters</h3>", unsafe_allow_html=True)
    selected_mission_type = st.sidebar.selectbox("Mission Architecture", options=["All"] + list(data['Mission Type'].unique()))
    selected_vehicle = st.sidebar.selectbox("Launch Platform", options=["All"] + list(data['Launch Vehicle'].unique()))
    min_year, max_year = int(data['Launch Year'].min()), int(data['Launch Year'].max())
    selected_year_range = st.sidebar.slider("Operational Window (Years)", min_year, max_year, (min_year, max_year))

    filtered_data = data.copy()
    if selected_mission_type != "All": filtered_data = filtered_data[filtered_data['Mission Type'] == selected_mission_type]
    if selected_vehicle != "All": filtered_data = filtered_data[filtered_data['Launch Vehicle'] == selected_vehicle]
    filtered_data = filtered_data[(filtered_data['Launch Year'] >= selected_year_range[0]) & (filtered_data['Launch Year'] <= selected_year_range[1])]

    st.markdown(f"<div class='glass-card'><h4>📡 Uplink Active: {len(filtered_data)} Records Filtered</h4></div>", unsafe_allow_html=True)
    
    # --- PART A: EXECUTIVE SUMMARY ---
    st.markdown("<h2>Macro-Level Launch Metrics</h2>", unsafe_allow_html=True)
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        fig1 = px.scatter(filtered_data, x='Payload Weight (tons)', y='Fuel Consumption (tons)', color='Outcome Status', size='Mission Cost (billion USD)', hover_data=['Mission Name', 'Launch Vehicle'], title="Mass-to-Propellant Ratio & Mission Viability Analysis", color_discrete_map=color_map_status)
        fig1.update_layout(template=cyber_template)
        st.plotly_chart(fig1, use_container_width=True)

    with col_a2:
        cost_df = filtered_data.groupby('Outcome Status')['Mission Cost (billion USD)'].sum().reset_index()
        fig2 = px.bar(cost_df, x='Outcome Status', y='Mission Cost (billion USD)', color='Outcome Status', title="Aggregate Financial Expenditure by Mission Outcome", color_discrete_map=color_map_status)
        fig2.update_layout(template=cyber_template)
        st.plotly_chart(fig2, use_container_width=True)

    col_a3, col_a4 = st.columns(2)
    with col_a3:
        line_data = filtered_data.sort_values(by='Distance from Earth (light-years)')
        fig3 = px.line(line_data, x='Distance from Earth (light-years)', y='Mission Duration (years)', markers=True, title="Orbital Reach: Distance Traveled vs. Operational Duration")
        fig3.update_layout(template=cyber_template)
        fig3.update_traces(line_color='#00f2fe', line_width=3, marker=dict(size=6, color="#ff007f"))
        st.plotly_chart(fig3, use_container_width=True)

    with col_a4:
        fig4 = px.box(filtered_data, x='Outcome Status', y='Crew Size', color='Outcome Status', title="Personnel Capacity Distribution Across Mission Status", color_discrete_map=color_map_status)
        fig4.update_layout(template=cyber_template)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # --- PART B: CORE STATISTICAL ANALYSIS ---
    st.markdown("<h2>Core Statistical Distributions (Matplotlib & Seaborn)</h2>", unsafe_allow_html=True)
    col_s1, col_s2, col_s3 = st.columns(3)
    
    with col_s1:
        fig_m1, ax_m1 = plt.subplots(figsize=(5, 4))
        cost_agg = filtered_data.groupby('Outcome Status')['Mission Cost (billion USD)'].mean()
        ax_m1.bar(cost_agg.index, cost_agg.values, color=['#FF3366', '#00FFA3'])
        ax_m1.set_ylabel("Avg Cost (Billion USD)")
        ax_m1.set_title("Mean Capital Expenditure per Mission Status", fontsize=10)
        st.pyplot(fig_m1)
        
    with col_s2:
        fig_s1, ax_s1 = plt.subplots(figsize=(5, 4))
        sns.boxplot(data=filtered_data, x='Outcome Status', y='Crew Size', palette={"Nominal (Success)": "#00FFA3", "Anomaly (Failure)": "#FF3366"}, ax=ax_s1)
        ax_s1.set_title("Statistical Dispersion of Crew Configurations", fontsize=10)
        st.pyplot(fig_s1)
        
    with col_s3:
        fig_s2, ax_s2 = plt.subplots(figsize=(5, 4))
        sns.scatterplot(data=filtered_data, x='Payload Weight (tons)', y='Fuel Consumption (tons)', hue='Outcome Status', palette={"Nominal (Success)": "#00FFA3", "Anomaly (Failure)": "#FF3366"}, ax=ax_s2)
        ax_s2.set_title("Propellant Consumption vs. Payload Mass", fontsize=10)
        st.pyplot(fig_s2)

    st.markdown("<hr>", unsafe_allow_html=True)

    # --- PART C: DEEP ORBITAL ANALYTICS ---
    st.markdown("<h2>Multi-Dimensional Systems Analytics</h2>", unsafe_allow_html=True)
    fig_3d = px.scatter_3d(filtered_data, x='Distance from Earth (light-years)', y='Fuel Consumption (tons)', z='Payload Weight (tons)', color='Mission Success (%)', size='Mission Cost (billion USD)', hover_name='Mission Name', hover_data=['Launch Vehicle', 'Target Name'], title="3D Parameter Space: Interstellar Distance, Fuel Mass, and Payload Limits", color_continuous_scale=px.colors.sequential.Sunsetdark, opacity=0.9)
    fig_3d.update_layout(template=cyber_template, height=700, scene=dict(
        xaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(0,242,254,0.1)"),
        yaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(0,242,254,0.1)"),
        zaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(0,242,254,0.1)")
    ))
    st.plotly_chart(fig_3d, use_container_width=True)

    col_b1, col_b2 = st.columns(2)
    with col_b1:
        num_df = filtered_data[['Mission Cost (billion USD)', 'Scientific Yield (points)', 'Crew Size', 'Mission Success (%)', 'Fuel Consumption (tons)', 'Payload Weight (tons)', 'Distance from Earth (light-years)']]
        fig_corr = px.imshow(num_df.corr(), text_auto=".2f", aspect="auto", color_continuous_scale='Picnic', origin='lower', title="Pearson Correlation Matrix of Key Mission Telemetry")
        fig_corr.update_layout(template=cyber_template, height=500)
        st.plotly_chart(fig_corr, use_container_width=True)

    with col_b2:
        fig_sun = px.sunburst(filtered_data, path=['Launch Vehicle', 'Target Type', 'Mission Type'], values='Mission Cost (billion USD)', color='Mission Success (%)', color_continuous_scale='Plotly3', title="Hierarchical Architecture of Spacecraft & Mission Objectives")
        fig_sun.update_layout(template=cyber_template, height=500, margin=dict(t=40, l=0, r=0, b=0))
        st.plotly_chart(fig_sun, use_container_width=True)

with tab2:
    st.markdown("<div class='glass-card'><h3>⚙️ Advanced 3D Flight Physics Simulator</h3><p>Integrates the Tsiolkovsky rocket equation, dynamic pressure (Max-Q) modeling, and Mach calculations for true-to-life orbital trajectory generation.</p></div>", unsafe_allow_html=True)
    
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
        
    else:
        st.markdown("#### 🔧 Vehicle Engineering Configuration")
        col1, col2 = st.columns(2)
        init_mass = col1.number_input("Dry Rocket Mass (kg)", value=1000000, step=50000)
        thrust = col2.number_input("Engine Thrust (N)", value=35000000, step=1000000)
        col3, col4 = st.columns(2)
        payload_kg = col3.number_input("Payload Weight (kg)", value=25000, step=1000)
        fuel_kg = col4.number_input("Propellant Mass (kg)", value=2000000, step=100000)
        col5, col6 = st.columns(2)
        drag_coeff = col5.slider("Aerodynamic Drag Factor (Cd)", 0.1, 1.0, 0.4)
        success_chance = col6.slider("System Reliability Prob. (%)", 10, 100, 90)
        vehicle = "Custom Prototype"

    # Pre-Launch Calculations (Orbital Mechanics)
    total_initial_mass = init_mass + payload_kg + fuel_kg
    initial_twr = thrust / (total_initial_mass * 9.81)
    burn_time_est = 120
    mass_flow_rate = fuel_kg / burn_time_est
    exhaust_velocity = thrust / mass_flow_rate if mass_flow_rate > 0 else 0
    delta_v = exhaust_velocity * np.log(total_initial_mass / (init_mass + payload_kg)) if exhaust_velocity > 0 else 0

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("Launch Platform", vehicle)
    col_m2.metric("Total Lift-off Mass", f"{total_initial_mass:,.0f} kg")
    col_m3.metric("Initial TWR", f"{initial_twr:.2f}")
    col_m4.metric("Est. Delta-V (Δv)", f"{delta_v/1000:.2f} km/s")

    st.markdown("<br>", unsafe_allow_html=True)
    live_telemetry = st.empty()

    if st.button("🚀 INITIATE IGNITION SEQUENCE", use_container_width=True):
        dt = 0.5
        time_steps = 400
        gravity = 9.81
        speed_of_sound = 343 # m/s
        
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
                status = "ANOMALY - CRITICAL ENGINE FAILURE"
                thrust = 0 
            
            # Gravity Turn Pitch Program
            if t > 10 and status == "Nominal":
                pitch_angle = max(0.1, pitch_angle - 0.006 * dt) 
            
            if fuel_kg > 0 and status == "Nominal":
                current_thrust = thrust
                fuel_spent = min(mass_flow_rate * dt, fuel_kg)
                fuel_kg -= fuel_spent
                current_mass -= fuel_spent
            else:
                current_thrust = 0
            
            # Aerodynamics & Environment
            air_density = max(0, 1.225 * np.exp(-z / 8000))
            v_mag = np.sqrt(vx**2 + vy**2 + vz**2)
            mach = v_mag / speed_of_sound
            
            # Dynamic Pressure Q = 1/2 rho v^2
            dynamic_pressure = 0.5 * air_density * (v_mag ** 2)
            if dynamic_pressure > max_q: max_q = dynamic_pressure
            
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
            
            vx += ax * dt
            vy += ay * dt
            vz += az * dt
            
            x += vx * dt
            y += vy * dt
            z += vz * dt
            
            current_twr = current_thrust / (current_mass * gravity) if current_mass > 0 else 0

            # Live HUD Update (sampled every 5 frames for Streamlit performance)
            if t_step % 5 == 0:
                live_telemetry.markdown(f"""
                <div class='telemetry-box'>
                <b>LIVE TELEMETRY T+{t:.1f}s</b> | <b>Status:</b> <span style='color:{'#00FFA3' if status=='Nominal' else '#FF3366'}'>{status}</span><br>
                <b>ALT:</b> {z/1000:.2f} km | <b>VEL:</b> {v_mag:.1f} m/s | <b>MACH:</b> {mach:.2f} | <b>TWR:</b> {current_twr:.2f} | <b>Q:</b> {dynamic_pressure/1000:.1f} kPa
                </div>
                """, unsafe_allow_html=True)
            
            if z <= 0 and t > 5:
                z = 0; vz = 0; vx = 0; vy = 0
                if status != "Nominal": status = "CATASTROPHIC SURFACE IMPACT"
                break
                
            time_list.append(t); x_list.append(x / 1000); y_list.append(y / 1000); z_list.append(z / 1000)
            status_list.append(status); mach_list.append(mach); q_list.append(dynamic_pressure)
            
        progress_bar.empty()
        if will_fail: st.error(f"💥 {status_list[-1]} at T+{failure_time}s. Max-Q reached: {max_q/1000:.1f} kPa")
        else: st.success(f"✨ ORBITAL INSERTION CONFIRMED. Apogee: {z_list[-1]:.2f} km. Max-Q: {max_q/1000:.1f} kPa")
        
        sim_df = pd.DataFrame({"Time (s)": time_list, "Downrange (km)": x_list, "Crossrange (km)": y_list, "Altitude (km)": z_list, "Status": status_list, "Mach": mach_list})
        
        # --- Advanced 3D Trajectory ---
        st.markdown("### 🛰️ 3D Kinematic Spatial Trajectory")
        fig_3d_traj = go.Figure()
        
        # Ground Plane representation
        fig_3d_traj.add_trace(go.Surface(z=np.zeros((5,5)), x=np.linspace(0, max(x_list)*1.2, 5), y=np.linspace(0, max(y_list)*1.2, 5), colorscale='Greens', opacity=0.1, showscale=False, name="Ground / Ocean"))
        
        # Continuous Trajectory Line colored by Mach number
        fig_3d_traj.add_trace(go.Scatter3d(
            x=sim_df["Downrange (km)"], y=sim_df["Crossrange (km)"], z=sim_df["Altitude (km)"],
            mode='lines', line=dict(color=sim_df['Mach'], colorscale='Plasma', width=6, showscale=True, colorbar=dict(title="Mach Number")),
            name="Flight Path"
        ))
        
        # Impact/Current Point Marker
        end_color = "#FF3366" if will_fail else "#00FFA3"
        fig_3d_traj.add_trace(go.Scatter3d(
            x=[sim_df["Downrange (km)"].iloc[-1]], y=[sim_df["Crossrange (km)"].iloc[-1]], z=[sim_df["Altitude (km)"].iloc[-1]],
            mode='markers+text', marker=dict(size=8, color=end_color), text=[status_list[-1]], textposition="top center", name="Terminal State"
        ))

        fig_3d_traj.update_layout(template=cyber_template, height=700, scene=dict(
            xaxis_title="Downrange (km)", yaxis_title="Crossrange (km)", zaxis_title="Altitude (km)",
            xaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(0,242,254,0.1)"),
            yaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(0,242,254,0.1)"),
            zaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(0,242,254,0.1)")
        ))
        st.plotly_chart(fig_3d_traj, use_container_width=True)

        # --- 2D Altitude Profile ---
        st.markdown("### 📺 2D Ascent Profile (Altitude vs Downrange)")
        fig_anim = px.scatter(sim_df.iloc[::2, :].copy(), x="Downrange (km)", y="Altitude (km)", animation_frame="Time (s)", 
                              range_x=[0, sim_df['Downrange (km)'].max() + 10], range_y=[0, sim_df['Altitude (km)'].max() * 1.2],
                              title="Cross-sectional Ascent Trajectory")
        fig_anim.update_traces(marker=dict(size=15, symbol="triangle-up", color=np.where(sim_df.iloc[::2, :]['Status'] == "Nominal", "#00FFA3", "#FF3366"), line=dict(width=2, color="white")))
        fig_anim.add_trace(go.Scatter(x=sim_df["Downrange (km)"], y=sim_df["Altitude (km)"], mode="lines", line=dict(color="rgba(0, 242, 254, 0.4)", width=2), name="Projected Path"))
        fig_anim.update_layout(template=cyber_template, updatemenus=[dict(type="buttons", showactive=False)])
        st.plotly_chart(fig_anim, use_container_width=True)
