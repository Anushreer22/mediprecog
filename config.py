"""
Configuration file for MediPrecog
"""

# Colors
COLORS = {
    'primary': '#00ff88',
    'secondary': '#00ccff',
    'danger': '#ff3366',
    'warning': '#ffcc00',
    'dark_bg': '#0c0c1d',
    'light_bg': '#1a1a2e',
    'text': '#f0f0f0',
    'text_secondary': '#aaaaaa'
}

# Disease parameters
DISEASE_PARAMS = {
    'diabetes': {
        'base_risk': 0.05,
        'weight_factor': 0.002,
        'age_factor': 0.005,
        'glucose_factor': 0.01
    },
    'cvd': {
        'base_risk': 0.03,
        'weight_factor': 0.0015,
        'age_factor': 0.004,
        'bp_factor': 0.015
    },
    'kidney': {
        'base_risk': 0.02,
        'weight_factor': 0.001,
        'age_factor': 0.003,
        'creatinine_factor': 0.02
    }
}

# Time projections
TIME_HORIZONS = [1, 3, 5, 10]  # years