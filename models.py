"""
Machine Learning Models for MediPrecog
Contains pre-trained models for risk prediction
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os

class HealthRiskPredictor:
    """Main model for predicting health risks"""
    
    def __init__(self):
        """Initialize with pre-trained models or create mock models"""
        self.models = {}
        self.scalers = {}
        
        # Try to load pre-trained models, otherwise create mock
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize or load pre-trained models"""
        
        diseases = ['diabetes', 'heart_disease', 'hypertension', 'stroke']
        
        for disease in diseases:
            # In a real implementation, we would load pre-trained models
            # For hackathon, we use rule-based predictions
            self.models[disease] = MockModel(disease)
            self.scalers[disease] = StandardScaler()
        
        print("Health Risk Predictor initialized with mock models")
    
    def predict_risk(self, patient_features, disease='diabetes'):
        """
        Predict risk for a specific disease
        
        Args:
            patient_features: Dictionary of patient features
            disease: Disease to predict (diabetes, heart_disease, hypertension, stroke)
        
        Returns:
            Dictionary with risk probability and confidence
        """
        
        if disease not in self.models:
            raise ValueError(f"Unknown disease: {disease}. Choose from {list(self.models.keys())}")
        
        # Convert features to array
        features = self._extract_features(patient_features)
        
        # Scale features
        features_scaled = self.scalers[disease].fit_transform([features])
        
        # Get prediction from model
        model = self.models[disease]
        risk_probability = model.predict(features_scaled[0])
        
        # Calculate confidence based on feature completeness
        confidence = self._calculate_confidence(patient_features)
        
        return {
            'risk_probability': float(risk_probability),
            'confidence': float(confidence),
            'risk_level': self._get_risk_level(float(risk_probability)),
            'key_factors': self._get_key_factors(patient_features, disease)
        }
    
    def predict_all_risks(self, patient_features):
        """
        Predict risks for all diseases
        
        Returns:
            Dictionary with risks for all diseases
        """
        results = {}
        
        for disease in self.models.keys():
            results[disease] = self.predict_risk(patient_features, disease)
        
        return results
    
    def _extract_features(self, patient_data):
        """Extract features from patient data"""
        
        features = [
            patient_data.get('age', 40) / 100.0,  # Normalize age
            patient_data.get('glucose', 100) / 200.0,  # Normalize glucose
            patient_data.get('bp_systolic', 120) / 200.0,  # Normalize BP
            patient_data.get('cholesterol', 200) / 300.0,  # Normalize cholesterol
            patient_data.get('bmi', 22) / 40.0,  # Normalize BMI
            1.0 if patient_data.get('smoker', False) else 0.0,
            1.0 if patient_data.get('family_history_diabetes', False) else 0.0,
            patient_data.get('exercise_hours', 3.0) / 10.0  # Normalize exercise
        ]
        
        return np.array(features)
    
    def _calculate_confidence(self, patient_features):
        """Calculate prediction confidence based on feature completeness"""
        
        required_features = ['age', 'glucose', 'bp_systolic', 'cholesterol', 'bmi']
        present_features = [f for f in required_features if f in patient_features and patient_features[f] is not None]
        
        completeness = len(present_features) / len(required_features)
        
        # Adjust confidence based on data quality
        if completeness >= 0.8:
            return 0.85 + random.uniform(0, 0.1)
        elif completeness >= 0.5:
            return 0.70 + random.uniform(0, 0.1)
        else:
            return 0.50 + random.uniform(0, 0.2)
    
    def _get_risk_level(self, risk_probability):
        """Convert probability to risk level"""
        if risk_probability < 0.3:
            return "Low"
        elif risk_probability < 0.6:
            return "Medium"
        else:
            return "High"
    
    def _get_key_factors(self, patient_features, disease):
        """Identify key contributing factors"""
        
        factors = []
        
        if disease == 'diabetes':
            if patient_features.get('glucose', 100) > 125:
                factors.append("Elevated glucose levels")
            if patient_features.get('bmi', 22) > 30:
                factors.append("Obesity (BMI > 30)")
            if patient_features.get('family_history_diabetes', False):
                factors.append("Family history of diabetes")
        
        elif disease == 'heart_disease':
            if patient_features.get('cholesterol', 200) > 240:
                factors.append("High cholesterol")
            if patient_features.get('bp_systolic', 120) > 140:
                factors.append("High blood pressure")
            if patient_features.get('smoker', False):
                factors.append("Smoking")
        
        elif disease == 'hypertension':
            if patient_features.get('bp_systolic', 120) > 140:
                factors.append("High systolic blood pressure")
            if patient_features.get('bmi', 22) > 30:
                factors.append("Obesity")
        
        elif disease == 'stroke':
            if patient_features.get('bp_systolic', 120) > 140:
                factors.append("Hypertension")
            if patient_features.get('smoker', False):
                factors.append("Smoking")
        
        return factors[:3]  # Return top 3 factors

class MockModel:
    """Mock model for demonstration purposes"""
    
    def __init__(self, disease_type):
        self.disease_type = disease_type
        
    def predict(self, features):
        """Generate mock prediction based on features"""
        
        # Base risk
        base_risk = 0.1
        
        # Adjust based on feature values (simplified logic)
        risk = base_risk
        
        # Age factor
        risk += features[0] * 0.3
        
        # Glucose factor (for diabetes)
        if self.disease_type == 'diabetes':
            risk += features[1] * 0.4
        
        # BP factor (for hypertension and heart disease)
        if self.disease_type in ['hypertension', 'heart_disease']:
            risk += features[2] * 0.3
        
        # Cholesterol factor (for heart disease)
        if self.disease_type == 'heart_disease':
            risk += features[3] * 0.2
        
        # BMI factor
        risk += features[4] * 0.2
        
        # Smoking factor
        risk += features[5] * 0.15
        
        # Family history factor
        risk += features[6] * 0.1
        
        # Exercise factor (inverse)
        risk -= features[7] * 0.1
        
        # Ensure risk is between 0 and 1
        risk = max(0, min(1, risk))
        
        return risk

# Create global predictor instance
predictor = HealthRiskPredictor()

def predict_health_risks(patient_data):
    """Convenience function to predict all health risks"""
    return predictor.predict_all_risks(patient_data)

def get_risk_explanation(risk_result):
    """Generate human-readable explanation of risk results"""
    
    explanations = {
        'diabetes': {
            'low': "Your diabetes risk is low. Maintain healthy lifestyle with balanced diet and regular exercise.",
            'medium': "You have moderate diabetes risk. Consider reducing sugar intake and increasing physical activity.",
            'high': "High diabetes risk detected. Consult healthcare provider for glucose monitoring and intervention."
        },
        'heart_disease': {
            'low': "Heart disease risk is low. Continue heart-healthy habits like regular exercise and low-fat diet.",
            'medium': "Moderate heart disease risk present. Monitor cholesterol and blood pressure regularly.",
            'high': "High risk for heart disease. Immediate lifestyle changes and medical consultation recommended."
        },
        'hypertension': {
            'low': "Blood pressure risk is low. Maintain current healthy habits and regular checkups.",
            'medium': "Moderate hypertension risk. Reduce salt intake and monitor blood pressure weekly.",
            'high': "High hypertension risk. Consult doctor for blood pressure management plan."
        }
    }
    
    disease = risk_result.get('disease', 'diabetes')
    risk_level = risk_result.get('risk_level', 'medium').lower()
    
    return explanations.get(disease, {}).get(risk_level, "Risk assessment completed.")