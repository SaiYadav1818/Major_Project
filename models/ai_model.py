import xgboost as xgb
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np

class GlucosePredictor:
    """
    XGBoost-based glucose level predictor for diabetes management.
    
    This model uses gradient boosting to predict blood glucose levels based on:
    - Age (years)
    - BMI (Body Mass Index)
    - Insulin Intake (units)
    - Blood Pressure (systolic, mmHg)
    - Diabetes Status (0=Non-diabetic, 1=Diabetic)
    
    The model is designed for clinical use and provides interpretable predictions
    to support personalized treatment strategies and automated insulin delivery systems.
    """
    
    def __init__(self):
        self.model = None
        self.is_trained = False
        self.training_metrics = {}
        self.feature_importance = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

    def train_model(self, data_path=None):
        """
        Train the XGBoost model for glucose prediction.
        If no data_path is provided, use synthetic data for demonstration.
        
        Args:
            data_path (str): Path to CSV file with training data
        """
        if data_path:
            # Load real data
            data = pd.read_csv(data_path)
        else:
            # Generate synthetic data for demonstration with realistic clinical relationships
            np.random.seed(42)
            n_samples = 2000
            age = np.random.randint(18, 80, n_samples)
            bmi = np.random.uniform(18, 40, n_samples)
            insulin_intake = np.random.uniform(0, 100, n_samples)
            blood_pressure = np.random.uniform(90, 180, n_samples)
            diabetes_status = np.random.choice([0, 1], n_samples)

            # Create glucose levels using a clinically plausible combination of features,
            # then add noise to simulate real-world variability.
            glucose_base = (
                80
                + 0.25 * (age - 35)
                + 1.8 * (bmi - 22)
                + 0.25 * (blood_pressure - 110)
                - 0.35 * insulin_intake
                + 30 * diabetes_status
            )
            noise = np.random.normal(0, 10, n_samples)
            glucose_level = np.clip(glucose_base + noise, 40, 400)

            data = pd.DataFrame({
                'age': age,
                'bmi': bmi,
                'insulin_intake': insulin_intake,
                'blood_pressure': blood_pressure,
                'diabetes_status': diabetes_status,
                'glucose_level': glucose_level
            })

        # Features and target
        X = data[['age', 'bmi', 'insulin_intake', 'blood_pressure', 'diabetes_status']]
        y = data['glucose_level']

        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Train XGBoost model with optimized parameters for clinical accuracy
        self.model = xgb.XGBRegressor(
            objective='reg:squarederror',
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            subsample=0.8,
            colsample_bytree=0.8
        )
        self.model.fit(self.X_train, self.y_train)

        # Calculate comprehensive evaluation metrics
        self._evaluate_model()
        
        # Extract feature importance
        self.feature_importance = self._get_feature_importance()

        self.is_trained = True
        print(f"Model trained successfully!")
        print(f"Training Metrics: {self.training_metrics}")

    def _evaluate_model(self):
        """Calculate robustness and accuracy metrics."""
        y_pred_train = self.model.predict(self.X_train)
        y_pred_test = self.model.predict(self.X_test)

        self.training_metrics = {
            'train_mse': mean_squared_error(self.y_train, y_pred_train),
            'test_mse': mean_squared_error(self.y_test, y_pred_test),
            'train_mae': mean_absolute_error(self.y_train, y_pred_train),
            'test_mae': mean_absolute_error(self.y_test, y_pred_test),
            'train_r2': r2_score(self.y_train, y_pred_train),
            'test_r2': r2_score(self.y_test, y_pred_test),
            'rmse': np.sqrt(mean_squared_error(self.y_test, y_pred_test))
        }

    def _get_feature_importance(self):
        """Extract and return feature importance scores for explainability."""
        importance = self.model.get_booster().get_score(importance_type='weight')
        return sorted(importance.items(), key=lambda x: x[1], reverse=True)

    def predict_glucose(self, age, bmi, insulin_intake, blood_pressure, diabetes_status):
        """
        Predict glucose level based on input clinical features.
        
        Args:
            age (float): Patient age in years (valid: 1-120)
            bmi (float): Body Mass Index (valid: 10-70 kg/m²)
            insulin_intake (float): Daily insulin intake in units (valid: 0-300)
            blood_pressure (float): Systolic blood pressure in mmHg (valid: 60-250)
            diabetes_status (int): 0 for non-diabetic, 1 for diabetic
            
        Returns:
            float: Predicted glucose level in mg/dL (range: 40-400)
            
        Raises:
            ValueError: If model not trained or invalid parameters
        """
        if not self.is_trained:
            raise ValueError("Model not trained yet. Call train_model() first.")
        
        # Validate input ranges - CRITICAL for model reliability
        if not (1 <= age <= 120):
            raise ValueError(f"Age must be between 1-120 years, got {age}")
        if not (10 <= bmi <= 70):
            raise ValueError(f"BMI must be between 10-70 kg/m², got {bmi}")
        if not (0 <= insulin_intake <= 300):
            raise ValueError(f"Insulin intake must be between 0-300 units, got {insulin_intake}")
        if not (60 <= blood_pressure <= 250):
            raise ValueError(f"Blood pressure must be between 60-250 mmHg, got {blood_pressure}")
        if diabetes_status not in [0, 1]:
            raise ValueError(f"Diabetes status must be 0 or 1, got {diabetes_status}")

        input_data = pd.DataFrame({
            'age': [age],
            'bmi': [bmi],
            'insulin_intake': [insulin_intake],
            'blood_pressure': [blood_pressure],
            'diabetes_status': [diabetes_status]
        })

        prediction = self.model.predict(input_data)[0]
        
        # Clamp prediction to clinical range (40-400 mg/dL)
        # <40: Severe hypoglycemia (life-threatening)
        # >400: Severe hyperglycemia (DKA risk)
        prediction = max(40, min(400, prediction))
        
        return prediction

    def get_clinical_assessment(self, glucose_level):
        """
        Provide clinical assessment based on predicted glucose level.
        
        Args:
            glucose_level (float): Predicted glucose level
            
        Returns:
            dict: Clinical assessment and recommendations
        """
        assessment = {
            'glucose_level': glucose_level,
            'status': '',
            'clinical_recommendation': '',
            'risk_level': ''
        }
        
        if glucose_level < 70:
            assessment['status'] = 'Hypoglycemic'
            assessment['risk_level'] = 'HIGH'
            assessment['clinical_recommendation'] = 'Immediate intervention required. Consume fast-acting carbohydrates.'
        elif 70 <= glucose_level < 100:
            assessment['status'] = 'Fasting Normal'
            assessment['risk_level'] = 'LOW'
            assessment['clinical_recommendation'] = 'Optimal glucose level. Maintain current treatment.'
        elif 100 <= glucose_level < 125:
            assessment['status'] = 'Impaired Fasting'
            assessment['risk_level'] = 'MODERATE'
            assessment['clinical_recommendation'] = 'Monitor diet and exercise. Consider consulting healthcare provider.'
        elif 125 <= glucose_level < 200:
            assessment['status'] = 'Hyperglycemic'
            assessment['risk_level'] = 'MODERATE'
            assessment['clinical_recommendation'] = 'Adjust insulin therapy. Increase physical activity and hydration.'
        else:
            assessment['status'] = 'Severely Hyperglycemic'
            assessment['risk_level'] = 'HIGH'
            assessment['clinical_recommendation'] = 'Urgent medical attention required. Seek healthcare provider immediately.'
        
        return assessment

    def get_model_metrics(self):
        """Return model performance metrics for clinical evaluation."""
        return self.training_metrics

    def get_feature_importance_dict(self):
        """Return feature importance for model explainability."""
        return dict(self.feature_importance) if self.feature_importance else {}

# Global instance
glucose_predictor = GlucosePredictor()
