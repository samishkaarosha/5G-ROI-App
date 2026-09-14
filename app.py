import streamlit as st
import pandas as pd
import joblib

# Load trained models and processed dataset
model = joblib.load('5g_roi_model.pkl')
kmeans = joblib.load('kmeans_model.pkl')
data = pd.read_csv('final_5g_data.csv')

st.set_page_config(page_title="5G ROI Dashboard", page_icon="📡", layout="wide")

# Sidebar Navigation
st.sidebar.title("📌 Navigation")
app_mode = st.sidebar.radio("Select Page:", ["🏆 District Rankings", "🧮 ROI Calculator"])

# Page 1: District Rankings Leaderboard
if app_mode == "🏆 District Rankings":
    st.title("🏆 5G Deployment: District Leaderboard")
    st.write("Sri Lankan districts ranked from highest to lowest potential based on predicted ROI.")
    
    ranked_data = data.sort_values(by='ROI_Percentage', ascending=False).reset_index(drop=True)
    ranked_data.index += 1
    display_data = ranked_data[['District', 'Priority_Cluster', 'ROI_Percentage']]
    display_data.columns = ['District', 'Economic Cluster', 'Estimated ROI (%)']
    st.dataframe(display_data, use_container_width=True)

# Page 2: Custom ROI Calculator
elif app_mode == "🧮 ROI Calculator":
    st.title("📡 Custom 5G ROI Calculator")
    st.write("Enter area metrics and total investment to compute exact net returns.")

    col1, col2 = st.columns(2)
    with col1:
        investment = st.number_input("Total Investment / CapEx (Rs.)", value=10000000, step=500000)
        urban = st.slider("Urban Percentage (%)", 0.0, 100.0, 20.0)
        density = st.number_input("Population Density (per km²)", value=500.0)
    with col2:
        arpu = st.number_input("Estimated ARPU (Rs.)", value=600.0)
        fiber = st.slider("Distance to Fiber Node (km)", 0.0, 5.0, 1.0)
        towers = st.number_input("Existing Tower Count", value=10)

    if st.button("Calculate Net Return 🚀"):
        cluster_input = pd.DataFrame([[urban, density, arpu]], columns=['Urban_Pct', 'Density_2024_per_km2', 'Estimated_ARPU_Rs_per_month'])
        predicted_cluster = kmeans.predict(cluster_input)[0]
        
        cluster_map = {0: 'Medium Potential', 1: 'High Potential', 2: 'Low Potential'}
        st.info(f"📍 Classified Zone: **{cluster_map[predicted_cluster]}**")

        input_data = pd.DataFrame([[urban, density, arpu, fiber, towers, predicted_cluster]],
                                  columns=['Urban_Pct', 'Density_2024_per_km2',
                                           'Estimated_ARPU_Rs_per_month', 'Fiber_Distance_km',
                                           'Dialog_Tower_Count', 'Priority_Cluster'])
        roi_percentage = model.predict(input_data)[0]
        estimated_profit = investment * (roi_percentage / 100)
        
        st.success(f"💰 **Estimated Net Profit: Rs. {estimated_profit:,.2f}**")
        st.caption(f"Based on a predicted ROI rate of {roi_percentage:.2f}%")