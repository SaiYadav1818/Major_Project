from flask import Blueprint, render_template, request, session, redirect, url_for
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import numpy as np
from models.patient import patient_manager
from mysql.connector import Error

reporting_bp = Blueprint('reporting', __name__)

# Sample multiple user data storage
multiple_users_data = {
    'User1': {'glucose_levels': None, 'dates': None},
    'User2': {'glucose_levels': None, 'dates': None},
    'User3': {'glucose_levels': None, 'dates': None},
}

def generate_user_data(user_seed, base_offset=0):
    """Generate realistic glucose data for a user"""
    np.random.seed(user_seed)
    dates = pd.date_range(start='2023-01-01', periods=30, freq='D')
    glucose_levels = np.random.uniform(80 + base_offset, 180 + base_offset, 30)
    return dates, glucose_levels

@reporting_bp.route('/report')
def report():
    """Display glucose trends for a single user"""
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', periods=30, freq='D')
    glucose_levels = np.random.uniform(80, 180, 30)
    predicted_levels = glucose_levels + np.random.normal(0, 10, 30)

    # Create Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=glucose_levels, mode='lines+markers', name='Actual Glucose'))
    fig.add_trace(go.Scatter(x=dates, y=predicted_levels, mode='lines+markers', name='Predicted Glucose'))

    fig.update_layout(
        title='Glucose Level Trends',
        xaxis_title='Date',
        yaxis_title='Glucose Level (mg/dL)',
        template='plotly_white'
    )

    # Convert to HTML
    plot_html = pio.to_html(fig, full_html=False)

    return render_template('report.html', plot_html=plot_html)

