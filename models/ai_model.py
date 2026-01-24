import xgboost as xgb
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np

class GlucosePredictor:
    def __init__(self):
        self.model = None
        self.is_trained = False

    def train_model(self, data_path=None):
        """
        Train the XGBoost model for glucose prediction.
        If no data_path is provided, use synthetic data for demonstration.
        """
        if data_path:
            # Load real data
            data = pd.read_csv(data_path)
        else:
            # Generate synthetic data for demonstration
            np.random.seed(42)
            n_samples = 1000
            data = pd.DataFrame({
                'age': np.random.randint(18, 80, n_samples),
                'bmi': np.random.uniform(18, 40, n_samples),
                'insulin_intake': np.random.uniform(0, 100, n_samples),
                'blood_pressure': np.random.uniform(90, 180, n_samples),
                'diabetes_status': np.random.choice([0, 1], n_samples),
                'glucose_level': np.random.uniform(70, 200, n_samples)
            })

        # Features and target
        X = data[['age', 'bmi', 'insulin_intake', 'blood_pressure', 'diabetes_status']]
        y = data['glucose_level']

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train XGBoost model
        self.model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)

        # Evaluate
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        print(f"Model trained. MSE: {mse:.2f}")

        self.is_trained = True

    def predict_glucose(self, age, bmi, insulin_intake, blood_pressure, diabetes_status):
        """
        Predict glucose level based on input features.
        """
        if not self.is_trained:
            raise ValueError("Model not trained yet. Call train_model() first.")

        input_data = pd.DataFrame({
            'age': [age],
            'bmi': [bmi],
            'insulin_intake': [insulin_intake],
            'blood_pressure': [blood_pressure],
            'diabetes_status': [diabetes_status]
        })

        prediction = self.model.predict(input_data)[0]
        return prediction

# Global instance
glucose_predictor = GlucosePredictor()
