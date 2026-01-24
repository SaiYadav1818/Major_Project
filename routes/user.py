from flask import Blueprint, request, render_template, redirect, url_for
from models.ai_model import glucose_predictor
from models.recommendation import recommendation_engine
from models.alert import alert_system
import plotly.graph_objects as go
import plotly.io as pio
import datetime

user_bp = Blueprint('user', __name__)

# Global list to store previous glucose predictions
previous_glucose_data = []

@user_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        age = float(request.form['age'])
        bmi = float(request.form['bmi'])
        insulin_intake = float(request.form['insulin_intake'])
        blood_pressure = float(request.form['blood_pressure'])
        diabetes_status = int(request.form['diabetes_status'])

        # Predict glucose level
        predicted_glucose = glucose_predictor.predict_glucose(
            age, bmi, insulin_intake, blood_pressure, diabetes_status
        )

        # Generate recommendations
        recommendations = recommendation_engine.generate_recommendations(
            predicted_glucose, age, bmi, diabetes_status
        )

        # Check for alerts
        alerts = alert_system.check_alerts(predicted_glucose)

        return render_template('results.html',
                             predicted_glucose=round(predicted_glucose, 1),
                             recommendations=recommendations,
                             alerts=alerts)

    return render_template('index.html')

@user_bp.route('/results')
def results():
    return render_template('results.html')
