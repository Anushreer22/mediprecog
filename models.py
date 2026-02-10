"""
Machine learning models for health predictions
(Mocked for hackathon demo)
"""

import numpy as np
from datetime import datetime, timedelta
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import json

class HealthPredictor:
    """Mock ML model for health predictions"""
    
    def __init__(self):
        self.model_name = "MediPrecog Health Predictor v1.0"
        self.trained_date = "2024-02-10"
        self.confidence = 0.94
        self.training_samples = 50000
        
    def predict_diabetes_risk(self, features):
        """Predict diabetes risk based on features"""
        # Mock prediction based on simple rules
        risk_score = 0.0
        
        # Age factor
        age = features.get('age', 35)
        risk_score += max(0, (age - 30) * 0.005)
        
        # BMI factor
        weight = features.get('weight', 185)
        height = features.get('height', 175)
        bmi = weight / ((height/100) ** 2)
        if bmi > 25:
            risk_score += (bmi - 25) * 0.01
        
        # Glucose factor
        glucose = features.get('glucose', 100)
        if glucose > 100:
            risk_score += (glucose - 100) * 0.005
        
        # Family history
        if features.get('family_history_diabetes', False):
            risk_score += 0.2
        
        # Ensure risk is between 0 and 1
        risk_score = min(0.95, max(0.05, risk_score))
        
        return {
            'risk_percentage': round(risk_score * 100, 1),
            'confidence': round(self.confidence * 100, 1),
            'timeline': self.get_timeline(risk_score),
            'key_factors': self.get_key_factors(features)
        }
    
    def predict_cvd_risk(self, features):
        """Predict cardiovascular disease risk"""
        risk_score = 0.0
        
        # Age factor
        age = features.get('age', 35)
        risk_score += max(0, (age - 30) * 0.004)
        
        # Blood pressure
        bp_systolic = features.get('bp_systolic', 120)
        if bp_systolic > 120:
            risk_score += (bp_systolic - 120) * 0.002
        
        # Cholesterol
        cholesterol = features.get('cholesterol', 200)
        if cholesterol > 200:
            risk_score += (cholesterol - 200) * 0.001
        
        # Smoking
        if features.get('smoking', False):
            risk_score += 0.3
        
        risk_score = min(0.95, max(0.05, risk_score))
        
        return {
            'risk_percentage': round(risk_score * 100, 1),
            'confidence': round(self.confidence * 100, 1),
            'timeline': self.get_timeline(risk_score),
            'key_factors': self.get_key_factors(features)
        }
    
    def predict_kidney_risk(self, features):
        """Predict kidney disease risk"""
        risk_score = 0.0
        
        # Creatinine
        creatinine = features.get('creatinine', 1.0)
        if creatinine > 1.0:
            risk_score += (creatinine - 1.0) * 0.1
        
        # Blood pressure
        bp_systolic = features.get('bp_systolic', 120)
        if bp_systolic > 130:
            risk_score += (bp_systolic - 130) * 0.001
        
        # Diabetes
        if features.get('has_diabetes', False):
            risk_score += 0.25
        
        risk_score = min(0.90, max(0.05, risk_score))
        
        return {
            'risk_percentage': round(risk_score * 100, 1),
            'confidence': round(self.confidence * 100, 1),
            'timeline': self.get_timeline(risk_score, disease='kidney'),
            'key_factors': self.get_key_factors(features)
        }
    
    def get_timeline(self, risk_score, disease='general'):
        """Get timeline prediction based on risk score"""
        if risk_score > 0.7:
            return "1-3 years"
        elif risk_score > 0.5:
            return "3-5 years"
        elif risk_score > 0.3:
            return "5-10 years"
        else:
            return "10+ years"
    
    def get_key_factors(self, features):
        """Identify key contributing factors"""
        factors = []
        
        if features.get('age', 35) > 40:
            factors.append("Age > 40")
        
        weight = features.get('weight', 185)
        height = features.get('height', 175)
        bmi = weight / ((height/100) ** 2)
        if bmi > 25:
            factors.append(f"BMI: {bmi:.1f} (Overweight)")
        
        if features.get('glucose', 100) > 100:
            factors.append("Elevated glucose")
        
        if features.get('bp_systolic', 120) > 130:
            factors.append("Elevated blood pressure")
        
        if features.get('cholesterol', 200) > 200:
            factors.append("Elevated cholesterol")
        
        return factors[:3]  # Return top 3 factors
    
    def predict_health_events(self, features):
        """Predict upcoming health events"""
        events = []
        
        # Migraine prediction
        if features.get('has_migraine_history', False):
            next_migraine = datetime.now() + timedelta(days=random.randint(7, 14))
            events.append({
                'type': 'Migraine Attack',
                'probability': 0.87,
                'date': next_migraine.strftime('%A, %b %d'),
                'time': '2:30 PM - 5:00 PM',
                'prevention': [
                    'Take 400mg Magnesium tonight',
                    'Avoid screen time tomorrow AM',
                    'Drink 3L water before 2 PM'
                ]
            })
        
        # Blood pressure event
        if features.get('bp_systolic', 120) > 130:
            events.append({
                'type': 'Blood Pressure Spike',
                'probability': 0.65,
                'date': (datetime.now() + timedelta(days=random.randint(3, 10))).strftime('%A, %b %d'),
                'time': 'Morning hours',
                'prevention': [
                    'Reduce sodium intake',
                    'Morning walk 20 minutes',
                    'Avoid caffeine before noon'
                ]
            })
        
        return events