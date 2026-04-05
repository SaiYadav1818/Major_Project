class RecommendationEngine:
    """
    Personalized treatment recommendation engine for diabetes management.
    
    Generates actionable clinical recommendations based on predicted glucose levels
    and individual health profiles to support personalized treatment strategies.
    """
    
    def __init__(self):
        # Define clinical thresholds for glucose levels (mg/dL)
        self.normal_fasting_range = (70, 100)
        self.normal_postprandial_range = (70, 140)
        self.high_threshold = 140
        self.low_threshold = 70
        self.severe_low_threshold = 54
        self.severe_high_threshold = 300

    def generate_recommendations(self, predicted_glucose, age, bmi, diabetes_status):
        """
        Generate personalized, evidence-based recommendations based on predicted glucose 
        level and individual clinical features.
        
        Args:
            predicted_glucose (float): Predicted glucose level in mg/dL
            age (float): Patient age in years
            bmi (float): Body Mass Index
            diabetes_status (int): 0=Non-diabetic, 1=Diabetic
            
        Returns:
            list: Personalized clinical recommendations
        """
        recommendations = []

        # Severity-based recommendations
        if predicted_glucose >= self.severe_high_threshold:
            recommendations.append("⚠️ URGENT: Glucose level severely elevated. Seek immediate medical attention.")
            recommendations.append("Contact your healthcare provider or emergency services immediately.")
            
        elif predicted_glucose > self.high_threshold:
            recommendations.append("📊 Your glucose level is elevated. Implement the following strategies:")
            recommendations.append("• Reduce refined carbohydrate intake and focus on complex carbohydrates")
            recommendations.append("• Increase physical activity to at least 150 minutes per week")
            recommendations.append("• Monitor blood glucose more frequently (every 2-3 hours)")
            
            if bmi > 25:
                recommendations.append("• Weight management is critical: aim for a 5-10% weight loss")
                recommendations.append("• Consider consulting a registered dietitian for personalized meal planning")
            
            if diabetes_status == 1:
                recommendations.append("• Review your insulin regimen with your endocrinologist")
                recommendations.append("• Consider adjusting medication dosage or timing")
                recommendations.append("• Ensure strict adherence to your diabetes management plan")
            else:
                recommendations.append("• This level indicates prediabetes risk; lifestyle intervention is crucial")
                recommendations.append("• Increase preventive screening frequency")

        elif predicted_glucose <= self.severe_low_threshold:
            recommendations.append("⚠️ URGENT: Glucose level severely low. Consume fast-acting carbohydrates immediately.")
            recommendations.append("• Drink 4-6 oz of juice or regular soda")
            recommendations.append("• If no improvement in 15 minutes, seek emergency care")
            
        elif predicted_glucose < self.low_threshold:
            recommendations.append("📊 Your glucose level is low. Take immediate action:")
            recommendations.append("• Consume 15g of fast-acting carbohydrates (glucose tablets, juice, or candy)")
            recommendations.append("• Recheck glucose level after 15 minutes")
            recommendations.append("• Avoid skipping meals and maintain consistent eating schedule")
            
            if age > 65:
                recommendations.append("• Older adults should be extra cautious about hypoglycemia")
                recommendations.append("• Consider wearing a continuous glucose monitor (CGM)")
                recommendations.append("• Inform family members about hypoglycemia symptoms")
            
            if diabetes_status == 1:
                recommendations.append("• Review your current insulin dose with your healthcare provider")
                recommendations.append("• Adjust medication timing or quantity as recommended")

        else:
            recommendations.append("✅ Your glucose level is within the target range. Excellent!")
            recommendations.append("• Continue your current lifestyle and medication regimen")
            recommendations.append("• Maintain consistent meal timing and portion sizes")
            recommendations.append("• Keep up your regular physical activity routine")

        # Age-specific recommendations
        if age < 30:
            recommendations.append("🎯 Young adults: Build healthy habits now to prevent future complications")
        elif age >= 65:
            recommendations.append("🎯 Seniors: Regular health screenings and medication review are essential")

        # General evidence-based recommendations
        recommendations.append("\n📋 General Diabetes Management Guidelines:")
        recommendations.append("• Stay hydrated: drink 8-10 glasses of water daily")
        recommendations.append("• Aim for at least 150 minutes of moderate aerobic activity weekly")
        recommendations.append("• Manage stress through meditation, yoga, or counseling")
        recommendations.append("• Get 7-9 hours of quality sleep each night")
        recommendations.append("• Schedule regular check-ups with your healthcare provider")
        recommendations.append("• Monitor for symptoms of diabetes complications (neuropathy, nephropathy)")

        return recommendations

    def get_insulin_adjustment_suggestion(self, predicted_glucose, diabetes_status):
        """
        Suggest insulin therapy adjustments based on predicted glucose levels.
        (For reference only - actual adjustments must be made by healthcare provider)
        
        Args:
            predicted_glucose (float): Predicted glucose level
            diabetes_status (int): Diabetes status
            
        Returns:
            str: Clinical insight on insulin adjustment
        """
        if diabetes_status != 1:
            return "Not applicable for non-diabetic patients."
        
        if predicted_glucose > 180:
            return "Suggestion: Consider discussing insulin dose increase with your healthcare provider."
        elif predicted_glucose > 140:
            return "Suggestion: Monitor glucose patterns. Discuss potential adjustments with provider if consistent."
        elif predicted_glucose < 70:
            return "Suggestion: Insulin dose may need reduction. Consult your healthcare provider."
        else:
            return "Current insulin therapy appears to be working well. Continue as prescribed."

# Global instance
recommendation_engine = RecommendationEngine()
