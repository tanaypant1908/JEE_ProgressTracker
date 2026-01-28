import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import date, datetime
import plotly.graph_objects as go

st.set_page_config(page_title="JEE Tracker", layout="wide", page_icon="🚀")

st.markdown("""
<style>
.main-header { font-size: 3rem !important; background: linear-gradient(90deg, #FF6B6B, #4ECDC4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.jee-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 15px; color: white; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🚀 JEE Progress Tracker Pro</h1>', unsafe_allow_html=True)
st.markdown('<h3 style="text-align: center; color: #4ECDC4;">Live Dashboard </h3>', unsafe_allow_html=True)

# Initialize data
if 'data' not in st.session_state:
    dates = pd.date_range(end=date.today(), periods=14)
    st.session_state.data = pd.DataFrame({
        'date': dates,
        'name': ['Tanay']*14,
        'phy_questions': np.random.randint(40, 80, 14),
        'chem_questions': np.random.randint(35, 75, 14),
        'math_questions': np.random.randint(30, 70, 14),
        'phy_study': np.random.uniform(1.5, 3.5, 14),
        'chem_study': np.random.uniform(1.2, 3.2, 14),
        'math_study': np.random.uniform(1.0, 3.0, 14),
        'revision': np.random.uniform(0.5, 2.0, 14),
        'social_media': np.random.uniform(0.5, 2.5, 14),
        'health': np.random.randint(6, 10, 14)
    })

data = st.session_state.data

# Sidebar
st.sidebar.title("👨‍🎓 Your Profile")
name = st.sidebar.text_input("Name", "")

# 4-TAB SIMPLIFIED DASHBOARD (No errors!)
tab1, tab2, tab3, tab4 = st.tabs(["📝 Log Today", "📊 Progress", "🔥 Heatmaps", "🤖 PRO TIPS"])

with tab1:
    st.header("🎯 Quick Daily Log")
    col1, col2, col3 = st.columns(3)
    with col1: phy_q, phy_h = st.number_input("Physics Qs", 0, 200, 50), st.number_input("Physics (self-study hrs)", 0.0, 6.0, 2.0)
    with col2: chem_q, chem_h = st.number_input("Chemistry Qs", 0, 200, 45), st.number_input("Chemistry (hrs)", 0.0, 6.0, 2.0)
    with col3: math_q, math_h = st.number_input("Math Qs", 0, 200, 40), st.number_input("Math (hrs)", 0.0, 6.0, 2.0)
    
    col4, col5 = st.columns(2)
    with col4: revision, social = st.number_input("Revision (h)", 0.0, 4.0, 1.0), st.number_input("Social Media (h)", 0.0, 5.0, 0.8)
    with col5: health = st.slider("Health (1-10)", 1, 10, 7)
    
    if st.button("✅ Log Today!", type="primary"):
        new_row = pd.DataFrame({
            'date': [date.today()], 'name': [name],
            'phy_questions': [phy_q], 'chem_questions': [chem_q], 'math_questions': [math_q],
            'phy_study': [phy_h], 'chem_study': [chem_h], 'math_study': [math_h],
            'revision': [revision], 'social_media': [social], 'health': [health]
        })
        st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
        st.success("✅ Data logged! Check Progress tab!")
        st.rerun()

with tab2:
    user_data = data[data['name'] == name].tail(14)
    if len(user_data) > 0:
        today = user_data.iloc[-1]
        total_qs = today['phy_questions'] + today['chem_questions'] + today['math_questions']
        total_study = today['phy_study'] + today['chem_study'] + today['math_study'] + today['revision']
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🎯 Total Questions", int(total_qs))
        col2.metric("📚 Study Hours", f"{self_study:.1f}h", "Target: 6h")
        col3.metric("📱 Social Media", f"{today['social_media']:.1f}h", "Goal: <0.75h")
        col4.metric("❤️ Health", today['health'])
        
        col1, col2 = st.columns(2)
        with col1:
            fig = px.line(user_data, x='date', y=['phy_questions','chem_questions','math_questions'],
                         title="📈 2-Week Progress", markers=True)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.pie(values=[today['phy_study'], today['chem_study'], today['math_study'], today['revision']],
                        names=['Physics','Chemistry','Math','Revision'])
            st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("🔥 Heatmaps - Study Patterns")
    
    # FIXED HEATMAP 1: Study vs Social Media
    study_cols = ['phy_study', 'chem_study', 'math_study']
    heatmap_df = data[study_cols + ['social_media', 'phy_questions']].corr()
    fig1 = px.imshow(heatmap_df, title="📊 Correlation: Study vs Output", color_continuous_scale='RdYlGn')
    st.plotly_chart(fig1, use_container_width=True)
    
    # FIXED HEATMAP 2: Subject Performance
    subjects = data[['phy_questions', 'chem_questions', 'math_questions']].mean().reset_index()
    subjects.columns = ['Subject', 'Avg_Qs']
    fig2 = px.bar(subjects, x='Subject', y='Avg_Qs', title="📈 Average Questions by Subject")
    st.plotly_chart(fig2, use_container_width=True)

with tab4:
    st.header("🤖PRO TIPS")
    if len(data[data['name'] == name]) > 0:
        today = data[data['name'] == name].iloc[-1]
        total_study = today['phy_study'] + today['chem_study'] + today['math_study'] + today['revision']
        
        if total_study < 6 and today['health'] > 6:
            st.error("⚠️ Self Study < 6h! 💪")
            st.info("""
            15 lakh students gave JEE Mains in 2025 out of which only top 2 lakh were selected to give JEE advanced.54,378 students qualified for IIT admissions. 
            This is your chance to change your life and your parents life. Mate, pain of discipline is always better than pain of regret. Just imagine your yourself in
            your dream institution. Hardwork always beats talent when talent does not work hard. You are not average or bad at studies, you just need to lock in. Let's do it.
            Lets track your progress and study smart.
            
            **🔬 Scientifically Proven Technique For Revison:**
            **Blank paper technique**: Take a blank page and and just try to write everything you have studied(active recall)roughly.If you forget,see your material and mark it.
            """)
        elif today['social_media'] > 0.75:
            st.warning("📱 Social Media > 45min!")
            st.info("""
            **🧠 Proven Fixes:**
            1. **AppBlock**: Set 45min limit
            2. **Phone Away**: Different room
            3. **Replace**: Duolingo instead
            **🎯 Tomorrow: <45min**
            """)
        else:
            st.success("✅ JEE READY! You're crushing it!")
        
        tomorrow_target = (today['phy_questions'] + today['chem_questions'] + today['math_questions']) * 1.1
        st.metric("🎯 Tomorrow Target", f"{tomorrow_target:.0f} Questions", "+10%")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <h3>👨‍💻Tanay Pant</h3>
    <p>🚀 JEE Tracker Pro | Live Analytics</p>
</div>
""", unsafe_allow_html=True)
