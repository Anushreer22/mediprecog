"""
Medical report scanner module
(Mocked for hackathon demo)
"""

import os
from datetime import datetime
from PIL import Image
import pandas as pd

class MedicalReportScanner:
    """Mock scanner for medical reports"""
    
    def __init__(self):
        self.supported_formats = ['.pdf', '.jpg', '.png', '.jpeg', '.txt', '.docx']
        self.scan_date = datetime.now()
    
    def scan_report(self, file_path):
        """Mock scanning of medical report"""
        # In real implementation, this would use OCR/text extraction
        # For hackathon, return mock data
        
        file_ext = os.path.splitext(file_path)[1].lower()
        
        mock_data = {
            'file_type': file_ext[1:].upper() if file_ext else 'UNKNOWN',
            'scan_date': self.scan_date.strftime('%Y-%m-%d %H:%M'),
            'pages': 1,
            'extracted_data': self.generate_mock_extraction(file_ext)
        }
        
        return mock_data
    
    def generate_mock_extraction(self, file_type):
        """Generate mock extracted data based on file type"""
        
        if file_type in ['.pdf', '.jpg', '.png', '.jpeg']:
            # Mock lab report
            return {
                'type': 'Lab Report',
                'patient_id': 'PAT-2024-001',
                'date': '2024-02-10',
                'lab_name': 'MediLabs Diagnostics',
                'results': {
                    'Glucose': {'value': 108, 'unit': 'mg/dL', 'normal_range': '70-100'},
                    'Creatinine': {'value': 1.1, 'unit': 'mg/dL', 'normal_range': '0.7-1.2'},
                    'Cholesterol': {'value': 215, 'unit': 'mg/dL', 'normal_range': '<200'},
                    'HDL': {'value': 42, 'unit': 'mg/dL', 'normal_range': '>40'},
                    'LDL': {'value': 148, 'unit': 'mg/dL', 'normal_range': '<100'},
                    'Triglycerides': {'value': 185, 'unit': 'mg/dL', 'normal_range': '<150'},
                    'HbA1c': {'value': 5.9, 'unit': '%', 'normal_range': '4.0-5.6'}
                },
                'interpretation': 'Elevated glucose and cholesterol levels detected.'
            }
        
        elif file_type == '.txt':
            # Mock doctor notes
            return {
                'type': 'Doctor Notes',
                'patient': 'John Doe',
                'date': '2024-02-10',
                'doctor': 'Dr. Sarah Chen, MD',
                'notes': """
Patient presents with fatigue and increased thirst.
Blood pressure: 138/88 mmHg
Weight: 185 lbs, BMI: 27.8
Family history: Father with Type 2 Diabetes
Recommendations: 
1. Follow up in 3 months for glucose test
2. Begin lifestyle modifications
3. Monitor blood pressure at home
                """,
                'diagnosis_codes': ['R53.83', 'R63.1']
            }
        
        elif file_type == '.docx':
            # Mock ECG report
            return {
                'type': 'ECG Report',
                'patient': 'John Doe',
                'date': '2024-02-10',
                'technician': 'Michael Rodriguez, RCVT',
                'findings': """
Normal sinus rhythm
Heart rate: 72 bpm
PR interval: 160 ms
QRS duration: 88 ms
QT interval: 410 ms
No significant ST segment changes
No arrhythmias detected
                """,
                'impression': 'Normal ECG. No acute abnormalities detected.'
            }
        
        else:
            return {
                'type': 'Unknown Document',
                'message': 'Document scanned successfully. Content analysis required.'
            }
    
    def extract_metrics(self, scan_data):
        """Extract health metrics from scanned data"""
        metrics = {
            'age': 35,
            'weight': 185,
            'glucose': 100,
            'cholesterol': 200,
            'creatinine': 1.0,
            'bp_systolic': 120,
            'bp_diastolic': 80
        }
        
        # Update with scanned data if available
        if 'results' in scan_data.get('extracted_data', {}):
            results = scan_data['extracted_data']['results']
            
            if 'Glucose' in results:
                metrics['glucose'] = results['Glucose']['value']
            
            if 'Creatinine' in results:
                metrics['creatinine'] = results['Creatinine']['value']
            
            if 'Cholesterol' in results:
                metrics['cholesterol'] = results['Cholesterol']['value']
        
        return metrics
    
    def validate_file(self, file_path):
        """Validate uploaded file"""
        if not os.path.exists(file_path):
            return False, "File does not exist"
        
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext not in self.supported_formats:
            return False, f"Unsupported file format. Supported: {', '.join(self.supported_formats)}"
        
        # Check file size (mock)
        file_size = os.path.getsize(file_path)
        if file_size > 200 * 1024 * 1024:  # 200MB
            return False, "File too large. Max size: 200MB"
        
        return True, "File validated successfully"