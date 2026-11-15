import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# Page Config
st.set_page_config(
    page_title="ExoSomatic Health | Deep-Space Command",
    page_icon="🌌",
    layout="wide",
)

# High-End Sci-Fi Mission Control Styling
st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at 50% 10%, #090d16 0%, #020408 100%);
        color: #e2e8f0;
        font-family: 'Segoe UI', Roboto, Helvetica, sans-serif;
    }
    .command-header {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9), rgba(30, 41, 59, 0.8));
        border: 1px solid rgba(56, 189, 248, 0.4);
        border-left: 4px solid #38bdf8;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.7), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        margin-bottom: 24px;
    }
    .metric-card-sci {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.9));
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-top: 2px solid #38bdf8;
        padding: 18px;
        border-radius: 10px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5);
        position: relative;
    }
    .status-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    .badge-nominal { background-color: rgba(5, 150, 105, 0.2); color: #34d399; border: 1px solid #059669; }
    .badge-warning { background-color: rgba(217, 119, 6, 0.2); color: #fbbf24; border: 1px solid #d97706; }
    .badge-danger { background-color: rgba(220, 38, 38, 0.2); color: #f87171; border: 1px solid #dc2626; }
    
    /* Interactive Card Styling */
    .diagnostic-card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(56, 189, 248, 0.2);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 12px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Header Section
st.markdown(
    """
    <div class="command-header">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h1 style='margin:0; font-size: 2.2rem; color: #f8fafc; font-weight: 700; letter-spacing: -0.02em;'>🌌 EXOSOMATIC HEALTH</h1>
                <p style='margin:6px 0 0 0; color: #94a3b8; font-size: 1rem;'>Autonomous Deep-Space Physiological Digital Twin & Preventative Triage System</p>
            </div>
            <div>
                <span class="status-badge badge-nominal">● SYSTEM ONLINE (TELEMETRY LIVE)</span>
            </div>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# Sidebar Controls
st.sidebar.markdown(
    "<h3 style='color:#38bdf8;'>🛠️ Mission Command</h3>", unsafe_allow_html=True
)
mission_day = st.sidebar.slider("Mission Sol / Day", 1, 180, 42)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<h3 style='color:#f87171;'>⚠️ Hazard Simulators</h3>", unsafe_allow_html=True
)
sim_radiation = st.sidebar.checkbox(
    "Solar Particle Event (SPE) / Radiation Spike", value=False
)
sim_sleep_dep = st.sidebar.checkbox("Severe Sleep Deprivation (< 4 hrs)", value=False)
sim_microg = st.sidebar.checkbox("Microgravity Fluid Shift", value=False)

# Generate Simulation Data
np.random.seed(42)
days = np.arange(1, 181)
base_hr = 65 + np.random.normal(0, 3, 180).cumsum() * 0.05
base_bp = 120 + np.random.normal(0, 2, 180).cumsum() * 0.03
base_sleep = 7.2 + np.random.normal(0, 0.4, 180)
base_rad = 0.4 + (days * 0.005) + np.random.exponential(0.1, 180)

if sim_radiation:
    base_rad[mission_day - 1] += 4.8
    base_hr[mission_day - 1] += 16
if sim_sleep_dep:
    base_sleep[mission_day - 1] = 3.1
    base_bp[mission_day - 1] += 14
if sim_microg:
    base_bp[mission_day - 1] -= 12

df_telemetry = pd.DataFrame(
    {
        "Sol": days,
        "Heart Rate (bpm)": np.clip(base_hr, 50, 115),
        "Systolic BP (mmHg)": np.clip(base_bp, 85, 160),
        "Sleep (Hours)": np.clip(base_sleep, 2, 10),
        "Radiation Flux (mSv/day)": np.clip(base_rad, 0.1, 9.0),
    }
)

current_row = df_telemetry[df_telemetry["Sol"] == mission_day].iloc[0]

# 4 Sci-Fi Metric Cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(
        f"""
        <div class="metric-card-sci">
            <span style="color: #64748b; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.05em;">HEART RATE</span>
            <h2 style="margin: 6px 0 0 0; color: #38bdf8; font-size: 1.8rem;">{current_row['Heart Rate (bpm)']:.1f} <span style="font-size: 0.9rem; color: #94a3b8;">bpm</span></h2>
        </div>
    """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-card-sci">
            <span style="color: #64748b; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.05em;">SYSTOLIC BP</span>
            <h2 style="margin: 6px 0 0 0; color: #818cf8; font-size: 1.8rem;">{current_row['Systolic BP (mmHg)']:.1f} <span style="font-size: 0.9rem; color: #94a3b8;">mmHg</span></h2>
        </div>
    """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
        <div class="metric-card-sci">
            <span style="color: #64748b; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.05em;">DAILY SLEEP</span>
            <h2 style="margin: 6px 0 0 0; color: #34d399; font-size: 1.8rem;">{current_row['Sleep (Hours)']:.1f} <span style="font-size: 0.9rem; color: #94a3b8;">hrs</span></h2>
        </div>
    """,
        unsafe_allow_html=True,
    )

with col4:
    rad_val = current_row["Radiation Flux (mSv/day)"]
    badge_color = "#f87171" if rad_val > 2.0 else "#34d399"
    st.markdown(
        f"""
        <div class="metric-card-sci" style="border-top-color: {badge_color};">
            <span style="color: #64748b; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.05em;">RADIATION FLUX</span>
            <h2 style="margin: 6px 0 0 0; color: {badge_color}; font-size: 1.8rem;">{rad_val:.2f} <span style="font-size: 0.9rem; color: #94a3b8;">mSv</span></h2>
        </div>
    """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# Main Navigation Tabs
tab1, tab2, tab3 = st.tabs(
    [
        "🩺 Body-System Diagnostics",
        "📈 180-Day Telemetry Trends",
        "🚨 Autonomous Triage & Countermeasures",
    ]
)

with tab1:
    st.markdown("### Interactive Physiological Sub-Systems")
    st.markdown(
        "Select a system module below to inspect real-time telemetry diagnostics:"
    )

    sys_col1, sys_col2 = st.columns(2)
    with sys_col1:
        card_sys1 = st.button(
            "🫀 Cardiovascular System (Fluid Shifts)", use_container_width=True
        )
        card_sys2 = st.button(
            "🦴 Musculoskeletal System (Bone Density)", use_container_width=True
        )
    with sys_col2:
        card_sys3 = st.button(
            "🧠 Neurological & Circadian System", use_container_width=True
        )
        card_sys4 = st.button(
            "🛡️ Immune & Radiation Defense", use_container_width=True
        )

    # State handler for interactive cards
    if "selected_system" not in st.session_state:
        st.session_state.selected_system = "Cardiovascular"

    if card_sys1:
        st.session_state.selected_system = "Cardiovascular"
    if card_sys2:
        st.session_state.selected_system = "Musculoskeletal"
    if card_sys3:
        st.session_state.selected_system = "Neurological"
    if card_sys4:
        st.session_state.selected_system = "Immune"

    st.markdown("<br>", unsafe_allow_html=True)
    if st.session_state.selected_system == "Cardiovascular":
        st.markdown(
            """
            <div class="diagnostic-card">
                <h4 style="color:#38bdf8; margin-top:0;">🫀 Cardiovascular Status: NOMINAL</h4>
                <p><strong>Condition:</strong> Adapted to 0G cephalic fluid shift. Orthostatic autoregulation stable.</p>
                <p><strong>Self-Evaluation Protocol:</strong> Daily tilt-table autoregulation check & 30-min cycle ergometer session.</p>
            </div>
        """,
            unsafe_allow_html=True,
        )
    elif st.session_state.selected_system == "Musculoskeletal":
        st.markdown(
            """
            <div class="diagnostic-card" style="border-color: rgba(217, 119, 6, 0.4);">
                <h4 style="color:#fbbf24; margin-top:0;">🦴 Musculoskeletal Status: MONITORING ACTIVE</h4>
                <p><strong>Condition:</strong> 1.2% monthly trabecular bone mineral density loss detected in lower lumbar region.</p>
                <p><strong>Self-Evaluation Protocol:</strong> Verify ARED (Resistive Exercise Device) load configuration and Vitamin D intake.</p>
            </div>
        """,
            unsafe_allow_html=True,
        )
    elif st.session_state.selected_system == "Neurological":
        st.markdown(
            """
            <div class="diagnostic-card" style="border-color: rgba(220, 38, 38, 0.4);">
                <h4 style="color:#f87171; margin-top:0;">🧠 Neurological & Circadian Status: ATTENTION REQUIRED</h4>
                <p><strong>Condition:</strong> Sleep fragmentation and circadian rhythm desynchronization identified.</p>
                <p><strong>Self-Evaluation Protocol:</strong> Adjust cabin LED spectrum to blue-enriched lighting and log Psychomotor Vigilance Test (PVT).</p>
            </div>
        """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="diagnostic-card">
                <h4 style="color:#34d399; margin-top:0;">🛡️ Immune & Radiation Defense: PROTECTED</h4>
                <p><strong>Condition:</strong> Cellular oxidative stress within normal limits. Water-wall shadow shield optimal.</p>
                <p><strong>Self-Evaluation Protocol:</strong> Monitor NASA DONKI real-time solar flare advisory feed.</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

with tab2:
    st.markdown("### Deep-Space Telemetry Time-Series Analysis")
    metric_to_plot = st.selectbox(
        "Select Telemetry Stream:",
        [
            "Heart Rate (bpm)",
            "Systolic BP (mmHg)",
            "Sleep (Hours)",
            "Radiation Flux (mSv/day)",
        ],
    )

    fig = px.line(
        df_telemetry,
        x="Sol",
        y=metric_to_plot,
        title=f"Longitudinal Mission Telemetry: {metric_to_plot}",
        markers=True,
    )
    fig.add_vline(
        x=mission_day,
        line_dash="dash",
        line_color="#f43f5e",
        annotation_text="Current Sol",
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0",
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)"),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)"),
    )
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.markdown("### Autonomous AI Flight Surgeon Triage Engine")

    if (
        current_row["Radiation Flux (mSv/day)"] > 2.0
        or current_row["Sleep (Hours)"] < 4.0
    ):
        st.markdown(
            f"""
            <div style="background: rgba(127, 29, 29, 0.4); border: 1px solid #dc2626; padding: 20px; border-radius: 10px;">
                <h3 style="color: #f87171; margin-top:0;">🚨 CRITICAL THRESHOLD BREACH (Sol {mission_day})</h3>
                <p><strong>Hazard Identified:</strong> Environmental radiation flux or sleep deprivation threshold exceeded.</p>
                <p><strong>Mandatory Preventative Action:</strong></p>
                <ul>
                    <li>Immediately relocate crew member to central water-wall storm shelter module.</li>
                    <li>Initiate 500mg antioxidant prophylaxis sequence.</li>
                    <li>Record mandatory PVT cognitive alertness assessment.</li>
                </ul>
            </div>
        """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div style="background: rgba(6, 78, 59, 0.4); border: 1px solid #059669; padding: 20px; border-radius: 10px;">
                <h3 style="color: #34d399; margin-top:0;">✅ ALL CREW VITALS NOMINAL</h3>
                <p>Physiological parameters remain strictly aligned with NASA Human Research Program (HRP) baseline safety limits. Continue standard transit operations.</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#64748b; font-size:0.85rem;'>ExoSomatic Health | NASA Space Apps Challenge 2026</p>",
    unsafe_allow_html=True,
)
