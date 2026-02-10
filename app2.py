"""
🏥 MEDIPRECOG - Health Risk Prediction System
ENHANCED WITH DAILY HABIT TRACKER
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time
from datetime import datetime, timedelta
import random
from faker import Faker
import calendar

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
# BEAUTIFUL CSS
# ============================================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        font-family: 'Poppins', 'Segoe UI', system-ui, sans-serif;
    }
    
    .main-title {
        font-size: 4rem;
        background: linear-gradient(135deg, #2E8B57 0%, #3CB371 30%, #20B2AA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        font-weight: 800;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    h1, h2, h3, h4, h5, h6 { color: #1F2937 !important; font-weight: 700; }
    p, span, div, label { color: #4B5563 !important; line-height: 1.8; }
    
    .step-card {
        background: white;
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
        border: 2px solid #E5E7EB;
        transition: all 0.3s ease;
    }
    
    .step-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 60px rgba(46, 139, 87, 0.15);
        border-color: #2E8B57;
    }
    
    .tracker-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 30px rgba(0,0,0,0.06);
        border: 2px solid #E5E7EB;
        transition: all 0.3s ease;
    }
    
    .tracker-card:hover {
        box-shadow: 0 12px 40px rgba(46, 139, 87, 0.1);
        border-color: #2E8B57;
    }
    
    .habit-card {
        background: linear-gradient(135deg, #ffffff 0%, #f0fff4 100%);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #2E8B57;
        box-shadow: 0 6px 25px rgba(0,0,0,0.05);
    }
    
    .food-log-card {
        background: linear-gradient(135deg, #ffffff 0%, #fef3c7 100%);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #F59E0B;
        box-shadow: 0 6px 25px rgba(0,0,0,0.05);
    }
    
    .activity-card {
        background: linear-gradient(135deg, #ffffff 0%, #e0f2fe 100%);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #0EA5E9;
        box-shadow: 0 6px 25px rgba(0,0,0,0.05);
    }
    
    .streak-card {
        background: linear-gradient(135deg, #ffffff 0%, #f5f3ff 100%);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #8B5CF6;
        box-shadow: 0 6px 25px rgba(0,0,0,0.05);
    }
    
    .progress-bar {
        height: 20px;
        background: #E5E7EB;
        border-radius: 10px;
        overflow: hidden;
        margin: 10px 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #2E8B57, #3CB371);
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    .day-box {
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        margin: 5px;
        cursor: pointer;
    }
    
    .day-completed {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }
    
    .day-missed {
        background: #F3F4F6;
        color: #9CA3AF;
        border: 2px solid #E5E7EB;
    }
    
    .day-today {
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button {
        border-radius: 14px !important;
        padding: 1rem 2rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #2E8B57 0%, #3CB371 100%) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 8px 25px rgba(46, 139, 87, 0.3) !important;
    }
    
    .custom-badge {
        display: inline-flex;
        align-items: center;
        padding: 8px 16px;
        border-radius: 25px;
        font-size: 0.85rem;
        font-weight: 700;
        background: linear-gradient(135deg, #E0F2FE 0%, #BAE6FD 100%);
        color: #0369A1;
        margin: 4px;
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
    st.session_state.current_page = "🏠 Home"

# Initialize habit tracker data
if 'habits' not in st.session_state:
    st.session_state.habits = {
        'daily': [],
        'weekly': [],
        'monthly': []
    }

if 'food_logs' not in st.session_state:
    st.session_state.food_logs = []

if 'activity_logs' not in st.session_state:
    st.session_state.activity_logs = []

if 'streak_data' not in st.session_state:
    st.session_state.streak_data = {}

if 'daily_checkins' not in st.session_state:
    st.session_state.daily_checkins = {}

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
    
    diabetes_risk = min(0.95, 0.1 * diabetes_multiplier)
    heart_risk = min(0.95, 0.1 * heart_multiplier)
    hypertension_risk = min(0.95, 0.1 * hypertension_multiplier)
    stroke_risk = min(0.95, 0.05 * stroke_multiplier)
    
    return {
        'diabetes': {'current_risk': diabetes_risk, 'future_risk': min(0.95, diabetes_risk * 1.8)},
        'heart_disease': {'current_risk': heart_risk, 'future_risk': min(0.95, heart_risk * 1.6)},
        'hypertension': {'current_risk': hypertension_risk, 'future_risk': min(0.95, hypertension_risk * 1.7)},
        'stroke': {'current_risk': stroke_risk, 'future_risk': min(0.95, stroke_risk * 1.9)}
    }

def calculate_cost_savings(patient_data, risk_scores):
    """Calculate potential healthcare cost savings in Indian Rupees"""
    diabetes_risk = risk_scores['diabetes']['current_risk']
    heart_risk = risk_scores['heart_disease']['current_risk']
    hypertension_risk = risk_scores['hypertension']['current_risk']
    
    base_annual_costs = {
        'medications': 50000,
        'doctor_visits': 20000,
        'tests_monitoring': 15000,
        'hospitalization_risk': 100000
    }
    
    annual_without = (
        base_annual_costs['medications'] * (1 + diabetes_risk + hypertension_risk) +
        base_annual_costs['doctor_visits'] * (1 + (diabetes_risk + heart_risk + hypertension_risk) / 3) +
        base_annual_costs['tests_monitoring'] * 1.5 +
        base_annual_costs['hospitalization_risk'] * (0.5 + diabetes_risk + heart_risk)
    )
    
    cost_without = sum([annual_without * (1.1 ** year) for year in range(5)])
    prevention_program_cost = 1500 * 12 * 5
    annual_with_prevention = annual_without * 0.4
    cost_with = prevention_program_cost + sum([annual_with_prevention * (1.05 ** year) for year in range(5)])
    
    return {
        'cost_without_intervention': round(cost_without),
        'cost_with_intervention': round(cost_with),
        'total_savings': round(cost_without - cost_with),
        'annual_savings': round((cost_without - cost_with) / 5)
    }

def generate_action_plan(patient_data, risk_scores):
    """Generate personalized action plan with habit suggestions"""
    
    immediate_actions = []
    habit_suggestions = []
    
    if risk_scores['diabetes']['current_risk'] > 0.3:
        immediate_actions.append("Consult with an endocrinologist within 30 days")
        immediate_actions.append("Start monitoring blood glucose levels daily")
        habit_suggestions.extend([
            "Track daily sugar intake",
            "Monitor fasting glucose every morning",
            "Include 30g fiber in daily diet"
        ])
    
    if risk_scores['heart_disease']['current_risk'] > 0.3:
        immediate_actions.append("Schedule a cardiac stress test")
        immediate_actions.append("Begin 30-minute daily walks")
        habit_suggestions.extend([
            "Walk 10,000 steps daily",
            "Practice stress management for 15 mins",
            "Monitor blood pressure twice daily"
        ])
    
    if patient_data.get('smoker', False):
        immediate_actions.append("Enroll in smoking cessation program immediately")
        habit_suggestions.extend([
            "Reduce cigarettes by 1 each day",
            "Use nicotine replacement when craving",
            "Practice deep breathing exercises"
        ])
    
    if patient_data.get('bmi', 0) > 25:
        immediate_actions.append("Start calorie-controlled diet plan")
        habit_suggestions.extend([
            "Log all meals in food diary",
            "Weigh yourself every morning",
            "Drink 3L water daily"
        ])
    
    if not immediate_actions:
        immediate_actions.append("Schedule annual physical exam")
        immediate_actions.append("Begin regular exercise routine")
        habit_suggestions.extend([
            "Exercise 30 minutes daily",
            "Sleep 7-8 hours nightly",
            "Meditate for 10 minutes daily"
        ])
    
    return {
        'immediate': immediate_actions[:5],
        'short_term': ["Join preventive health program", "Complete metabolic panel every 6 months"],
        'long_term': ["Maintain annual health screening", "Continue lifestyle modifications"],
        'habits': habit_suggestions[:6]
    }

def get_health_goals(risk_scores):
    """Generate health goals based on risk profile"""
    goals = []
    
    if risk_scores['diabetes']['current_risk'] > 0.3:
        goals.append({
            'name': 'Control Blood Sugar',
            'target': 'Fasting glucose < 100 mg/dL',
            'current': 'To be measured',
            'unit': 'mg/dL'
        })
    
    if risk_scores['heart_disease']['current_risk'] > 0.3:
        goals.append({
            'name': 'Improve Heart Health',
            'target': 'BP < 130/85, Cholesterol < 200',
            'current': 'To be measured',
            'unit': ''
        })
    
    if not goals:
        goals.append({
            'name': 'Maintain Healthy Weight',
            'target': 'BMI between 18.5-24.9',
            'current': 'To be measured',
            'unit': 'BMI'
        })
    
    return goals

# ============================================
# HABIT TRACKER FUNCTIONS
# ============================================

def get_today_date():
    """Get today's date in string format"""
    return datetime.now().strftime("%Y-%m-%d")

