from flask import Flask, session, redirect, url_for
from routes.user import user_bp
from routes.reporting import reporting_bp
from routes.auth import auth_bp
from models.ai_model import glucose_predictor
from models.patient import patient_manager
import os

app = Flask(__name__)

# Configure session (SECRET_KEY required for session management)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production-12345')

# Initialize MySQL database for patient management
patient_manager.init_db()

# Register blueprints with appropriate prefixes
app.register_blueprint(auth_bp)  # /register, /login, /logout, /profile, /dashboard
app.register_blueprint(user_bp, url_prefix='/user')  # /user/predict
app.register_blueprint(reporting_bp, url_prefix='/reporting')

# Train the model on startup (using synthetic data for demonstration)
glucose_predictor.train_model()

# Login page as default
@app.route('/')
def index():
    if 'patient_id' in session:
        return redirect(url_for('auth.dashboard'))
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True)
