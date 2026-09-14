import streamlit as st
import pandas as pd
import joblib
import numpy as np

# සේව් කරගත් Model එක Load කිරීම
model = joblib.load('5g_roi_model.pkl')

st.set_page_config(page_title="5G ROI Predictor", page_icon="📡")

st.title("📡 5G ROI Prediction Software")
st.write("දිස්ත්‍රික්කයේ තොරතුරු ඇතුළත් කර 5G ආයෝජනයෙන් ලැබෙන ලාභ ප්‍රතිශතය (ROI) ගණනය කරන්න.")

# තොරතුරු ලබාගන්නා කොටු (Inputs)
col1, col2 = st.columns(2)
with col1:
    pop = st.number_input("ජනගහනය (Population)", value=500000)
    urban = st.slider("නාගරික ප්‍රතිශතය (%)", 0.0, 100.0, 20.0)
    density = st.number_input("ජනගහන ඝනත්වය (per km²)", value=500)
with col2:
    arpu = st.number_input("අනුමාන ARPU ආදායම (Rs.)", value=600)
    fiber = st.slider("Fiber ජාලයට ඇති දුර (km)", 0.0, 5.0, 1.0)
    towers = st.number_input("දැනට ඇති Dialog කුලුනු ගණන", value=10)

cluster = st.selectbox("ප්‍රමුඛතා කලාපය", options=[1, 0, 2], format_func=lambda x: "High Potential" if x==1 else ("Medium Potential" if x==0 else "Low Potential"))

# Calculate Button එක
if st.button("Calculate 5G ROI 🚀"):
    # දත්ත Model එකට යැවීම
    input_data = pd.DataFrame([[pop, urban, density, arpu, fiber, towers, cluster]],
                              columns=['Population_2024', 'Urban_Pct', 'Density_2024_per_km2',
                                       'Estimated_ARPU_Rs_per_month', 'Fiber_Distance_km',
                                       'Dialog_Tower_Count', 'Priority_Cluster'])
    prediction = model.predict(input_data)[0]
    
    # ප්‍රතිඵලය පෙන්වීම
    st.success(f"🎉 මෙම ප්‍රදේශයේ අනුමාන 5G ROI ප්‍රතිශතය: **{prediction:.2f}%**")