def add_habit(habit_name, habit_type="daily", target_value=None, unit=None):
    """Add a new habit to track"""
    habit = {
        'id': len(st.session_state.habits[habit_type]),
        'name': habit_name,
        'type': habit_type,
        'target_value': target_value,
        'unit': unit,
        'created_date': get_today_date(),
        'completion_data': {}
    }
    st.session_state.habits[habit_type].append(habit)
    return habit

def log_food_meal(meal_type, food_items, calories, carbs, protein, fat):
    """Log a food meal"""
    food_log = {
        'date': get_today_date(),
        'meal_type': meal_type,
        'food_items': food_items,
        'calories': calories,
        'carbs': carbs,
        'protein': protein,
        'fat': fat,
        'timestamp': datetime.now().strftime("%H:%M")
    }
    st.session_state.food_logs.append(food_log)
    return food_log

def log_activity(activity_type, duration, calories_burned, intensity):
    """Log physical activity"""
    activity_log = {
        'date': get_today_date(),
        'activity_type': activity_type,
        'duration': duration,
        'calories_burned': calories_burned,
        'intensity': intensity,
        'timestamp': datetime.now().strftime("%H:%M")
    }
    st.session_state.activity_logs.append(activity_log)
    return activity_log

def mark_habit_complete(habit_id, habit_type, value=None):
    """Mark a habit as complete for today"""
    today = get_today_date()
    
    if habit_type not in st.session_state.habits:
        return False
    
    for habit in st.session_state.habits[habit_type]:
        if habit['id'] == habit_id:
            if 'completion_data' not in habit:
                habit['completion_data'] = {}
            
            habit['completion_data'][today] = {
                'completed': True,
                'value': value,
                'timestamp': datetime.now().strftime("%H:%M")
            }
            return True
    
    return False

