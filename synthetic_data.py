"""
Generate synthetic patient data for demonstration
"""

from faker import Faker
import random
from datetime import datetime, timedelta
import json

fake = Faker()

def generate_patient_profile(age=35, weight=185):
    """Generate complete patient profile"""
    return {
        'id': fake.uuid4(),
        'name': fake.name(),
        'age': age,
        'weight': weight,
        'height': random.randint(165, 185),
        'blood_pressure': f"{random.randint(110, 140)}/{random.randint(70, 90)}",
        'glucose': random.randint(85, 110),
        'cholesterol': random.randint(180, 220),
        'creatinine': round(random.uniform(0.8, 1.2), 1),
        'last_checkup': fake.date_between(start_date='-6m', end_date='today'),
        'medications': random.sample(['Metformin', 'Lisinopril', 'Atorvastatin', 'None'], 1)[0],
        'allergies': random.choice(['None', 'Penicillin', 'Sulfa', 'Peanuts']),
        'family_history': random.sample(['Diabetes', 'Heart Disease', 'Hypertension', 'None'], random.randint(0, 2))
    }

def generate_lab_results():
    """Generate synthetic lab results"""
    return {
        'CBC': {
            'WBC': round(random.uniform(4.0, 10.0), 1),
            'RBC': round(random.uniform(4.2, 5.8), 1),
            'Hemoglobin': round(random.uniform(13.0, 17.0), 1),
            'Hematocrit': round(random.uniform(38.0, 50.0), 1),
            'Platelets': random.randint(150, 400)
        },
        'Metabolic Panel': {
            'Glucose': random.randint(85, 110),
            'Calcium': round(random.uniform(8.5, 10.2), 1),
            'Sodium': random.randint(135, 145),
            'Potassium': round(random.uniform(3.5, 5.2), 1),
            'Creatinine': round(random.uniform(0.7, 1.2), 1),
            'BUN': random.randint(7, 20)
        },
        'Lipid Panel': {
            'Total Cholesterol': random.randint(180, 220),
            'HDL': random.randint(40, 60),
            'LDL': random.randint(100, 160),
            'Triglycerides': random.randint(100, 200)
        }
    }

def generate_health_timeline(current_age=35):
    """Generate health projections over time"""
    timeline = {}
    
    for years in [1, 3, 5, 10]:
        age = current_age + years
        
        # Generate deteriorating health metrics
        timeline[years] = {
            'age': age,
            'diabetes_risk': min(0.95, 0.3 + (years * 0.1) + random.uniform(-0.05, 0.1)),
            'cvd_risk': min(0.95, 0.25 + (years * 0.08) + random.uniform(-0.05, 0.08)),
            'kidney_risk': min(0.90, 0.2 + (years * 0.06) + random.uniform(-0.04, 0.06)),
            'heart_function': max(0.3, 0.9 - (years * 0.04) + random.uniform(-0.02, 0.02)),
            'medical_costs': 5000 + (years * 7500) + random.randint(-2000, 2000),
            'expected_events': random.sample([
                'Mild hypertension diagnosis',
                'Pre-diabetes diagnosis',
                'High cholesterol medication',
                'Weight gain (+15 lbs)',
                'Joint pain onset'
            ], min(2, years))
        }
    
    return timeline

def generate_with_intervention(current_age=35):
    """Generate improved health timeline with intervention"""
    timeline = {}
    
    for years in [1, 3, 5, 10]:
        age = current_age + years
        
        # Generate improved health metrics with intervention
        timeline[years] = {
            'age': age,
            'diabetes_risk': max(0.05, 0.3 - (years * 0.05) + random.uniform(-0.03, 0.03)),
            'cvd_risk': max(0.05, 0.25 - (years * 0.04) + random.uniform(-0.03, 0.03)),
            'kidney_risk': max(0.05, 0.2 - (years * 0.03) + random.uniform(-0.02, 0.02)),
            'heart_function': min(0.98, 0.9 + (years * 0.015) + random.uniform(-0.01, 0.01)),
            'medical_costs': 2000 + (years * 1000) + random.randint(-500, 500),
            'cost_savings': (5000 + (years * 7500)) - (2000 + (years * 1000)),
            'health_gains': random.sample([
                'Weight loss (-20 lbs)',
                'Blood pressure normalized',
                'Cholesterol improved',
                'Energy levels increased',
                'Sleep quality improved'
            ], min(3, years + 1))
        }
    
    return timeline