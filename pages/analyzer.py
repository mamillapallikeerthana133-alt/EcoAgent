import os

import streamlit as st

import google.generativeai as genai


from agent.safety_rules import check_safety

from agent.knowledge_base import get_device_info

from agent.decision_engine import make_decision

from utils.impact import calculate_impact

from utils.report import generate_report

from database import initialize_database, save_analysis


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Analyze Device - EcoAgent",
    page_icon="🌱",
    layout="wide"
)


# ============================================================
# INITIALIZE DATABASE
# ============================================================

initialize_database()


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #666666;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 28px;
        font-weight: 650;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# GEMINI CONFIGURATION
# ============================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(
        api_key=GEMINI_API_KEY
    )


# ============================================================
# GEMINI AI ANALYSIS
# ============================================================

def get_gemini_analysis(
    device_data,
    recommendation
):

    if not GEMINI_API_KEY:

        return (
            "🤖 **AI Explanation Temporarily Unavailable**\n\n"
            "Gemini API key was not found.\n\n"
            "EcoAgent's rule-based recommendation is still available."
        )

    prompt = f"""
You are EcoAgent, an AI-based e-waste life extension assistant.

Your goal is to determine whether an electronic device can be
saved before becoming e-waste.

DEVICE INFORMATION
------------------
Device Type: {device_data.get("device_type")}
Brand: {device_data.get("brand")}
Model: {device_data.get("model")}
Age: {device_data.get("age")} years
Physical Condition: {device_data.get("physical_condition")}
Power Status: {device_data.get("power_status")}
Battery Condition: {device_data.get("battery_condition")}
Recent Upgrade/Repair: {device_data.get("recent_upgrade")}
Main Problem: {device_data.get("main_problem")}
RAM: {device_data.get("ram")}
Storage: {device_data.get("storage")}

RULE-BASED RECOMMENDATION
-------------------------
{recommendation}

Analyze the device and explain the recommendation.

Use these four sections:

1. What is causing the problem?

2. Can a repair or upgrade extend its life?

3. Could the device be reused or donated?

4. When is recycling or safe disposal appropriate?

Give practical and easy-to-understand advice.

Do not invent exact repair prices.

Do not recommend unsafe battery handling.

Focus on extending the useful life of the device whenever reasonably possible.
"""

    try:

        model = genai.GenerativeModel(
            "gemini-3.5-flash"
        )

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception:

        return (
            "🤖 **AI Explanation Temporarily Unavailable**\n\n"
            "Gemini is temporarily unavailable or the API quota "
            "has been reached.\n\n"
            "EcoAgent's rule-based recommendation is still available."
        )


# ============================================================
# PAGE HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🔍 Analyze Your Device</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Find out whether your device can be repaired, upgraded, '
    'reused, donated, recycled, or safely disposed of.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# DEVICE INFORMATION
# ============================================================