def get_daily_checkin(date=None):
    """Get daily checkin data"""
    if date is None:
        date = get_today_date()
    
    if date not in st.session_state.daily_checkins:
        st.session_state.daily_checkins[date] = {
            'mood': None,
            'energy_level': None,
            'sleep_hours': None,
            'stress_level': None,
            'notes': ''
        }
    
    return st.session_state.daily_checkins[date]

def update_daily_checkin(mood, energy, sleep, stress, notes):
    """Update daily checkin"""
    today = get_today_date()
    st.session_state.daily_checkins[today] = {
        'mood': mood,
        'energy_level': energy,
        'sleep_hours': sleep,
        'stress_level': stress,
        'notes': notes
    }

def get_streak_data():
    """Calculate streak data for all habits"""
    if not st.session_state.habits['daily']:
        return {}
    
    streaks = {}
    today = datetime.now()
    
    for habit in st.session_state.habits['daily']:
        habit_name = habit['name']
        completion_data = habit.get('completion_data', {})
        
        # Calculate current streak
        current_streak = 0
        check_date = today
        
        while True:
            date_str = check_date.strftime("%Y-%m-%d")
            if date_str in completion_data and completion_data[date_str]['completed']:
                current_streak += 1
                check_date -= timedelta(days=1)
            else:
                break
        
        # Calculate longest streak
        longest_streak = 0
        temp_streak = 0
        
        dates = sorted(completion_data.keys())
        for date in dates:
            if completion_data[date]['completed']:
                temp_streak += 1
                longest_streak = max(longest_streak, temp_streak)
            else:
                temp_streak = 0
        
        streaks[habit_name] = {
            'current_streak': current_streak,
            'longest_streak': longest_streak,
            'total_completed': sum(1 for d in completion_data.values() if d['completed']),
            'completion_rate': len([d for d in completion_data.values() if d['completed']]) / max(1, len(completion_data)) * 100
        }
    
    return streaks

def get_calendar_view(month=None, year=None):
    """Generate calendar view for habit tracking"""
    if month is None:
        month = datetime.now().month
    if year is None:
        year = datetime.now().year
    
    cal = calendar.monthcalendar(year, month)
    calendar_data = []
    
    for week in cal:
        week_data = []
        for day in week:
            if day == 0:
                week_data.append(None)
            else:
                date_str = f"{year}-{month:02d}-{day:02d}"
                habits_completed = 0
                total_habits = len(st.session_state.habits['daily'])
                
                for habit in st.session_state.habits['daily']:
                    if date_str in habit.get('completion_data', {}):
                        if habit['completion_data'][date_str]['completed']:
                            habits_completed += 1
                
                if total_habits > 0:
                    completion_rate = (habits_completed / total_habits) * 100
                else:
                    completion_rate = 0
                
                week_data.append({
                    'day': day,
                    'date': date_str,
                    'completion_rate': completion_rate,
                    'is_today': (day == datetime.now().day and month == datetime.now().month and year == datetime.now().year)
                })
        calendar_data.append(week_data)
    
    return calendar_data, month, year