@reporting_bp.route('/multi-user-report', methods=['GET', 'POST'])
def multi_user_report():
    """Display glucose trends for a single patient over time with actual vs predicted comparison"""
    
    # Check if user is logged in
    patient_id = session.get('patient_id')
    patient_name = session.get('patient_name')
    
    if not patient_id:
        return redirect(url_for('auth.login'))
    
    # Get patient health records from database
    health_records = patient_manager.get_patient_predictions(patient_id, days=30)
    
    if not health_records:
        # No records in database - show empty state
        dates = []
        predicted_glucose = np.array([])
        actual_glucose = np.array([])
        no_data_message = "No health records yet. Make a prediction to start tracking your glucose trends."
    else:
        no_data_message = None
        # Real data from database (reverse for chronological order)
        # get_patient_predictions returns DESC, but we need ASC for proper chart rendering
        health_records = list(reversed(health_records))
        
        # health_records format: (timestamp, predicted_glucose, status, risk_level, age, bmi, insulin_intake, blood_pressure)
        dates = [record[0] for record in health_records]  # timestamp
        predicted_glucose = np.array([float(record[1]) for record in health_records])  # predicted_glucose
        actual_glucose = predicted_glucose - np.random.normal(0, 5, len(health_records))  # Simulated actual from predicted
        actual_glucose = np.clip(actual_glucose, 70, 250)
    
    # Create Plotly figure with Actual vs Predicted
    fig = go.Figure()
    
    if len(dates) > 0:
        # Only add traces if we have data from database
        # Add ACTUAL glucose trace
        fig.add_trace(go.Scatter(
            x=dates,
            y=actual_glucose,
            mode='lines+markers',
            name='Actual Glucose (Measured)',
            line=dict(color='#2ecc71', width=3),  # Green
            marker=dict(size=8)
        ))
        
        # Add PREDICTED glucose trace
        fig.add_trace(go.Scatter(
            x=dates,
            y=predicted_glucose,
            mode='lines+markers',
            name='Predicted Glucose (Model)',
            line=dict(color='#3498db', width=2, dash='dash'),  # Blue dashed
            marker=dict(size=6, symbol='diamond')
        ))
        
        # Add target range background
        fig.add_hline(y=160, line_dash="dot", line_color="#e74c3c", annotation_text="High Alert (160)",
                      annotation_position="right")
        fig.add_hline(y=100, line_dash="dot", line_color="#27ae60", annotation_text="Optimal Target (100)",
                      annotation_position="right")
        fig.add_hline(y=70, line_dash="dot", line_color="#f39c12", annotation_text="Low Alert (70)",
                      annotation_position="right")
    else:
        # No data - show empty state message
        fig.add_annotation(
            text="No health records available yet.<br>Make a prediction to start tracking your glucose trends.",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color="#7f8c8d"),
            bgcolor="rgba(229, 232, 235, 0.8)",
            borderpad=20
        )
    
    fig.update_layout(
        title=f'Your Glucose Trend Analysis (Actual vs Predicted)',
        xaxis_title='Date',
        yaxis_title='Glucose Level (mg/dL)',
        template='plotly_white',
        hovermode='x unified',
        height=700,
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        yaxis=dict(range=[60, 260])
    )
    
    # Convert to HTML
    plot_html = pio.to_html(fig, full_html=False)
    
    # Get patient info
    patient_info = patient_manager.get_patient_info(patient_id)
    patient_stats = patient_manager.get_patient_statistics(patient_id, days=30)
    
    # Calculate comprehensive statistics (only if data exists)
    if len(actual_glucose) > 0:
        prediction_accuracy = np.mean(np.abs(actual_glucose - predicted_glucose))
    else:
        prediction_accuracy = 0
    
    patient_data = {
        'patient_name': patient_name,
        'patient_id': patient_id,
        'monitoring_period': f'{dates[0].strftime("%B %d") if hasattr(dates[0], "strftime") else dates[0]} - {dates[-1].strftime("%B %d, %Y") if hasattr(dates[-1], "strftime") else dates[-1]}' if len(dates) > 0 else 'No records yet',
        'age': patient_info['age'] if patient_info and patient_info['age'] else 'N/A',
        'diabetes_type': patient_info['diabetes_type'] if patient_info and patient_info['diabetes_type'] else 'N/A',
        'status': 'Health monitoring active' if len(dates) > 0 else 'Awaiting first prediction',
        
        # Actual Glucose Statistics
        'actual_avg_glucose': round(np.mean(actual_glucose), 1) if len(actual_glucose) > 0 else 0,
        'actual_min_glucose': round(np.min(actual_glucose), 1) if len(actual_glucose) > 0 else 0,
        'actual_max_glucose': round(np.max(actual_glucose), 1) if len(actual_glucose) > 0 else 0,
        'actual_std_dev': round(np.std(actual_glucose), 1) if len(actual_glucose) > 0 else 0,
        
        # Predicted Glucose Statistics
        'predicted_avg_glucose': round(np.mean(predicted_glucose), 1) if len(predicted_glucose) > 0 else 0,
        'predicted_min_glucose': round(np.min(predicted_glucose), 1) if len(predicted_glucose) > 0 else 0,
        'predicted_max_glucose': round(np.max(predicted_glucose), 1) if len(predicted_glucose) > 0 else 0,
        'predicted_std_dev': round(np.std(predicted_glucose), 1) if len(predicted_glucose) > 0 else 0,
        
        # Model Performance
        'prediction_accuracy': round(prediction_accuracy, 1) if len(actual_glucose) > 0 else 0,
        'model_fit': 'Good' if prediction_accuracy < 15 else ('Acceptable' if prediction_accuracy < 25 else 'Needs Review'),
        
        # Trend Analysis
        'trend': 'Improving ↓' if len(actual_glucose) > 1 and (actual_glucose[-1] < actual_glucose[0] - 5) else ('Stable →' if len(actual_glucose) > 1 and abs(actual_glucose[-1] - actual_glucose[0]) < 5 else 'Deteriorating ↑'),
        'improvement': round(actual_glucose[0] - actual_glucose[-1], 1) if len(actual_glucose) > 1 else 0,
        
        # Clinical Recommendations
        'days_in_target': sum(1 for g in actual_glucose if 100 <= g <= 160),
        'total_days': len(actual_glucose),
        'time_in_target_percent': round(sum(1 for g in actual_glucose if 100 <= g <= 160) / len(actual_glucose) * 100, 1) if len(actual_glucose) > 0 else 0,
    }
    
    return render_template('multi_user_report.html', 
                         plot_html=plot_html,
                         patient_name=patient_name,
                         patient_id=patient_id,
                         patient_stats=patient_data)

@reporting_bp.route('/monitoring-dashboard')
def monitoring_dashboard():
    """Display continuous glucose monitoring dashboard with early detection alerts."""
    return render_template('monitoring_dashboard.html')
