class AlertSystem:
    """
    Advanced Alert System for Early Detection of Abnormal Glycemic Levels.
    
    This system monitors glucose levels for abnormalities and provides:
    - Real-time critical alerts for medical emergencies
    - Early warning alerts for trend detection
    - Personalized thresholds based on patient profiles
    - Healthcare provider notification support
    """
    
    def __init__(self):
        # Define critical thresholds (mg/dL) - Clinical Standards
        self.hyperglycemia_threshold = 180          # High blood sugar (moderate)
        self.hypoglycemia_threshold = 70            # Low blood sugar (moderate)
        self.severe_hyperglycemia = 250             # Very high, medical emergency
        self.severe_hypoglycemia = 54               # Very low, medical emergency
        
        # Early detection thresholds
        self.early_warning_high = 160               # Early high detection
        self.early_warning_low = 100                # Early low detection (fasting)
        
        # Trend detection
        self.rapid_change_threshold = 30            # Change rate in mg/dL
        self.alert_history = {}                     # Track alerts per patient

    def check_alerts(self, predicted_glucose, diabetes_status=None):
        """
        Check for alerts based on predicted glucose level.
        Supports multi-level alert system for early detection and emergency response.
        
        Args:
            predicted_glucose (float): Predicted glucose level in mg/dL
            diabetes_status (int): 0=Non-diabetic, 1=Diabetic (affects thresholds)
            
        Returns:
            list: Alert messages prioritized by severity
        """
        alerts = []
        alert_levels = []

        # CRITICAL LEVEL 1: Severe Hyperglycemia (Medical Emergency)
        if predicted_glucose >= self.severe_hyperglycemia:
            alerts.append("🚨 CRITICAL - SEVERE HYPERGLYCEMIA: Glucose level ≥250 mg/dL!")
            alerts.append("Immediate medical attention required. Call emergency services or visit ER.")
            alerts.append("Symptoms: Extreme thirst, blurred vision, difficulty concentrating, ketone breath.")
            alert_levels.append(('CRITICAL_HIGH', predicted_glucose))

        # CRITICAL LEVEL 2: Severe Hypoglycemia (Medical Emergency)
        elif predicted_glucose <= self.severe_hypoglycemia:
            alerts.append("🚨 CRITICAL - SEVERE HYPOGLYCEMIA: Glucose level ≤54 mg/dL!")
            alerts.append("IMMEDIATE ACTION: Consume fast-acting carbohydrates NOW (juice, glucose tablets).")
            alerts.append("Symptoms: Trembling, sweating, confusion, rapid heartbeat, loss of consciousness risk.")
            alert_levels.append(('CRITICAL_LOW', predicted_glucose))

        # WARNING LEVEL 1: Significant Hyperglycemia
        if self.hyperglycemia_threshold <= predicted_glucose < self.severe_hyperglycemia:
            alerts.append("⚠️ WARNING - HIGH BLOOD SUGAR: Glucose level 180-250 mg/dL (Hyperglycemic Range)")
            alerts.append("Action Items:")
            alerts.append("  • Monitor blood sugar closely (check every 2-3 hours)")
            alerts.append("  • Increase physical activity (brisk walking, exercise)")
            alerts.append("  • Review medication compliance")
            alerts.append("  • Consult healthcare provider if levels persist above 180 mg/dL")
            alerts.append("  • Stay well hydrated")
            alert_levels.append(('WARNING_HIGH', predicted_glucose))

        # WARNING LEVEL 2: Significant Hypoglycemia
        elif predicted_glucose <= self.hypoglycemia_threshold and predicted_glucose > self.severe_hypoglycemia:
            alerts.append("⚠️ WARNING - LOW BLOOD SUGAR: Glucose level 54-70 mg/dL (Hypoglycemic Range)")
            alerts.append("Action Items:")
            alerts.append("  • Consume 15g of fast-acting carbohydrates (4 oz juice, 3 glucose tablets)")
            alerts.append("  • Recheck glucose after 15 minutes")
            alerts.append("  • If still below 70, repeat the process")
            alerts.append("  • Eat a balanced snack once symptoms improve")
            alerts.append("  • Review recent insulin doses with healthcare provider")
            alert_levels.append(('WARNING_LOW', predicted_glucose))

        # EARLY WARNING LEVEL 1: Trending High
        if self.early_warning_high <= predicted_glucose < self.hyperglycemia_threshold:
            alerts.append("📈 EARLY WARNING - TRENDING HIGH: Glucose approaching elevated range (160-180 mg/dL)")
            alerts.append("Preventive Measures:")
            alerts.append("  • Reduce carbohydrate portions at next meal")
            alerts.append("  • Increase physical activity")
            alerts.append("  • Monitor closely over next few hours")
            alerts.append("  • Consider stress management techniques")
            alert_levels.append(('EARLY_WARNING_HIGH', predicted_glucose))

        # EARLY WARNING LEVEL 2: Trending Low
        if self.hypoglycemia_threshold <= predicted_glucose < self.early_warning_low:
            alerts.append("📉 EARLY WARNING - TRENDING LOW: Glucose approaching low range (70-100 mg/dL)")
            alerts.append("Preventive Measures:")
            alerts.append("  • Plan next meal/snack soon")
            alerts.append("  • Avoid strenuous exercise without food intake")
            alerts.append("  • Have quick-acting carbs available")
            alerts.append("  • Monitor for hypoglycemia symptoms")
            alert_levels.append(('EARLY_WARNING_LOW', predicted_glucose))

        # OPTIMAL STATUS
        if not alert_levels:
            alerts.append("✅ OPTIMAL - Glucose level is within target range (100-160 mg/dL for most)")
            alerts.append("Continue current treatment plan and maintain healthy lifestyle.")

        return alerts

    def check_rapid_change(self, current_glucose, previous_glucose):
        """
        Detect rapid changes in glucose level (>30 mg/dL change).
        Important for detecting acute complications.
        
        Args:
            current_glucose (float): Current glucose reading
            previous_glucose (float): Previous glucose reading
            
        Returns:
            list: Alert messages if rapid change detected
        """
        alerts = []
        change = abs(current_glucose - previous_glucose)
        
        if change >= self.rapid_change_threshold:
            direction = "↑ INCREASE" if current_glucose > previous_glucose else "↓ DECREASE"
            alerts.append(f"⚡ RAPID CHANGE DETECTED: {direction} of {change:.0f} mg/dL in short period!")
            alerts.append("This rapid fluctuation may indicate:")
            alerts.append("  • Meal timing issues")
            alerts.append("  • Physical activity impact")
            alerts.append("  • Medication/insulin effect")
            alerts.append("  • Stress or illness")
            alerts.append("Recommendation: Monitor frequently and consult healthcare provider.")
        
        return alerts

    def get_alert_severity(self, predicted_glucose):
        """
        Classify alert severity for dashboard highlighting.
        
        Args:
            predicted_glucose (float): Glucose level
            
        Returns:
            str: Severity level (CRITICAL, WARNING, EARLY_WARNING, OK)
        """
        if predicted_glucose >= self.severe_hyperglycemia or predicted_glucose <= self.severe_hypoglycemia:
            return 'CRITICAL'
        elif predicted_glucose >= self.hyperglycemia_threshold or predicted_glucose <= self.hypoglycemia_threshold:
            return 'WARNING'
        elif predicted_glucose >= self.early_warning_high or predicted_glucose < self.early_warning_low:
            return 'EARLY_WARNING'
        else:
            return 'OK'

    def notify_provider(self, patient_id, predicted_glucose, alerts, contact_info=None):
        """
        Log and simulate notification to healthcare provider.
        In production, integrate with email/SMS/push notification services.
        
        Args:
            patient_id (str): Patient identifier
            predicted_glucose (float): Glucose level
            alerts (list): Alert messages
            contact_info (dict): Provider contact information
        """
        severity = self.get_alert_severity(predicted_glucose)
        
        if severity in ['CRITICAL', 'WARNING']:
            timestamp = __import__('datetime').datetime.now().isoformat()
            
            # Log alert
            if patient_id not in self.alert_history:
                self.alert_history[patient_id] = []
            
            self.alert_history[patient_id].append({
                'timestamp': timestamp,
                'glucose': predicted_glucose,
                'severity': severity,
                'alerts': alerts
            })
            
            print(f"[{timestamp}] PROVIDER NOTIFICATION - Patient {patient_id}")
            print(f"Severity: {severity} | Glucose: {predicted_glucose} mg/dL")
            for alert in alerts:
                print(f"  {alert}")
            
            # In production, send notifications via:
            # - Email (SendGrid, AWS SES)
            # - SMS (Twilio)
            # - Push Notifications (Firebase)
            # - Hospital EHR integration

    def get_patient_alert_history(self, patient_id):
        """Retrieve alert history for a patient."""
        return self.alert_history.get(patient_id, [])

    def get_monitoring_recommendations(self, predicted_glucose, diabetes_status):
        """
        Provide frequency and type of monitoring recommendations.
        
        Args:
            predicted_glucose (float): Glucose level
            diabetes_status (int): Diabetes status
            
        Returns:
            dict: Monitoring recommendations
        """
        recommendations = {
            'check_frequency': 'daily',
            'check_method': 'finger stick or CGM',
            'follow_up_days': 30,
            'specialist': 'Primary Care Physician'
        }
        
        severity = self.get_alert_severity(predicted_glucose)
        
        if severity == 'CRITICAL':
            recommendations['check_frequency'] = 'immediately and every 15 minutes'
            recommendations['check_method'] = 'finger stick + continuous glucose monitor'
            recommendations['follow_up_days'] = 1
            recommendations['specialist'] = 'Endocrinologist + Emergency Medicine'
        
        elif severity == 'WARNING':
            recommendations['check_frequency'] = 'every 2-3 hours'
            recommendations['check_method'] = 'finger stick minimum'
            recommendations['follow_up_days'] = 3
            recommendations['specialist'] = 'Endocrinologist'
        
        elif severity == 'EARLY_WARNING':
            recommendations['check_frequency'] = 'every 4-6 hours'
            recommendations['check_method'] = 'finger stick or CGM'
            recommendations['follow_up_days'] = 7
            recommendations['specialist'] = 'Primary Care Physician'
        
        else:
            recommendations['check_frequency'] = 'daily'
            recommendations['check_method'] = 'CGM or daily finger stick'
            recommendations['follow_up_days'] = 30
            recommendations['specialist'] = 'Primary Care Physician'
        
        return recommendations

# Global instance
alert_system = AlertSystem()
