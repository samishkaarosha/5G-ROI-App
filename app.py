import streamlit as st
import pandas as pd
import joblib

# Load models and data
model = joblib.load('5g_roi_model.pkl')
kmeans = joblib.load('kmeans_model.pkl')
data = pd.read_csv('final_5g_data.csv')

st.set_page_config(page_title="Dialog 5G ROI Intelligence Hub", page_icon="📡", layout="wide")

if 'screen' not in st.session_state:
    st.session_state.screen = 'welcome'

# -------------------------------------------------------------------------
# Screen 1: Welcome / Launch Screen (Attractive UI & Dual Buttons)
# -------------------------------------------------------------------------
if st.session_state.screen == 'welcome':
    
    # Center Logo perfectly using balanced columns
    col_l1, col_l2, col_l3 = st.columns([1.5, 1, 1.5])
    with col_l2:
        try:
            st.image('dialog_logo.png', width=220)
        except:
            st.markdown("<h2 style='text-align: center; color: #E60000;'>Dialog Axiata PLC</h2>", unsafe_allow_html=True)

    st.markdown("""
        <div style='text-align: center; padding: 10px 0px 20px 0px;'>
            <h2 style='color: #ffffff; font-weight: 600;'>5G Network Expansion & ROI Intelligence Platform</h2>
            <p style='color: #b0b0b0; font-size: 1.1em;'>Select a target district or choose an advanced tool below to begin your analysis.</p>
        </div>
    """, unsafe_allow_html=True)

    # Main Selection Box inside an attractive container
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.markdown("### 🎯 District Quick Insight")
            district_list = sorted(data['District'].unique().tolist())
            selected_district = st.selectbox("Select Target District for 5G Deployment:", district_list)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Generate District Analytics 🚀", use_container_width=True):
                st.session_state.selected_district = selected_district
                st.session_state.screen = 'analytics'
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Two Separate Buttons at the bottom for direct access
    st.markdown("<h4 style='text-align: center; color: #ffffff;'>Or Access Advanced Tools</h4>", unsafe_allow_html=True)
    bcol1, bcol2 = st.columns(2)
    with bcol1:
        if st.button("🏆 Open Full District Leaderboard", use_container_width=True):
            st.session_state.screen = 'leaderboard'
            st.rerun()
    with bcol2:
        if st.button("🧮 Open Custom ROI Calculator", use_container_width=True):
            st.session_state.screen = 'calculator'
            st.rerun()

# -------------------------------------------------------------------------
# Screen 2: District-Specific Quick Analytics View
# -------------------------------------------------------------------------
elif st.session_state.screen == 'analytics':
    district = st.session_state.selected_district
    row = data[data['District'] == district].iloc[0]
    
    ranked_full = data.sort_values(by='ROI_Percentage', ascending=False).reset_index(drop=True)
    district_rank = ranked_full[ranked_full['District'] == district].index[0] + 1
    total_districts = len(ranked_full)

    st.markdown(f"## 📊 5G Deployment Report: **{district}**")
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(label="National ROI Rank", value=f"#{district_rank} of {total_districts}")
    with m2:
        st.metric(label="Predicted ROI Rate", value=f"{row['ROI_Percentage']:.2f}%")
    with m3:
        st.metric(label="Total Population", value=f"{int(row.get('Population_2024', 500000)):,}")
    with m4:
        st.metric(label="Existing Dialog Towers", value=f"{int(row['Dialog_Tower_Count'])}")

    cluster_labels = {0: 'Medium Potential Zone', 1: 'High Potential Zone', 2: 'Low Potential Zone'}
    cluster_name = cluster_labels.get(row['Priority_Cluster'], 'Standard Zone')
    st.info(f"💡 **Economic Zone Classification:** **{cluster_name}** (Density: **{row['Density_2024_per_km2']:,.0f} people/km²**)")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅️ Back to Home"):
        st.session_state.screen = 'welcome'
        st.rerun()

# -------------------------------------------------------------------------
# Screen 3: Full District Leaderboard View
# -------------------------------------------------------------------------
elif st.session_state.screen == 'leaderboard':
    st.title("🏆 National 5G Investment Leaderboard")
    st.write("Sri Lankan districts ranked from highest to lowest potential based on predicted ROI.")
    
    ranked_data = data.sort_values(by='ROI_Percentage', ascending=False).reset_index(drop=True)
    ranked_data.index += 1
    display_df = ranked_data[['District', 'Priority_Cluster', 'ROI_Percentage', 'Dialog_Tower_Count']]
    display_df.columns = ['District', 'Economic Cluster', 'Estimated ROI (%)', 'Tower Count']
    st.dataframe(display_df, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅️ Back to Home"):
        st.session_state.screen = 'welcome'
        st.rerun()

# -------------------------------------------------------------------------
# Screen 4: Custom ROI Calculator View
# -------------------------------------------------------------------------
elif st.session_state.screen == 'calculator':
    st.title("📡 Custom Micro-Region ROI Simulator")
    st.write("Enter area metrics and total investment to compute exact net returns.")
    
    c1, c2 = st.columns(2)
    with c1:
        investment = st.number_input("Total Investment / CapEx (Rs.)", value=10000000, step=500000)
        urban = st.slider("Urban Percentage (%)", 0.0, 100.0, 20.0)
        density = st.number_input("Population Density (per km²)", value=500.0)
    with c2:
        arpu = st.number_input("Estimated ARPU (Rs.)", value=600.0)
        fiber = st.slider("Distance to Fiber Node (km)", 0.0, 5.0, 1.0)
        towers = st.number_input("Existing Tower Count", value=10)

    if st.button("Compute Custom Net Return 🚀"):
        cluster_input = pd.DataFrame([[urban, density, arpu]], columns=['Urban_Pct', 'Density_2024_per_km2', 'Estimated_ARPU_Rs_per_month'])
        pred_cluster = kmeans.predict(cluster_input)[0]
        
        input_payload = pd.DataFrame([[urban, density, arpu, fiber, towers, pred_cluster]],
                                  columns=['Urban_Pct', 'Density_2024_per_km2',
                                           'Estimated_ARPU_Rs_per_month', 'Fiber_Distance_km',
                                           'Dialog_Tower_Count', 'Priority_Cluster'])
        roi_val = model.predict(input_payload)[0]
        profit = investment * (roi_val / 100)
        
        st.success(f"💰 **Estimated Net Profit: Rs. {profit:,.2f}** (ROI: {roi_val:.2f}%)")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅️ Back to Home"):
        st.session_state.screen = 'welcome'
        st.rerun()
