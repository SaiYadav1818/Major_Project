from flask import Blueprint, request, render_template, redirect, url_for, session
from models.ai_model import glucose_predictor
from models.recommendation import recommendation_engine
from models.alert import alert_system
from models.patient import patient_manager
import plotly.graph_objects as go
import plotly.io as pio
import datetime
import os

user_bp = Blueprint('user', __name__)

def login_required(f):
    """Decorator to require login"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'patient_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# Clinical value ranges (mg/dL, and other units)
CLINICAL_RANGES = {
    'age': {'min': 1, 'max': 120, 'unit': 'years'},
    'bmi': {'min': 10, 'max': 70, 'unit': 'kg/m²'},
    'insulin_intake': {'min': 0, 'max': 300, 'unit': 'units'},
    'blood_pressure': {'min': 60, 'max': 250, 'unit': 'mmHg'},
    'glucose': {'min': 40, 'max': 400, 'unit': 'mg/dL'}
}

def validate_input(age, bmi, insulin_intake, blood_pressure, diabetes_status):
    """
    Validate clinical parameters against medical ranges.
    Returns: (is_valid, error_message)
    """
    try:
        age = float(age)
        bmi = float(bmi)
        insulin_intake = float(insulin_intake)
        blood_pressure = float(blood_pressure)
        diabetes_status = int(diabetes_status)
    except (ValueError, TypeError):
        return False, "Invalid input format. All values must be numeric."
    
    # Validate age
    if not CLINICAL_RANGES['age']['min'] <= age <= CLINICAL_RANGES['age']['max']:
        return False, f"Age must be between {CLINICAL_RANGES['age']['min']}-{CLINICAL_RANGES['age']['max']} years."
    
    # Validate BMI
    if not CLINICAL_RANGES['bmi']['min'] <= bmi <= CLINICAL_RANGES['bmi']['max']:
        return False, f"BMI must be between {CLINICAL_RANGES['bmi']['min']}-{CLINICAL_RANGES['bmi']['max']} kg/m²."
    
    # Validate Insulin Intake
    if not CLINICAL_RANGES['insulin_intake']['min'] <= insulin_intake <= CLINICAL_RANGES['insulin_intake']['max']:
        return False, f"Insulin intake must be between {CLINICAL_RANGES['insulin_intake']['min']}-{CLINICAL_RANGES['insulin_intake']['max']} units."
    
    # Validate Blood Pressure
    if not CLINICAL_RANGES['blood_pressure']['min'] <= blood_pressure <= CLINICAL_RANGES['blood_pressure']['max']:
        return False, f"Blood pressure must be between {CLINICAL_RANGES['blood_pressure']['min']}-{CLINICAL_RANGES['blood_pressure']['max']} mmHg."
    
    # Validate Diabetes Status
    if diabetes_status not in [0, 1]:
        return False, "Diabetes status must be 0 (Non-diabetic) or 1 (Diabetic)."
    
    return True, None


# Global list to store previous glucose predictions
previous_glucose_data = []

# Global list to store previous glucose predictions
previous_glucose_data = []

@user_bp.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    """Predict glucose level for logged-in patient"""
    patient_id = session.get('patient_id')
    patient_name = session.get('patient_name')
    error_message = None
    warning_message = None
    
    if request.method == 'POST':
        try:
            # Get form data
            age = request.form.get('age', '').strip()
            bmi = request.form.get('bmi', '').strip()
            insulin_intake = request.form.get('insulin_intake', '').strip()
            blood_pressure = request.form.get('blood_pressure', '').strip()
            diabetes_status = request.form.get('diabetes_status', '').strip()
            
            # Import age validation function
            from models.patient import validate_age
            
            # Get patient's registered date of birth
            patient_info = patient_manager.get_patient_info(patient_id)
            if not patient_info:
                error_message = "❌ Could not retrieve your patient information"
                return render_template('user/predict.html', error=error_message, patient_name=patient_name)
            
            # Validate age against DOB
            age_valid, calculated_age, age_error = validate_age(patient_info.get('date_of_birth'), age)
            
            if not age_valid:
                error_message = f"❌ Age Validation Failed: {age_error}"
                return render_template('user/predict.html', error=error_message, patient_name=patient_name)
            
            # Validate other inputs
            is_valid, error_message = validate_input(age, bmi, insulin_intake, blood_pressure, diabetes_status)
            
            if not is_valid:
                return render_template('user/predict.html', error=error_message, patient_name=patient_name)
            
            # Convert to appropriate types after validation
            age = float(age)
            bmi = float(bmi)
            insulin_intake = float(insulin_intake)
            blood_pressure = float(blood_pressure)
            diabetes_status = int(diabetes_status)

            # Predict glucose level
            predicted_glucose = glucose_predictor.predict_glucose(
                age, bmi, insulin_intake, blood_pressure, diabetes_status
            )

            # Get clinical assessment
            clinical_assessment = glucose_predictor.get_clinical_assessment(predicted_glucose)

            # Generate recommendations
            recommendations = recommendation_engine.generate_recommendations(
                predicted_glucose, age, bmi, diabetes_status
            )

            # Check for alerts
            alerts = alert_system.check_alerts(predicted_glucose, diabetes_status)

            # Get model metrics for explainability
            model_metrics = glucose_predictor.get_model_metrics()
            
            # Get feature importance
            feature_importance = glucose_predictor.get_feature_importance_dict()
            
            # Calculate total importance for percentage normalization
            total_importance = sum(feature_importance.values()) if feature_importance else 1
            feature_importance_percent = {
                feature: (importance / total_importance) * 100 
                for feature, importance in feature_importance.items()
            } if feature_importance else {}
            
            # Save prediction to PATIENT database
            patient_manager.save_patient_prediction(
                patient_id, age, bmi, insulin_intake, blood_pressure, 
                diabetes_status, predicted_glucose, clinical_assessment['status'], 
                clinical_assessment['risk_level']
            )

            return render_template('user/results.html',
                                 patient_name=patient_name,
                                 predicted_glucose=round(predicted_glucose, 1),
                                 clinical_status=clinical_assessment['status'],
                                 clinical_recommendation=clinical_assessment['clinical_recommendation'],
                                 risk_level=clinical_assessment['risk_level'],
                                 recommendations=recommendations,
                                 alerts=alerts,
                                 model_metrics=model_metrics,
                                 feature_importance=feature_importance_percent,
                                 input_data={
                                     'age': age,
                                     'bmi': bmi,
                                     'insulin_intake': insulin_intake,
                                     'blood_pressure': blood_pressure
                                 })
        
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}. Please try again."
            return render_template('user/predict.html', error=error_message, patient_name=patient_name)

    return render_template('user/predict.html', error=error_message, patient_name=patient_name)

