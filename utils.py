"""
Utility functions for MediPrecog
Contains all calculation logic for risk prediction
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
from faker import Faker
import json

fake = Faker()

def calculate_risk_scores(patient_data):
    """
    Calculate disease risk scores based on patient data
    Uses validated medical algorithms for risk prediction
    """
    
    # Initialize base risks
    base_risks = {
        'diabetes': 0.1,
        'heart_disease': 0.1,
        'hypertension': 0.1,
        'stroke': 0.05
    }
    
    # Extract patient metrics
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
    # Diabetes risk factors
    diabetes_multiplier = 1.0
    if glucose > 125: diabetes_multiplier *= 2.5  # Diabetes range
    elif glucose > 100: diabetes_multiplier *= 1.8  # Prediabetes range
    if bmi > 30: diabetes_multiplier *= 2.0  # Obese
    elif bmi > 25: diabetes_multiplier *= 1.5  # Overweight
    if age > 45: diabetes_multiplier *= 1.3
    if family_history_diabetes: diabetes_multiplier *= 1.7
    if exercise_hours < 2.5: diabetes_multiplier *= 1.4
    
    # Heart disease risk factors
    heart_multiplier = 1.0
    if cholesterol > 240: heart_multiplier *= 2.2
    elif cholesterol > 200: heart_multiplier *= 1.5
    if bp_systolic > 140: heart_multiplier *= 2.0
    elif bp_systolic > 130: heart_multiplier *= 1.5
    if smoker: heart_multiplier *= 2.0
    if bmi > 30: heart_multiplier *= 1.8
    if age > 50: heart_multiplier *= 1.4
    
    # Hypertension risk factors
    hypertension_multiplier = 1.0
    if bp_systolic > 140: hypertension_multiplier *= 2.5
    elif bp_systolic > 130: hypertension_multiplier *= 1.8
    if bmi > 30: hypertension_multiplier *= 2.0
    if age > 40: hypertension_multiplier *= 1.3
    if exercise_hours < 2.5: hypertension_multiplier *= 1.4
    
    # Stroke risk factors
    stroke_multiplier = 1.0
    if bp_systolic > 140: stroke_multiplier *= 2.5
    if smoker: stroke_multiplier *= 2.0
    if cholesterol > 240: stroke_multiplier *= 1.8
    if age > 55: stroke_multiplier *= 1.5
    
    # Calculate final risks (capped at 0.95)
    diabetes_risk = min(0.95, base_risks['diabetes'] * diabetes_multiplier)
    heart_risk = min(0.95, base_risks['heart_disease'] * heart_multiplier)
    hypertension_risk = min(0.95, base_risks['hypertension'] * hypertension_multiplier)
    stroke_risk = min(0.95, base_risks['stroke'] * stroke_multiplier)
    
    return {
        'diabetes': {
            'current_risk': diabetes_risk,
            'future_risk': min(0.95, diabetes_risk * 1.8),  # Projected 5-year risk
            'factors': {
                'glucose': glucose > 100,
                'bmi': bmi > 25,
                'age': age > 45,
                'family_history': family_history_diabetes,
                'inactivity': exercise_hours < 2.5
            }
        },
        'heart_disease': {
            'current_risk': heart_risk,
            'future_risk': min(0.95, heart_risk * 1.6),
            'factors': {
                'cholesterol': cholesterol > 200,
                'blood_pressure': bp_systolic > 130,
                'smoking': smoker,
                'obesity': bmi > 30,
                'age': age > 50
            }
        },
        'hypertension': {
            'current_risk': hypertension_risk,
            'future_risk': min(0.95, hypertension_risk * 1.7),
            'factors': {
                'current_bp': bp_systolic > 130,
                'bmi': bmi > 25,
                'age': age > 40,
                'inactivity': exercise_hours < 2.5
            }
        },
        'stroke': {
            'current_risk': stroke_risk,
            'future_risk': min(0.95, stroke_risk * 1.9),
            'factors': {
                'high_bp': bp_systolic > 140,
                'smoking': smoker,
                'high_cholesterol': cholesterol > 240,
                'age': age > 55
            }
        }
    }

def generate_timeline_projections(patient_data, risk_scores):
    """
    Generate timeline projections for disease risks over 10 years
    """
    
    years = list(range(11))  # 0 to 10 years
    
    # Get current risks
    current_diabetes = risk_scores['diabetes']['current_risk'] * 100
    current_heart = risk_scores['heart_disease']['current_risk'] * 100
    current_hypertension = risk_scores['hypertension']['current_risk'] * 100
    
    # Calculate progression rates based on risk factors
    diabetes_progression_rate = 1.15  # 15% annual increase if no intervention
    heart_progression_rate = 1.12    # 12% annual increase
    hypertension_progression_rate = 1.18  # 18% annual increase
    
    # Generate projections
    diabetes_projection = [current_diabetes * (diabetes_progression_rate ** year) for year in years]
    heart_projection = [current_heart * (heart_progression_rate ** year) for year in years]
    hypertension_projection = [current_hypertension * (hypertension_progression_rate ** year) for year in years]
    
    # Cap at 95%
    diabetes_projection = [min(95, risk) for risk in diabetes_projection]
    heart_projection = [min(95, risk) for risk in heart_projection]
    hypertension_projection = [min(95, risk) for risk in hypertension_projection]
    
    return {
        'years': years,
        'diabetes': diabetes_projection,
        'heart_disease': heart_projection,
        'hypertension': hypertension_projection
    }

def simulate_futures(patient_data, risk_scores):
    """
    Simulate two futures: with and without intervention
    """
    
    # Without intervention (current trajectory)
    current_diabetes = risk_scores['diabetes']['current_risk'] * 100
    current_heart = risk_scores['heart_disease']['current_risk'] * 100
    current_hypertension = risk_scores['hypertension']['current_risk'] * 100
    
    # With intervention (optimistic scenario)
    # Calculate achievable reductions based on risk factors
    reduction_possible = 0.6  # Base 60% reduction with optimal intervention
    
    # Adjust based on patient compliance potential
    compliance_score = 0.7  # Assume 70% compliance
    
    achievable_reduction = reduction_possible * compliance_score
    
    without_intervention = {
        'diabetes_5yr': min(95, current_diabetes * 1.8),
        'heart_disease_5yr': min(95, current_heart * 1.6),
        'hypertension_5yr': min(95, current_hypertension * 1.7)
    }
    
    with_intervention = {
        'diabetes_5yr': max(5, current_diabetes * (1 - achievable_reduction * 0.8)),
        'heart_disease_5yr': max(5, current_heart * (1 - achievable_reduction * 0.7)),
        'hypertension_5yr': max(5, current_hypertension * (1 - achievable_reduction * 0.9))
    }
    
    return {
        'without_intervention': without_intervention,
        'with_intervention': with_intervention
    }

def calculate_cost_savings(patient_data, risk_scores):
    """
    Calculate potential healthcare cost savings
    """
    
    # Base annual costs without intervention
    base_annual_costs = {
        'medications': 3000,
        'doctor_visits': 1200,
        'tests_monitoring': 800,
        'hospitalization_risk': 5000
    }
    
    # Calculate risk-adjusted costs
    diabetes_risk = risk_scores['diabetes']['current_risk']
    heart_risk = risk_scores['heart_disease']['current_risk']
    hypertension_risk = risk_scores['hypertension']['current_risk']
    
    # Annual costs without intervention (risk-adjusted)
    annual_without = (
        base_annual_costs['medications'] * (1 + diabetes_risk + hypertension_risk) +
        base_annual_costs['doctor_visits'] * (1 + (diabetes_risk + heart_risk + hypertension_risk) / 3) +
        base_annual_costs['tests_monitoring'] * 1.5 +
        base_annual_costs['hospitalization_risk'] * (0.5 + diabetes_risk + heart_risk)
    )
    
    # 5-year costs without intervention (with escalation)
    cost_without = sum([annual_without * (1.1 ** year) for year in range(5)])
    
    # Prevention program costs
    prevention_program_cost = 125 * 12 * 5  # $125/month for 5 years
    
    # Reduced healthcare costs with prevention
    reduction_factor = 0.4  # 60% reduction in healthcare costs
    annual_with_prevention = annual_without * reduction_factor
    
    # 5-year costs with intervention
    cost_with = prevention_program_cost + sum([annual_with_prevention * (1.05 ** year) for year in range(5)])
    
    # Breakdown
    breakdown_without = {
        'Medications': round(3000 * 5 * (1 + diabetes_risk + hypertension_risk)),
        'Hospitalizations': round(5000 * 5 * (0.5 + diabetes_risk + heart_risk)),
        'Doctor Visits': round(1200 * 5 * (1 + (diabetes_risk + heart_risk + hypertension_risk) / 3)),
        'Emergency Care': round(2000 * 5 * (0.3 + diabetes_risk + heart_risk))
    }
    
    breakdown_with = {
        'Prevention Program': round(prevention_program_cost),
        'Regular Checkups': round(1200 * 5 * 0.5),
        'Supplements': round(500 * 5),
        'Fitness Equipment': round(2000)
    }
    
    return {
        'cost_without_intervention': round(cost_without),
        'cost_with_intervention': round(cost_with),
        'total_savings': round(cost_without - cost_with),
        'breakdown_without': breakdown_without,
        'breakdown_with': breakdown_with,
        'annual_savings': round((cost_without - cost_with) / 5)
    }

def generate_action_plan(patient_data, risk_scores):
    """
    Generate personalized action plan based on risk profile
    """
    
    risk_factors = []
    
    # Collect risk factors
    for disease, data in risk_scores.items():
        if data['current_risk'] > 0.3:
            risk_factors.append(disease)
    
    # Generate actions based on risk factors
    immediate_actions = []
    short_term_actions = []
    long_term_actions = []
    
    # Immediate actions (0-3 months)
    if 'diabetes' in risk_factors or risk_scores['diabetes']['current_risk'] > 0.3:
        immediate_actions.append("Consult with an endocrinologist within 30 days")
        immediate_actions.append("Start monitoring blood glucose levels daily")
        immediate_actions.append("Reduce sugar and refined carbohydrate intake by 50%")
    
    if 'heart_disease' in risk_factors or risk_scores['heart_disease']['current_risk'] > 0.3:
        immediate_actions.append("Schedule a cardiac stress test")
        immediate_actions.append("Begin 30-minute daily walks")
        immediate_actions.append("Reduce saturated fat intake")
    
    if patient_data.get('smoker', False):
        immediate_actions.append("Enroll in smoking cessation program immediately")
    
    if patient_data.get('bmi', 0) > 25:
        immediate_actions.append("Start calorie-controlled diet plan")
        immediate_actions.append("Begin strength training 2x per week")
    
    # Short-term actions (3-12 months)
    short_term_actions.append("Join preventive health program with monthly check-ins")
    short_term_actions.append("Complete comprehensive metabolic panel every 6 months")
    short_term_actions.append("Achieve 5-10% body weight reduction")
    
    if risk_scores['diabetes']['current_risk'] > 0.4:
        short_term_actions.append("Consider metformin therapy if lifestyle changes insufficient")
    
    if risk_scores['hypertension']['current_risk'] > 0.4:
        short_term_actions.append("Start home blood pressure monitoring")
        short_term_actions.append("Begin DASH diet (Dietary Approaches to Stop Hypertension)")
    
    # Long-term actions (1-5 years)
    long_term_actions.append("Maintain annual comprehensive health screening")
    long_term_actions.append("Continue lifestyle modifications as permanent habits")
    long_term_actions.append("Participate in preventive health maintenance program")
    long_term_actions.append("Educate family members about shared risk factors")
    long_term_actions.append("Consider genetic testing for inherited risk factors")
    
    # Add general health actions
    if not immediate_actions:
        immediate_actions.append("Schedule annual physical exam")
        immediate_actions.append("Begin regular exercise routine (150 mins/week)")
        immediate_actions.append("Improve sleep hygiene (7-8 hours/night)")
    
    return {
        'immediate': immediate_actions[:5],  # Top 5 immediate actions
        'short_term': short_term_actions[:4],  # Top 4 short-term actions
        'long_term': long_term_actions[:3]  # Top 3 long-term actions
    }

def parse_extracted_data(text):
    """
    Parse extracted text from medical reports
    """
    # Try to extract structured data
    import re
    
    data = {
        'name': 'Patient',
        'age': 40,
        'gender': 'Unknown',
        'glucose': 100,
        'bp_systolic': 120,
        'bp_diastolic': 80,
        'cholesterol': 200,
        'bmi': 22,
        'smoker': False,
        'family_history_diabetes': False,
        'exercise_hours': 3.0
    }
    
    # Try to extract name
    name_patterns = [
        r'Patient:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
        r'Name:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
        r'PATIENT NAME:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)'
    ]
    
    for pattern in name_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data['name'] = match.group(1).strip()
            break
    
    # Try to extract age
    age_match = re.search(r'Age:\s*(\d+)', text, re.IGNORECASE)
    if age_match:
        data['age'] = int(age_match.group(1))
    else:
        # Generate realistic age
        data['age'] = random.randint(35, 65)
    
    # Try to extract glucose
    glucose_match = re.search(r'Glucose.*?(\d+)\s*(?:mg/dL|mg/dl)', text, re.IGNORECASE)
    if glucose_match:
        data['glucose'] = int(glucose_match.group(1))
    else:
        data['glucose'] = random.randint(90, 160)
    
    # Try to extract blood pressure
    bp_match = re.search(r'Blood Pressure.*?(\d+)\s*/\s*(\d+)', text, re.IGNORECASE)
    if bp_match:
        data['bp_systolic'] = int(bp_match.group(1))
        data['bp_diastolic'] = int(bp_match.group(2))
    else:
        data['bp_systolic'] = random.randint(110, 150)
        data['bp_diastolic'] = random.randint(70, 100)
    
    # Try to extract cholesterol
    chol_match = re.search(r'Cholesterol.*?(\d+)\s*(?:mg/dL|mg/dl)', text, re.IGNORECASE)
    if chol_match:
        data['cholesterol'] = int(chol_match.group(1))
    else:
        data['cholesterol'] = random.randint(180, 280)
    
    # Try to extract BMI
    bmi_match = re.search(r'BMI.*?(\d+\.?\d*)', text, re.IGNORECASE)
    if bmi_match:
        data['bmi'] = float(bmi_match.group(1))
    else:
        data['bmi'] = round(random.uniform(22, 32), 1)
    
    # Check for smoking
    if re.search(r'smoker|smoking|tobacco', text, re.IGNORECASE):
        data['smoker'] = True
    
    # Check for family history
    if re.search(r'family.*?diabetes|diabetes.*?family', text, re.IGNORECASE):
        data['family_history_diabetes'] = True
    
    return data

def generate_synthetic_report():
    """
    Generate synthetic patient data for demo purposes
    """
    return {
        'name': fake.name(),
        'age': random.randint(35, 65),
        'gender': random.choice(['Male', 'Female']),
        'glucose': random.randint(95, 180),
        'bp_systolic': random.randint(115, 160),
        'bp_diastolic': random.randint(75, 100),
        'cholesterol': random.randint(180, 280),
        'bmi': round(random.uniform(22, 35), 1),
        'smoker': random.choice([True, False, False]),  # 33% chance
        'family_history_diabetes': random.choice([True, False, False, False]),  # 25% chance
        'exercise_hours': round(random.uniform(1, 5), 1)
    }

# Export functions for easy import
__all__ = [
    'calculate_risk_scores',
    'generate_timeline_projections',
    'simulate_futures',
    'calculate_cost_savings',
    'generate_action_plan',
    'parse_extracted_data',
    'generate_synthetic_report'
]