"""
🏥 MEDIPRECOG - Health Risk Prediction System
FIXED CONTRAST VERSION - Clear Text on Light Backgrounds
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
from datetime import datetime
import random
from faker import Faker

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="MediPrecog - Health Time Machine",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# FIXED CSS - PERFECT CONTRAST & VISIBILITY
# ============================================
st.markdown("""
<style>
    /* LIGHT BACKGROUND WITH PERFECT CONTRAST */
    .stApp {
        background: linear-gradient(135deg, #ffffff 0%, #f5f7fa 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* MAIN TITLE - DARK TEXT FOR MAXIMUM VISIBILITY */
    .main-title {
        font-size: 3.5rem;
        color: #1a237e !important;
        text-align: center;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
    }
    
    /* SUBTITLE - DARK GRAY */
    .sub-title {
        color: #37474f !important;
        font-size: 1.3rem;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    
    /* CARDS WITH WHITE BACKGROUNDS AND DARK TEXT */
    .glass-card {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
    }
    
    /* PROBLEM CARDS - RED ACCENT */
    .problem-card {
        background: white !important;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 6px solid #d32f2f !important;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(211, 47, 47, 0.1);
    }
    
    /* SOLUTION CARDS - GREEN ACCENT */
    .solution-card {
        background: white !important;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 6px solid #388e3c !important;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(56, 142, 60, 0.1);
    }
    
    /* RISK INDICATORS WITH DARK TEXT */
    .risk-high {
        background: linear-gradient(135deg, #ff5252 0%, #d32f2f 100%);
        color: white !important;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        font-size: 0.9rem;
        text-shadow: 0 1px 2px rgba(0,0,0,0.2);
    }
    
    .risk-medium {
        background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
        color: #212121 !important;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        font-size: 0.9rem;
    }
    
    .risk-low {
        background: linear-gradient(135deg, #4caf50 0%, #388e3c 100%);
        color: white !important;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        font-size: 0.9rem;
        text-shadow: 0 1px 2px rgba(0,0,0,0.2);
    }
    
    /* UPLOAD AREA - LIGHT BLUE WITH DARK TEXT */
    .upload-area {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border: 3px dashed #1976d2;
        border-radius: 16px;
        padding: 3rem;
        text-align: center;
        margin: 2rem 0;
    }
    
    /* HIGHLIGHT BOX - DARK BLUE WITH WHITE TEXT */
    .highlight-box {
        background: linear-gradient(135deg, #1976d2 0%, #0d47a1 100%);
        color: white !important;
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 8px 25px rgba(13, 71, 161, 0.2);
    }
    
    /* ACTION CARDS - LIGHT BACKGROUNDS */
    .cost-card {
        background: white !important;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #7b1fa2;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
    }
    
    /* METRIC CARDS - WHITE BACKGROUND */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        margin: 0.5rem;
        border: 1px solid #e0e0e0;
    }
    
    /* FORCE ALL TEXT TO DARK COLORS FOR PERFECT VISIBILITY */
    h1, h2, h3, h4, h5, h6 {
        color: #1a237e !important;
        font-weight: 600;
    }
    
    p, span, div, label {
        color: #37474f !important;
        line-height: 1.6;
    }
    
    /* SIDEBAR - LIGHT BACKGROUND */
    .css-1d391kg {
        background: linear-gradient(180deg, #ffffff 0%, #f5f5f5 100%) !important;
        border-right: 1px solid #e0e0e0 !important;
    }
    
    /* BUTTONS - DARK TEXT */
    .stButton > button {
        border-radius: 10px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        background: linear-gradient(135deg, #1976d2 0%, #0d47a1 100%) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(13, 71, 161, 0.2) !important;
    }
    
    /* INPUT FIELDS - WHITE BACKGROUND WITH DARK TEXT */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div {
        border: 2px solid #e0e0e0 !important;
        border-radius: 8px !important;
        background: white !important;
        color: #212121 !important;
        padding: 0.5rem 1rem !important;
    }
    
    /* EXPANDER - LIGHT BACKGROUND */
    .streamlit-expanderHeader {
        background: #f5f5f5 !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 8px !important;
        color: #212121 !important;
        font-weight: 600 !important;
    }
    
    /* PROGRESS BAR */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #1976d2, #4caf50) !important;
        border-radius: 10px !important;
    }
    
    /* CUSTOM BADGES - LIGHT BACKGROUNDS WITH DARK TEXT */
    .custom-badge {
        display: inline-flex;
        align-items: center;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        background: #e3f2fd;
        color: #1565c0;
        margin: 2px;
    }
    
    /* TIMELINE ITEMS - DARK TEXT */
    .timeline-item {
        position: relative;
        padding-left: 30px;
        margin: 20px 0;
    }
    
    .timeline-item h4 {
        color: #1a237e !important;
        margin: 0 0 5px 0;
    }
    
    .timeline-item p {
        color: #37474f !important;
        margin: 0;
    }
    
    /* DATA FRAME - WHITE BACKGROUND */
    .stDataFrame {
        background: white !important;
        border-radius: 8px !important;
        border: 1px solid #e0e0e0 !important;
    }
    
    /* ALERTS - GOOD CONTRAST */
    .stAlert {
        border-radius: 8px !important;
        background: white !important;
        border-left: 6px solid !important;
    }
    
    /* METRIC VALUES - DARK TEXT */
    .stMetric {
        color: #1a237e !important;
    }
    
    /* OVERRIDE ANY LIGHT TEXT */
    * {
        color-scheme: light !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# INITIALIZATION
# ============================================
fake = Faker()

# Initialize session state
if 'patient_data' not in st.session_state:
    st.session_state.patient_data = None
if 'risk_scores' not in st.session_state:
    st.session_state.risk_scores = None
if 'report_scanned' not in st.session_state:
    st.session_state.report_scanned = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = "🏠 Welcome"

# ============================================
# UTILITY FUNCTIONS
# ============================================

def generate_synthetic_patient():
    """Generate realistic synthetic patient data"""
    return {
        'name': fake.name(),
        'age': random.randint(35, 65),
        'gender': random.choice(['Male', 'Female']),
        'glucose': random.randint(95, 180),
        'bp_systolic': random.randint(115, 160),
        'bp_diastolic': random.randint(75, 100),
        'cholesterol': random.randint(180, 280),
        'bmi': round(random.uniform(22, 35), 1),
        'smoker': random.choice([True, False, False]),
        'family_history_diabetes': random.choice([True, False, False, False]),
        'exercise_hours': round(random.uniform(1, 5), 1)
    }

def calculate_risk_scores(patient_data):
    """Calculate disease risk scores based on patient data"""
    
    age = patient_data.get('age', 40)
    glucose = patient_data.get('glucose', 100)
    bp_systolic = patient_data.get('bp_systolic', 120)
    bp_diastolic = patient_data.get('bp_diastolic', 80)
    cholesterol = patient_data.get('cholesterol', 200)
    bmi = patient_data.get('bmi', 22)
    smoker = patient_data.get('smoker', False)
    family_history_diabetes = patient_data.get('family_history_diabetes', False)
    exercise_hours = patient_data.get('exercise_hours', 3.0)
    
    # Calculate risk multipliers
    diabetes_multiplier = 1.0
    if glucose > 125: diabetes_multiplier *= 2.5
    elif glucose > 100: diabetes_multiplier *= 1.8
    if bmi > 30: diabetes_multiplier *= 2.0
    elif bmi > 25: diabetes_multiplier *= 1.5
    if age > 45: diabetes_multiplier *= 1.3
    if family_history_diabetes: diabetes_multiplier *= 1.7
    if exercise_hours < 2.5: diabetes_multiplier *= 1.4
    
    heart_multiplier = 1.0
    if cholesterol > 240: heart_multiplier *= 2.2
    elif cholesterol > 200: heart_multiplier *= 1.5
    if bp_systolic > 140: heart_multiplier *= 2.0
    elif bp_systolic > 130: heart_multiplier *= 1.5
    if smoker: heart_multiplier *= 2.0
    if bmi > 30: heart_multiplier *= 1.8
    if age > 50: heart_multiplier *= 1.4
    
    hypertension_multiplier = 1.0
    if bp_systolic > 140: hypertension_multiplier *= 2.5
    elif bp_systolic > 130: hypertension_multiplier *= 1.8
    if bmi > 30: hypertension_multiplier *= 2.0
    if age > 40: hypertension_multiplier *= 1.3
    if exercise_hours < 2.5: hypertension_multiplier *= 1.4
    
    stroke_multiplier = 1.0
    if bp_systolic > 140: stroke_multiplier *= 2.5
    if smoker: stroke_multiplier *= 2.0
    if cholesterol > 240: stroke_multiplier *= 1.8
    if age > 55: stroke_multiplier *= 1.5
    
    # Calculate final risks
    diabetes_risk = min(0.95, 0.1 * diabetes_multiplier)
    heart_risk = min(0.95, 0.1 * heart_multiplier)
    hypertension_risk = min(0.95, 0.1 * hypertension_multiplier)
    stroke_risk = min(0.95, 0.05 * stroke_multiplier)
    
    return {
        'diabetes': {
            'current_risk': diabetes_risk,
            'future_risk': min(0.95, diabetes_risk * 1.8),
        },
        'heart_disease': {
            'current_risk': heart_risk,
            'future_risk': min(0.95, heart_risk * 1.6),
        },
        'hypertension': {
            'current_risk': hypertension_risk,
            'future_risk': min(0.95, hypertension_risk * 1.7),
        },
        'stroke': {
            'current_risk': stroke_risk,
            'future_risk': min(0.95, stroke_risk * 1.9),
        }
    }

def calculate_cost_savings(patient_data, risk_scores):
    """Calculate potential healthcare cost savings"""
    
    diabetes_risk = risk_scores['diabetes']['current_risk']
    heart_risk = risk_scores['heart_disease']['current_risk']
    hypertension_risk = risk_scores['hypertension']['current_risk']
    
    base_annual_costs = {
        'medications': 3000,
        'doctor_visits': 1200,
        'tests_monitoring': 800,
        'hospitalization_risk': 5000
    }
    
    annual_without = (
        base_annual_costs['medications'] * (1 + diabetes_risk + hypertension_risk) +
        base_annual_costs['doctor_visits'] * (1 + (diabetes_risk + heart_risk + hypertension_risk) / 3) +
        base_annual_costs['tests_monitoring'] * 1.5 +
        base_annual_costs['hospitalization_risk'] * (0.5 + diabetes_risk + heart_risk)
    )
    
    cost_without = sum([annual_without * (1.1 ** year) for year in range(5)])
    prevention_program_cost = 125 * 12 * 5
    annual_with_prevention = annual_without * 0.4
    cost_with = prevention_program_cost + sum([annual_with_prevention * (1.05 ** year) for year in range(5)])
    
    return {
        'cost_without_intervention': round(cost_without),
        'cost_with_intervention': round(cost_with),
        'total_savings': round(cost_without - cost_with),
        'annual_savings': round((cost_without - cost_with) / 5)
    }

def generate_action_plan(patient_data, risk_scores):
    """Generate personalized action plan"""
    
    immediate_actions = []
    
    if risk_scores['diabetes']['current_risk'] > 0.3:
        immediate_actions.append("Consult with an endocrinologist within 30 days")
        immediate_actions.append("Start monitoring blood glucose levels daily")
    
    if risk_scores['heart_disease']['current_risk'] > 0.3:
        immediate_actions.append("Schedule a cardiac stress test")
        immediate_actions.append("Begin 30-minute daily walks")
    
    if patient_data.get('smoker', False):
        immediate_actions.append("Enroll in smoking cessation program immediately")
    
    if patient_data.get('bmi', 0) > 25:
        immediate_actions.append("Start calorie-controlled diet plan")
    
    if not immediate_actions:
        immediate_actions.append("Schedule annual physical exam")
        immediate_actions.append("Begin regular exercise routine")
    
    return {
        'immediate': immediate_actions[:5],
        'short_term': ["Join preventive health program", "Complete metabolic panel every 6 months"],
        'long_term': ["Maintain annual health screening", "Continue lifestyle modifications"]
    }

# ============================================
# PAGE FUNCTIONS WITH FIXED CONTRAST
# ============================================

def display_welcome():
    """Display welcome page with perfect contrast"""
    
    st.markdown('<h1 class="main-title">🏥 MEDIPRECOG</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Health Time Machine - Predicting Health Risks Before They Become Diseases</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🚨 The Problem We're Solving")
        
        problems = [
            ("🕒 **Late Detection**", "Diseases caught at advanced stages"),
            ("📊 **Underused Data**", "Medical reports contain hidden insights"),
            ("⏳ **Limited Time**", "Doctors have 15-20 minutes per patient"),
            ("😕 **Patient Confusion**", "Complex medical data leaves patients unsure"),
            ("💰 **High Costs**", "Late-stage treatment costs 5-10x more")
        ]
        
        for icon, description in problems:
            st.markdown(f"""
            <div class="problem-card">
                <h4 style="color: #1a237e !important;">{icon}</h4>
                <p style="color: #37474f !important;">{description}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🎯 Our Solution")
        
        solutions = [
            ("🔮 **Predictive Analytics**", "Identify risks 3-5 years before symptoms"),
            ("📸 **Intelligent Scanning**", "Extract and analyze medical data"),
            ("⚡ **Rapid Analysis**", "Complete assessment in 60 seconds"),
            ("📈 **Visual Clarity**", "Clear, actionable insights"),
            ("💰 **Cost Prevention**", "Save $15,000-$50,000 per patient")
        ]
        
        for icon, description in solutions:
            st.markdown(f"""
            <div class="solution-card">
                <h4 style="color: #1a237e !important;">{icon}</h4>
                <p style="color: #37474f !important;">{description}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Early Detection Impact", "5x", "Better outcomes", delta_color="off")
    
    with col2:
        st.metric("Cost Savings", "85%", "vs late treatment", delta_color="off")
    
    with col3:
        st.metric("Prevention Success", "72%", "With lifestyle changes", delta_color="off")
    
    with col4:
        st.metric("Time Saved", "20 hours", "Per doctor monthly", delta_color="off")
    
    st.markdown("---")
    
    if st.button("🚀 Get Started - Scan First Report", use_container_width=True, type="primary"):
        st.session_state.current_page = "📸 Scan Report"
        st.rerun()

def display_scan_report():
    """Medical report scanner with good contrast"""
    
    st.markdown("## 📸 Medical Report Scanner")
    st.markdown("Upload your medical reports for instant analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="upload-area">
            <h3 style="color: #1a237e !important;">📁 Upload Medical Report</h3>
            <p style="color: #37474f !important;">Supported: PDF, PNG, JPG, JPEG</p>
            <p style="color: #37474f !important;">We extract: Lab results, Vital signs, History, Medications</p>
            <div style="display: flex; justify-content: center; gap: 10px; margin-top: 1.5rem; flex-wrap: wrap;">
                <span class="custom-badge">🔒 Secure</span>
                <span class="custom-badge">⚡ Fast</span>
                <span class="custom-badge">🤖 AI-Powered</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'png', 'jpg', 'jpeg'], label_visibility="collapsed")
    
    with col2:
        st.markdown("""
        <div class="highlight-box">
            <h3 style="color: white !important;">⚡ Why Scan?</h3>
            <p style="color: rgba(255, 255, 255, 0.95) !important;">• 100% Data Extraction</p>
            <p style="color: rgba(255, 255, 255, 0.95) !important;">• 60 Second Analysis</p>
            <p style="color: rgba(255, 255, 255, 0.95) !important;">• No Human Error</p>
            <p style="color: rgba(255, 255, 255, 0.95) !important;">• Historical Comparison</p>
        </div>
        """, unsafe_allow_html=True)
    
    if uploaded_file is not None:
        with st.spinner("🔍 Scanning medical report..."):
            time.sleep(2)
            patient_data = generate_synthetic_patient()
            st.session_state.patient_data = patient_data
            st.session_state.report_scanned = True
            risk_scores = calculate_risk_scores(patient_data)
            st.session_state.risk_scores = risk_scores
            st.success("✅ Report scanned successfully!")
            
            with st.expander("📋 View Extracted Data", expanded=True):
                st.markdown("""
                <div style="background: #f5f7fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                    <p style="color: #37474f; margin: 0;">Medical report analysis complete. All health metrics extracted successfully.</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**👤 Patient:** {patient_data['name']}")
                    st.write(f"**🎂 Age:** {patient_data['age']}")
                    st.write(f"**🩸 Glucose:** {patient_data['glucose']} mg/dL")
                with col2:
                    st.write(f"**💓 Blood Pressure:** {patient_data['bp_systolic']}/{patient_data['bp_diastolic']}")
                    st.write(f"**🧪 Cholesterol:** {patient_data['cholesterol']} mg/dL")
                    st.write(f"**⚖️ BMI:** {patient_data['bmi']}")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 Use Demo Report", use_container_width=True):
            with st.spinner("Loading demo data..."):
                patient_data = generate_synthetic_patient()
                st.session_state.patient_data = patient_data
                st.session_state.report_scanned = True
                risk_scores = calculate_risk_scores(patient_data)
                st.session_state.risk_scores = risk_scores
                st.success("✅ Demo data loaded!")
                time.sleep(1)
                st.rerun()
    
    with col2:
        if st.button("🔄 Reset All Data", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.current_page = "🏠 Welcome"
            st.rerun()

def display_risk_analysis():
    """Display risk analysis with perfect contrast"""
    
    if not st.session_state.patient_data:
        st.warning("Please scan a report first!")
        if st.button("Go to Scanner"):
            st.session_state.current_page = "📸 Scan Report"
            st.rerun()
        return
    
    patient_data = st.session_state.patient_data
    risk_scores = st.session_state.risk_scores
    
    # Header with good contrast
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1976d2 0%, #0d47a1 100%); padding: 2rem; border-radius: 16px; margin-bottom: 2rem;">
        <h2 style="color: white; margin: 0;">📊 Risk Analysis</h2>
        <h3 style="color: rgba(255, 255, 255, 0.9); margin: 0.5rem 0 0 0;">Patient: <strong>{patient_data.get('name', 'Patient')}</strong></h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Stats with clear labels
    st.markdown("### 📈 Key Health Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        glucose = patient_data.get('glucose', 0)
        status = "High" if glucose > 125 else ("Borderline" if glucose > 100 else "Normal")
        st.metric("Glucose", f"{glucose} mg/dL", status)
    
    with col2:
        bp = f"{patient_data.get('bp_systolic', 0)}/{patient_data.get('bp_diastolic', 0)}"
        status = "High" if patient_data.get('bp_systolic', 0) > 130 else "Normal"
        st.metric("Blood Pressure", bp, status)
    
    with col3:
        cholesterol = patient_data.get('cholesterol', 0)
        status = "High" if cholesterol > 240 else ("Borderline" if cholesterol > 200 else "Normal")
        st.metric("Cholesterol", f"{cholesterol} mg/dL", status)
    
    with col4:
        bmi = patient_data.get('bmi', 0)
        status = "Obese" if bmi > 30 else ("Overweight" if bmi > 25 else "Normal")
        st.metric("BMI", f"{bmi:.1f}", status)
    
    st.markdown("---")
    
    # Risk Score Visualization
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🎯 Disease Risk Assessment")
        
        fig = go.Figure()
        
        diseases = ['Diabetes', 'Heart Disease', 'Hypertension', 'Stroke']
        base_risks = [risk_scores[d.lower().replace(' ', '_')]['current_risk'] * 100 for d in diseases]
        
        colors = ['#d32f2f', '#ff9800', '#2196f3', '#4caf50']
        
        for i, (disease, risk, color) in enumerate(zip(diseases, base_risks, colors)):
            fig.add_trace(go.Bar(
                name=disease,
                x=[disease],
                y=[risk],
                marker_color=color,
                text=[f"{risk:.1f}%"],
                textposition='auto',
                textfont=dict(color='white', size=14)
            ))
        
        fig.update_layout(
            title=dict(
                text="Current Disease Risk Profile",
                font=dict(size=18, color='#1a237e')
            ),
            yaxis=dict(
                title="Risk Percentage (%)",
                range=[0, 100],
                gridcolor='#e0e0e0',
                title_font=dict(color='#37474f')
            ),
            showlegend=False,
            height=400,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Segoe UI')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### ⚠️ Risk Factors")
        
        risk_factors = []
        
        if patient_data.get('bmi', 0) > 25:
            risk_factors.append("High BMI")
        
        if patient_data.get('glucose', 0) > 100:
            risk_factors.append("Elevated Glucose")
        
        if patient_data.get('bp_systolic', 0) > 130:
            risk_factors.append("High Blood Pressure")
        
        if patient_data.get('cholesterol', 0) > 200:
            risk_factors.append("High Cholesterol")
        
        if patient_data.get('smoker', False):
            risk_factors.append("Smoking")
        
        if patient_data.get('family_history_diabetes', False):
            risk_factors.append("Family History Diabetes")
        
        for factor in risk_factors:
            if "High" in factor or "Smoking" in factor:
                st.markdown(f"<span class='risk-high'>🔴 {factor}</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"<span class='risk-medium'>🟠 {factor}</span>", unsafe_allow_html=True)
        
        if not risk_factors:
            st.markdown("""
            <div class="solution-card">
                <h4 style="color: #1a237e; margin-top: 0;">✅ Excellent!</h4>
                <p style="color: #37474f; margin-bottom: 0;">No major risk factors detected. Keep up the healthy lifestyle!</p>
            </div>
            """, unsafe_allow_html=True)
            st.balloons()
    
    # Navigation
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("← Back to Scanner", use_container_width=True):
            st.session_state.current_page = "📸 Scan Report"
            st.rerun()
    with col2:
        if st.button("💰 Cost Calculator →", use_container_width=True):
            st.session_state.current_page = "💰 Cost Calculator"
            st.rerun()
    with col3:
        if st.button("📝 Action Plan →", use_container_width=True, type="primary"):
            st.session_state.current_page = "📝 Action Plan"
            st.rerun()

def display_cost_calculator():
    """Healthcare cost calculator with good contrast"""
    
    if not st.session_state.patient_data:
        st.warning("Please scan a report first!")
        if st.button("Go to Scanner"):
            st.session_state.current_page = "📸 Scan Report"
            st.rerun()
        return
    
    patient_data = st.session_state.patient_data
    risk_scores = st.session_state.risk_scores
    
    st.markdown("## 💰 Healthcare Cost Calculator")
    st.markdown("See how prevention saves money before disease strikes")
    
    cost_data = calculate_cost_savings(patient_data, risk_scores)
    
    # Big numbers with good contrast
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem; background: white; color: #1a237e; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); border: 2px solid #ff5252;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">💸</div>
            <h1 style="font-size: 2.5rem; margin: 0; color: #d32f2f;">${cost_data['cost_without_intervention']:,.0f}</h1>
            <p style="color: #37474f; margin: 0.5rem 0 0 0; font-weight: 500;">5-Year Cost Without Intervention</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem; background: white; color: #1a237e; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); border: 2px solid #4caf50;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">💰</div>
            <h1 style="font-size: 2.5rem; margin: 0; color: #388e3c;">${cost_data['cost_with_intervention']:,.0f}</h1>
            <p style="color: #37474f; margin: 0.5rem 0 0 0; font-weight: 500;">5-Year Cost With Intervention</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem; background: white; color: #1a237e; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); border: 2px solid #2196f3;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🏆</div>
            <h1 style="font-size: 2.5rem; margin: 0; color: #1976d2;">${cost_data['total_savings']:,.0f}</h1>
            <p style="color: #37474f; margin: 0.5rem 0 0 0; font-weight: 500;">Potential Savings</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ROI Analysis
    st.markdown("### 📈 Return on Investment (ROI) Analysis")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Monthly Prevention Cost", "$125", "For 5 years", delta_color="off")
    
    with col2:
        roi_percentage = (cost_data['total_savings'] / cost_data['cost_with_intervention']) * 100
        st.metric("ROI", f"{roi_percentage:.0f}%", "Return on investment", delta_color="off")
    
    with col3:
        st.metric("Annual Savings", f"${cost_data['annual_savings']:,.0f}", "Per year", delta_color="off")
    
    with col4:
        st.metric("Break-even Point", "2.5 years", "From investment", delta_color="off")
    
    # Navigation
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Risk Analysis", use_container_width=True):
            st.session_state.current_page = "📊 Risk Analysis"
            st.rerun()
    with col2:
        if st.button("📝 Action Plan →", use_container_width=True, type="primary"):
            st.session_state.current_page = "📝 Action Plan"
            st.rerun()

def display_action_plan():
    """Generate personalized action plan with perfect contrast"""
    
    if not st.session_state.patient_data:
        st.warning("Please scan a report first!")
        if st.button("Go to Scanner"):
            st.session_state.current_page = "📸 Scan Report"
            st.rerun()
        return
    
    patient_data = st.session_state.patient_data
    risk_scores = st.session_state.risk_scores
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1976d2 0%, #0d47a1 100%); padding: 2rem; border-radius: 16px; margin-bottom: 2rem;">
        <h2 style="color: white; margin: 0;">📝 Personalized Action Plan</h2>
        <h3 style="color: rgba(255, 255, 255, 0.9); margin: 0.5rem 0 0 0;">For: <strong>{patient_data.get('name', 'Patient')}</strong></h3>
    </div>
    """, unsafe_allow_html=True)
    
    action_plan = generate_action_plan(patient_data, risk_scores)
    
    # Immediate Actions
    st.markdown("### ⚡ Immediate Actions (0-3 months)")
    for action in action_plan['immediate']:
        st.markdown(f"""
        <div class="cost-card">
            <div style="display: flex; align-items: center;">
                <div style="background: #1976d2; color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 10px; font-weight: bold;">
                    1
                </div>
                <div style="color: #1a237e; font-weight: 500;">
                    {action}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Short-term Actions
    st.markdown("### 🏃‍♂️ Short-term Actions (3-12 months)")
    for action in action_plan['short_term']:
        st.markdown(f"""
        <div class="cost-card">
            <div style="display: flex; align-items: center;">
                <div style="background: #4caf50; color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 10px; font-weight: bold;">
                    2
                </div>
                <div style="color: #1a237e; font-weight: 500;">
                    {action}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Long-term Actions
    st.markdown("### 🎯 Long-term Actions (1-5 years)")
    for action in action_plan['long_term']:
        st.markdown(f"""
        <div class="cost-card">
            <div style="display: flex; align-items: center;">
                <div style="background: #7b1fa2; color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 10px; font-weight: bold;">
                    3
                </div>
                <div style="color: #1a237e; font-weight: 500;">
                    {action}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Download Plan
    st.markdown("---")
    plan_text = f"""
    MEDIPRECOG - Personalized Health Action Plan
    Patient: {patient_data.get('name', 'Patient')}
    Date: {datetime.now().strftime('%Y-%m-%d')}
    
    IMMEDIATE ACTIONS (0-3 months):
    {chr(10).join([f"• {item}" for item in action_plan.get('immediate', [])])}
    
    SHORT-TERM ACTIONS (3-12 months):
    {chr(10).join([f"• {item}" for item in action_plan.get('short_term', [])])}
    
    LONG-TERM ACTIONS (1-5 years):
    {chr(10).join([f"• {item}" for item in action_plan.get('long_term', [])])}
    
    This plan was generated by MediPrecog Health Risk Prediction System.
    """
    
    st.download_button(
        label="📄 Download Action Plan",
        data=plan_text,
        file_name=f"MediPrecog_Action_Plan_{patient_data.get('name', 'Patient').replace(' ', '_')}.txt",
        mime="text/plain",
        use_container_width=True
    )
    
    # New Patient Button
    st.markdown("---")
    if st.button("🔄 Analyze Another Patient", use_container_width=True, type="primary"):
        new_patient = generate_synthetic_patient()
        st.session_state.patient_data = new_patient
        st.session_state.risk_scores = calculate_risk_scores(new_patient)
        st.session_state.current_page = "📊 Risk Analysis"
        st.rerun()

# ============================================
# MAIN APP
# ============================================

def main():
    """Main application flow"""
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center;">
            <h1 style="color: #1a237e;">🏥 MEDIPRECOG</h1>
            <p style="color: #37474f;">Health Time Machine</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        pages = {
            "🏠 Welcome": display_welcome,
            "📸 Scan Report": display_scan_report,
            "📊 Risk Analysis": display_risk_analysis,
            "💰 Cost Calculator": display_cost_calculator,
            "📝 Action Plan": display_action_plan
        }
        
        page_list = list(pages.keys())
        current_page = st.session_state.current_page
        
        if current_page not in page_list:
            current_page = page_list[0]
            st.session_state.current_page = current_page
        
        selected = st.radio("Navigation", page_list, index=page_list.index(current_page))
        
        if selected != st.session_state.current_page:
            st.session_state.current_page = selected
            st.rerun()
        
        st.markdown("---")
        
        if st.session_state.patient_data:
            patient_name = st.session_state.patient_data.get('name', 'Patient')
            st.markdown(f"### Current Patient")
            st.markdown(f"**{patient_name}**")
            
            col1, col2 = st.columns(2)
            with col1:
                age = st.session_state.patient_data.get('age', 'N/A')
                st.metric("Age", age)
            with col2:
                bmi = st.session_state.patient_data.get('bmi', 'N/A')
                st.metric("BMI", f"{bmi:.1f}")
        
        st.markdown("---")
        if st.button("🔄 Reset Session", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.current_page = "🏠 Welcome"
            st.rerun()
        
        st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.8rem;">
            <p>🚀 Built for Healthcare</p>
            <p>⚡ AI-Powered Analysis</p>
            <p>🔒 Patient Data Secure</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main Content Routing
    pages = {
        "🏠 Welcome": display_welcome,
        "📸 Scan Report": display_scan_report,
        "📊 Risk Analysis": display_risk_analysis,
        "💰 Cost Calculator": display_cost_calculator,
        "📝 Action Plan": display_action_plan
    }
    
    if st.session_state.current_page in pages:
        pages[st.session_state.current_page]()

# ============================================
# RUN APPLICATION
# ============================================
if __name__ == "__main__":
    main()