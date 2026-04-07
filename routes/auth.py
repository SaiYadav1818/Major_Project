from flask import Blueprint, request, render_template, session, redirect, url_for
from models.patient import patient_manager

auth_bp = Blueprint('auth', __name__)

@auth_bp.before_request
def load_logged_in_user():
    """Load logged-in user into g object for all routes"""
    user_id = session.get('patient_id')
    if user_id is None:
        user = None
    else:
        user = patient_manager.get_patient_info(user_id)
    
    # g is not available here, so we'll pass it through session

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Patient registration page"""
    error = None
    success = None
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '')
        date_of_birth = request.form.get('date_of_birth', '').strip()
        diabetes_type = request.form.get('diabetes_type', '')
        
        # Validate input
        if not name:
            error = "Patient name is required"
        elif not email and not phone:
            error = "Email or phone is required"
        elif not password:
            error = "Password is required"
        elif not date_of_birth:
            error = "Date of birth is required"
        
        if not error:
            success, patient_id, message = patient_manager.register_patient(
                name=name,
                email=email if email else None,
                phone=phone if phone else None,
                password=password,
                date_of_birth=date_of_birth,
                diabetes_type=diabetes_type if diabetes_type else None
            )
            
            if success:
                success = f"✅ Registration successful! Your Patient ID: {patient_id}. Age auto-calculated from your date of birth."
                # Clear form
                name = email = phone = password = date_of_birth = diabetes_type = ''
            else:
                error = f"❌ {message}"
    
    return render_template('auth/register.html', error=error, success=success)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Patient login page"""
    error = None
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '')
        
        if not email and not phone:
            error = "Email or phone is required"
        elif not password:
            error = "Password is required"
        
        if not error:
            success, patient_id, patient_name, message = patient_manager.login_patient(
                email=email if email else None,
                phone=phone if phone else None,
                password=password
            )
            
            if success:
                session['patient_id'] = patient_id
                session['patient_name'] = patient_name
                return redirect(url_for('auth.dashboard'))
            else:
                error = message
    
    return render_template('auth/login.html', error=error)

@auth_bp.route('/logout')
def logout():
    """Logout patient"""
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bp.route('/dashboard')
def dashboard():
    """Patient dashboard - shows statistics and recent predictions"""
    patient_id = session.get('patient_id')
    patient_name = session.get('patient_name')
    
    if not patient_id:
        return redirect(url_for('auth.login'))
    
    # Get patient statistics
    stats = patient_manager.get_patient_statistics(patient_id, days=30)
    
    # Get recent predictions (last 10)
    predictions = patient_manager.get_patient_predictions(patient_id, days=30)
    
    return render_template(
        'user/dashboard.html',
        patient_id=patient_id,
        patient_name=patient_name,
        stats=stats,
        predictions=predictions
    )

@auth_bp.route('/profile')
def profile():
    """View patient profile"""
    patient_id = session.get('patient_id')
    patient_name = session.get('patient_name')
    
    if not patient_id:
        return redirect(url_for('auth.login'))
    
    patient_info = patient_manager.get_patient_info(patient_id)
    
    if not patient_info:
        return redirect(url_for('auth.login'))
    
    stats = patient_manager.get_patient_statistics(patient_id, days=30)
    
    return render_template(
        'auth/profile.html',
        patient_id=patient_id,
        patient_name=patient_name,
        patient_info=patient_info,
        stats=stats
    )
