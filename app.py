"""
🏥 MEDIPRECOG - Health Time Machine
Complete with Medical Report Analysis & Advanced UI
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time
from datetime import datetime, timedelta
import random
import json
import base64
from io import BytesIO
import re
import warnings
warnings.filterwarnings('ignore')

# ============================================
# ENHANCED PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="MediPrecog - Health Time Machine",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/mediprecog',
        'Report a bug': "https://github.com/mediprecog/issues",
        'About': "# 🧬 MediPrecog v2.0\nAI-Powered Health Risk Prediction"
    }
)

# ============================================
# ADVANCED ANIMATED CSS
# ============================================
st.markdown("""
<style>
    /* Enhanced Modern Base */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #e2e8f0;
    }
    
    /* Animated Title */
    .main-title {
        font-size: 3.2rem;
        font-weight: 900;
        background: linear-gradient(90deg, #00d4ff 0%, #8b5cf6 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1.5rem;
        text-align: center;
        padding: 1.5rem;
        animation: glow 2s ease-in-out infinite alternate;
        position: relative;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 20px rgba(0, 212, 255, 0.3); }
        to { text-shadow: 0 0 30px rgba(139, 92, 246, 0.5), 0 0 40px rgba(139, 92, 246, 0.3); }
    }
    
    .main-title::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 25%;
        width: 50%;
        height: 3px;
        background: linear-gradient(90deg, transparent, #00d4ff, #8b5cf6, transparent);
        border-radius: 3px;
    }
    
    /* Glassmorphic Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 1.8rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.4);
        border-color: rgba(0, 212, 255, 0.3);
    }
    
    .highlight-card {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 12px 40px rgba(37, 99, 235, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .highlight-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #00d4ff, #8b5cf6);
    }
    
    /* Section Titles with Icons */
    .section-title {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #60a5fa 0%, #38bdf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 2.5rem 0 1.5rem;
        padding-left: 0.5rem;
        border-left: 5px solid #3b82f6;
        padding-left: 1rem;
    }
    
    .subsection-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #cbd5e1;
        margin: 1.5rem 0 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Risk Cards with Pulse Animation */
    .risk-card {
        background: rgba(30, 41, 59, 0.9);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 6px solid;
        position: relative;
        overflow: hidden;
    }
    
    .risk-low { 
        border-left-color: #10b981;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.2);
    }
    
    .risk-medium { 
        border-left-color: #f59e0b;
        box-shadow: 0 4px 20px rgba(245, 158, 11, 0.2);
    }
    
    .risk-high { 
        border-left-color: #ef4444;
        box-shadow: 0 4px 20px rgba(239, 68, 68, 0.3);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 4px 20px rgba(239, 68, 68, 0.3); }
        50% { box-shadow: 0 4px 30px rgba(239, 68, 68, 0.5); }
        100% { box-shadow: 0 4px 20px rgba(239, 68, 68, 0.3); }
    }
    
    /* Enhanced Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.9rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        border-radius: 12px !important;
        transition: all 0.3s !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: 0.5s;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.4) !important;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .secondary-btn > button {
        background: transparent !important;
        color: #3b82f6 !important;
        border: 2px solid #3b82f6 !important;
    }
    
    /* Enhanced Metrics */
    .metric-container {
        background: rgba(30, 41, 59, 0.8);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        transition: all 0.3s;
    }
    
    .metric-container:hover {
        border-color: #3b82f6;
        transform: scale(1.02);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #60a5fa, #38bdf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        color: #94a3b8;
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Progress Bars */
    .progress-container {
        margin: 1.5rem 0;
    }
    
    .progress-bar {
        height: 12px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 6px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #00d4ff, #8b5cf6);
        border-radius: 6px;
        transition: width 1s cubic-bezier(0.34, 1.56, 0.64, 1);
        position: relative;
        overflow: hidden;
    }
    
    .progress-fill::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;
        background-image: linear-gradient(
            -45deg,
            rgba(255, 255, 255, 0.2) 25%,
            transparent 25%,
            transparent 50%,
            rgba(255, 255, 255, 0.2) 50%,
            rgba(255, 255, 255, 0.2) 75%,
            transparent 75%,
            transparent
        );
        z-index: 1;
        background-size: 50px 50px;
        animation: move 2s linear infinite;
    }
    
    @keyframes move {
        0% { background-position: 0 0; }
        100% { background-position: 50px 50px; }
    }
    
    /* Enhanced Form Elements */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div,
    .stTextArea > div > div > textarea {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 0.9rem 1.2rem !important;
        font-size: 1rem !important;
        color: #e2e8f0 !important;
        transition: all 0.3s !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1) !important;
    }
    
    /* Enhanced Tables */
    .dataframe {
        background: rgba(30, 41, 59, 0.8) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    .dataframe th {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 1rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    
    .dataframe td {
        padding: 0.8rem 1rem !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
        color: #cbd5e1 !important;
    }
    
    /* Status Indicators */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .status-good {
        background: rgba(16, 185, 129, 0.2);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .status-warning {
        background: rgba(245, 158, 11, 0.2);
        color: #f59e0b;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    
    .status-danger {
        background: rgba(239, 68, 68, 0.2);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
        animation: pulse-badge 2s infinite;
    }
    
    @keyframes pulse-badge {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    /* File Upload Styling */
    .uploaded-file {
        background: rgba(30, 41, 59, 0.8);
        border: 2px dashed #475569;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin: 1.5rem 0;
        transition: all 0.3s;
    }
    
    .uploaded-file:hover {
        border-color: #3b82f6;
        background: rgba(59, 130, 246, 0.1);
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #2563eb, #7c3aed);
    }
    
    /* Loading Animation */
    .loading-spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 3rem;
    }
    
    /* Divider */
    .divider {
        height: 1px;
        background: linear-gradient(to right, transparent, #475569, transparent);
        margin: 2.5rem 0;
    }
    
    /* Tag Styling */
    .tag {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        background: rgba(59, 130, 246, 0.2);
        color: #60a5fa;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin: 0.2rem;
    }
    
    /* Sidebar Enhancement */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Card Grid */
    .card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# ENHANCED INITIALIZATION
# ============================================

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        'patient_data': None,
        'risk_scores': None,
        'timeline_data': None,
        'cost_analysis': None,
        'action_plan': None,
        'uploaded_report': None,
        'extracted_data': None,
        'current_page': "dashboard",
        'analysis_history': [],
        'health_metrics': {}
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

init_session_state()

# ============================================
# ENHANCED MEDICAL REPORT ANALYSIS
# ============================================

class EnhancedMedicalReportAnalyzer:
    """Enhanced analyzer for medical reports"""
    
    @staticmethod
    def extract_from_pdf(file):
        """Extract text from PDF file"""
        try:
            extracted_text = ""
            import pdfplumber
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        extracted_text += text + "\n"
            return extracted_text
        except Exception as e:
            return f"PDF extraction failed. Error: {str(e)}\nPlease try manual entry."
    
    @staticmethod
    def parse_medical_report(text):
        """Enhanced parsing with more medical terms"""
        
        patterns = {
            'glucose': r'(?i)(?:glucose|blood sugar|sugar|fbs)[:\s]+(\d{2,3})',
            'cholesterol': r'(?i)(?:cholesterol|chol|ldl|hdl)[:\s]+(\d{3})',
            'bp_systolic': r'(?i)(?:bp|blood pressure)[:\s]*(\d{2,3})\s*[/\s]\s*(\d{2,3})',
            'age': r'(?i)(?:age|dob.*age)[:\s]+(\d{2})',
            'bmi': r'(?i)(?:bmi|body mass index)[:\s]+(\d{2}\.\d|\d{2})',
            'weight': r'(?i)(?:weight|wt)[:\s]+(\d{2,3})',
            'height': r'(?i)(?:height|ht)[:\s]+(\d{3})',
            'hb': r'(?i)(?:hemoglobin|hb)[:\s]+(\d{1,2}\.\d)',
            'creatinine': r'(?i)(?:creatinine)[:\s]+(\d\.\d)',
            'diabetes': r'(?i)(?:diabetes|dm|diabetic)',
            'hypertension': r'(?i)(?:hypertension|htn|high bp)',
            'smoking': r'(?i)(?:smoking|smoker|tobacco)',
            'alcohol': r'(?i)(?:alcohol|drinking)'
        }
        
        extracted = {}
        
        for key, pattern in patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                if key == 'bp_systolic':
                    extracted['bp_systolic'] = int(matches[0][0])
                    extracted['bp_diastolic'] = int(matches[0][1])
                elif key == 'glucose':
                    extracted['glucose'] = int(matches[0])
                elif key == 'cholesterol':
                    extracted['cholesterol'] = int(matches[0])
                elif key == 'age':
                    extracted['age'] = int(matches[0])
                elif key == 'bmi':
                    extracted['bmi'] = float(matches[0])
                elif key == 'weight':
                    extracted['weight'] = int(matches[0])
                elif key == 'height':
                    extracted['height'] = int(matches[0])
                elif key == 'hb':
                    extracted['hb'] = float(matches[0])
                elif key == 'creatinine':
                    extracted['creatinine'] = float(matches[0])
                elif key in ['diabetes', 'hypertension', 'smoking', 'alcohol']:
                    extracted[key] = True
        
        return extracted
    
    @staticmethod
    def analyze_report(file):
        """Analyze uploaded medical report"""
        file_extension = file.name.split('.')[-1].lower()
        
        if file_extension == 'pdf':
            extracted_text = EnhancedMedicalReportAnalyzer.extract_from_pdf(BytesIO(file.read()))
        elif file_extension in ['txt', 'text']:
            extracted_text = file.read().decode('utf-8')
        else:
            # Simulate image OCR
            extracted_text = """MEDICAL REPORT
Patient: John Doe
Age: 45
Height: 175 cm
Weight: 80 kg
BMI: 26.1
Blood Pressure: 135/85
Fasting Glucose: 110 mg/dL
Cholesterol: 210 mg/dL
Smoking: No
Diabetes: No
Hypertension: Borderline"""
        
        # Parse the text
        extracted_data = EnhancedMedicalReportAnalyzer.parse_medical_report(extracted_text)
        
        # Fill missing values
        defaults = {
            'age': 45,
            'glucose': 95,
            'cholesterol': 180,
            'bp_systolic': 120,
            'bp_diastolic': 80,
            'bmi': 24,
            'diabetes': False,
            'hypertension': False,
            'smoking': False,
            'alcohol': False
        }
        
        for key, default_value in defaults.items():
            if key not in extracted_data:
                extracted_data[key] = default_value
        
        # Calculate BMI if weight/height available
        if 'weight' in extracted_data and 'height' in extracted_data:
            height_m = extracted_data['height'] / 100
            extracted_data['bmi'] = round(extracted_data['weight'] / (height_m ** 2), 1)
        
        return {
            'extracted_text': extracted_text[:800] + "..." if len(extracted_text) > 800 else extracted_text,
            'parsed_data': extracted_data,
            'file_name': file.name,
            'file_size': f"{file.size / 1024:.1f} KB",
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M")
        }

# ============================================
# ENHANCED RISK CALCULATOR
# ============================================

class EnhancedRiskCalculator:
    """Advanced risk calculation engine"""
    
    @staticmethod
    def calculate_health_score(patient_data):
        """Calculate overall health score (0-100)"""
        if not patient_data:
            return 75  # Default score
        
        score = 100
        
        # BMI penalty
        bmi = patient_data.get('bmi', 24)
        if bmi > 30:
            score -= 25
        elif bmi > 25:
            score -= 15
        
        # Glucose penalty
        glucose = patient_data.get('glucose', 95)
        if glucose > 126:
            score -= 20
        elif glucose > 100:
            score -= 10
        
        # BP penalty
        systolic = patient_data.get('bp_systolic', 120)
        if systolic > 140:
            score -= 20
        elif systolic > 130:
            score -= 10
        
        # Cholesterol penalty
        cholesterol = patient_data.get('cholesterol', 180)
        if cholesterol > 240:
            score -= 15
        elif cholesterol > 200:
            score -= 8
        
        # Lifestyle penalties
        if patient_data.get('smoking', False):
            score -= 15
        if patient_data.get('alcohol', False):
            score -= 5
        
        return max(0, min(100, score))
    
    @staticmethod
    def get_score_feedback(score):
        """Get feedback based on health score"""
        if score >= 80:
            return "Excellent health! Keep up the good habits."
        elif score >= 60:
            return "Good health. Some areas for improvement."
        elif score >= 40:
            return "Moderate health. Consider lifestyle changes."
        else:
            return "Needs attention. Consult a healthcare provider."
    
    @staticmethod
    def calculate_risks(patient_data):
        """Calculate enhanced disease risks"""
        if not patient_data:
            return None
            
        age = patient_data.get('age', 45)
        glucose = patient_data.get('glucose', 95)
        bp_systolic = patient_data.get('bp_systolic', 120)
        cholesterol = patient_data.get('cholesterol', 180)
        bmi = patient_data.get('bmi', 24)
        smoking = patient_data.get('smoking', False)
        diabetes_history = patient_data.get('diabetes', False)
        hypertension_history = patient_data.get('hypertension', False)
        
        # Enhanced diabetes risk
        diabetes_risk = 0.08
        if glucose > 126: diabetes_risk += 0.40
        elif glucose > 100: diabetes_risk += 0.25
        if bmi > 30: diabetes_risk += 0.30
        elif bmi > 25: diabetes_risk += 0.20
        if age > 50: diabetes_risk += 0.15
        elif age > 40: diabetes_risk += 0.08
        if diabetes_history: diabetes_risk += 0.25
        if patient_data.get('family_diabetes', False): diabetes_risk += 0.12
        
        # Enhanced heart disease risk
        heart_risk = 0.06
        if cholesterol > 240: heart_risk += 0.35
        elif cholesterol > 200: heart_risk += 0.20
        if bp_systolic > 140: heart_risk += 0.30
        elif bp_systolic > 130: heart_risk += 0.18
        if smoking: heart_risk += 0.30
        if bmi > 30: heart_risk += 0.25
        if age > 55: heart_risk += 0.20
        elif age > 45: heart_risk += 0.10
        if patient_data.get('family_heart', False): heart_risk += 0.15
        
        # Enhanced hypertension risk
        hypertension_risk = 0.12
        if bp_systolic > 140: hypertension_risk += 0.40
        elif bp_systolic > 130: hypertension_risk += 0.25
        if bmi > 30: hypertension_risk += 0.25
        if hypertension_history: hypertension_risk += 0.30
        if age > 45: hypertension_risk += 0.15
        if smoking: hypertension_risk += 0.10
        
        # Kidney disease risk (new)
        kidney_risk = 0.04
        if bp_systolic > 140: kidney_risk += 0.25
        if glucose > 126: kidney_risk += 0.20
        if patient_data.get('creatinine', 0.8) > 1.2: kidney_risk += 0.30
        if age > 60: kidney_risk += 0.15
        
        # Cap risks
        risks = {
            'diabetes': min(0.98, diabetes_risk),
            'heart_disease': min(0.98, heart_risk),
            'hypertension': min(0.98, hypertension_risk),
            'kidney_disease': min(0.98, kidney_risk)
        }
        
        # Determine levels
        def get_level(risk):
            if risk < 0.25: return "Low"
            elif risk < 0.5: return "Medium"
            elif risk < 0.75: return "High"
            else: return "Critical"
        
        result = {}
        for disease, risk in risks.items():
            result[disease] = {
                'risk': risk,
                'level': get_level(risk),
                'percentage': round(risk * 100, 1),
                'description': EnhancedRiskCalculator.get_risk_description(disease, risk)
            }
        result['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M")
        return result
    
    @staticmethod
    def get_risk_description(disease, risk):
        """Get descriptive text for risk level"""
        if disease == 'diabetes':
            if risk < 0.25: return "Normal glucose control"
            elif risk < 0.5: return "Pre-diabetic range"
            elif risk < 0.75: return "High diabetes risk"
            else: return "Probable diabetes"
        elif disease == 'heart_disease':
            if risk < 0.25: return "Healthy cardiovascular profile"
            elif risk < 0.5: return "Moderate heart risk"
            elif risk < 0.75: return "High heart risk"
            else: return "Very high heart risk"
        elif disease == 'hypertension':
            if risk < 0.25: return "Normal blood pressure"
            elif risk < 0.5: return "Borderline hypertension"
            elif risk < 0.75: return "High hypertension risk"
            else: return "Probable hypertension"
        else:
            if risk < 0.25: return "Normal kidney function"
            elif risk < 0.5: return "Moderate kidney risk"
            elif risk < 0.75: return "High kidney risk"
            else: return "Probable kidney issues"
    
    @staticmethod
    def generate_timeline(risk_scores):
        """Generate 10-year risk timeline with interventions"""
        if not risk_scores:
            return None
            
        years = list(range(11))  # 0 to 10 years
        
        timeline = {
            'years': years,
            'without_intervention': {},
            'with_intervention': {}
        }
        
        interventions = {
            'diabetes': {'effectiveness': 0.35, 'delay': 1},
            'heart_disease': {'effectiveness': 0.40, 'delay': 2},
            'hypertension': {'effectiveness': 0.45, 'delay': 1},
            'kidney_disease': {'effectiveness': 0.30, 'delay': 2}
        }
        
        for disease, data in risk_scores.items():
            if disease == 'timestamp':
                continue
            current_risk = data.get('risk', 0.1)
            
            # Without intervention (compounding risk)
            without = [current_risk]
            for year in range(1, 11):
                age_factor = 1 + (year * 0.015)  # 1.5% increase per year due to aging
                progression = 1 + (0.06 * year)  # 6% progression per year
                new_risk = min(0.95, without[-1] * age_factor * progression)
                without.append(new_risk)
            
            # With intervention
            with_int = [current_risk]
            intervention = interventions.get(disease, {'effectiveness': 0.3, 'delay': 1})
            
            for year in range(1, 11):
                if year <= intervention['delay']:
                    # Initial adjustment period
                    adj_risk = with_int[-1] * 1.02
                else:
                    # Intervention takes effect
                    improvement = 1 - (intervention['effectiveness'] * (1 - np.exp(-0.3 * (year - intervention['delay']))))
                    adj_risk = max(0.05, with_int[-1] * improvement)
                
                with_int.append(adj_risk)
            
            timeline['without_intervention'][disease] = without
            timeline['with_intervention'][disease] = with_int
        
        return timeline

# ============================================
# ENHANCED VISUALIZATION FUNCTIONS
# ============================================

class EnhancedVisualizations:
    """Advanced visualization components"""
    
    @staticmethod
    def create_risk_radar(risk_scores):
        """Create radar chart for risks"""
        if not risk_scores:
            return None
            
        categories = []
        values = []
        for disease, data in risk_scores.items():
            if disease != 'timestamp' and isinstance(data, dict):
                categories.append(disease.replace('_', ' ').title())
                values.append(data.get('percentage', 0))
        
        if not categories:
            return None
            
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Risk Levels',
            line=dict(color='#3b82f6', width=3),
            fillcolor='rgba(59, 130, 246, 0.3)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(color='#cbd5e1'),
                    gridcolor='rgba(255, 255, 255, 0.1)'
                ),
                angularaxis=dict(
                    tickfont=dict(color='#cbd5e1'),
                    gridcolor='rgba(255, 255, 255, 0.1)'
                ),
                bgcolor='rgba(30, 41, 59, 0.8)'
            ),
            showlegend=False,
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    @staticmethod
    def create_health_timeline(timeline_data):
        """Create animated timeline chart"""
        if not timeline_data:
            return None
            
        years = timeline_data['years']
        
        fig = go.Figure()
        
        colors = {
            'diabetes': '#8b5cf6',
            'heart_disease': '#ef4444',
            'hypertension': '#3b82f6',
            'kidney_disease': '#10b981'
        }
        
        # Add traces for each disease
        diseases = ['diabetes', 'heart_disease', 'hypertension']
        for disease in diseases:
            without_data = timeline_data['without_intervention'].get(disease)
            with_data = timeline_data['with_intervention'].get(disease)
            
            if without_data and with_data:
                fig.add_trace(go.Scatter(
                    x=years,
                    y=[r * 100 for r in without_data],
                    mode='lines',
                    name=f'{disease.replace("_", " ").title()} - No Action',
                    line=dict(color=colors[disease], width=3, dash='dash'),
                    hovertemplate='%{y:.1f}% risk'
                ))
                
                fig.add_trace(go.Scatter(
                    x=years,
                    y=[r * 100 for r in with_data],
                    mode='lines',
                    name=f'{disease.replace("_", " ").title()} - With Prevention',
                    line=dict(color=colors[disease], width=3),
                    hovertemplate='%{y:.1f}% risk'
                ))
        
        fig.update_layout(
            title=dict(
                text='10-Year Risk Projection',
                font=dict(size=20, color='white'),
                x=0.5
            ),
            xaxis_title=dict(text='Years from Now', font=dict(color='#cbd5e1')),
            yaxis_title=dict(text='Risk Probability (%)', font=dict(color='#cbd5e1')),
            height=450,
            hovermode='x unified',
            plot_bgcolor='rgba(30, 41, 59, 0.8)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1'),
            legend=dict(
                bgcolor='rgba(30, 41, 59, 0.8)',
                bordercolor='rgba(255, 255, 255, 0.1)',
                borderwidth=1
            ),
            xaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.1)',
                zerolinecolor='rgba(255, 255, 255, 0.1)'
            ),
            yaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.1)',
                zerolinecolor='rgba(255, 255, 255, 0.1)'
            )
        )
        
        return fig