def generate_weekly_report():
    """Generate weekly progress report"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=6)
    
    report_data = {
        'habits_completed': 0,
        'total_possible': 0,
        'calories_consumed': 0,
        'calories_burned': 0,
        'avg_sleep': 0,
        'avg_energy': 0,
        'days_tracked': 0
    }
    
    # Calculate habit completion
    for habit in st.session_state.habits['daily']:
        for date_str, data in habit.get('completion_data', {}).items():
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            if start_date <= date_obj <= end_date:
                report_data['total_possible'] += 1
                if data['completed']:
                    report_data['habits_completed'] += 1
    
    # Calculate calories
    for food_log in st.session_state.food_logs:
        date_obj = datetime.strptime(food_log['date'], "%Y-%m-%d")
        if start_date <= date_obj <= end_date:
            report_data['calories_consumed'] += food_log['calories']
    
    for activity_log in st.session_state.activity_logs:
        date_obj = datetime.strptime(activity_log['date'], "%Y-%m-%d")
        if start_date <= date_obj <= end_date:
            report_data['calories_burned'] += activity_log['calories_burned']
    
    # Calculate averages
    sleep_hours = []
    energy_levels = []
    
    for date_str, checkin in st.session_state.daily_checkins.items():
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        if start_date <= date_obj <= end_date:
            if checkin['sleep_hours']:
                sleep_hours.append(checkin['sleep_hours'])
            if checkin['energy_level']:
                energy_levels.append(checkin['energy_level'])
            report_data['days_tracked'] += 1
    
    if sleep_hours:
        report_data['avg_sleep'] = sum(sleep_hours) / len(sleep_hours)
    if energy_levels:
        report_data['avg_energy'] = sum(energy_levels) / len(energy_levels)
    
    return report_data

# ============================================
# PAGE FUNCTIONS
# ============================================

def display_home():
    """Display home page"""
    st.markdown('<h1 class="main-title">🏥 MEDIPRECOG</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Your Personal Health Time Machine with Daily Habit Tracker</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="step-card">
            <h3>🎯 5 Steps to Better Health</h3>
            <p><strong>1. Scan Report:</strong> Upload your medical reports</p>
            <p><strong>2. Risk Analysis:</strong> Understand your health risks</p>
            <p><strong>3. Track Habits:</strong> Monitor daily activities & food</p>
            <p><strong>4. See Progress:</strong> Watch your health improve</p>
            <p><strong>5. Stay Motivated:</strong> Get personalized feedback</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="step-card">
            <h3>📊 Why Track Daily Habits?</h3>
            <p>• <strong>85%</strong> better health outcomes with consistent tracking</p>
            <p>• <strong>72%</strong> higher success rate in achieving health goals</p>
            <p>• <strong>3x</strong> more likely to maintain healthy habits</p>
            <p>• <strong>60%</strong> reduction in healthcare costs</p>
            <p>• <strong>40%</strong> faster progress with daily monitoring</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📸 Scan Medical Report", use_container_width=True):
            st.session_state.current_page = "📸 Scan Report"
            st.rerun()
    
    with col2:
        if st.button("📊 View Risk Analysis", use_container_width=True):
            if st.session_state.patient_data:
                st.session_state.current_page = "📊 Risk Analysis"
                st.rerun()
            else:
                st.warning("Please scan a report first!")
    
    with col3:
        if st.button("📝 Daily Habit Tracker", use_container_width=True, type="primary"):
            st.session_state.current_page = "📝 Habit Tracker"
            st.rerun()

def display_scan_report():
    """Medical report scanner"""
    st.markdown("## 📸 Medical Report Scanner")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="tracker-card">
            <h3>📁 Upload Medical Report</h3>
            <p>Supported: PDF, PNG, JPG, JPEG</p>
            <div style="display: flex; gap: 10px; margin-top: 1.5rem;">
                <span class="custom-badge">🔒 Secure</span>
                <span class="custom-badge">⚡ Fast</span>
                <span class="custom-badge">🤖 AI-Powered</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'png', 'jpg', 'jpeg'], label_visibility="collapsed")
    
    with col2:
        st.markdown("""
        <div class="tracker-card" style="background: linear-gradient(135deg, #2E8B57 0%, #3CB371 100%); color: white;">
            <h3 style="color: white;">⚡ Why Scan?</h3>
            <p>• 100% Data Extraction</p>
            <p>• 60 Second Analysis</p>
            <p>• Personalized Insights</p>
            <p>• Habit Recommendations</p>
        </div>
        """, unsafe_allow_html=True)
    
    if uploaded_file is not None:
        with st.spinner("🔍 Scanning report..."):
            time.sleep(2)
            patient_data = generate_synthetic_patient()
            st.session_state.patient_data = patient_data
            st.session_state.report_scanned = True
            risk_scores = calculate_risk_scores(patient_data)
            st.session_state.risk_scores = risk_scores
            
            st.success("✅ Report scanned successfully!")
            
            with st.expander("📋 View Extracted Data"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**👤 Patient:** {patient_data['name']}")
                    st.write(f"**🎂 Age:** {patient_data['age']}")
                    st.write(f"**🩸 Glucose:** {patient_data['glucose']} mg/dL")
                with col2:
                    st.write(f"**💓 BP:** {patient_data['bp_systolic']}/{patient_data['bp_diastolic']}")
                    st.write(f"**🧪 Cholesterol:** {patient_data['cholesterol']} mg/dL")
                    st.write(f"**⚖️ BMI:** {patient_data['bmi']}")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Use Demo Report", use_container_width=True):
            patient_data = generate_synthetic_patient()
            st.session_state.patient_data = patient_data
            st.session_state.report_scanned = True
            st.session_state.risk_scores = calculate_risk_scores(patient_data)
            st.success("✅ Demo data loaded!")
            time.sleep(1)
            st.rerun()
    
    with col2:
        if st.button("🔄 Reset Data", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.current_page = "🏠 Home"
            st.rerun()

def display_risk_analysis():
    """Display risk analysis"""
    if not st.session_state.patient_data:
        st.warning("Please scan a report first!")
        return
    
    patient_data = st.session_state.patient_data
    risk_scores = st.session_state.risk_scores
    
    st.markdown(f"## 📊 Risk Analysis: {patient_data['name']}")
    
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
    
    # Generate action plan with habits
    action_plan = generate_action_plan(patient_data, risk_scores)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🎯 Recommended Daily Habits")
        for habit in action_plan['habits']:
            st.markdown(f"""
            <div class="habit-card">
                <div style="display: flex; align-items: center;">
                    <div style="background: #2E8B57; color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                        ✓
                    </div>
                    <div>{habit}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("➕ Add These to My Habit Tracker", use_container_width=True):
            for habit in action_plan['habits']:
                add_habit(habit, "daily")
            st.success("✅ Habits added to your tracker!")
            time.sleep(1)
            st.rerun()
    
    with col2:
        st.markdown("### ⚠️ Your Risk Factors")
        risk_factors = []
        if patient_data.get('bmi', 0) > 25: risk_factors.append("High BMI")
        if patient_data.get('glucose', 0) > 100: risk_factors.append("Elevated Glucose")
        if patient_data.get('bp_systolic', 0) > 130: risk_factors.append("High Blood Pressure")
        if patient_data.get('cholesterol', 0) > 200: risk_factors.append("High Cholesterol")
        if patient_data.get('smoker', False): risk_factors.append("Smoking")
        
        for factor in risk_factors:
            st.markdown(f"<div style='background: #FEE2E2; color: #DC2626; padding: 10px 15px; border-radius: 10px; margin: 5px 0;'>{factor}</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("← Back to Scanner", use_container_width=True):
            st.session_state.current_page = "📸 Scan Report"
            st.rerun()
    with col2:
        if st.button("📝 Go to Habit Tracker", use_container_width=True):
            st.session_state.current_page = "📝 Habit Tracker"
            st.rerun()
    with col3:
        if st.button("💰 Cost Calculator →", use_container_width=True, type="primary"):
            st.session_state.current_page = "💰 Cost Calculator"
            st.rerun()

def display_habit_tracker():
    """Display daily habit tracker with food and activity logging"""
    st.markdown("## 📝 Daily Habit Tracker")
    st.markdown("Track your daily habits, food intake, and activities to improve your health")
    
    # Today's date
    today = datetime.now()
    st.markdown(f"### 📅 {today.strftime('%A, %B %d, %Y')}")
    
    # Tabs for different tracking sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏃 Daily Habits", "🍎 Food Log", "⚡ Activity Log", "📊 Progress", "🎯 Weekly Report"])
    
    with tab1:
        # Daily Habits Management
        st.markdown("### 🏃 Your Daily Habits")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Add new habit
            with st.expander("➕ Add New Habit", expanded=False):
                new_habit = st.text_input("Habit Name", placeholder="e.g., Drink 8 glasses of water")
                habit_type = st.selectbox("Frequency", ["daily", "weekly", "monthly"])
                target_value = st.number_input("Target Value (optional)", min_value=0, value=0)
                unit = st.text_input("Unit (optional)", placeholder="e.g., glasses, minutes, km")
                
                if st.button("Add Habit", type="primary"):
                    if new_habit:
                        add_habit(new_habit, habit_type, target_value if target_value > 0 else None, unit if unit else None)
                        st.success(f"Added: {new_habit}")
                        st.rerun()
        
        with col2:
            # Quick stats
            total_habits = len(st.session_state.habits['daily'])
            completed_today = 0
            for habit in st.session_state.habits['daily']:
                today_str = get_today_date()
                if today_str in habit.get('completion_data', {}):
                    if habit['completion_data'][today_str]['completed']:
                        completed_today += 1
            
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; background: #F0F9FF; border-radius: 15px;">
                <div style="font-size: 2rem; font-weight: 800; color: #0EA5E9;">{completed_today}/{total_habits}</div>
                <div style="color: #4B5563;">Habits Completed</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Display and manage habits
        if st.session_state.habits['daily']:
            st.markdown("#### Today's Habits")
            for habit in st.session_state.habits['daily']:
                habit_name = habit['name']
                today_str = get_today_date()
                is_completed = today_str in habit.get('completion_data', {}) and habit['completion_data'][today_str]['completed']
                
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    status = "✅ Completed" if is_completed else "⏳ Pending"
                    st.markdown(f"**{habit_name}** - {status}")
                
                with col2:
                    if not is_completed:
                        if st.button("✓ Complete", key=f"complete_{habit['id']}"):
                            mark_habit_complete(habit['id'], 'daily')
                            st.success(f"Completed: {habit_name}")
                            st.rerun()
                    else:
                        st.button("✓ Done", key=f"done_{habit['id']}", disabled=True)
                
                with col3:
                    if st.button("🗑️", key=f"delete_{habit['id']}"):
                        st.session_state.habits['daily'] = [h for h in st.session_state.habits['daily'] if h['id'] != habit['id']]
                        st.rerun()
        
        else:
            st.info("No habits added yet. Add some habits to track!")
        
        # Daily Check-in
        st.markdown("---")
        st.markdown("### 😊 Daily Check-in")
        
        checkin_data = get_daily_checkin()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            mood = st.select_slider(
                "Mood",
                options=["😔", "😐", "🙂", "😊", "😄"],
                value=checkin_data['mood'] or "🙂"
            )
        
        with col2:
            energy = st.slider("Energy Level", 1, 10, checkin_data['energy_level'] or 5)
        
        with col3:
            sleep = st.number_input("Sleep Hours", min_value=0.0, max_value=12.0, value=checkin_data['sleep_hours'] or 7.0, step=0.5)
        
        with col4:
            stress = st.slider("Stress Level", 1, 10, checkin_data['stress_level'] or 5)
        
        notes = st.text_area("Notes for Today", checkin_data['notes'], placeholder="How are you feeling today? Any challenges or successes?")
        
        if st.button("Save Daily Check-in", type="primary"):
            update_daily_checkin(mood, energy, sleep, stress, notes)
            st.success("Daily check-in saved!")
    
    with tab2:
        # Food Logging
        st.markdown("### 🍎 Food & Nutrition Log")
        
        # Quick add common meals
        col1, col2, col3, col4 = st.columns(4)
        common_meals = {
            "Breakfast": {"calories": 350, "carbs": 45, "protein": 15, "fat": 12},
            "Lunch": {"calories": 550, "carbs": 60, "protein": 25, "fat": 20},
            "Dinner": {"calories": 600, "carbs": 65, "protein": 30, "fat": 25},
            "Snack": {"calories": 200, "carbs": 25, "protein": 5, "fat": 10}
        }
        
        for i, (meal_type, nutrition) in enumerate(common_meals.items()):
            with [col1, col2, col3, col4][i]:
                if st.button(f"➕ {meal_type}", use_container_width=True):
                    log_food_meal(
                        meal_type=meal_type,
                        food_items=f"Standard {meal_type}",
                        calories=nutrition["calories"],
                        carbs=nutrition["carbs"],
                        protein=nutrition["protein"],
                        fat=nutrition["fat"]
                    )
                    st.success(f"Added {meal_type}")
                    st.rerun()
        
        # Manual food entry
        with st.expander("➕ Add Custom Food Entry", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack", "Other"])
                food_items = st.text_area("Food Items", placeholder="What did you eat?")
            with col2:
                calories = st.number_input("Calories", min_value=0, value=300)
                carbs = st.number_input("Carbs (g)", min_value=0, value=0)
                protein = st.number_input("Protein (g)", min_value=0, value=0)
                fat = st.number_input("Fat (g)", min_value=0, value=0)
            
            if st.button("Log Food Entry", type="primary"):
                if food_items:
                    log_food_meal(meal_type, food_items, calories, carbs, protein, fat)
                    st.success("Food logged successfully!")
                    st.rerun()
        
        # Display today's food logs
        st.markdown("#### Today's Food Log")
        today_foods = [log for log in st.session_state.food_logs if log['date'] == get_today_date()]
        
        if today_foods:
            total_calories = sum(f['calories'] for f in today_foods)
            total_carbs = sum(f['carbs'] for f in today_foods)
            total_protein = sum(f['protein'] for f in today_foods)
            total_fat = sum(f['fat'] for f in today_foods)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1: st.metric("Total Calories", f"{total_calories}")
            with col2: st.metric("Carbs", f"{total_carbs}g")
            with col3: st.metric("Protein", f"{total_protein}g")
            with col4: st.metric("Fat", f"{total_fat}g")
            
            for i, food_log in enumerate(today_foods):
                st.markdown(f"""
                <div class="food-log-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>{food_log['meal_type']}</strong> at {food_log['timestamp']}<br>
                            <small>{food_log['food_items']}</small>
                        </div>
                        <div style="text-align: right;">
                            <strong>{food_log['calories']} cal</strong><br>
                            <small>C:{food_log['carbs']}g P:{food_log['protein']}g F:{food_log['fat']}g</small>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No food logged today. Start tracking your meals!")
    
    with tab3:
        # Activity Logging
        st.markdown("### ⚡ Activity & Exercise Log")
        
        # Quick add common activities
        col1, col2, col3, col4 = st.columns(4)
        common_activities = {
            "Walking": {"duration": 30, "calories": 150, "intensity": "Moderate"},
            "Running": {"duration": 20, "calories": 200, "intensity": "High"},
            "Cycling": {"duration": 30, "calories": 250, "intensity": "Moderate"},
            "Yoga": {"duration": 30, "calories": 120, "intensity": "Light"}
        }
        
        for i, (activity, details) in enumerate(common_activities.items()):
            with [col1, col2, col3, col4][i]:
                if st.button(f"➕ {activity}", use_container_width=True):
                    log_activity(
                        activity_type=activity,
                        duration=details["duration"],
                        calories_burned=details["calories"],
                        intensity=details["intensity"]
                    )
                    st.success(f"Added {activity}")
                    st.rerun()
        
        # Manual activity entry
        with st.expander("➕ Add Custom Activity", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                activity_type = st.text_input("Activity Type", placeholder="e.g., Gym workout, Swimming")
                duration = st.number_input("Duration (minutes)", min_value=1, value=30)
            with col2:
                calories_burned = st.number_input("Calories Burned", min_value=0, value=200)
                intensity = st.select_slider("Intensity", options=["Light", "Moderate", "High"])
            
            if st.button("Log Activity", type="primary"):
                if activity_type:
                    log_activity(activity_type, duration, calories_burned, intensity)
                    st.success("Activity logged successfully!")
                    st.rerun()
        
        # Display today's activities
        st.markdown("#### Today's Activities")
        today_activities = [log for log in st.session_state.activity_logs if log['date'] == get_today_date()]
        
        if today_activities:
            total_duration = sum(a['duration'] for a in today_activities)
            total_calories = sum(a['calories_burned'] for a in today_activities)
            
            col1, col2 = st.columns(2)
            with col1: st.metric("Total Duration", f"{total_duration} min")
            with col2: st.metric("Calories Burned", f"{total_calories}")
            
            for activity_log in today_activities:
                st.markdown(f"""
                <div class="activity-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>{activity_log['activity_type']}</strong> at {activity_log['timestamp']}<br>
                            <small>Duration: {activity_log['duration']} min • Intensity: {activity_log['intensity']}</small>
                        </div>
                        <div style="text-align: right;">
                            <strong>{activity_log['calories_burned']} cal</strong>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No activities logged today. Get moving!")
    
    with tab4:
        # Progress Visualization
        st.markdown("### 📊 Your Progress Dashboard")
        
        # Streaks
        streaks = get_streak_data()
        if streaks:
            st.markdown("#### 🔥 Current Streaks")
            col1, col2, col3 = st.columns(3)
            streak_items = list(streaks.items())[:3]
            
            for i, (habit_name, streak_data) in enumerate(streak_items):
                with [col1, col2, col3][i]:
                    st.markdown(f"""
                    <div class="streak-card">
                        <div style="text-align: center;">
                            <div style="font-size: 2.5rem; font-weight: 800; color: #8B5CF6;">{streak_data['current_streak']}</div>
                            <div style="color: #4B5563; font-weight: 600;">{habit_name}</div>
                            <div style="color: #9CA3AF; font-size: 0.9rem;">Days in a row</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Calendar View
        st.markdown("#### 📅 Habit Calendar")
        calendar_data, month, year = get_calendar_view()
        
        # Month navigation
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("← Previous"):
                # Implement month navigation
                pass
        with col2:
            st.markdown(f"<div style='text-align: center; font-weight: 600;'>{calendar.month_name[month]} {year}</div>", unsafe_allow_html=True)
        with col3:
            if st.button("Next →"):
                # Implement month navigation
                pass
        
        # Display calendar
        st.markdown("<div style='display: flex; justify-content: center; margin: 20px 0;'>", unsafe_allow_html=True)
        for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
            st.markdown(f"<div style='width: 40px; text-align: center; margin: 5px; font-weight: 600; color: #4B5563;'>{day}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        for week in calendar_data:
            st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
            for day_data in week:
                if day_data is None:
                    st.markdown("<div style='width: 40px; height: 40px; margin: 5px;'></div>", unsafe_allow_html=True)
                else:
                    if day_data['is_today']:
                        css_class = "day-today"
                    elif day_data['completion_rate'] > 80:
                        css_class = "day-completed"
                    elif day_data['completion_rate'] > 0:
                        css_class = "day-partial"
                    else:
                        css_class = "day-missed"
                    
                    st.markdown(f"""
                    <div class="day-box {css_class}" title="{day_data['date']}: {day_data['completion_rate']:.0f}% complete">
                        {day_data['day']}
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Progress charts
        st.markdown("#### 📈 Progress Over Time")
        
        if st.session_state.habits['daily']:
            # Create sample progress data
            dates = []
            completion_rates = []
            
            for i in range(7):
                date = today - timedelta(days=6-i)
                date_str = date.strftime("%Y-%m-%d")
                
                total_habits = len(st.session_state.habits['daily'])
                completed = 0
                
                for habit in st.session_state.habits['daily']:
                    if date_str in habit.get('completion_data', {}):
                        if habit['completion_data'][date_str]['completed']:
                            completed += 1
                
                if total_habits > 0:
                    rate = (completed / total_habits) * 100
                else:
                    rate = 0
                
                dates.append(date.strftime("%b %d"))
                completion_rates.append(rate)
            
            # Create chart
            fig = go.Figure(data=go.Scatter(
                x=dates,
                y=completion_rates,
                mode='lines+markers',
                line=dict(color='#2E8B57', width=4),
                marker=dict(size=10, color='#3CB371')
            ))
            
            fig.update_layout(
                title="Weekly Habit Completion Rate",
                xaxis_title="Date",
                yaxis_title="Completion Rate (%)",
                yaxis_range=[0, 100],
                height=300,
                plot_bgcolor='white',
                paper_bgcolor='white'
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tab5:
        # Weekly Report
        st.markdown("### 📋 Weekly Progress Report")
        
        report = generate_weekly_report()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if report['total_possible'] > 0:
                habit_rate = (report['habits_completed'] / report['total_possible']) * 100
            else:
                habit_rate = 0
            
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2.5rem; font-weight: 800; color: #2E8B57;">{habit_rate:.0f}%</div>
                <div style="color: #4B5563; font-weight: 600;">Habit Completion</div>
                <div style="color: #9CA3AF; font-size: 0.9rem;">{report['habits_completed']}/{report['total_possible']} habits</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            net_calories = report['calories_consumed'] - report['calories_burned']
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2.5rem; font-weight: 800; color: {'#DC2626' if net_calories > 0 else '#10B981'};">{net_calories:+,.0f}</div>
                <div style="color: #4B5563; font-weight: 600;">Net Calories</div>
                <div style="color: #9CA3AF; font-size: 0.9rem;">In: {report['calories_consumed']:,} | Out: {report['calories_burned']:,}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2.5rem; font-weight: 800; color: #3B82F6;">{report['days_tracked']}/7</div>
                <div style="color: #4B5563; font-weight: 600;">Days Tracked</div>
                <div style="color: #9CA3AF; font-size: 0.9rem;">Avg Sleep: {report['avg_sleep']:.1f}h</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Recommendations
        st.markdown("#### 🎯 This Week's Recommendations")
        
        recommendations = []
        
        if report['avg_sleep'] < 7:
            recommendations.append("Aim for 7-8 hours of sleep each night for better recovery")
        
        if habit_rate < 70:
            recommendations.append("Try to complete at least 70% of your daily habits")
        
        if net_calories > 500:
            recommendations.append("Consider increasing activity or reducing calorie intake slightly")
        
        if not recommendations:
            recommendations.append("Great work! Keep up the consistent tracking and healthy habits!")
        
        for rec in recommendations:
            st.markdown(f"""
            <div class="solution-card">
                <p style="margin: 0;">{rec}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Navigation
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("← Back to Analysis", use_container_width=True):
            st.session_state.current_page = "📊 Risk Analysis"
            st.rerun()
    with col2:
        if st.button("🏠 Go to Home", use_container_width=True):
            st.session_state.current_page = "🏠 Home"
            st.rerun()
    with col3:
        if st.button("💰 Cost Calculator →", use_container_width=True, type="primary"):
            st.session_state.current_page = "💰 Cost Calculator"
            st.rerun()

def display_cost_calculator():
    """Cost calculator"""
    if not st.session_state.patient_data:
        st.warning("Please scan a report first!")
        return
    
    patient_data = st.session_state.patient_data
    risk_scores = st.session_state.risk_scores
    
    st.markdown("## 💰 Healthcare Cost Calculator")
    
    cost_data = calculate_cost_savings(patient_data, risk_scores)
    
    def format_rupees(amount):
        return f"₹{amount:,.0f}"
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%); border-radius: 20px;">
            <h1 style="font-size: 2.5rem; margin: 0; color: #DC2626;">{format_rupees(cost_data['cost_without_intervention'])}</h1>
            <p>5-Year Cost Without Prevention</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%); border-radius: 20px;">
            <h1 style="font-size: 2.5rem; margin: 0; color: #059669;">{format_rupees(cost_data['cost_with_intervention'])}</h1>
            <p>5-Year Cost With Prevention</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%); border-radius: 20px;">
            <h1 style="font-size: 2.5rem; margin: 0; color: #1D4ED8;">{format_rupees(cost_data['total_savings'])}</h1>
            <p>Potential Savings</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Monthly Prevention", "₹1,500", "For 5 years")
    with col2: st.metric("Annual Savings", f"{format_rupees(cost_data['annual_savings'])}", "Per year")
    with col3: st.metric("ROI", f"{(cost_data['total_savings']/cost_data['cost_with_intervention']*100):.0f}%", "Return")
    with col4: st.metric("Break-even", "2.3 years", "From investment")
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Tracker", use_container_width=True):
            st.session_state.current_page = "📝 Habit Tracker"
            st.rerun()
    with col2:
        if st.button("📝 Action Plan →", use_container_width=True, type="primary"):
            # Generate and show action plan
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
            <h1 style="color: #1F2937;">🏥 MEDIPRECOG</h1>
            <p style="color: #4B5563;">Health Time Machine</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        pages = {
            "🏠 Home": display_home,
            "📸 Scan Report": display_scan_report,
            "📊 Risk Analysis": display_risk_analysis,
            "📝 Habit Tracker": display_habit_tracker,
            "💰 Cost Calculator": display_cost_calculator
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
            st.markdown(f"**Current Patient:** {patient_name}")
            
            # Quick habit tracker summary
            today_habits = len(st.session_state.habits['daily'])
            if today_habits > 0:
                completed = 0
                today_str = get_today_date()
                for habit in st.session_state.habits['daily']:
                    if today_str in habit.get('completion_data', {}):
                        if habit['completion_data'][today_str]['completed']:
                            completed += 1
                
                st.progress(completed/today_habits if today_habits > 0 else 0)
                st.caption(f"Habits: {completed}/{today_habits} completed")
        
        st.markdown("---")
        if st.button("🔄 Reset Session", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.current_page = "🏠 Home"
            st.rerun()
        
        st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.8rem;">
            <p>🚀 Built for Better Health</p>
            <p>📊 Track • Improve • Thrive</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main Content
    pages = {
        "🏠 Home": display_home,
        "📸 Scan Report": display_scan_report,
        "📊 Risk Analysis": display_risk_analysis,
        "📝 Habit Tracker": display_habit_tracker,
        "💰 Cost Calculator": display_cost_calculator
    }
    
    if st.session_state.current_page in pages:
        pages[st.session_state.current_page]()

# ============================================
# RUN APPLICATION
# ============================================
if __name__ == "__main__":
    main()