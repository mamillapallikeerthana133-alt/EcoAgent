# ============================================================
# EcoAgent - Main Dashboard
# ============================================================

import streamlit as st
import pandas as pd

from database import (
    initialize_database,
    get_analysis_history
)


# ------------------------------------------------------------
# Page Configuration
# ------------------------------------------------------------

st.set_page_config(
    page_title="EcoAgent",
    page_icon="🌱",
    layout="wide"
)


# ------------------------------------------------------------
# Initialize Database
# ------------------------------------------------------------

initialize_database()


# ------------------------------------------------------------
# Custom CSS
# ------------------------------------------------------------

st.markdown(
    """
    <style>

    /* Statistics cards */
    .stat-card {
        border: 1px solid #d9d9d9;
        border-radius: 12px;
        padding: 18px 20px;
        background-color: #ffffff;
        min-height: 125px;
        margin-bottom: 15px;
    }

    .stat-title {
        font-size: 15px;
        font-weight: 600;
        margin-bottom: 12px;
    }

    .stat-value {
        font-size: 30px;
        font-weight: 600;
        margin-top: 5px;
    }

    /* Feature cards */
    .feature-card {
        border: 1px solid #d9d9d9;
        border-radius: 12px;
        padding: 20px;
        min-height: 140px;
        background-color: #ffffff;
    }

    .feature-title {
        font-size: 19px;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .feature-text {
        font-size: 14px;
        line-height: 1.5;
    }

    /* Goal box */
    .goal-box {
        border-radius: 10px;
        padding: 15px 18px;
        background-color: #eaf3ff;
        margin-top: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# Sidebar Navigation
# ------------------------------------------------------------

st.sidebar.title("🌱 EcoAgent")

st.sidebar.markdown("### Navigation")

if st.sidebar.button(
    "🏠 Dashboard",
    use_container_width=True
):
    st.switch_page("app.py")

if st.sidebar.button(
    "🔍 Analyze Device",
    use_container_width=True
):
    st.switch_page("pages/analyzer.py")

if st.sidebar.button(
    "📊 Impact & Report",
    use_container_width=True
):
    st.switch_page("pages/impact_report.py")


# ------------------------------------------------------------
# Load Analysis History
# ------------------------------------------------------------

history = get_analysis_history()


# ------------------------------------------------------------
# Calculate Statistics
# ------------------------------------------------------------

total_devices = len(history)

total_mass = sum(
    record[6] or 0
    for record in history
)

repair_count = sum(
    1 for record in history
    if record[5] == "Repair"
)

upgrade_count = sum(
    1 for record in history
    if record[5] == "Upgrade"
)

reuse_count = sum(
    1 for record in history
    if record[5] == "Reuse / Donate"
)

recycle_count = sum(
    1 for record in history
    if record[5] == "Recycle"
)

disposal_count = sum(
    1 for record in history
    if record[5] == "Safe Disposal"
)


# ============================================================
# DASHBOARD
# ============================================================

st.title("🌱 EcoAgent")

st.write(
    "Smart E-Waste Life Extension Agent"
)

st.markdown(
    "## Can this device be saved before it becomes e-waste?"
)

st.write(
    "EcoAgent analyzes an old electronic device and helps determine "
    "whether it can be repaired, upgraded, reused, donated, recycled, "
    "or safely disposed of."
)


# ============================================================
# ECOAGENT STATISTICS
# ============================================================

st.markdown("## 📈 EcoAgent Statistics")


# First row
col1, col2, col3 = st.columns(3)


with col1:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-title">📱 Devices Analyzed</div>
            <div class="stat-value">{total_devices}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-title">🌱 Device Mass</div>
            <div class="stat-value">{total_mass:.1f} kg</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-title">⚡ Upgrades</div>
            <div class="stat-value">{upgrade_count}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# Second row
col1, col2, col3, col4 = st.columns(4)


with col1:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-title">🔧 Repairs</div>
            <div class="stat-value">{repair_count}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-title">♻️ Reuse / Donate</div>
            <div class="stat-value">{reuse_count}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-title">🗑️ Recycled</div>
            <div class="stat-value">{recycle_count}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col4:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-title">🚨 Safe Disposal</div>
            <div class="stat-value">{disposal_count}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# RECOMMENDATION DISTRIBUTION
# ============================================================

st.markdown("## 📊 Recommendation Distribution")


recommendation_data = pd.DataFrame(
    {
        "Recommendation": [
            "Repair",
            "Upgrade",
            "Reuse / Donate",
            "Recycle",
            "Safe Disposal"
        ],
        "Devices": [
            repair_count,
            upgrade_count,
            reuse_count,
            recycle_count,
            disposal_count
        ]
    }
)


st.bar_chart(
    recommendation_data,
    x="Recommendation",
    y="Devices",
    use_container_width=True
)


st.caption(
    "This chart shows how EcoAgent has classified the analyzed devices."
)


# ============================================================
# FEATURE CARDS
# ============================================================

col1, col2, col3 = st.columns(3)


with col1:
    st.markdown(
        """
        <div class="feature-card">

        <div class="feature-title">
        🔧 Repair
        </div>

        <div class="feature-text">
        Identify problems that may be repairable instead of
        replacing the entire device.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with col2:
    st.markdown(
        """
        <div class="feature-card">

        <div class="feature-title">
        ⚡ Upgrade
        </div>

        <div class="feature-text">
        Find possible upgrades such as RAM, SSD or battery
        replacement to extend device life.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with col3:
    st.markdown(
        """
        <div class="feature-card">

        <div class="feature-title">
        ♻️ Reuse / Recycle
        </div>

        <div class="feature-text">
        Find out whether the device can be reused, donated,
        recycled or safely disposed of.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# HOW ECOAGENT WORKS
# ============================================================

st.markdown("## 🔄 How EcoAgent Works")

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.markdown("### 1️⃣")
    st.write("Enter Device Details")


with col2:
    st.markdown("### 2️⃣")
    st.write("AI Analyzes the Device")


with col3:
    st.markdown("### 3️⃣")
    st.write("Get Recommendation")


with col4:
    st.markdown("### 4️⃣")
    st.write("Extend Device Life")


if st.button(
    "🚀 Analyze My Device",
    use_container_width=True
):
    st.switch_page("pages/analyzer.py")


# ============================================================
# RECENT ANALYSIS HISTORY
# ============================================================

st.markdown("## 📊 Recent Analysis History")

if history:

    st.write(
        f"You have completed {len(history)} analysis(es)."
    )

    for record in history[:5]:

        (
            record_id,
            device_type,
            brand,
            model,
            age,
            recommendation,
            device_weight,
            useful_life,
            analysis_date
        ) = record

        model_display = model if model else "Unknown Model"

        st.markdown(
            f"""
            **#{record_id} — {brand} {model_display}**

            📱 {device_type}
            &nbsp;&nbsp;&nbsp;&nbsp;
            🎯 {recommendation}
            &nbsp;&nbsp;&nbsp;&nbsp;
            📅 {analysis_date}
            """
        )

        st.divider()

else:

    st.info(
        "No device analyses have been completed yet."
    )


# ============================================================
# OUR GOAL
# ============================================================

st.markdown("## 🌍 Our Goal")

st.write(
    "EcoAgent focuses on preventing unnecessary e-waste by helping "
    "people extend the useful life of their electronic devices."
)

st.write(
    "Instead of immediately throwing away an old device, "
    "EcoAgent asks:"
)

st.markdown(
    """
    <div class="goal-box">

    💡 <strong>
    Can we repair it, upgrade it, reuse it, or donate it before recycling?
    </strong>

    </div>
    """,
    unsafe_allow_html=True
)