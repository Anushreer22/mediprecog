"""
Utility functions for calculations and data processing
"""

import numpy as np
from datetime import datetime, timedelta
import random

def calculate_disease_risk(age, weight, glucose=100, bp=120, creatinine=1.0):
    """
    Calculate disease risks based on patient metrics
    Returns dictionary of risk percentages
    """
    
    # Diabetes risk calculation
    diabetes_risk = (
        0.05 +  # Base risk
        (age - 30) * 0.005 +  # Age factor
        (weight - 150) * 0.002 +  # Weight factor
        (glucose - 100) * 0.01  # Glucose factor
    )
    
    # Cardiovascular disease risk
    cvd_risk = (
        0.03 +  # Base risk
        (age - 30) * 0.004 +
        (weight - 150) * 0.0015 +
        (bp - 120) * 0.001
    )
    
    # Kidney disease risk
    kidney_risk = (
        0.02 +  # Base risk
        (age - 30) * 0.003 +
        (weight - 150) * 0.001 +
        (creatinine - 1.0) * 0.02
    )
    
    # Cap at 95%
    risks = {
        'diabetes': min(0.95, diabetes_risk),
        'cvd': min(0.95, cvd_risk),
        'kidney': min(0.90, kidney_risk)
    }
    
    # Convert to percentages
    for key in risks:
        risks[key] = round(risks[key] * 100, 1)
    
    return risks

def generate_timeline_projection(current_age, current_risks, years=5):
    """
    Project disease risks over time
    """
    timeline = []
    
    for year in range(1, years + 1):
        age = current_age + year
        year_data = {
            'year': year,
            'age': age,
            'risks': {}
        }
        
        # Project increasing risks over time
        for disease, current_risk in current_risks.items():
            # Risk increases 3-8% per year depending on disease
            annual_increase = {
                'diabetes': 0.05,
                'cvd': 0.04,
                'kidney': 0.03
            }.get(disease, 0.04)
            
            projected_risk = current_risk + (annual_increase * 100 * year)
            year_data['risks'][disease] = min(99, projected_risk)
        
        timeline.append(year_data)
    
    return timeline

def calculate_medical_costs(risks, years=5):
    """
    Estimate medical costs based on risks
    """
    base_cost_per_year = 5000
    
    total_cost = 0
    for year in range(years):
        year_cost = base_cost_per_year
        
        # Add cost based on risks
        for disease, risk in risks.items():
            if risk > 50:
                year_cost += 2000 * (risk / 100)
            elif risk > 30:
                year_cost += 1000 * (risk / 100)
        
        # Apply 5% annual increase
        year_cost *= (1 + 0.05) ** year
        total_cost += year_cost
    
    return round(total_cost)

def calculate_savings_with_intervention(current_costs, risks):
    """
    Calculate potential savings with intervention
    """
    # Calculate reduced costs
    savings_percentage = 0
    
    for disease, risk in risks.items():
        if risk > 70:
            savings_percentage += 0.15
        elif risk > 50:
            savings_percentage += 0.10
        elif risk > 30:
            savings_percentage += 0.05
    
    # Cap at 60% savings
    savings_percentage = min(0.60, savings_percentage)
    
    # Apply savings to each year
    total_savings = 0
    for year_cost in current_costs:
        year_savings = year_cost * savings_percentage
        total_savings += year_savings
    
    return round(total_savings)

def format_currency(amount):
    """Format amount as currency"""
    return f"${amount:,.0f}"

def get_risk_color(percentage):
    """Get color based on risk percentage"""
    if percentage >= 70:
        return '#ff3366'  # Red for high risk
    elif percentage >= 50:
        return '#ffcc00'  # Yellow for medium risk
    else:
        return '#00ff88'  # Green for low risk

def get_prevention_plan(risks):
    """Generate personalized prevention plan based on risks"""
    plan = []
    
    if risks.get('diabetes', 0) > 50:
        plan.extend([
            "Lose 7% body weight (13 lbs)",
            "Exercise 150 minutes/week",
            "Reduce sugar to <25g/day",
            "Increase fiber intake to 30g/day"
        ])
    
    if risks.get('cvd', 0) > 50:
        plan.extend([
            "Omega-3 supplements (1000mg/day)",
            "Stress management (meditation 10min/day)",
            "Regular cholesterol checks",
            "Reduce sodium to <1500mg/day"
        ])
    
    if risks.get('kidney', 0) > 40:
        plan.extend([
            "Increase water to 3L/day",
            "Monitor blood pressure weekly",
            "Reduce protein intake if creatinine high",
            "Avoid NSAIDs"
        ])
    
    # Add general health tips
    plan.extend([
        "Sleep 7-8 hours per night",
        "Regular health check-ups every 6 months",
        "Maintain healthy BMI (18.5-24.9)",
        "Limit alcohol to 1 drink/day"
    ])
    
    return plan[:8]  # Return top 8 recommendations