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

# Immersive 3D Glassmorphism & Neon Space Styling
st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at 50% 20%, #111827 0%, #030712 100%);
        color: #f3f4f6;
    }
    .main-header {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.9));
        border: 1px solid rgba(56, 189, 248, 0.3);
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        margin-bottom: 24px;
    }
    .metric-card-3d {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-top: 1px solid rgba(56, 189, 248, 0.4);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4), 0 0 15px rgba(56, 189, 248, 0.05);
        transition: transform 0.2s ease;
    }
    .metric-card-3d:hover {
        transform: translateY(-3px);
        border-color: rgba(56, 189, 248, 0.6);
    }
    .alert-box-safe {
        background: rgba(6, 78, 59, 0.6);
        border: 1px solid #059669;
        color: #34d399;
        padding: 16px;
        border-radius: 10px;
        backdrop-filter: blur(6px);
    }
    .alert-box-danger {
        background: rgba(127, 29, 29, 0.6);
        border: 1px solid #dc2626;
        color: #f87171;
        padding: 16px;
        border-radius: 10px;
        backdrop-filter: blur(6px);
        box-shadow: 0 0 20px rgba(220, 38, 38, 0.3);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Header Section
st.markdown(
    """
    <div class="main-header">
        <h1 style='margin:0; font-size: 2.4rem; background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>🌌 ExoSomatic Health</h1>
        <p style='margin:8px 0 0 0; color: #94a3b8; font-size: 1.1rem;'>Autonomous Deep-Space Physiological Digital Twin & Preventative Triage System</p>
    </div>
""",
    unsafe_allow_html=True,
)

# Sidebar Controls
st.sidebar.markdown("### 🛠️ Orbital Command Hub")
mission_day = st.sidebar.slider("Mission Sol / Day", 1, 180, 42)

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚠️ Hazard Simulators")
sim_radiation = st.sidebar.checkbox(
    "Solar Particle Event (SPE) / Radiation Spike", value=False
)
sim_sleep_dep = st.sidebar.checkbox("Severe Sleep Deprivation (< 4 hrs)", value=False)
sim_microg = st.sidebar.checkbox("Microgravity Fluid Shift", value=False)

# Generate 180-Day Simulation Data
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

# 3D Metric Cards Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(
        f"""
        <div class="metric-card-3d">
            <p style='margin:0; color:#94a3b8; font-size:0.9rem;'>HEART RATE</p>
            <h2 style='margin:5px 0 0 0; color:#38bdf8;'>{current_row['Heart Rate (bpm)']:.1f} <span style='font-size:1rem;'>bpm</span></h2>
        </div>
    """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-card-3d">
            <p style='margin:0; color:#94a3b8; font-size:0.9rem;'>SYSTOLIC BP</p>
            <h2 style='margin:5px 0 0 0; color:#818cf8;'>{current_row['Systolic BP (mmHg)']:.1f} <span style='font-size:1rem;'>mmHg</span></h2>
        </div>
    """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
        <div class="metric-card-3d">
            <p style='margin:0; color:#94a3b8; font-size:0.9rem;'>DAILY SLEEP</p>
            <h2 style='margin:5px 0 0 0; color:#34d399;'>{current_row['Sleep (Hours)']:.1f} <span style='font-size:1rem;'>hrs</span></h2>
        </div>
    """,
        unsafe_allow_html=True,
    )

with col4:
    rad_color = (
        "#f87171" if current_row["Radiation Flux (mSv/day)"] > 2.0 else "#34d399"
    )
    st.markdown(
        f"""
        <div class="metric-card-3d">
            <p style='margin:0; color:#94a3b8; font-size:0.9rem;'>RADIATION FLUX</p>
            <h2 style='margin:5px 0 0 0; color:{rad_color};'>{current_row['Radiation Flux (mSv/day)']:.2f} <span style='font-size:1rem;'>mSv</span></h2>
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
    st.markdown("### Interactive Human Physiological System Status")
    system_choice = st.selectbox(
        "Select System to Inspect:",
        [
            "Cardiovascular System (Fluid Shifts & Orthostatic Stress)",
            "Musculoskeletal System (Bone Density & Atrophy)",
            "Neurological & Circadian System (Sleep & Vigilance)",
            "Immune & Radiation Defense System",
        ],
    )

    if "Cardiovascular" in system_choice:
        st.info(
            "**Status:** NOMINAL (Adapted to 0G cephalic fluid shift). Daily tilt-table autoregulation check active."
        )
    elif "Musculoskeletal" in system_choice:
        st.warning(
            "**Status:** MONITORING (1.2% monthly trabecular bone loss). Verify ARED resistance harness calibration."
        )
    elif "Neurological" in system_choice:
        st.error(
            "**Status:** ATTENTION REQUIRED (Circadian desynchronization detected). Adjust cabin spectrum to blue-enriched LED."
        )
    else:
        st.success(
            "**Status:** PROTECTED. Water-wall shadow shielding active against GCR background flux."
        )

with tab2:
    st.markdown("### Deep-Space Telemetry Time Series")
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
        title=f"Mission Telemetry Curve: {metric_to_plot}",
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
        font_color="#f3f4f6",
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
    )
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.markdown("### Autonomous AI Flight Surgeon Recommendations")

    if (
        current_row["Radiation Flux (mSv/day)"] > 2.0
        or current_row["Sleep (Hours)"] < 4.0
    ):
        st.markdown(
            f"""
            <div class="alert-box-danger">
                <strong>🚨 CRITICAL ANOMALY DETECTED (Sol {mission_day})</strong><br>
                • Threshold breach identified in environmental/physiological sensors.<br>
                • <strong>Action Required:</strong> Relocate to central water-wall storm shelter, administer antioxidant prophylaxis, and log PVT cognitive score.
            </div>
        """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="alert-box-safe">
                <strong>✅ ALL SYSTEMS NOMINAL</strong><br>
                • Crew member operating within NASA Human Research Program baseline risk parameters.<br>
                • Continue standard resistive exercise and circadian schedule.
            </div>
        """,
            unsafe_allow_html=True,
        )

st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#64748b; font-size:0.85rem;'>ExoSomatic Health | Built for NASA Space Apps Challenge 2026</p>",
    unsafe_allow_html=True,
)
