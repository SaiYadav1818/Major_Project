# Quick Start Guide - AI Glycemic Control System

## Installation & Setup

### 1. Prerequisites
- Python 3.8 or higher
- pip package manager
- Modern web browser

### 2. Installation Steps

```bash
# Navigate to project directory
cd c:\Users\dudim\Major_Project

# Install required dependencies
pip install -r requirements.txt

# Run the Flask application
python app.py
```

### 3. Access the Application
- Open your browser and navigate to: `http://localhost:5000`
- The application will be running on Flask's debug server

---

## Feature Overview

### Main Dashboard (`/`)
**Purpose**: Patient health data input and glucose prediction

**How to Use**:
1. Enter your health data:
   - Age (years)
   - BMI (kg/m²)
   - Insulin Intake (units)
   - Blood Pressure (mmHg, systolic)
   - Diabetes Status (0 or 1)
2. Click "Predict Glucose Level"
3. View your personalized results

**What You'll Get**:
- Predicted glucose level (mg/dL)
- Clinical status and risk level
- Real-time early detection alerts
- Personalized treatment recommendations
- Model performance metrics
- Feature importance (explainability)

---

### Results Page (`/results`)
**Purpose**: Comprehensive clinical assessment and recommendations

**Displays**:
- 🔴 Glucose Level with color-coded status
- ⚠️ Multi-level alerts (CRITICAL, WARNING, EARLY_WARNING)
- 💊 Personalized treatment recommendations
- 📊 Model performance metrics (MSE, MAE, RMSE, R²)
- 🔍 Feature importance for explainability
- 📈 Glucose trend chart
- 📋 Clinical summary and risk assessment

**Alert Levels**:
- **CRITICAL**: Requires immediate medical attention (≤54 or ≥250 mg/dL)
- **WARNING**: Urgent review needed (54-70 or 180-250 mg/dL)
- **EARLY WARNING**: Preventive measures recommended (100-70 or 160-180 mg/dL)
- **OK**: Optimal glucose range (100-160 mg/dL)

---

### Single User Report (`/reporting/report`)
**Purpose**: Glucose trends for individual patient

**Features**:
- 30-day glucose trend visualization
- Actual vs. predicted glucose comparison
- Interactive Plotly chart
- Historical trend analysis

---

### Multi-User Report (`/reporting/multi-user-report`)
**Purpose**: Comparative analysis across multiple patients

**Features**:
- Compare 3 sample users' glucose patterns
- Color-coded trend lines for easy identification
- Individual statistics:
  - Average glucose
  - Minimum glucose
  - Maximum glucose
  - Standard deviation (variability)
- Unified hover information
- Population health insights

---

### Continuous Monitoring Dashboard (`/reporting/monitoring-dashboard`)
**Purpose**: Real-time continuous glucose monitoring

**Features**:
- Current glucose status display
- 24-hour glucose trends with targets
- Real-time early detection alerts
- Personalized monitoring schedule
- Clinical information and system status
- Action lists and preventive measures

---

## Alert System Guide

### Understanding Alerts

#### 🚨 CRITICAL Alerts
**Trigger**: Glucose ≤54 or ≥250 mg/dL
**Action**: Seek immediate medical help
**Monitoring**: Every 15 minutes
**Examples**:
- CRITICAL - SEVERE HYPERGLYCEMIA
- CRITICAL - SEVERE HYPOGLYCEMIA

#### ⚠️ WARNING Alerts
**Trigger**: Glucose 54-70 or 180-250 mg/dL
**Action**: Monitor closely, adjust treatment
**Monitoring**: Every 2-3 hours
**Examples**:
- WARNING - HIGH BLOOD SUGAR (180-250 mg/dL)
- WARNING - LOW BLOOD SUGAR (54-70 mg/dL)

#### 📈📉 EARLY WARNING Alerts
**Trigger**: Glucose 100-70 fasting or 160-180 mg/dL
**Action**: Implement preventive measures
**Monitoring**: Every 4-6 hours
**Examples**:
- EARLY WARNING - TRENDING HIGH
- EARLY WARNING - TRENDING LOW

---

## Personalized Recommendations

### For High Glucose (Hyperglycemia)
1. Reduce refined carbohydrate intake
2. Focus on complex carbohydrates
3. Increase physical activity (150+ min/week)
4. Monitor blood glucose more frequently
5. Consult healthcare provider

### For Low Glucose (Hypoglycemia)
1. Consume 15g fast-acting carbohydrates
2. Recheck glucose after 15 minutes
3. Maintain consistent meal schedule
4. Avoid skipping meals
5. Keep quick-acting carbs available

### General Guidelines
- Stay hydrated (8-10 glasses/day)
- Sleep 7-9 hours nightly
- Manage stress effectively
- Regular healthcare check-ups
- Maintain medication compliance