st.markdown(
    '<div class="section-title">📱 Device Information</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


with col1:

    device_type = st.selectbox(
        "Device Type",
        [
            "Laptop",
            "Smartphone",
            "Tablet",
            "Battery",
            "TV",
            "Desktop",
            "Other"
        ]
    )

    brand = st.text_input(
        "Brand *",
        placeholder="Example: Dell, HP, Samsung, Apple"
    )

    model = st.text_input(
        "Model",
        placeholder="Example: Inspiron 15"
    )

    age = st.number_input(
        "Device Age (years)",
        min_value=0,
        max_value=30,
        value=3,
        step=1
    )

    physical_condition = st.selectbox(
        "Physical Condition",
        [
            "Good",
            "Fair",
            "Poor",
            "Damaged"
        ]
    )


with col2:

    power_status = st.selectbox(
        "Does the device power on?",
        [
            "Yes",
            "No",
            "Sometimes"
        ]
    )

    battery_options = [
        "Good",
        "Fair",
        "Poor",
        "Swollen"
    ]

    if device_type in [
        "Desktop",
        "TV"
    ]:

        battery_options.append(
            "Not Applicable"
        )

    battery_condition = st.selectbox(
        "Battery Condition",
        battery_options
    )

    recent_upgrade = st.text_input(
        "Recent Upgrade / Repair",
        placeholder="Example: RAM upgraded 1 year ago"
    )

    main_problem = st.text_area(
        "Main Problem *",
        placeholder=(
            "Example: Laptop is very slow and "
            "takes a long time to start"
        ),
        height=120
    )


# ============================================================
# LAPTOP / DESKTOP HARDWARE
# ============================================================

ram = "N/A"
storage = "N/A"

if device_type in [
    "Laptop",
    "Desktop"
]:

    st.markdown(
        '<div class="section-title">💻 Hardware Information</div>',
        unsafe_allow_html=True
    )

    hardware_col1, hardware_col2 = st.columns(2)

    with hardware_col1:

        ram = st.selectbox(
            "RAM",
            [
                "2 GB",
                "4 GB",
                "8 GB",
                "16 GB",
                "32 GB",
                "Not Sure"
            ]
        )

    with hardware_col2:

        storage = st.selectbox(
            "Storage",
            [
                "HDD",
                "SSD",
                "HDD + SSD",
                "Not Sure"
            ]
        )


# ============================================================
# ANALYZE BUTTON
# ============================================================

st.write("")

analyze_button = st.button(
    "🚀 Analyze My Device",
    use_container_width=True
)


# ============================================================
# ANALYSIS
# ============================================================

if analyze_button:

    # --------------------------------------------------------
    # BASIC VALIDATION
    # --------------------------------------------------------

    if not brand.strip():

        st.error(
            "Please enter the device brand."
        )

        st.stop()


    # --------------------------------------------------------
    # DEVICE DATA
    # --------------------------------------------------------

    device_data = {

        "device_type": device_type,

        "brand": brand.strip(),

        "model": model.strip(),

        "age": age,

        "physical_condition": physical_condition,

        "power_status": power_status,

        "battery_condition": battery_condition,

        "recent_upgrade": recent_upgrade.strip(),

        "main_problem": main_problem.strip(),

        "ram": ram,

        "storage": storage
    }


    # --------------------------------------------------------
    # SAFETY CHECK
    # --------------------------------------------------------

    safety_result = check_safety(
        device_data
    )


    if not safety_result["is_safe"]:

        st.markdown(
            '<div class="section-title">🚨 Safety Alert</div>',
            unsafe_allow_html=True
        )

        st.error(
            safety_result["reason"]
        )

        st.warning(
            safety_result["action"]
        )

        st.info(
            "The device assessment has been stopped "
            "because a potential safety issue was detected."
        )

        st.stop()


    # --------------------------------------------------------
    # MAIN PROBLEM VALIDATION
    # --------------------------------------------------------

    if not main_problem.strip():

        st.error(
            "Please describe the main problem with the device."
        )

        st.stop()


    # --------------------------------------------------------
    # KNOWLEDGE BASE
    # --------------------------------------------------------

    device_info = get_device_info(
        device_type
    )


    # --------------------------------------------------------
    # DECISION ENGINE
    # --------------------------------------------------------

    decision = make_decision(
        device_data
    )

    recommendation = decision[
        "recommendation"
    ]


    # ========================================================
    # RECOMMENDATION
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '🎯 EcoAgent Recommendation'
        '</div>',
        unsafe_allow_html=True
    )

    st.success(
        f"Recommended Action: {recommendation}"
    )

    st.markdown(
        "### 💡 Why this recommendation?"
    )

    st.write(
        decision["reason"]
    )


    # ========================================================
    # SUGGESTED ACTIONS
    # ========================================================

    st.markdown(
        "### 🛠️ Suggested Actions"
    )

    for action in decision[
        "actions"
    ]:

        st.write(
            f"• {action}"
        )


    # ========================================================
    # GEMINI AI ANALYSIS
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '🤖 AI Analysis'
        '</div>',
        unsafe_allow_html=True
    )

    with st.spinner(
        "EcoAgent is analyzing your device..."
    ):

        ai_analysis = get_gemini_analysis(
            device_data,
            recommendation
        )

    st.markdown(
        ai_analysis
    )


    # ========================================================
    # ENVIRONMENTAL IMPACT
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '🌱 Environmental Impact'
        '</div>',
        unsafe_allow_html=True
    )

    impact = calculate_impact(
        device_data,
        recommendation
    )

    impact_col1, impact_col2 = st.columns(2)

    with impact_col1:

        st.metric(
            "Estimated Device Mass Kept in Use",
            f'{impact["device_weight"]} kg'
        )

    with impact_col2:

        st.metric(
            "Potential Additional Useful Life",
            impact["useful_life"]
        )


    # ========================================================
    # SAVE ANALYSIS TO DATABASE
    # ========================================================

    save_analysis(
        device_data,
        decision,
        impact
    )

    st.success(
        "✅ This analysis has been saved to your EcoAgent history."
    )


    # ========================================================
    # REPAIR VS REPLACE
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '⚖️ Repair vs Replace'
        '</div>',
        unsafe_allow_html=True
    )

    repair_cost = 6000

    replacement_cost = 40000

    difference = (
        replacement_cost -
        repair_cost
    )

    repair_col1, repair_col2, repair_col3 = st.columns(3)

    with repair_col1:

        st.metric(
            "Estimated Repair Cost",
            f"₹{repair_cost:,}"
        )

    with repair_col2:

        st.metric(
            "Example Replacement Cost",
            f"₹{replacement_cost:,}"
        )

    with repair_col3:

        st.metric(
            "Difference",
            f"₹{difference:,}"
        )

    st.info(
        "These are example MVP values for comparison. "
        "Actual repair and replacement costs depend on "
        "the device, parts and service provider."
    )


    # ========================================================
    # KNOWLEDGE BASE INSIGHTS
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '📚 Knowledge Base Insights'
        '</div>',
        unsafe_allow_html=True
    )

    kb_col1, kb_col2 = st.columns(2)


    with kb_col1:

        st.markdown(
            "### 🔧 Repair Options"
        )

        repair_options = device_info.get(
            "repair_options",
            []
        )

        if repair_options:

            for option in repair_options:

                st.write(
                    f"• {option}"
                )

        else:

            st.write(
                "No specific repair options available."
            )


        st.markdown(
            "### ⚡ Upgrade Options"
        )

        upgrade_options = device_info.get(
            "upgrade_options",
            []
        )

        if upgrade_options:

            for option in upgrade_options:

                st.write(
                    f"• {option}"
                )

        else:

            st.write(
                "No specific upgrade options available."
            )


    with kb_col2:

        st.markdown(
            "### ♻️ Reuse Options"
        )

        reuse_options = device_info.get(
            "reuse_options",
            []
        )

        if reuse_options:

            for option in reuse_options:

                st.write(
                    f"• {option}"
                )

        else:

            st.write(
                "No specific reuse options available."
            )


        st.markdown(
            "### 🗑️ Disposal Options"
        )

        disposal_options = device_info.get(
            "disposal",
            []
        )

        if disposal_options:

            for option in disposal_options:

                st.write(
                    f"• {option}"
                )

        else:

            st.write(
                "Use an authorized e-waste recycling "
                "facility when disposal becomes necessary."
            )


    # ========================================================
    # DEVICE SUMMARY
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '📋 Device Summary'
        '</div>',
        unsafe_allow_html=True
    )

    with st.expander(
        "View Complete Device Information"
    ):

        st.write(
            f"**Device Type:** {device_type}"
        )

        st.write(
            f"**Brand:** {brand}"
        )

        st.write(
            f"**Model:** "
            f"{model if model else 'N/A'}"
        )

        st.write(
            f"**Age:** {age} years"
        )

        st.write(
            f"**Physical Condition:** "
            f"{physical_condition}"
        )

        st.write(
            f"**Power Status:** "
            f"{power_status}"
        )

        st.write(
            f"**Battery Condition:** "
            f"{battery_condition}"
        )

        st.write(
            f"**Recent Upgrade / Repair:** "
            f"{recent_upgrade if recent_upgrade else 'N/A'}"
        )

        st.write(
            f"**Main Problem:** "
            f"{main_problem}"
        )

        if device_type in [
            "Laptop",
            "Desktop"
        ]:

            st.write(
                f"**RAM:** {ram}"
            )

            st.write(
                f"**Storage:** {storage}"
            )


    # ========================================================
    # REPORT GENERATION
    # ========================================================

    report = generate_report(
        device_data,
        decision,
        impact
    )


    # ========================================================
    # DOWNLOAD REPORT
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '📄 EcoAgent Report'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Download the complete analysis as a text report."
    )

    st.download_button(
        label="📄 Download EcoAgent Report",
        data=report,
        file_name="EcoAgent_Report.txt",
        mime="text/plain",
        use_container_width=True
    )


    # ========================================================
    # FINAL RESULT
    # ========================================================

    st.divider()

    st.success(
        f"🌱 EcoAgent recommends: "
        f"{recommendation}"
    )

    st.info(
        "The goal of EcoAgent is to extend the useful "
        "life of electronic devices and reduce "
        "unnecessary e-waste."
    )