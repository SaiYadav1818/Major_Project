from flask import Blueprint, render_template
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import numpy as np

reporting_bp = Blueprint('reporting', __name__)

@reporting_bp.route('/report')
def report():
    # Generate sample data for demonstration
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