---

## Model Metrics Explanation

### Key Performance Indicators

**MSE (Mean Squared Error)**
- Lower values = better accuracy
- Typical range: 50-200
- Unit: (mg/dL)²

**MAE (Mean Absolute Error)**
- Average prediction error in mg/dL
- Directly interpretable
- Typical range: 5-15 mg/dL

**RMSE (Root Mean Squared Error)**
- Square root of MSE
- Standard deviation of errors
- Typical range: 7-14 mg/dL

**R² Score**
- Proportion of variance explained
- Range: 0-1
- 0.85+ indicates good fit

---

## Feature Importance Guide

The model explains predictions through feature importance scores:

**What It Means**: Which patient factors most influence glucose predictions

**Example Interpretation**:
- Insulin Intake: 40% importance
- Blood Pressure: 25% importance
- Age: 20% importance
- BMI: 10% importance
- Diabetes Status: 5% importance

**Clinical Use**: Identifies which factors to prioritize for glucose management

---

## Clinical Safety Information

### Important Disclaimers
- 🏥 Not a replacement for medical diagnosis
- 👨‍⚕️ Recommendations must be reviewed by healthcare provider
- 📋 Supplementary to clinical judgment
- 🚨 For emergencies, call 911 or visit ER immediately

### When to Seek Emergency Help
- Glucose ≤54 mg/dL with severe symptoms
- Glucose ≥250 mg/dL with DKA symptoms
- Confusion, loss of consciousness
- Severe chest pain or shortness of breath
- Any life-threatening symptoms

### Target Glucose Ranges
| Time | Target Range |
|------|--------------|
| Fasting | 80-130 mg/dL |
| Before Meals | 80-130 mg/dL |
| After Meals | <180 mg/dL |
| Bedtime | 100-140 mg/dL |
| HbA1c | <7% |

---

## Troubleshooting

### Application Won't Start
```
Error: "Port 5000 already in use"
Solution: Close other Flask apps or use: python app.py --port 5001
```

### Prediction Errors
```
Error: "Model not trained"
Solution: Restart application (model trains on startup)
```

### Chart Not Displaying
```
Problem: Plotly charts appear blank
Solution: 
- Ensure JavaScript is enabled in browser
- Clear browser cache
- Try different browser
```

### Alerts Not Showing
```
Problem: No alerts displayed
Solution:
- Check glucose level (must be outside normal range)
- Refresh page
- Check browser console for errors
```

---

## System Requirements

### Minimum Hardware
- Processor: Intel i3 or equivalent
- RAM: 4 GB
- Storage: 500 MB free space
- Internet: Optional (can run offline)

### Recommended Hardware
- Processor: Intel i5 or better
- RAM: 8 GB+
- SSD: 1 GB free space
- Internet: For healthcare provider notifications

---

## Advanced Features

### API Integration Ready
The system is designed for integration with:
- Continuous Glucose Monitors (CGM)
- Electronic Health Records (EHR)
- Insulin pump systems
- Healthcare provider portals
- Patient mobile apps

### Customization Options
- Adjust alert thresholds
- Modify recommendation templates
- Add patient-specific data
- Integrate external APIs
- Deploy on cloud platforms

---

## Support & Resources

### Documentation Files
- `RESEARCH_DOCUMENTATION.md`: Research background and methodology
- `SYSTEM_OVERVIEW.md`: Complete system architecture
- `README.md`: Project information

### Getting Help
1. Check error messages carefully
2. Review troubleshooting section
3. Examine code comments
4. Consult documentation files

### Reporting Issues
When reporting issues, include:
- Error message (exact text)
- Input data that caused error
- Screenshots
- Browser and OS information

---

## Best Practices

### For Patients
1. ✅ Input data accurately
2. ✅ Monitor regularly (daily preferred)
3. ✅ Keep healthcare provider updated
4. ✅ Follow personalized recommendations
5. ✅ Seek medical help for critical alerts

### For Healthcare Providers
1. ✅ Review patient data regularly
2. ✅ Validate AI predictions
3. ✅ Maintain clinical oversight
4. ✅ Use alerts for prioritization
5. ✅ Document provider recommendations

---

## Version Information

**Current Version**: 1.0  
**Release Date**: January 2026  
**Status**: Production Ready  
**Last Updated**: January 28, 2026

---

## Next Steps

1. **Get Started**: Enter your health data on the home page
2. **Review Results**: Check your personalized recommendations
3. **Monitor Trends**: Use the monitoring dashboard regularly
4. **Consult Provider**: Share results with your healthcare team
5. **Track Progress**: Monitor improvements over time

---

**Happy monitoring! Remember: This system enhances but does not replace professional medical care.**
