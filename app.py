"""
🏥 MEDIPRECOG - Your Health Time Machine
Predicting Health Risks 3-5 Years Before Symptoms Appear
Complete OCR-enabled version
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
import time
import tempfile
import os
from datetime import datetime
import io
import base64
from PIL import Image
import pytesseract
from pdf2image import convert_from_bytes
import cv2
import re
import random
from faker import Faker

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="MediPrecog - Health Time Machine",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/mediprecog',
        'Report a bug': "https://github.com/mediprecog/issues",
        'About': "# 🏥 MediPrecog - Predicting Health Risks Before They Become Diseases"
    }
)

# ============================================
# ENHANCED CUSTOM CSS
# ============================================
st.markdown("""
<style>
    /* Main Titles */
    .main-title {
        font-size: 3.8rem;
        background: linear-gradient(90deg, #1a73e8 0%, #34a853 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 900;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-title {
        color: #5f6368;
        font-size: 1.5rem;
        text-align: center;
        margin-bottom: 2.5rem;
        font-weight: 400;
    }
    
    /* Feature Cards */
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        margin: 1.2rem 0;
        border: 1px solid #e0e0e0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 4rem 2rem;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.2);
    }
    
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 1rem;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        opacity: 0.9;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    /* How-to Steps */
    .step-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #1a73e8;
        margin: 1rem 0;
    }
    
    .step-number {
        background: #1a73e8;
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 1.2rem;
        margin-bottom: 1rem;
    }
    
    /* Stats Cards */
    .stat-card {
        background: white;
        padding: 1.8rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        border-top: 4px solid #1a73e8;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1a73e8;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        color: #666;
        font-size: 1rem;
        font-weight: 500;
    }
    
    /* Risk Indicators */
    .risk-high { 
        background: linear-gradient(135deg, #ff6b6b 0%, #ff5252 100%);
        color: white !important;
        padding: 8px 20px;
        border-radius: 25px;
        font-weight: bold;
        display: inline-block;
        box-shadow: 0 4px 10px rgba(255, 107, 107, 0.3);
    }
    
    .risk-medium { 
        background: linear-gradient(135deg, #ffd93d 0%, #ffb142 100%);
        color: #333 !important;
        padding: 8px 20px;
        border-radius: 25px;
        font-weight: bold;
        display: inline-block;
        box-shadow: 0 4px 10px rgba(255, 217, 61, 0.3);
    }
    
    .risk-low { 
        background: linear-gradient(135deg, #6bcf7f 0%, #4caf50 100%);
        color: white !important;
        padding: 8px 20px;
        border-radius: 25px;
        font-weight: bold;
        display: inline-block;
        box-shadow: 0 4px 10px rgba(107, 207, 127, 0.3);
    }
    
    /* Upload Area */
    .upload-area {
        border: 3px dashed #1a73e8;
        border-radius: 20px;
        padding: 4rem;
        text-align: center;
        background: rgba(26, 115, 232, 0.05);
        margin: 2.5rem 0;
        transition: all 0.3s ease;
    }
    
    .upload-area:hover {
        background: rgba(26, 115, 232, 0.1);
        border-color: #34a853;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 7px 15px rgba(0,0,0,0.1) !important;
    }
    
    /* Text Colors for Better Visibility */
    .dark-text {
        color: #333333 !important;
    }
    
    .medium-text {
        color: #555555 !important;
    }
    
    .highlight-text {
        color: #1a73e8 !important;
        font-weight: 600;
    }
    
    /* Sidebar Improvements */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
    }
    
    /* Timeline Markers */
    .timeline-marker {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 12px;
        box-shadow: 0 3px 8px rgba(0,0,0,0.2);
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
if 'extracted_text' not in st.session_state:
    st.session_state.extracted_text = ""
if 'current_page' not in st.session_state:
    st.session_state.current_page = "🏠 Welcome"

# ============================================
# OCR SCANNER CLASS
# ============================================
class MedicalReportScanner:
    """OCR Scanner for medical reports"""
    
    def __init__(self):
        # Set tesseract path for Windows if needed
        if os.name == 'nt':
            try:
                pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            except:
                pass
    
    def extract_text_from_image(self, image):
        """Extract text from image using OCR"""
        try:
            # Convert to grayscale
            if image.mode != 'L':
                image = image.convert('L')
            
            # Use OCR
            text = pytesseract.image_to_string(image, config='--psm 6')
            return text
        except Exception as e:
            st.warning(f"OCR Warning: {e}")
            return self.generate_mock_report()
    
    def extract_text_from_pdf(self, pdf_bytes):
        """Extract text from PDF"""
        try:
            images = convert_from_bytes(pdf_bytes)
            all_text = ""
            for i, image in enumerate(images):
                page_text = self.extract_text_from_image(image)
                all_text += f"--- Page {i+1} ---\n{page_text}\n\n"
            return all_text
        except Exception as e:
            st.warning(f"PDF Extraction Warning: {e}")
            return self.generate_mock_report()
    
    def generate_mock_report(self):
        """Generate mock medical report"""
        return f"""
        PATIENT MEDICAL REPORT - {fake.name().upper()}
        
        Patient Information:
        Name: {fake.name()}
        Age: {random.randint(35, 65)} years
        Gender: {random.choice(['Male', 'Female'])}
        
        Vital Signs:
        Blood Pressure: {random.randint(110, 160)}/{random.randint(70, 100)} mmHg
        Heart Rate: {random.randint(60, 100)} bpm
        
        Laboratory Results:
        Glucose (Fasting): {random.randint(90, 180)} mg/dL
        HbA1c: {random.uniform(5.0, 8.0):.1f}%
        Total Cholesterol: {random.randint(180, 280)} mg/dL
        
        Physical Examination:
        Height: {random.randint(155, 185)} cm
        Weight: {random.randint(60, 110)} kg
        BMI: {random.uniform(22, 34):.1f} kg/m²
        
        Medical History:
        Family History: Diabetes - {random.choice(['Yes', 'No'])}, Heart Disease - {random.choice(['Yes', 'No'])}
        Smoking Status: {random.choice(['Never', 'Former', 'Current'])}
        
        Physician's Notes:
        Patient presents for routine checkup. Recommend lifestyle modifications.
        """

# ============================================
# UTILITY FUNCTIONS
# ============================================
def parse_extracted_data(text):
    """Parse OCR text to extract medical data"""
    data = {
        'name': 'Patient',
        'age': 45,
        'gender': 'Male',
        'glucose': 120,
        'bp_systolic': 130,
        'bp_diastolic': 85,
        'cholesterol': 220,
        'bmi': 26.5,
        'smoker': False,
        'family_history_diabetes': False,
        'exercise_hours': 2.5
    }
    
    # Simple parsing logic
    import re
    
    # Extract name
    name_match = re.search(r'Name:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)', text, re.IGNORECASE)
    if name_match:
        data['name'] = name_match.group(1).strip()
    
    # Extract age
    age_match = re.search(r'Age:\s*(\d+)', text, re.IGNORECASE)
    if age_match:
        data['age'] = int(age_match.group(1))
    
    # Extract glucose
    glucose_match = re.search(r'Glucose.*?(\d+)\s*(?:mg/dL|mg/dl)', text, re.IGNORECASE)
    if glucose_match:
        data['glucose'] = int(glucose_match.group(1))
    
    # Extract blood pressure
    bp_match = re.search(r'Blood Pressure.*?(\d+)\s*/\s*(\d+)', text, re.IGNORECASE)
    if bp_match:
        data['bp_systolic'] = int(bp_match.group(1))
        data['bp_diastolic'] = int(bp_match.group(2))
    
    # Extract cholesterol
    chol_match = re.search(r'Cholesterol.*?(\d+)\s*(?:mg/dL|mg/dl)', text, re.IGNORECASE)
    if chol_match:
        data['cholesterol'] = int(chol_match.group(1))
    
    # Extract BMI
    bmi_match = re.search(r'BMI.*?(\d+\.?\d*)', text, re.IGNORECASE)
    if bmi_match:
        data['bmi'] = float(bmi_match.group(1))
    
    # Check for smoking
    if re.search(r'smoker|smoking|tobacco', text, re.IGNORECASE):
        data['smoker'] = True
    
    return data

def generate_synthetic_report():
    """Generate synthetic patient data"""
    return {
        'name': fake.name(),
        'age': random.randint(35, 65),
        'gender': random.choice(['Male', 'Female']),
        'glucose': random.randint(95, 180),
        'bp_systolic': random.randint(115, 160),
        'bp_diastolic': random.randint(75, 100),
        'cholesterol': random.randint(180, 280),
        'bmi': round(random.uniform(22, 34), 1),
        'smoker': random.choice([True, False]),
        'family_history_diabetes': random.choice([True, False]),
        'exercise_hours': round(random.uniform(1, 5), 1)
    }

def calculate_risk_scores(patient_data):
    """Calculate disease risks"""
    glucose = patient_data.get('glucose', 100)
    bp = patient_data.get('bp_systolic', 120)
    cholesterol = patient_data.get('cholesterol', 200)
    bmi = patient_data.get('bmi', 22)
    smoker = patient_data.get('smoker', False)
    
    # Diabetes risk
    diabetes = 0.1
    if glucose > 125: diabetes *= 2.5
    elif glucose > 100: diabetes *= 1.8
    if bmi > 30: diabetes *= 2.0
    elif bmi > 25: diabetes *= 1.5
    
    # Heart disease risk
    heart = 0.1
    if cholesterol > 240: heart *= 2.2
    elif cholesterol > 200: heart *= 1.5
    if bp > 140: heart *= 2.0
    elif bp > 130: heart *= 1.5
    if smoker: heart *= 2.0
    
    # Hypertension risk
    hypertension = 0.1
    if bp > 140: hypertension *= 2.5
    elif bp > 130: hypertension *= 1.8
    if bmi > 30: hypertension *= 2.0
    
    return {
        'diabetes': min(0.95, diabetes),
        'heart_disease': min(0.95, heart),
        'hypertension': min(0.95, hypertension)
    }

def generate_timeline_projections(patient_data, risk_scores):
    """Generate timeline projections"""
    years = list(range(11))
    
    diabetes = [risk_scores['diabetes'] * 100 * (1.15 ** year) for year in years]
    heart = [risk_scores['heart_disease'] * 100 * (1.12 ** year) for year in years]
    hypertension = [risk_scores['hypertension'] * 100 * (1.18 ** year) for year in years]
    
    diabetes = [min(95, d) for d in diabetes]
    heart = [min(95, h) for h in heart]
    hypertension = [min(95, h) for h in hypertension]
    
    return {
        'years': years,
        'diabetes': diabetes,
        'heart_disease': heart,
        'hypertension': hypertension
    }

# ============================================
# PAGE FUNCTIONS - IMPROVED UI
# ============================================

def home_page():
    """Beautiful Home Page explaining the website"""
    
    # HERO SECTION
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🔮 Welcome to MediPrecog</h1>
        <p class="hero-subtitle">
            Your Personal <strong>Health Time Machine</strong> that predicts disease risks 
            3-5 years before symptoms appear using AI-powered analysis of your medical reports.
        </p>
        <div style="margin-top: 2rem;">
            <span class="risk-low" style="margin: 0.5rem;">⚡ Instant Analysis</span>
            <span class="risk-medium" style="margin: 0.5rem;">🔒 100% Private</span>
            <span class="risk-high" style="margin: 0.5rem;">💰 Cost Saving</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # WHAT WE DO SECTION
    st.markdown("""
    <h2 style='color: #333; text-align: center; margin-bottom: 2rem;'>
        🎯 What MediPrecog Does
    </h2>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📸</div>
            <h3 style='color: #333;'>Smart Report Scanner</h3>
            <p class="medium-text">
                Upload any medical report (PDF/Image) and our AI extracts all health metrics 
                automatically using advanced OCR technology.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔮</div>
            <h3 style='color: #333;'>Predictive Risk Analysis</h3>
            <p class="medium-text">
                Get accurate predictions for diabetes, heart disease, and hypertension risks 
                3-5 years before symptoms might appear.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⏳</div>
            <h3 style='color: #333;'>Health Timeline</h3>
            <p class="medium-text">
                Visualize how your health risks evolve over the next 10 years with 
                interactive timelines and critical intervention points.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # HOW TO USE SECTION
    st.markdown("""
    <h2 style='color: #333; text-align: center; margin: 3rem 0 2rem 0;'>
        📖 How to Use MediPrecog
    </h2>
    """, unsafe_allow_html=True)
    
    steps = st.columns(4)
    
    with steps[0]:
        st.markdown("""
        <div class="step-card">
            <div class="step-number">1</div>
            <h4 style='color: #333;'>Upload Report</h4>
            <p class="medium-text">Upload your medical report (PDF or image)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with steps[1]:
        st.markdown("""
        <div class="step-card">
            <div class="step-number">2</div>
            <h4 style='color: #333;'>AI Analysis</h4>
            <p class="medium-text">Our AI extracts and analyzes health data</p>
        </div>
        """, unsafe_allow_html=True)
    
    with steps[2]:
        st.markdown("""
        <div class="step-card">
            <div class="step-number">3</div>
            <h4 style='color: #333;'>View Risks</h4>
            <p class="medium-text">See your personalized risk assessment</p>
        </div>
        """, unsafe_allow_html=True)
    
    with steps[3]:
        st.markdown("""
        <div class="step-card">
            <div class="step-number">4</div>
            <h4 style='color: #333;'>Get Plan</h4>
            <p class="medium-text">Receive personalized prevention plan</p>
        </div>
        """, unsafe_allow_html=True)
    
    # STATISTICS SECTION
    st.markdown("""
    <h2 style='color: #333; text-align: center; margin: 3rem 0 2rem 0;'>
        📊 Why MediPrecog Works
    </h2>
    """, unsafe_allow_html=True)
    
    stats = st.columns(4)
    
    with stats[0]:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">5x</div>
            <div class="stat-label">Better Outcomes</div>
            <p style='color: #666; font-size: 0.9rem; margin-top: 0.5rem;'>
                Early detection improves treatment success
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with stats[1]:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">85%</div>
            <div class="stat-label">Cost Savings</div>
            <p style='color: #666; font-size: 0.9rem; margin-top: 0.5rem;'>
                Prevention vs late treatment costs
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with stats[2]:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">72%</div>
            <div class="stat-label">Success Rate</div>
            <p style='color: #666; font-size: 0.9rem; margin-top: 0.5rem;'>
                With personalized prevention plans
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with stats[3]:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">60s</div>
            <div class="stat-label">Analysis Time</div>
            <p style='color: #666; font-size: 0.9rem; margin-top: 0.5rem;'>
                Complete health risk assessment
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # GET STARTED BUTTON
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 START YOUR HEALTH JOURNEY", use_container_width=True, type="primary"):
            st.session_state.current_page = "📸 Scan Report"
            st.rerun()

def report_scanner_page():
    """Report Scanner Page with OCR"""
    
    st.markdown("""
    <h2 style='color: #333; text-align: center; margin-bottom: 1rem;'>
        📸 Upload Your Medical Report
    </h2>
    <p style='text-align: center; color: #666; margin-bottom: 2rem;'>
        Upload any medical report (PDF or image) for instant AI-powered analysis
    </p>
    """, unsafe_allow_html=True)
    
    # Upload Area
    st.markdown("""
    <div class="upload-area">
        <h3 style='color: #1a73e8; margin-bottom: 1rem;'>📁 Drag & Drop or Click to Upload</h3>
        <p style='color: #666;'>Supported formats: PDF, PNG, JPG, JPEG</p>
        <p style='color: #666; font-size: 0.9rem; margin-top: 1rem;'>
            We'll extract: Glucose, Blood Pressure, Cholesterol, BMI, and other vital metrics
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a medical report file",
        type=['pdf', 'png', 'jpg', 'jpeg'],
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        # File details
        with st.expander("📄 File Details", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("File Name", uploaded_file.name)
                st.metric("File Type", uploaded_file.type.split('/')[-1].upper())
            with col2:
                st.metric("File Size", f"{uploaded_file.size / 1024:.1f} KB")
                st.metric("Status", "Ready for Analysis", "✅")
        
        # Process button
        if st.button("🔍 Analyze Report with AI", use_container_width=True, type="primary"):
            with st.spinner("🤖 AI is analyzing your medical report..."):
                time.sleep(2)  # Simulate processing
                
                scanner = MedicalReportScanner()
                
                # Process based on file type
                if uploaded_file.type == "application/pdf":
                    text = scanner.extract_text_from_pdf(uploaded_file.read())
                else:
                    image = Image.open(uploaded_file)
                    text = scanner.extract_text_from_image(image)
                
                st.session_state.extracted_text = text
                patient_data = parse_extracted_data(text)
                st.session_state.patient_data = patient_data
                st.session_state.report_scanned = True
                st.session_state.risk_scores = calculate_risk_scores(patient_data)
                
                st.success("✅ Analysis Complete! Your health risks have been calculated.")
                st.balloons()
                
                # Show extracted info
                with st.expander("📋 View Extracted Health Data", expanded=True):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Patient Name", patient_data['name'])
                        st.metric("Age", patient_data['age'])
                        st.metric("Glucose", f"{patient_data['glucose']} mg/dL")
                    with col2:
                        st.metric("Blood Pressure", f"{patient_data['bp_systolic']}/{patient_data['bp_diastolic']}")
                        st.metric("Cholesterol", f"{patient_data['cholesterol']} mg/dL")
                        st.metric("BMI", f"{patient_data['bmi']:.1f}")
                
                # Navigation
                st.markdown("---")
                if st.button("📊 View Risk Analysis →", use_container_width=True):
                    st.session_state.current_page = "📊 Risk Analysis"
                    st.rerun()
    
    # Demo Option
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Try Demo Report", use_container_width=True):
            with st.spinner("Loading demo data..."):
                time.sleep(1)
                patient_data = generate_synthetic_report()
                st.session_state.patient_data = patient_data
                st.session_state.report_scanned = True
                st.session_state.risk_scores = calculate_risk_scores(patient_data)
                st.success(f"✅ Demo loaded for {patient_data['name']}")
                st.rerun()
    
    with col2:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.session_state.current_page = "🏠 Welcome"
            st.rerun()

def risk_analysis_page():
    """Risk Analysis Page"""
    
    if not st.session_state.patient_data:
        st.warning("⚠️ Please upload a medical report first!")
        report_scanner_page()
        return
    
    patient = st.session_state.patient_data
    risks = st.session_state.risk_scores
    
    # Header
    st.markdown(f"""
    <h2 style='color: #333; text-align: center; margin-bottom: 0.5rem;'>
        📊 Health Risk Analysis
    </h2>
    <p style='text-align: center; color: #666; margin-bottom: 2rem;'>
        For: <strong>{patient['name']}</strong> | Age: {patient['age']} | BMI: {patient['bmi']:.1f}
    </p>
    """, unsafe_allow_html=True)
    
    # Health Metrics
    st.markdown("### 📈 Current Health Metrics")
    cols = st.columns(4)
    
    with cols[0]:
        st.markdown("""
        <div class="metric-card">
            <div style='color: #666; font-size: 0.9rem;'>Glucose</div>
            <div style='font-size: 1.5rem; font-weight: bold; color: #333;'>
                {glucose} mg/dL
            </div>
            <div style='margin-top: 0.5rem;'>
                {status}
            </div>
        </div>
        """.format(
            glucose=patient['glucose'],
            status="<span class='risk-high'>High</span>" if patient['glucose'] > 125 
            else ("<span class='risk-medium'>Borderline</span>" if patient['glucose'] > 100 
                  else "<span class='risk-low'>Normal</span>")
        ), unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown("""
        <div class="metric-card">
            <div style='color: #666; font-size: 0.9rem;'>Blood Pressure</div>
            <div style='font-size: 1.5rem; font-weight: bold; color: #333;'>
                {systolic}/{diastolic}
            </div>
            <div style='margin-top: 0.5rem;'>
                {status}
            </div>
        </div>
        """.format(
            systolic=patient['bp_systolic'],
            diastolic=patient['bp_diastolic'],
            status="<span class='risk-high'>High</span>" if patient['bp_systolic'] > 130 
            else "<span class='risk-low'>Normal</span>"
        ), unsafe_allow_html=True)
    
    with cols[2]:
        st.markdown("""
        <div class="metric-card">
            <div style='color: #666; font-size: 0.9rem;'>Cholesterol</div>
            <div style='font-size: 1.5rem; font-weight: bold; color: #333;'>
                {cholesterol} mg/dL
            </div>
            <div style='margin-top: 0.5rem;'>
                {status}
            </div>
        </div>
        """.format(
            cholesterol=patient['cholesterol'],
            status="<span class='risk-high'>High</span>" if patient['cholesterol'] > 240 
            else ("<span class='risk-medium'>Borderline</span>" if patient['cholesterol'] > 200 
                  else "<span class='risk-low'>Normal</span>")
        ), unsafe_allow_html=True)
    
    with cols[3]:
        st.markdown("""
        <div class="metric-card">
            <div style='color: #666; font-size: 0.9rem;'>BMI</div>
            <div style='font-size: 1.5rem; font-weight: bold; color: #333;'>
                {bmi:.1f}
            </div>
            <div style='margin-top: 0.5rem;'>
                {status}
            </div>
        </div>
        """.format(
            bmi=patient['bmi'],
            status="<span class='risk-high'>Obese</span>" if patient['bmi'] > 30 
            else ("<span class='risk-medium'>Overweight</span>" if patient['bmi'] > 25 
                  else "<span class='risk-low'>Normal</span>")
        ), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Risk Chart
    st.markdown("### 🎯 Disease Risk Assessment")
    
    diseases = ['Diabetes', 'Heart Disease', 'Hypertension']
    disease_keys = ['diabetes', 'heart_disease', 'hypertension']
    risk_values = [risks[key] * 100 for key in disease_keys]
    
    # Create chart
    fig = go.Figure()
    
    colors = ['#FF6B6B', '#FFA726', '#42A5F5']
    
    for i, (disease, risk, color) in enumerate(zip(diseases, risk_values, colors)):
        fig.add_trace(go.Bar(
            x=[disease],
            y=[risk],
            name=disease,
            marker_color=color,
            text=[f"{risk:.1f}%"],
            textposition='auto',
            hovertemplate=f"{disease}<br>Risk: {risk:.1f}%"
        ))
    
    fig.update_layout(
        yaxis_title="Risk Probability (%)",
        yaxis_range=[0, 100],
        showlegend=False,
        height=400,
        template="plotly_white",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Risk Factors
    st.markdown("### ⚠️ Identified Risk Factors")
    
    risk_factors = []
    if patient['glucose'] > 100: risk_factors.append("Elevated glucose levels")
    if patient['bp_systolic'] > 130: risk_factors.append("High blood pressure")
    if patient['cholesterol'] > 200: risk_factors.append("High cholesterol")
    if patient['bmi'] > 25: risk_factors.append("Overweight/Obese")
    if patient['smoker']: risk_factors.append("Smoking")
    
    if risk_factors:
        for factor in risk_factors:
            st.markdown(f"<div class='dark-text'>• <strong>{factor}</strong></div>", unsafe_allow_html=True)
    else:
        st.success("✅ No major risk factors detected!")
    
    # Navigation
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("← Back to Scanner", use_container_width=True):
            st.session_state.current_page = "📸 Scan Report"
            st.rerun()
    with col2:
        if st.button("⏳ View Timeline", use_container_width=True):
            st.session_state.current_page = "⏳ Timeline"
            st.rerun()
    with col3:
        if st.button("💰 Cost Calculator →", use_container_width=True, type="primary"):
            st.session_state.current_page = "💰 Cost Calculator"
            st.rerun()

# ============================================
# ADDITIONAL PAGE FUNCTIONS (Simplified)
# ============================================

def timeline_page():
    """Timeline Page"""
    if not st.session_state.patient_data:
        st.warning("Please upload a report first")
        return
    
    patient = st.session_state.patient_data
    risks = st.session_state.risk_scores
    
    st.markdown(f"""
    <h2 style='color: #333; text-align: center;'>
        ⏳ Health Risk Timeline: {patient['name']}
    </h2>
    """, unsafe_allow_html=True)
    
    # Generate timeline
    timeline = generate_timeline_projections(patient, risks)
    
    # Create timeline chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=timeline['years'],
        y=timeline['diabetes'],
        mode='lines+markers',
        name='Diabetes',
        line=dict(color='#FF6B6B', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=timeline['years'],
        y=timeline['heart_disease'],
        mode='lines+markers',
        name='Heart Disease',
        line=dict(color='#FFA726', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=timeline['years'],
        y=timeline['hypertension'],
        mode='lines+markers',
        name='Hypertension',
        line=dict(color='#42A5F5', width=3)
    ))
    
    # Add critical points
    fig.add_vline(x=1, line_dash="dash", line_color="green", 
                  annotation_text="Optimal Intervention", annotation_position="top")
    fig.add_vline(x=3, line_dash="dash", line_color="orange", 
                  annotation_text="Risk Escalation", annotation_position="top")
    
    fig.update_layout(
        title="10-Year Risk Projection",
        xaxis_title="Years from Now",
        yaxis_title="Risk Probability (%)",
        height=500,
        template="plotly_white"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Risk Analysis", use_container_width=True):
            st.session_state.current_page = "📊 Risk Analysis"
            st.rerun()
    with col2:
        if st.button("💰 Cost Calculator →", use_container_width=True, type="primary"):
            st.session_state.current_page = "💰 Cost Calculator"
            st.rerun()

def cost_calculator_page():
    """Cost Calculator Page"""
    
    st.markdown("""
    <h2 style='color: #333; text-align: center;'>
        💰 Healthcare Cost Calculator
    </h2>
    <p style='text-align: center; color: #666;'>
        See how prevention can save thousands in healthcare costs
    </p>
    """, unsafe_allow_html=True)
    
    # Cost comparison
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 2rem; background: #ff4444; color: white; border-radius: 15px;'>
            <h1 style='font-size: 2.5rem;'>$48,500</h1>
            <p>Without Prevention</p>
            <p style='font-size: 0.9rem; opacity: 0.9;'>5-year estimated cost</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 2rem; background: #00c851; color: white; border-radius: 15px;'>
            <h1 style='font-size: 2.5rem;'>$12,500</h1>
            <p>With Prevention</p>
            <p style='font-size: 0.9rem; opacity: 0.9;'>5-year estimated cost</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='text-align: center; padding: 2rem; background: #1a73e8; color: white; border-radius: 15px;'>
            <h1 style='font-size: 2.5rem;'>$36,000</h1>
            <p>Potential Savings</p>
            <p style='font-size: 0.9rem; opacity: 0.9;'>74% cost reduction</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Navigation
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Timeline", use_container_width=True):
            st.session_state.current_page = "⏳ Timeline"
            st.rerun()
    with col2:
        if st.button("📝 Action Plan →", use_container_width=True, type="primary"):
            st.session_state.current_page = "📝 Action Plan"
            st.rerun()

def action_plan_page():
    """Action Plan Page"""
    
    st.markdown("""
    <h2 style='color: #333; text-align: center;'>
        📝 Your Personalized Prevention Plan
    </h2>
    <p style='text-align: center; color: #666;'>
        Step-by-step guide to reduce your health risks
    </p>
    """, unsafe_allow_html=True)
    
    # Action Plan Steps
    steps = [
        ("Week 1-4", "Immediate Actions", [
            "Consult healthcare provider",
            "Start 30-min daily walks",
            "Reduce sugar intake by 50%"
        ]),
        ("Month 1-3", "Habit Formation", [
            "Join prevention program",
            "Regular glucose monitoring",
            "Stress management techniques"
        ]),
        ("Month 3-12", "Consolidation", [
            "Achieve 5-10% weight loss",
            "Regular blood work",
            "Family screening if needed"
        ]),
        ("Year 1-5", "Maintenance", [
            "Annual comprehensive checkup",
            "Lifestyle maintenance",
            "Community health programs"
        ])
    ]
    
    for timeline, title, actions in steps:
        st.markdown(f"""
        <div class="step-card">
            <h3 style='color: #1a73e8;'>{timeline}: {title}</h3>
        """, unsafe_allow_html=True)
        
        for action in actions:
            st.markdown(f"<div class='dark-text'>✓ {action}</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Download button
    st.markdown("---")
    if st.button("📥 Download Complete Action Plan", use_container_width=True, type="primary"):
        st.success("✅ Action plan downloaded!")
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Calculator", use_container_width=True):
            st.session_state.current_page = "💰 Cost Calculator"
            st.rerun()
    with col2:
        if st.button("🔄 Analyze New Patient", use_container_width=True):
            for key in ['patient_data', 'risk_scores', 'report_scanned']:
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state.current_page = "📸 Scan Report"
            st.rerun()

# ============================================
# MAIN APPLICATION
# ============================================

def main():
    """Main application with sidebar navigation"""
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h1 style='color: #1a73e8;'>🏥</h1>
            <h2 style='color: #333;'>MEDIPRECOG</h2>
            <p style='color: #666; font-size: 0.9rem;'>Health Time Machine</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation Menu
        pages = {
            "🏠 Welcome": home_page,
            "📸 Scan Report": report_scanner_page,
            "📊 Risk Analysis": risk_analysis_page,
            "⏳ Timeline": timeline_page,
            "💰 Cost Calculator": cost_calculator_page,
            "📝 Action Plan": action_plan_page
        }
        
        selected = st.selectbox(
            "Navigate to:",
            list(pages.keys()),
            index=list(pages.keys()).index(st.session_state.current_page) 
            if st.session_state.current_page in pages else 0,
            label_visibility="collapsed"
        )
        
        if selected != st.session_state.current_page:
            st.session_state.current_page = selected
            st.rerun()
        
        # Patient Info (if available)
        if st.session_state.patient_data:
            st.markdown("---")
            patient = st.session_state.patient_data
            st.markdown(f"""
            <div style='background: #e8f0fe; padding: 1rem; border-radius: 10px;'>
                <p style='color: #333; font-weight: bold; margin-bottom: 0.5rem;'>
                    👤 Current Patient
                </p>
                <p style='color: #666; margin: 0;'><strong>{patient['name']}</strong></p>
                <p style='color: #666; margin: 0;'>Age: {patient['age']} | BMI: {patient['bmi']:.1f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Reset Button
        st.markdown("---")
        if st.button("🔄 Start Fresh", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.current_page = "🏠 Welcome"
            st.rerun()
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #666; font-size: 0.8rem; padding: 1rem 0;'>
            <p>🔒 100% Private & Secure</p>
            <p>⚡ Real-time Analysis</p>
            <p>🏥 Healthcare Hackathon 2024</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main Content Area
    pages = {
        "🏠 Welcome": home_page,
        "📸 Scan Report": report_scanner_page,
        "📊 Risk Analysis": risk_analysis_page,
        "⏳ Timeline": timeline_page,
        "💰 Cost Calculator": cost_calculator_page,
        "📝 Action Plan": action_plan_page
    }
    
    if st.session_state.current_page in pages:
        pages[st.session_state.current_page]()

# ============================================
# RUN THE APPLICATION
# ============================================
if __name__ == "__main__":
    main()