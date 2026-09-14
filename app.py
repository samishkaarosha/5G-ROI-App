import streamlit as st
import pandas as pd
import joblib
import numpy as np

# සේව් කරගත් Models දෙකම Load කිරීම (ROI එකට සහ කලාපය සෙවීමට)
model = joblib.load('5g_roi_model.pkl')
kmeans = joblib.load('kmeans_model.pkl')

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

# Calculate Button එක
if st.button("Calculate 5G ROI 🚀"):
    
    # 1. K-Means මඟින් ප්‍රමුඛතා කලාපය ස්වයංක්‍රීයව සෙවීම
    cluster_input = pd.DataFrame([[urban, density, arpu]], columns=['Urban_Pct', 'Density_2024_per_km2', 'Estimated_ARPU_Rs_per_month'])
    predicted_cluster = kmeans.predict(cluster_input)[0]
    
    # කලාපයේ නම සෑදීම
    cluster_map = {0: 'Medium Potential (මධ්‍යම ප්‍රමුඛතා කලාපය)', 1: 'High Potential (ඉහළ ප්‍රමුඛතා කලාපය)', 2: 'Low Potential (අඩු ප්‍රමුඛතා කලාපය)'}
    cluster_name = cluster_map[predicted_cluster]
    
    st.info(f"📍 ඇතුළත් කළ දත්ත අනුව මෙම ප්‍රදේශය අයත් වන්නේ: **{cluster_name}**ටයි.")

    # 2. Random Forest මඟින් ROI එක ගණනය කිරීම
    input_data = pd.DataFrame([[pop, urban, density, arpu, fiber, towers, predicted_cluster]],
                              columns=['Population_2024', 'Urban_Pct', 'Density_2024_per_km2',
                                       'Estimated_ARPU_Rs_per_month', 'Fiber_Distance_km',
                                       'Dialog_Tower_Count', 'Priority_Cluster'])
    prediction = model.predict(input_data)[0]
    
    # ප්‍රතිඵලය පෙන්වීම
    st.success(f"🎉 මෙම ප්‍රදේශයේ අනුමාන 5G ROI ප්‍රතිශතය: **{prediction:.2f}%**")