class AlertSystem:
    def __init__(self):
        # Define critical thresholds (mg/dL)
        self.hyperglycemia_threshold = 180  # High blood sugar
        self.hypoglycemia_threshold = 70    # Low blood sugar
        self.severe_hyperglycemia = 250     # Very high, medical emergency
        self.severe_hypoglycemia = 54       # Very low, medical emergency

    def check_alerts(self, predicted_glucose):
        """
        Check for alerts based on predicted glucose level.
        Returns a list of alert messages.
        """
        alerts = []

        if predicted_glucose >= self.severe_hyperglycemia:
            alerts.append("CRITICAL: Severe hyperglycemia detected! Seek immediate medical attention.")
        elif predicted_glucose >= self.hyperglycemia_threshold:
            alerts.append("WARNING: High blood sugar level predicted. Monitor closely and consider adjusting diet or medication.")

        if predicted_glucose <= self.severe_hypoglycemia:
            alerts.append("CRITICAL: Severe hypoglycemia detected! Consume fast-acting carbohydrates immediately.")
        elif predicted_glucose <= self.hypoglycemia_threshold:
            alerts.append("WARNING: Low blood sugar level predicted. Check blood sugar and consume carbohydrates if needed.")

        return alerts

    def notify_provider(self, patient_id, predicted_glucose, alerts):
        """
        Simulate notification to healthcare provider.
        In a real implementation, this would send emails, SMS, or push notifications.
        """
        if alerts:
            print(f"NOTIFICATION: Alert for patient {patient_id} - Glucose: {predicted_glucose} mg/dL")
            for alert in alerts:
                print(f"  {alert}")
            # Here you would integrate with notification services like Twilio, SendGrid, etc.

# Global instance
alert_system = AlertSystem()