# ============================================
# ENHANCED DASHBOARD
# ============================================

def show_enhanced_dashboard():
    """Enhanced Dashboard with Modern UI"""
    
    st.markdown('<div class="main-title">🧬 MediPrecog Health Intelligence</div>', unsafe_allow_html=True)
    
    # Welcome Section
    if st.session_state.patient_data:
        patient_name = st.session_state.patient_data.get('name', 'Patient')
        st.markdown(f'''
        <div class="glass-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h2 style="margin: 0; color: #60a5fa;">👋 Welcome back, {patient_name}</h2>
                    <p style="color: #94a3b8; margin: 0.5rem 0;">Your health insights are ready. Let's optimize your wellness journey.</p>
                </div>
                <div class="status-badge status-good">Active Analysis</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div class="glass-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h2 style="margin: 0; color: #60a5fa;">👋 Welcome to MediPrecog</h2>
                    <p style="color: #94a3b8; margin: 0.5rem 0;">Start your health analysis to get personalized insights and risk predictions.</p>
                </div>
                <div class="status-badge status-warning">Ready to Analyze</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Health Score Card
    health_score = EnhancedRiskCalculator.calculate_health_score(st.session_state.patient_data)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f'''
        <div class="glass-card">
            <div style="text-align: center;">
                <div class="metric-label">Overall Health Score</div>
                <div class="metric-value">{health_score:.0f}/100</div>
                <div class="progress-bar" style="margin: 1rem auto; max-width: 300px;">
                    <div class="progress-fill" style="width: {health_score}%"></div>
                </div>
                <div style="color: #94a3b8; font-size: 0.9rem;">
                    {EnhancedRiskCalculator.get_score_feedback(health_score)}
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        # Quick stats
        if st.session_state.risk_scores:
            high_risks = sum(1 for d in st.session_state.risk_scores.values() 
                           if isinstance(d, dict) and d.get('level') in ['High', 'Critical'])
            st.markdown(f'''
            <div class="metric-container">
                <div class="metric-label">High Risks</div>
                <div class="metric-value">{high_risks}</div>
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
            <div class="metric-container">
                <div class="metric-label">Waiting for Analysis</div>
                <div class="metric-value">--</div>
            </div>
            ''', unsafe_allow_html=True)
    
    # Main Dashboard Grid
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Risk Analysis Section
        st.markdown('<div class="section-title">⚠️ Risk Assessment</div>', unsafe_allow_html=True)
        
        # Create tabs for different views
        risk_tab1, risk_tab2 = st.tabs(["📊 Risk Levels", "🎯 Radar View"])
        
        with risk_tab1:
            if st.session_state.risk_scores:
                for disease, data in st.session_state.risk_scores.items():
                    if disease != 'timestamp' and isinstance(data, dict):
                        level = data.get('level', 'Low')
                        percentage = data.get('percentage', 0)
                        description = data.get('description', 'No description')
                        
                        if level == "Low":
                            status_class = "status-good"
                            card_class = "risk-low"
                        elif level == "Medium":
                            status_class = "status-warning"
                            card_class = "risk-medium"
                        elif level == "High":
                            status_class = "status-danger"
                            card_class = "risk-high"
                        else:  # Critical
                            status_class = "status-danger"
                            card_class = "risk-high"
                        
                        st.markdown(f'''
                        <div class="risk-card {card_class}">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                                <div>
                                    <h3 style="margin: 0; color: #e2e8f0;">{disease.replace('_', ' ').title()}</h3>
                                    <div style="display: flex; align-items: center; gap: 1rem; margin-top: 0.25rem;">
                                        <span class="{status_class}">{level} Risk</span>
                                        <span style="color: #94a3b8; font-size: 0.9rem;">{description}</span>
                                    </div>
                                </div>
                                <div style="font-size: 2rem; font-weight: 800; color: #60a5fa;">
                                    {percentage:.1f}%
                                </div>
                            </div>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: {percentage}%"></div>
                            </div>
                        </div>
                        ''', unsafe_allow_html=True)
            else:
                st.markdown('''
                <div class="glass-card">
                    <div style="text-align: center; padding: 3rem 2rem;">
                        <div style="font-size: 4rem; margin-bottom: 1rem;">📊</div>
                        <h3 style="color: #60a5fa;">No Risk Analysis Available</h3>
                        <p style="color: #94a3b8;">Upload a medical report or enter health data to get personalized risk analysis.</p>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with risk_tab2:
            if st.session_state.risk_scores:
                fig = EnhancedVisualizations.create_risk_radar(st.session_state.risk_scores)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No risk data available for radar chart")
            else:
                st.info("Please analyze your health data first to see the radar chart")
        
        # Timeline Visualization
        if st.session_state.timeline_data:
            st.markdown('<div class="section-title">📈 Risk Timeline Projection</div>', unsafe_allow_html=True)
            fig = EnhancedVisualizations.create_health_timeline(st.session_state.timeline_data)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Quick Actions Panel
        st.markdown('<div class="section-title">⚡ Quick Actions</div>', unsafe_allow_html=True)
        
        # Always show all buttons
        if st.button("📤 Upload Report", use_container_width=True, key="dash_upload"):
            st.session_state.current_page = "analyzer"
            st.rerun()
        
        if st.button("📝 Enter Data", use_container_width=True, key="dash_enter"):
            st.session_state.current_page = "analyzer"
            st.rerun()
        
        if st.button("💰 Cost Analysis", use_container_width=True, key="dash_cost"):
            if st.session_state.patient_data:
                st.session_state.current_page = "cost"
                st.rerun()
            else:
                st.warning("Please analyze your health data first")
        
        if st.button("🎯 Action Plan", use_container_width=True, key="dash_plan"):
            if st.session_state.patient_data:
                st.session_state.current_page = "plan"
                st.rerun()
            else:
                st.warning("Please analyze your health data first")
        
        if st.button("📋 Full Report", use_container_width=True, key="dash_report"):
            if st.session_state.patient_data:
                st.session_state.current_page = "report"
                st.rerun()
            else:
                st.warning("Please analyze your health data first")
        
        if st.button("🔄 New Analysis", use_container_width=True, key="dash_new"):
            st.session_state.patient_data = None
            st.session_state.risk_scores = None
            st.session_state.timeline_data = None
            st.session_state.current_page = "analyzer"
            st.rerun()
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # Health Tips Carousel
        st.markdown('<div class="section-title">💡 Daily Health Tips</div>', unsafe_allow_html=True)
        
        tips = [
            {"icon": "💧", "text": "Drink 8 glasses of water daily", "category": "Hydration"},
            {"icon": "🏃", "text": "Walk 10,000 steps every day", "category": "Exercise"},
            {"icon": "🥗", "text": "Include greens in every meal", "category": "Nutrition"},
            {"icon": "😴", "text": "Aim for 7-8 hours of sleep", "category": "Sleep"},
            {"icon": "🧘", "text": "Practice 10-min daily meditation", "category": "Mental"},
            {"icon": "📱", "text": "Take screen breaks every hour", "category": "Digital"}
        ]
        
        # Create a carousel effect
        tip_idx = int(time.time() / 10) % len(tips)
        tip = tips[tip_idx]
        
        st.markdown(f'''
        <div class="glass-card">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                <div style="font-size: 2rem;">{tip['icon']}</div>
                <div>
                    <div style="font-size: 0.8rem; color: #60a5fa; font-weight: 600;">{tip['category']}</div>
                    <div style="font-size: 1rem; font-weight: 500;">{tip['text']}</div>
                </div>
            </div>
            <div style="display: flex; justify-content: center; gap: 0.5rem;">
                {"".join(['●' if i == tip_idx else '○' for i in range(len(tips))])}
            </div>
        </div>
        ''', unsafe_allow_html=True)

# ============================================
# ENHANCED REPORT ANALYZER - FIXED VERSION
# ============================================

def show_enhanced_analyzer():
    """Enhanced Report Analyzer with fixed form data capture"""
    
    st.markdown('<div class="main-title">🔬 Medical Intelligence Analyzer</div>', unsafe_allow_html=True)
    
    # Dual Mode Selection
    analyze_mode = st.radio(
        "Choose Analysis Mode",
        ["📄 Upload Medical Report", "📝 Manual Data Entry"],
        horizontal=True,
        label_visibility="collapsed",
        key="analyze_mode_radio_main"
    )
    
    if analyze_mode == "📄 Upload Medical Report":
        st.markdown('<div class="section-title">📁 Upload Medical Report</div>', unsafe_allow_html=True)
        
        # Upload area with better styling
        uploaded_file = st.file_uploader(
            "Drag and drop your medical report here",
            type=['pdf', 'png', 'jpg', 'jpeg', 'txt', 'csv'],
            help="Supported formats: PDF, Images, Text, CSV",
            label_visibility="collapsed",
            key="file_uploader_main"
        )
        
        if uploaded_file is not None:
            # File preview
            st.markdown(f'''
            <div class="uploaded-file">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📄</div>
                <h4 style="margin: 0; color: #e2e8f0;">{uploaded_file.name}</h4>
                <p style="color: #94a3b8; margin: 0.5rem 0;">
                    Size: {uploaded_file.size / 1024:.1f} KB | Type: {uploaded_file.type}
                </p>
                <div style="margin-top: 1rem;">
                    <span class="tag">Ready for Analysis</span>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            # Analysis options
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🚀 Perform Advanced Analysis", type="primary", use_container_width=True, key="analyze_report_main"):
                    with st.spinner("🔍 Analyzing with AI..."):
                        progress_bar = st.progress(0)
                        for i in range(100):
                            time.sleep(0.01)
                            progress_bar.progress(i + 1)
                        
                        # Analyze report
                        analyzer = EnhancedMedicalReportAnalyzer()
                        analysis_result = analyzer.analyze_report(uploaded_file)
                        
                        # Store results
                        st.session_state.uploaded_report = uploaded_file.name
                        st.session_state.extracted_data = analysis_result
                        extracted = analysis_result['parsed_data']
                        extracted['name'] = "Report Analysis"
                        st.session_state.patient_data = extracted
                        
                        # Calculate risks
                        calculator = EnhancedRiskCalculator()
                        st.session_state.risk_scores = calculator.calculate_risks(extracted)
                        st.session_state.timeline_data = calculator.generate_timeline(st.session_state.risk_scores)
                        
                        st.success("✅ Analysis complete! Generating insights...")
                        time.sleep(1)
                        st.session_state.current_page = "dashboard"
                        st.rerun()
        else:
            st.markdown('''
            <div class="glass-card">
                <div style="text-align: center; padding: 2rem;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">📁</div>
                    <h3 style="color: #60a5fa;">Upload Your Medical Report</h3>
                    <p style="color: #94a3b8;">Drag and drop your PDF, image, or text file here</p>
                    <div style="margin-top: 1rem;">
                        <span class="tag">PDF</span>
                        <span class="tag">JPG/PNG</span>
                        <span class="tag">TXT</span>
                        <span class="tag">CSV</span>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
    
    else:  # Manual Data Entry - SIMPLIFIED WITHOUT FORM
        st.markdown('<div class="section-title">📝 Health Data Entry</div>', unsafe_allow_html=True)
        
        # Create a simple data entry without form to avoid conflicts
        st.markdown('<div class="subsection-title">👤 Personal Information</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", "John Doe", key="manual_name_input")
            age = st.slider("Age", 18, 100, 45, 1, key="manual_age_slider")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="manual_gender_select")
        
        with col2:
            height = st.number_input("Height (cm)", 100, 250, 175, 1, key="manual_height_input")
            weight = st.number_input("Weight (kg)", 30, 200, 80, 1, key="manual_weight_input")
            
            # Auto-calculate BMI
            if height > 0:
                bmi = weight / ((height/100) ** 2)
                # Display BMI using markdown instead of st.metric
                st.markdown(f'''
                <div class="metric-container">
                    <div class="metric-label">BMI</div>
                    <div class="metric-value">{bmi:.1f}</div>
                </div>
                ''', unsafe_allow_html=True)
        
        st.markdown('<div class="subsection-title">🩺 Medical Metrics</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            glucose = st.slider("Fasting Glucose (mg/dL)", 50, 300, 95, 1, key="manual_glucose_slider")
            systolic = st.slider("Systolic BP", 80, 200, 120, 1, key="manual_systolic_slider")
        
        with col2:
            cholesterol = st.slider("Cholesterol (mg/dL)", 100, 400, 180, 1, key="manual_cholesterol_slider")
            diastolic = st.slider("Diastolic BP", 50, 130, 80, 1, key="manual_diastolic_slider")
        
        st.markdown('<div class="subsection-title">🏃 Lifestyle Factors</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            smoker = st.checkbox("Smoker", key="manual_smoker_check")
            alcohol = st.checkbox("Regular Alcohol", key="manual_alcohol_check")
        
        with col2:
            exercise = st.select_slider(
                "Weekly Exercise",
                options=["None", "1-2 hours", "3-4 hours", "5+ hours"],
                value="3-4 hours",
                key="manual_exercise_slider"
            )
        
        with col3:
            sleep = st.select_slider(
                "Daily Sleep",
                options=["<5 hours", "5-6 hours", "6-7 hours", "7-8 hours", "8+ hours"],
                value="7-8 hours",
                key="manual_sleep_slider"
            )
        
        # Family History
        st.markdown('<div class="subsection-title">👨‍👩‍👧‍👦 Family History</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            family_diabetes = st.checkbox("Diabetes", key="manual_family_diabetes_check")
            family_heart = st.checkbox("Heart Disease", key="manual_family_heart_check")
        
        with col2:
            family_hypertension = st.checkbox("Hypertension", key="manual_family_hypertension_check")
            family_cancer = st.checkbox("Cancer", key="manual_family_cancer_check")
        
        # Submit button (not in a form)
        st.markdown('<div style="margin: 2rem 0;"></div>', unsafe_allow_html=True)
        
        if st.button("🚀 Analyze My Health Profile", type="primary", use_container_width=True, key="manual_submit_btn"):
            with st.spinner("🧠 Computing health insights..."):
                # Create patient data dictionary with ALL fields
                patient_data = {
                    'name': name,
                    'age': age,
                    'gender': gender,
                    'height': height,
                    'weight': weight,
                    'bmi': round(bmi, 1),
                    'glucose': glucose,
                    'bp_systolic': systolic,
                    'bp_diastolic': diastolic,
                    'cholesterol': cholesterol,
                    'smoking': smoker,
                    'alcohol': alcohol,
                    'exercise': exercise,
                    'sleep': sleep,
                    'family_diabetes': family_diabetes,
                    'family_heart': family_heart,
                    'family_hypertension': family_hypertension,
                    'family_cancer': family_cancer
                }
                
                # Debug: Show captured data
                st.info(f"📊 Capturing patient data for analysis...")
                
                # Calculate risks
                st.session_state.patient_data = patient_data
                calculator = EnhancedRiskCalculator()
                st.session_state.risk_scores = calculator.calculate_risks(patient_data)
                st.session_state.timeline_data = calculator.generate_timeline(st.session_state.risk_scores)
                
                st.success("✅ Profile analysis complete!")
                time.sleep(2)
                st.session_state.current_page = "dashboard"
                st.rerun()

# ============================================
# SIMPLIFIED PAGE FUNCTIONS
# ============================================

def show_cost_calculator():
    """Simplified Cost Calculator"""
    st.markdown('<div class="main-title">💰 Healthcare Cost Analysis</div>', unsafe_allow_html=True)
    
    if not st.session_state.patient_data:
        st.warning("Please analyze your health data first.")
        if st.button("📤 Go to Health Analysis", use_container_width=True, key="cost_goto_analyzer_main"):
            st.session_state.current_page = "analyzer"
            st.rerun()
        return
    
    st.markdown('<div class="section-title">📈 Cost Projections</div>', unsafe_allow_html=True)
    
    # Generate simple cost analysis
    if st.session_state.risk_scores:
        total_risk = 0
        count = 0
        for disease, data in st.session_state.risk_scores.items():
            if disease != 'timestamp' and isinstance(data, dict):
                total_risk += data.get('percentage', 0)
                count += 1
        
        if count > 0:
            avg_risk = total_risk / count
        else:
            avg_risk = 30  # Default
        
        # Cost calculations
        base_cost = 50000
        risk_multiplier = 1 + (avg_risk / 100)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Annual Cost (No Prevention)", f"₹{base_cost * risk_multiplier:,.0f}")
        with col2:
            st.metric("Annual Cost (With Prevention)", f"₹{base_cost * risk_multiplier * 0.6:,.0f}")
        with col3:
            st.metric("Annual Savings", f"₹{base_cost * risk_multiplier * 0.4:,.0f}")
        
        # Simple chart
        years = list(range(1, 11))
        without_costs = [base_cost * risk_multiplier * (1.05 ** (y-1)) for y in years]
        with_costs = [base_cost * risk_multiplier * 0.6 * (1.03 ** (y-1)) for y in years]
        
        df = pd.DataFrame({
            'Year': years,
            'Without Prevention': without_costs,
            'With Prevention': with_costs
        })
        
        fig = px.line(df, x='Year', y=['Without Prevention', 'With Prevention'],
                     title="10-Year Cost Projection",
                     markers=True)
        st.plotly_chart(fig, use_container_width=True)

def show_action_plan():
    """Simplified Action Plan"""
    st.markdown('<div class="main-title">🎯 Personalized Action Plan</div>', unsafe_allow_html=True)
    
    if not st.session_state.patient_data:
        st.warning("Please analyze your health data first.")
        if st.button("📤 Go to Health Analysis", use_container_width=True, key="plan_goto_analyzer_main"):
            st.session_state.current_page = "analyzer"
            st.rerun()
        return
    
    st.markdown('<div class="section-title">📋 Recommended Actions</div>', unsafe_allow_html=True)
    
    actions = []
    
    if st.session_state.risk_scores:
        for disease, data in st.session_state.risk_scores.items():
            if disease != 'timestamp' and isinstance(data, dict):
                level = data.get('level', 'Low')
                if level in ['High', 'Critical']:
                    if disease == 'diabetes':
                        actions.append("Monitor blood glucose levels daily")
                        actions.append("Consult endocrinologist within 2 weeks")
                        actions.append("Follow low-GI diet plan")
                    elif disease == 'heart_disease':
                        actions.append("Get ECG and stress test")
                        actions.append("Consult cardiologist within 1 week")
                        actions.append("Start heart-healthy diet")
                    elif disease == 'hypertension':
                        actions.append("Monitor BP twice daily")
                        actions.append("Reduce sodium intake")
                        actions.append("Practice stress management")
    
    # General lifestyle recommendations
    if st.session_state.patient_data.get('bmi', 24) > 25:
        actions.append("Aim to lose 5-10% of body weight")
        actions.append("30 minutes moderate exercise daily")
    
    if st.session_state.patient_data.get('smoking', False):
        actions.append("Start smoking cessation program")
    
    if not actions:
        actions = [
            "Maintain current healthy lifestyle",
            "Continue regular health checkups",
            "Stay physically active",
            "Eat balanced diet",
            "Get adequate sleep",
            "Manage stress effectively"
        ]
    
    # Display actions
    for i, action in enumerate(actions[:6], 1):
        st.markdown(f'''
        <div class="glass-card">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div style="font-size: 1.5rem;">✅</div>
                <div>
                    <h4 style="margin: 0;">Action {i}</h4>
                    <p style="margin: 0.5rem 0; color: #cbd5e1;">{action}</p>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

def show_full_report():
    """Simplified Full Report"""
    st.markdown('<div class="main-title">📊 Complete Health Report</div>', unsafe_allow_html=True)
    
    if not st.session_state.patient_data:
        st.warning("Please analyze your health data first.")
        if st.button("📤 Go to Health Analysis", use_container_width=True, key="report_goto_analyzer_main"):
            st.session_state.current_page = "analyzer"
            st.rerun()
        return
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="section-title">👤 Patient Summary</div>', unsafe_allow_html=True)
        patient = st.session_state.patient_data
        
        # Display all patient data
        info_html = ""
        for key, value in patient.items():
            if key != 'timestamp':
                formatted_key = key.replace('_', ' ').title()
                info_html += f"<div style='margin: 0.5rem 0;'><strong>{formatted_key}:</strong> {value}</div>"
        
        st.markdown(f'''
        <div class="glass-card">
            <h3 style="color: #60a5fa; margin-bottom: 1rem;">{patient.get('name', 'Patient')}</h3>
            {info_html}
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="section-title">⚠️ Risk Summary</div>', unsafe_allow_html=True)
        if st.session_state.risk_scores:
            risk_data = []
            for disease, data in st.session_state.risk_scores.items():
                if disease != 'timestamp' and isinstance(data, dict):
                    risk_data.append({
                        'Condition': disease.replace('_', ' ').title(),
                        'Risk Level': data.get('level', 'Low'),
                        'Probability': f"{data.get('percentage', 0):.1f}%"
                    })
            
            if risk_data:
                df = pd.DataFrame(risk_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No risk analysis available")
    
    # Health Score
    health_score = EnhancedRiskCalculator.calculate_health_score(st.session_state.patient_data)
    st.markdown('<div class="section-title">🏆 Health Score</div>', unsafe_allow_html=True)
    st.markdown(f'''
    <div class="glass-card">
        <div style="text-align: center;">
            <div class="metric-label">Overall Health Score</div>
            <div class="metric-value">{health_score:.0f}/100</div>
            <div class="progress-bar" style="margin: 1rem auto; max-width: 400px;">
                <div class="progress-fill" style="width: {health_score}%"></div>
            </div>
            <div style="color: #94a3b8; font-size: 1rem;">
                {EnhancedRiskCalculator.get_score_feedback(health_score)}
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Download button
    if st.button("📥 Generate PDF Report", type="primary", use_container_width=True, key="download_report_main"):
        st.success("Report generation started! This would generate a PDF in a real implementation.")

# ============================================
# ENHANCED SIDEBAR
# ============================================

def create_enhanced_sidebar():
    """Create enhanced sidebar navigation"""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2.5rem;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🧬</div>
            <h2 style="color: #60a5fa; margin-bottom: 0.25rem; font-weight: 800;">MediPrecog</h2>
            <p style="color: #94a3b8; font-size: 0.9rem;">Health Intelligence Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation Menu
        pages = {
            "dashboard": "🏠 Dashboard",
            "analyzer": "🔬 Analyzer",
            "cost": "💰 Cost AI",
            "plan": "🎯 Action AI",
            "report": "📊 Insights"
        }
        
        # Create navigation buttons - always render all buttons
        for page_id, page_name in pages.items():
            is_selected = st.session_state.current_page == page_id
            if st.button(
                page_name,
                use_container_width=True,
                type="primary" if is_selected else "secondary",
                key=f"nav_{page_id}_main"
            ):
                if st.session_state.current_page != page_id:
                    st.session_state.current_page = page_id
                    st.rerun()
        
        st.markdown("---")
        
        # Patient Status
        if st.session_state.patient_data:
            st.markdown(f'''
            <div class="glass-card" style="padding: 1rem;">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="font-size: 1.5rem;">👤</div>
                    <div>
                        <div style="font-weight: 600; color: #e2e8f0;">{st.session_state.patient_data.get('name', 'User')}</div>
                        <div style="font-size: 0.8rem; color: #94a3b8;">Profile Active</div>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
            <div class="glass-card" style="padding: 1rem;">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="font-size: 1.5rem;">👤</div>
                    <div>
                        <div style="font-weight: 600; color: #e2e8f0;">No Profile</div>
                        <div style="font-size: 0.8rem; color: #94a3b8;">Start analysis to create profile</div>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        # Quick Actions
        st.markdown("### ⚡ Quick Access")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh", use_container_width=True, key="sidebar_refresh_main"):
                st.rerun()
        with col2:
            if st.button("📥 Export", use_container_width=True, key="sidebar_export_main"):
                st.success("Export initiated!")
        
        # Demo Data
        if st.button("🎮 Load Demo Data", use_container_width=True, type="secondary", key="sidebar_demo_main"):
            demo_data = {
                'name': 'Alex Johnson',
                'age': 42,
                'gender': 'Male',
                'bmi': 27.8,
                'glucose': 128,
                'bp_systolic': 138,
                'bp_diastolic': 88,
                'cholesterol': 245,
                'smoking': True,
                'alcohol': False,
                'exercise': '1-2 hours',
                'sleep': '6-7 hours',
                'family_diabetes': True,
                'family_heart': True,
                'family_hypertension': False,
                'family_cancer': False
            }
            
            calculator = EnhancedRiskCalculator()
            st.session_state.patient_data = demo_data
            st.session_state.risk_scores = calculator.calculate_risks(demo_data)
            st.session_state.timeline_data = calculator.generate_timeline(st.session_state.risk_scores)
            
            st.success("Demo data loaded!")
            st.session_state.current_page = "dashboard"
            st.rerun()
        
        st.markdown("---")
        
        # Status
        if st.session_state.risk_scores:
            risks = 0
            for d in st.session_state.risk_scores.values():
                if isinstance(d, dict) and d.get('level') in ['High', 'Critical']:
                    risks += 1
            
            color = '#ef4444' if risks > 0 else '#10b981'
            st.markdown(f'''
            <div style="text-align: center;">
                <div style="font-size: 0.8rem; color: #94a3b8;">Current Status</div>
                <div style="font-size: 1.2rem; font-weight: 700; color: {color}">
                    {risks} Critical Risk{'' if risks == 1 else 's'}
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Footer
        st.markdown("""
        <div style="text-align: center; color: #64748b; font-size: 0.8rem; padding: 1rem;">
            <div>⚕️ For informational purposes only</div>
            <div>Consult healthcare professionals</div>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# MAIN APP ENTRY
# ============================================

def main():
    """Main application entry point"""
    
    # Create sidebar
    create_enhanced_sidebar()
    
    # Page routing
    current_page = st.session_state.current_page
    
    if current_page == "dashboard":
        show_enhanced_dashboard()
    elif current_page == "analyzer":
        show_enhanced_analyzer()
    elif current_page == "cost":
        show_cost_calculator()
    elif current_page == "plan":
        show_action_plan()
    elif current_page == "report":
        show_full_report()

# ============================================
# RUN APPLICATION
# ============================================
if __name__ == "__main__":
    main()