from flask import Blueprint, render_template, request
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import numpy as np

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
    """Display glucose trends for multiple users"""
    
    # Generate sample data for multiple users
    users_data = {}
    user_names = ['User1', 'User2', 'User3']
    base_offsets = [0, 10, -10]
    
    for idx, (user_name, offset) in enumerate(zip(user_names, base_offsets)):
        dates, glucose_levels = generate_user_data(user_seed=42 + idx, base_offset=offset)
        users_data[user_name] = {
            'dates': dates,
            'glucose_levels': glucose_levels,
            'predicted_levels': glucose_levels + np.random.normal(0, 10, len(glucose_levels))
        }
    
    # Create Plotly figure with multiple users
    fig = go.Figure()
    
    colors = ['blue', 'red', 'green']
    for (user_name, data), color in zip(users_data.items(), colors):
        fig.add_trace(go.Scatter(
            x=data['dates'], 
            y=data['glucose_levels'], 
            mode='lines+markers', 
            name=f'{user_name} - Actual',
            line=dict(color=color, width=2)
        ))
    
    fig.update_layout(
        title='Multi-User Glucose Level Trends Comparison',
        xaxis_title='Date',
        yaxis_title='Glucose Level (mg/dL)',
        template='plotly_white',
        hovermode='x unified',
        height=600
    )
    
    # Convert to HTML
    plot_html = pio.to_html(fig, full_html=False)
    
    # Calculate statistics for each user
    user_stats = {}
    for user_name, data in users_data.items():
        user_stats[user_name] = {
            'avg_glucose': round(np.mean(data['glucose_levels']), 1),
            'min_glucose': round(np.min(data['glucose_levels']), 1),
            'max_glucose': round(np.max(data['glucose_levels']), 1),
            'std_dev': round(np.std(data['glucose_levels']), 1)
        }
    
    return render_template('multi_user_report.html', 
                         plot_html=plot_html, 
                         user_stats=user_stats,
                         users=list(users_data.keys()))

@reporting_bp.route('/monitoring-dashboard')
def monitoring_dashboard():
    """Display continuous glucose monitoring dashboard with early detection alerts."""
    return render_template('monitoring_dashboard.html')
