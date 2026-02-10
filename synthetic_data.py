"""
Synthetic Data Generator for MediPrecog
Creates realistic medical reports for demonstration
"""

import json
import random
from datetime import datetime, timedelta
from faker import Faker
import pandas as pd

fake = Faker()

class SyntheticReportGenerator:
    """Generate synthetic medical reports for demo purposes"""
    
    def __init__(self):
        self.diseases = ['Diabetes', 'Heart Disease', 'Hypertension', 'Stroke']
        self.lab_tests = ['Glucose', 'HbA1c', 'Cholesterol', 'Triglycerides', 'HDL', 'LDL']
        self.vitals = ['Blood Pressure', 'Heart Rate', 'BMI', 'Waist Circumference']
    
    def generate_patient_profile(self, risk_level='medium'):
        """
        Generate a synthetic patient profile
        
        Args:
            risk_level: 'low', 'medium', or 'high' risk profile
        """
        
        # Base patient info
        patient = {
            'id': f"PAT-{random.randint(10000, 99999)}",
            'name': fake.name(),
            'age': random.randint(25, 75),
            'gender': random.choice(['Male', 'Female']),
            'date_of_birth': fake.date_of_birth(minimum_age=25, maximum_age=75).strftime('%Y-%m-%d'),
            'contact': {
                'phone': fake.phone_number(),
                'email': fake.email()
            }
        }
        
        # Generate vitals based on risk level
        vitals = self._generate_vitals(risk_level)
        patient.update(vitals)
        
        # Generate lab results
        labs = self._generate_lab_results(risk_level)
        patient.update(labs)
        
        # Generate medical history
        history = self._generate_medical_history(risk_level)
        patient.update(history)
        
        # Calculate derived metrics
        patient['bmi'] = round(patient['weight_kg'] / ((patient['height_cm'] / 100) ** 2), 1)
        
        return patient
    
    def _generate_vitals(self, risk_level):
        """Generate vital signs based on risk level"""
        
        if risk_level == 'low':
            bp_systolic = random.randint(100, 120)
            bp_diastolic = random.randint(60, 80)
            weight = random.randint(60, 80)  # kg
            height = random.randint(160, 185)  # cm
            
        elif risk_level == 'medium':
            bp_systolic = random.randint(120, 140)
            bp_diastolic = random.randint(80, 90)
            weight = random.randint(75, 95)
            height = random.randint(155, 180)
            
        else:  # high risk
            bp_systolic = random.randint(140, 160)
            bp_diastolic = random.randint(90, 100)
            weight = random.randint(85, 110)
            height = random.randint(150, 175)
        
        return {
            'blood_pressure': f"{bp_systolic}/{bp_diastolic}",
            'bp_systolic': bp_systolic,
            'bp_diastolic': bp_diastolic,
            'heart_rate': random.randint(60, 100),
            'respiratory_rate': random.randint(12, 20),
            'temperature': round(random.uniform(36.5, 37.5), 1),
            'spo2': random.randint(95, 100),
            'height_cm': height,
            'weight_kg': weight
        }
    
    def _generate_lab_results(self, risk_level):
        """Generate laboratory results based on risk level"""
        
        if risk_level == 'low':
            glucose = random.randint(70, 100)
            hba1c = round(random.uniform(4.5, 5.6), 1)
            cholesterol = random.randint(150, 200)
            triglycerides = random.randint(70, 150)
            hdl = random.randint(40, 60)
            ldl = random.randint(70, 130)
            
        elif risk_level == 'medium':
            glucose = random.randint(100, 125)
            hba1c = round(random.uniform(5.7, 6.4), 1)
            cholesterol = random.randint(200, 240)
            triglycerides = random.randint(150, 200)
            hdl = random.randint(35, 45)
            ldl = random.randint(130, 160)
            
        else:  # high risk
            glucose = random.randint(125, 180)
            hba1c = round(random.uniform(6.5, 9.0), 1)
            cholesterol = random.randint(240, 300)
            triglycerides = random.randint(200, 300)
            hdl = random.randint(30, 40)
            ldl = random.randint(160, 200)
        
        return {
            'glucose': glucose,
            'hba1c': hba1c,
            'cholesterol_total': cholesterol,
            'triglycerides': triglycerides,
            'cholesterol_hdl': hdl,
            'cholesterol_ldl': ldl,
            'creatinine': round(random.uniform(0.6, 1.2), 2),
            'alt': random.randint(10, 40),
            'ast': random.randint(10, 35)
        }
    
    def _generate_medical_history(self, risk_level):
        """Generate medical history based on risk level"""
        
        # Smoking status
        smoking_options = ['Never', 'Former', 'Current']
        smoking_weights = {
            'low': [0.8, 0.15, 0.05],
            'medium': [0.6, 0.25, 0.15],
            'high': [0.4, 0.3, 0.3]
        }
        
        smoking = random.choices(smoking_options, weights=smoking_weights[risk_level])[0]
        
        # Alcohol consumption
        alcohol_options = ['Never', 'Occasional', 'Regular']
        alcohol_weights = {
            'low': [0.4, 0.5, 0.1],
            'medium': [0.3, 0.5, 0.2],
            'high': [0.2, 0.4, 0.4]
        }
        
        alcohol = random.choices(alcohol_options, weights=alcohol_weights[risk_level])[0]
        
        # Physical activity
        activity_options = ['Sedentary', 'Light', 'Moderate', 'Active']
        activity_weights = {
            'low': [0.1, 0.3, 0.4, 0.2],
            'medium': [0.2, 0.4, 0.3, 0.1],
            'high': [0.4, 0.4, 0.15, 0.05]
        }
        
        activity = random.choices(activity_options, weights=activity_weights[risk_level])[0]
        
        # Family history probability based on risk level
        family_history_prob = {'low': 0.2, 'medium': 0.4, 'high': 0.6}[risk_level]
        
        history = {
            'smoking_status': smoking,
            'alcohol_consumption': alcohol,
            'physical_activity': activity,
            'exercise_hours': random.uniform(1, 5),
            'family_history': {
                'diabetes': random.random() < family_history_prob,
                'heart_disease': random.random() < family_history_prob,
                'hypertension': random.random() < family_history_prob,
                'stroke': random.random() < family_history_prob * 0.8
            },
            'medications': random.sample(['None', 'Metformin', 'Statins', 'ACE Inhibitors', 'Beta Blockers'], 
                                         k=random.randint(1, 3)),
            'allergies': random.choice(['None', 'Penicillin', 'Sulfa', 'NSAIDs', 'Food allergies'])
        }
        
        return history
    
    def generate_full_report(self, patient_id=None, risk_level='medium'):
        """Generate a complete medical report"""
        
        if not patient_id:
            patient_id = f"REP-{random.randint(100000, 999999)}"
        
        patient = self.generate_patient_profile(risk_level)
        
        report = {
            'report_id': patient_id,
            'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'patient': patient,
            'summary': self._generate_summary(patient, risk_level),
            'recommendations': self._generate_recommendations(patient, risk_level),
            'next_steps': self._generate_next_steps(risk_level)
        }
        
        return report
    
    def _generate_summary(self, patient, risk_level):
        """Generate report summary"""
        
        summaries = {
            'low': "Patient presents with generally healthy biomarkers and lifestyle factors. Low risk profile for chronic diseases. Continue current healthy practices.",
            'medium': "Patient shows moderate risk factors requiring attention. Some biomarkers are borderline elevated. Lifestyle modifications recommended to reduce future disease risk.",
            'high': "Patient exhibits multiple high-risk factors requiring immediate intervention. Significant biomarker elevations present. Urgent lifestyle changes and medical follow-up recommended."
        }
        
        return summaries[risk_level]
    
    def _generate_recommendations(self, patient, risk_level):
        """Generate personalized recommendations"""
        
        base_recommendations = [
            "Maintain regular physical activity (150+ minutes per week)",
            "Follow balanced diet with plenty of fruits and vegetables",
            "Schedule annual health check-up",
            "Monitor blood pressure regularly"
        ]
        
        if risk_level == 'medium':
            additional = [
                "Consider dietary consultation for weight management",
                "Increase exercise to 30 minutes daily",
                "Reduce processed food and sugar intake",
                "Consider stress management techniques"
            ]
        elif risk_level == 'high':
            additional = [
                "Consult with primary care physician within 30 days",
                "Begin regular monitoring of blood glucose",
                "Enroll in lifestyle modification program",
                "Consider medication evaluation if lifestyle changes insufficient"
            ]
        else:
            additional = []
        
        return base_recommendations + additional[:3]
    
    def _generate_next_steps(self, risk_level):
        """Generate next steps based on risk level"""
        
        if risk_level == 'low':
            return [
                {"timeline": "1 year", "action": "Annual comprehensive checkup"},
                {"timeline": "6 months", "action": "Routine blood work"},
                {"timeline": "Immediate", "action": "Maintain current healthy lifestyle"}
            ]
        elif risk_level == 'medium':
            return [
                {"timeline": "3 months", "action": "Follow-up blood tests"},
                {"timeline": "1 month", "action": "Begin lifestyle modifications"},
                {"timeline": "6 months", "action": "Re-evaluation of risk factors"}
            ]
        else:  # high
            return [
                {"timeline": "30 days", "action": "Consult with healthcare provider"},
                {"timeline": "1 week", "action": "Begin immediate lifestyle changes"},
                {"timeline": "3 months", "action": "Specialist referral if needed"}
            ]

# Create global generator instance
report_generator = SyntheticReportGenerator()

# Convenience functions
def generate_demo_patients(count=10):
    """Generate multiple demo patients"""
    patients = []
    for i in range(count):
        risk_level = random.choice(['low', 'medium', 'high'])
        patient = report_generator.generate_patient_profile(risk_level)
        patient['risk_level'] = risk_level
        patients.append(patient)
    
    return patients

def generate_sample_report():
    """Generate a sample medical report"""
    return report_generator.generate_full_report(risk_level='medium')

def export_to_csv(patients, filename='demo_patients.csv'):
    """Export patient data to CSV"""
    df = pd.DataFrame(patients)
    df.to_csv(filename, index=False)
    return filename