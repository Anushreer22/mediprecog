"""
Configuration and constants for MediPrecog
"""

import os
from datetime import datetime

# Application Configuration
APP_NAME = "MediPrecog"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Predictive Health Risk Analysis Platform"
DEVELOPER = "Healthcare Hackathon Team"
CONTACT_EMAIL = "hello@mediprecog.com"

# File Paths
DATA_DIR = "data"
MODELS_DIR = "models"
REPORTS_DIR = "reports"

# Create directories if they don't exist
for directory in [DATA_DIR, MODELS_DIR, REPORTS_DIR]:
    os.makedirs(directory, exist_ok=True)

# Medical Constants
RISK_THRESHOLDS = {
    'diabetes': {
        'low': 0.3,      # < 30% risk
        'medium': 0.6,   # 30-60% risk
        'high': 0.6      # > 60% risk
    },
    'heart_disease': {
        'low': 0.25,
        'medium': 0.5,
        'high': 0.5
    },
    'hypertension': {
        'low': 0.3,
        'medium': 0.6,
        'high': 0.6
    },
    'stroke': {
        'low': 0.2,
        'medium': 0.4,
        'high': 0.4
    }
}

HEALTH_RANGES = {
    'glucose': {
        'normal': (70, 100),
        'prediabetes': (100, 125),
        'diabetes': (125, 999)
    },
    'blood_pressure': {
        'normal': (90, 120),
        'elevated': (120, 130),
        'hypertension_stage1': (130, 140),
        'hypertension_stage2': (140, 180)
    },
    'cholesterol': {
        'desirable': (0, 200),
        'borderline': (200, 240),
        'high': (240, 999)
    },
    'bmi': {
        'underweight': (0, 18.5),
        'normal': (18.5, 25),
        'overweight': (25, 30),
        'obese': (30, 999)
    }
}

# Color Scheme
COLORS = {
    'primary': '#1a73e8',
    'secondary': '#34a853',
    'accent': '#ff6b6b',
    'warning': '#ffa726',
    'success': '#4caf50',
    'danger': '#f44336',
    'info': '#2196f3',
    
    # Risk levels
    'risk_low': '#4caf50',
    'risk_medium': '#ffa726',
    'risk_high': '#f44336',
    
    # Timeline
    'timeline_now': '#1a73e8',
    'timeline_future': '#34a853',
    'timeline_critical': '#f44336'
}

# UI Text
UI_TEXT = {
    'app_title': "🏥 MEDIPRECOG - Health Time Machine",
    'app_subtitle': "Predicting Health Risks Before They Become Diseases",
    
    'problems': [
        ("Late Detection", "Diseases caught too late for effective intervention"),
        ("Underused Data", "Medical reports contain insights that go unanalyzed"),
        ("Patient Confusion", "Complex data leaves patients anxious and unsure"),
        ("High Costs", "Late treatment costs 5-10x more than prevention")
    ],
    
    'solutions': [
        ("Predictive Analytics", "Identify risks 3-5 years before symptoms"),
        ("Intelligent Scanning", "Extract and analyze every piece of data"),
        ("Visual Clarity", "Transform data into clear, actionable insights"),
        ("Cost Prevention", "Save thousands in healthcare costs")
    ],
    
    'features': [
        "Medical Report Scanner",
        "Disease Risk Predictor",
        "Timeline Projections",
        "Future Simulator",
        "Cost Calculator",
        "Personalized Action Plan"
    ]
}

# Business Configuration
BUSINESS = {
    'pricing_tiers': {
        'free': {
            'price': 0,
            'features': ['Basic scanning', 'Risk assessment', 'Basic timeline'],
            'patients': 10
        },
        'professional': {
            'price': 99,
            'features': ['Advanced scanning', 'Detailed reports', 'Future simulator', 'Cost calculator'],
            'patients': 100
        },
        'enterprise': {
            'price': 999,
            'features': ['Unlimited scanning', 'API access', 'Custom models', 'Priority support'],
            'patients': 'Unlimited'
        }
    },
    
    'revenue_streams': [
        {"name": "Hospital Licensing", "revenue": 2500000, "margin": 0.85},
        {"name": "Insurance Partnerships", "revenue": 3200000, "margin": 0.75},
        {"name": "Corporate Wellness", "revenue": 1500000, "margin": 0.80},
        {"name": "Direct Subscriptions", "revenue": 1800000, "margin": 0.70}
    ],
    
    'market_size': {
        'hospitals': 5000,
        'clinics': 25000,
        'insurance_companies': 50,
        'corporations': 500,
        'individuals': 10000000
    }
}

# Export settings
EXPORT_FORMATS = ['PDF', 'CSV', 'JSON', 'HTML']
REPORT_TEMPLATES = ['basic', 'detailed', 'executive']

# Validation rules
VALIDATION_RULES = {
    'age': (0, 120),
    'glucose': (20, 1000),
    'bp_systolic': (50, 250),
    'bp_diastolic': (30, 150),
    'cholesterol': (50, 500),
    'bmi': (10, 60)
}

# Cache settings
CACHE_TTL = 3600  # 1 hour in seconds
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

def get_current_year():
    """Get current year for reports"""
    return datetime.now().year

def get_app_metadata():
    """Get application metadata"""
    return {
        'name': APP_NAME,
        'version': APP_VERSION,
        'description': APP_DESCRIPTION,
        'developer': DEVELOPER,
        'year': get_current_year()
    }