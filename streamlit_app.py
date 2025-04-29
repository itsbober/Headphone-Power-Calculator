import streamlit as st
import math

# Set page configuration
st.set_page_config(
    page_title="Headphone Power Calculator",
    layout="centered"
)

# Custom CSS for Medium-like styling
st.markdown("""
    <style>
    .main {
        max-width: 800px;
        margin: 0 auto;
        font-family: 'Source Serif Pro', serif;
    }
    h1 {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 24px;
    }
    .stTextInput > div > div > input {
        font-size: 16px;
    }
    .result-container {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 5px;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("Headphone Power Calculator")

# Create two columns for inputs
col1, col2 = st.columns(2)

with col1:
    sensitivity = st.number_input(
        "Sensitivity",
        min_value=0.0,
        value=100.0,
        step=0.1,
        help="Headphone sensitivity"
    )
    
    impedance = st.number_input(
        "Impedance (Ω)",
        min_value=0.0,
        value=32.0,
        step=0.1,
        help="Headphone impedance in ohms"
    )

with col2:
    unit = st.selectbox(
        "Sensitivity Unit",
        options=["dB/mW", "dB/V"],
        index=0,
        help="Choose the unit of sensitivity measurement"
    )

# SPL Slider
target_spl = st.slider(
    "Target SPL (dB)",
    min_value=60.0,
    max_value=120.0,
    value=110.0,
    step=0.1,
    help="Target Sound Pressure Level in decibels"
)

# Calculate and display results automatically
try:
    # Convert unit selection to match original code
    unit = 'dbv' if unit == 'dB/V' else 'dbmw'

    # Calculate both sensitivity representations
    if unit == 'dbv':
        sensitivity_dbmw = sensitivity - 10 * math.log10(1000 / impedance)
        sensitivity_dbv = sensitivity
    else:
        sensitivity_dbmw = sensitivity
        sensitivity_dbv = sensitivity + 10 * math.log10(1000 / impedance)

    # Use dB/mW for power calculations
    spl_diff = target_spl - sensitivity_dbmw
    power_mW = 10 ** (spl_diff / 10)
    power_W = power_mW / 1000
    voltage_V = math.sqrt(power_W * impedance)
    current_A = voltage_V / impedance

    # Display results in a nice format
    st.markdown("### Results")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Voltage Required", f"{voltage_V:.4f} V")
        st.metric("Current Required", f"{current_A*1000:.4f} mA")
        
    with col2:
        st.metric("Power Required", f"{power_mW:.4f} mW")
        st.metric("Target Loudness", f"{target_spl:.1f} dB")

    # Create a progress bar for SPL visualization
    spl_percentage = (target_spl - 60) / (120 - 60)  # Normalize to 0-1 range
    st.progress(spl_percentage)

    # Add SPL context
    if target_spl <= 70:
        spl_context = "Quiet listening level"
    elif target_spl <= 85:
        spl_context = "Normal listening level"
    elif target_spl <= 100:
        spl_context = "Loud listening level"
    else:
        spl_context = "Very loud listening level 💔🥀 "
    
    st.caption(spl_context)

    # Display sensitivity conversions
    st.markdown("### Sensitivity Conversions")
    st.info(f"""
        - Sensitivity in dB/V: {sensitivity_dbv:.4f}
        - Sensitivity in dB/mW: {sensitivity_dbmw:.4f}
    """)

except ValueError as e:
    st.error("Error: Invalid input values. Please check your inputs and try again.")
