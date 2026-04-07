#!/usr/bin/env python3
"""Test chart generation"""
import sys
sys.path.insert(0, '.')
from models.patient import patient_manager
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np

patient_id = 'PT-150147B924E7'
health_records = patient_manager.get_patient_predictions(patient_id, days=30)

if health_records:
    health_records = list(reversed(health_records))
    dates = [record[0] for record in health_records]
    predicted_glucose = np.array([float(record[1]) for record in health_records])
    actual_glucose = predicted_glucose - np.random.normal(0, 5, len(health_records))
    actual_glucose = np.clip(actual_glucose, 70, 250)
    
    print(f'Dates: {dates}')
    print(f'Predicted: {predicted_glucose}')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=actual_glucose, mode='lines+markers', name='Actual'))
    fig.add_trace(go.Scatter(x=dates, y=predicted_glucose, mode='lines+markers', name='Predicted'))
    
    plot_html = pio.to_html(fig, full_html=False)
    
    print(f'Plot HTML length: {len(plot_html)}')
    print(f'Contains plotly: {"plotly" in plot_html.lower()}')
    print(f'Contains div: {"<div" in plot_html}')
    print(f'\nFirst 800 chars:\n{plot_html[:800]}')
    
    # Save to file for inspection
    with open('test_plot.html', 'w') as f:
        f.write(plot_html)
    print('\nSaved to test_plot.html')
else:
    print('No records found')
