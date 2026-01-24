from flask import Flask
from routes.user import user_bp
from routes.reporting import reporting_bp
from models.ai_model import glucose_predictor

app = Flask(__name__)

# Register blueprints
app.register_blueprint(user_bp)
app.register_blueprint(reporting_bp, url_prefix='/reporting')

# Train the model on startup (using synthetic data for demonstration)
glucose_predictor.train_model()

if __name__ == '__main__':
    app.run(debug=True)
