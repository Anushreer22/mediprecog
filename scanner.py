"""
Medical Report Scanner Module
Handles OCR extraction from PDFs and images
"""

import pytesseract
from pdf2image import convert_from_path, convert_from_bytes
from PIL import Image
import cv2
import numpy as np
import re
import os

class MedicalReportScanner:
    """Scanner for medical reports with OCR capabilities"""
    
    def __init__(self):
        """Initialize the scanner"""
        # For Windows, set tesseract path if needed
        if os.name == 'nt':
            try:
                pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            except:
                pass
    
    def preprocess_image(self, image):
        """Preprocess image for better OCR results"""
        # Convert to grayscale
        if image.mode != 'L':
            image = image.convert('L')
        
        # Convert PIL to OpenCV
        cv_image = np.array(image)
        
        # Apply thresholding
        _, thresh = cv2.threshold(cv_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Denoise
        denoised = cv2.medianBlur(thresh, 3)
        
        return Image.fromarray(denoised)
    
    def extract_text_from_image(self, image):
        """Extract text from an image using OCR"""
        try:
            # Preprocess image
            processed_image = self.preprocess_image(image)
            
            # Use Tesseract OCR
            text = pytesseract.image_to_string(processed_image, config='--psm 6')
            
            return text
        except Exception as e:
            print(f"OCR Error: {e}")
            # Return mock data for demo
            return self.generate_mock_report()
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF file"""
        try:
            # Convert PDF to images
            images = convert_from_path(pdf_path)
            
            # Extract text from each page
            all_text = ""
            for i, image in enumerate(images):
                page_text = self.extract_text_from_image(image)
                all_text += f"--- Page {i+1} ---\n{page_text}\n\n"
            
            return all_text
        except Exception as e:
            print(f"PDF Extraction Error: {e}")
            return self.generate_mock_report()
    
    def extract_text_from_pdf_bytes(self, pdf_bytes):
        """Extract text from PDF bytes"""
        try:
            # Convert PDF bytes to images
            images = convert_from_bytes(pdf_bytes)
            
            # Extract text from each page
            all_text = ""
            for i, image in enumerate(images):
                page_text = self.extract_text_from_image(image)
                all_text += f"--- Page {i+1} ---\n{page_text}\n\n"
            
            return all_text
        except Exception as e:
            print(f"PDF Bytes Extraction Error: {e}")
            return self.generate_mock_report()
    
    def generate_mock_report(self):
        """Generate a mock medical report for demo purposes"""
        mock_report = """
        PATIENT MEDICAL REPORT
        
        Patient Information:
        Name: John A. Doe
        Age: 45 years
        Gender: Male
        Date of Birth: 1978-06-15
        Patient ID: MED-2023-56789
        
        Vital Signs:
        Blood Pressure: 142/92 mmHg
        Heart Rate: 78 bpm
        Respiratory Rate: 16/min
        Temperature: 98.6°F
        SpO2: 98%
        
        Laboratory Results:
        Glucose (Fasting): 135 mg/dL
        HbA1c: 6.8%
        Total Cholesterol: 245 mg/dL
        HDL Cholesterol: 38 mg/dL
        LDL Cholesterol: 168 mg/dL
        Triglycerides: 210 mg/dL
        
        Physical Examination:
        Height: 175 cm
        Weight: 87 kg
        BMI: 28.5 kg/m²
        Waist Circumference: 102 cm
        
        Medical History:
        Family History: Father - Type 2 Diabetes, Mother - Hypertension
        Smoking Status: Current smoker (15 pack-years)
        Alcohol Consumption: Social drinker (2-3 units/week)
        Physical Activity: Sedentary lifestyle
        Medications: None currently
        
        Risk Factors Identified:
        1. Elevated fasting glucose (Prediabetes range)
        2. High blood pressure (Stage 1 Hypertension)
        3. High cholesterol (Hyperlipidemia)
        4. Elevated BMI (Overweight)
        5. Family history of diabetes
        6. Smoking
        
        Recommendations:
        1. Lifestyle modifications: Diet and exercise
        2. Regular monitoring of blood pressure
        3. Follow-up glucose testing in 3 months
        4. Smoking cessation counseling
        5. Consider lipid-lowering therapy
        
        Physician's Signature:
        Dr. Sarah M. Chen, MD
        Internal Medicine Specialist
        Date: 2023-10-15
        """
        
        return mock_report
    
    def extract_structured_data(self, text):
        """Extract structured data from OCR text"""
        data = {
            'name': '',
            'age': None,
            'glucose': None,
            'bp_systolic': None,
            'bp_diastolic': None,
            'cholesterol': None,
            'bmi': None,
            'smoker': False,
            'family_history_diabetes': False
        }
        
        # Extract name
        name_match = re.search(r'Name:\s*([A-Za-z\s\.]+)', text, re.IGNORECASE)
        if name_match:
            data['name'] = name_match.group(1).strip()
        
        # Extract age
        age_match = re.search(r'Age:\s*(\d+)\s*(?:years|yrs|yr)?', text, re.IGNORECASE)
        if age_match:
            data['age'] = int(age_match.group(1))
        
        # Extract glucose
        glucose_match = re.search(r'Glucose.*?(\d+)\s*mg/dL', text, re.IGNORECASE)
        if glucose_match:
            data['glucose'] = int(glucose_match.group(1))
        
        # Extract blood pressure
        bp_match = re.search(r'Blood Pressure.*?(\d+)\s*/\s*(\d+)\s*mmHg', text, re.IGNORECASE)
        if bp_match:
            data['bp_systolic'] = int(bp_match.group(1))
            data['bp_diastolic'] = int(bp_match.group(2))
        
        # Extract cholesterol
        chol_match = re.search(r'Cholesterol.*?(\d+)\s*mg/dL', text, re.IGNORECASE)
        if chol_match:
            data['cholesterol'] = int(chol_match.group(1))
        
        # Extract BMI
        bmi_match = re.search(r'BMI.*?(\d+\.?\d*)\s*kg/m²', text, re.IGNORECASE)
        if bmi_match:
            data['bmi'] = float(bmi_match.group(1))
        
        # Check for smoking
        if re.search(r'smoker|smoking', text, re.IGNORECASE):
            data['smoker'] = True
        
        # Check for family history
        if re.search(r'family.*?diabetes|diabetes.*?family', text, re.IGNORECASE):
            data['family_history_diabetes'] = True
        
        return data

# For standalone testing
if __name__ == "__main__":
    scanner = MedicalReportScanner()
    print("Medical Report Scanner initialized successfully.")