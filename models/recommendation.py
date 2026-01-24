class RecommendationEngine:
    def __init__(self):
        # Define thresholds for glucose levels (mg/dL)
        self.normal_range = (70, 140)
        self.high_threshold = 140
        self.low_threshold = 70

    def generate_recommendations(self, predicted_glucose, age, bmi, diabetes_status):
        """
        Generate personalized recommendations based on predicted glucose level and user data.
        """
        recommendations = []

        if predicted_glucose > self.high_threshold:
            recommendations.append("Your predicted glucose level is high. Consider reducing carbohydrate intake and increasing physical activity.")
            recommendations.append("Monitor your blood sugar regularly and consult with your healthcare provider.")
            if bmi > 25:
                recommendations.append("Maintaining a healthy weight through diet and exercise can help improve glycemic control.")
            if diabetes_status == 1:
                recommendations.append("As a diabetic, ensure you're following your prescribed insulin regimen and meal plan.")

        elif predicted_glucose < self.low_threshold:
            recommendations.append("Your predicted glucose level is low. Consider consuming a small snack with complex carbohydrates.")
            recommendations.append("Avoid skipping meals and monitor your blood sugar to prevent hypoglycemia.")
            if age > 65:
                recommendations.append("Older adults may be more susceptible to hypoglycemia; consult your doctor for personalized advice.")

        else:
            recommendations.append("Your predicted glucose level is within the normal range. Keep up the good work!")
            recommendations.append("Continue with your healthy lifestyle choices, including balanced diet and regular exercise.")

        # General recommendations
        recommendations.append("Stay hydrated and aim for at least 30 minutes of moderate exercise daily.")
        recommendations.append("Regular check-ups with your healthcare provider are essential for managing diabetes.")

        return recommendations

# Global instance
recommendation_engine = RecommendationEngine()
