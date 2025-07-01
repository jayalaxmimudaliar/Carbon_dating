import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import io
# Define emission factors
EMISSION_FACTORS = {
    "India": {
        "Transportation": 0.14,  # kg CO2 per km
        "Electricity": 0.82,     # kg CO2 per kWh
        "Diet": 1.25,            # kg CO2 per meal
        "Waste": 0.1             # kg CO2 per kg
    }
}

# Set layout and title
st.set_page_config(layout="wide", page_title="Personal Carbon Calculator")
st.title("🌿 Personal Carbon Calculator App")

# Country (only India for now)
country = st.selectbox("🌍 Select your country", ["India"])

# Input columns
col1, col2 = st.columns(2)

with col1:
    distance = st.slider("🚗 Daily commute distance (km)", 0.0, 100.0, 10.0)
    electricity = st.slider("💡 Monthly electricity consumption (kWh)", 0.0, 1000.0, 250.0)

with col2:
    waste = st.slider("🗑️ Weekly waste generation (kg)", 0.0, 100.0, 5.0)
    meals = st.number_input("🍽️ Meals per day", 0, 10, 3)

# Normalize to yearly
distance *= 365
electricity *= 12
waste *= 52
meals *= 365

# Emission calculation
transport = EMISSION_FACTORS[country]["Transportation"] * distance / 1000
power = EMISSION_FACTORS[country]["Electricity"] * electricity / 1000
diet = EMISSION_FACTORS[country]["Diet"] * meals / 1000
trash = EMISSION_FACTORS[country]["Waste"] * waste / 1000

total = round(transport + power + diet + trash, 2)

# Pie chart data
emission_data = {
    "Transportation": transport,
    "Electricity": power,
    "Diet": diet,
    "Waste": trash
}

# Display emissions
if st.button("Calculate CO2 Emissions"):
    st.header("📊 Your Emissions Summary")
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("🛋️ Breakdown")
        st.info(f"Transportation: {transport:.2f} tonnes/year")
        st.info(f"Electricity: {power:.2f} tonnes/year")
        st.info(f"Diet: {diet:.2f} tonnes/year")
        st.info(f"Waste: {trash:.2f} tonnes/year")

    with col4:
        st.subheader("🌿 Total Carbon Footprint")
        st.success(f"{total} tonnes CO2 per year")

        # Pie chart
        fig, ax = plt.subplots()
        ax.pie(emission_data.values(), labels=emission_data.keys(), autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)

    # Tips section
    st.markdown("---")
    top_source = max(emission_data, key=emission_data.get)
    tips = {
        "Transportation": ["Use public transport", "Carpool", "Switch to cycling"],
        "Electricity": ["Use LED bulbs", "Unplug idle electronics", "Use solar where possible"],
        "Diet": ["Reduce red meat", "Avoid food waste", "Try plant-based meals"],
        "Waste": ["Recycle", "Compost organic waste", "Avoid plastic packaging"]
    }

    st.subheader(f"🔹 Tips to reduce {top_source} emissions:")
    for tip in tips[top_source]:
        st.write(f"- {tip}")
    # CSV Export
    st.markdown("---")
    st.subheader("📥 Download Your Emission Report")
    df = pd.DataFrame({
        "Category": list(emission_data.keys()) + ["Total"],
        "Emissions (tonnes CO2/year)": [round(v, 2) for v in emission_data.values()] + [total]
    })

    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    st.download_button(
        label="Download Emission Report as CSV",
        data=csv_buffer.getvalue(),
        file_name="carbon_emission_report.csv",
        mime="text/csv"
    )