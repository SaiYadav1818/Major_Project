import mysql.connector
from mysql.connector import Error
import uuid
import hashlib
from datetime import datetime, date

def calculate_age(date_of_birth):
    """Calculate age from date of birth"""
    try:
        if isinstance(date_of_birth, str):
            dob = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
        else:
            dob = date_of_birth
        
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age
    except:
        return None

def validate_age(stored_dob, entered_age, tolerance=1):
    """
    Validate if entered age matches calculated age from DOB
    tolerance: Allow +/- years in case user birthday is soon
    Returns: (is_valid, calculated_age, error_message)
    """
    if not stored_dob:
        return False, None, "No date of birth on file"
    
    calculated_age = calculate_age(stored_dob)
    if calculated_age is None:
        return False, None, "Could not calculate age from DOB"
    
    try:
        entered_age = int(entered_age)
    except:
        return False, calculated_age, "Age must be a number"
    
    # Check if age is within tolerance (handles upcoming birthdays)
    if abs(entered_age - calculated_age) <= tolerance:
        return True, calculated_age, "Age validated"
    else:
        return False, calculated_age, f"Age mismatch! Your age should be {calculated_age} years old based on DOB, but you entered {entered_age}"

class PatientManager:
    """
    Manages patient registration, login, and profile information.
    Uses MySQL database (majorP).
    """
    
    # MySQL connection configuration
    DB_CONFIG = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': '99637101sai',
        'database': 'majorP'
    }
    
    @staticmethod
    def get_connection():
        """Get MySQL database connection"""
        try:
            conn = mysql.connector.connect(**PatientManager.DB_CONFIG)
            return conn
        except Error as e:
            print(f"❌ Database connection error: {e}")
            return None
    
    @staticmethod
    def init_db():
        """Verify patient database tables exist"""
        try:
            conn = PatientManager.get_connection()
            if not conn:
                return False
            
            c = conn.cursor()
            
            # Check if patients table exists
            c.execute("SHOW TABLES LIKE 'patients'")
            if not c.fetchone():
                print("⚠️  Patients table not found. Creating...")
                c.execute('''
                    CREATE TABLE patients (
                        id VARCHAR(20) PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        email VARCHAR(255) UNIQUE,
                        phone VARCHAR(20),
                        password VARCHAR(255) NOT NULL,
                        age INT,
                        diabetes_type VARCHAR(50),
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        last_login DATETIME
                    )
                ''')
            
            # Check if health_records table exists
            c.execute("SHOW TABLES LIKE 'health_records'")
            if not c.fetchone():
                print("⚠️  Health records table not found. Creating...")
                c.execute('''
                    CREATE TABLE health_records (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        patient_id VARCHAR(20) NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        age INT,
                        bmi DECIMAL(5,2),
                        insulin_intake DECIMAL(5,2),
                        blood_pressure DECIMAL(5,2),
                        diabetes_status TINYINT,
                        predicted_glucose DECIMAL(5,2),
                        status VARCHAR(50),
                        risk_level VARCHAR(50),
                        FOREIGN KEY (patient_id) REFERENCES patients(id)
                    )
                ''')
            
            conn.commit()
            c.close()
            conn.close()
            print("✅ Patient database verified successfully")
            return True
        except Error as e:
            print(f"❌ Database initialization error: {e}")
            return False
    
    @staticmethod
    def generate_patient_id():
        """Generate unique patient ID"""
        return f"PT-{uuid.uuid4().hex[:12].upper()}"
    
    @staticmethod
    def hash_password(password):
        """Hash password for security"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def register_patient(name, email=None, phone=None, password=None, date_of_birth=None, diabetes_type=None):
        """
        Register a new patient
        
        Args:
            name: Patient's full name
            email: Patient's email (optional but recommended)
            phone: Patient's phone number (optional)
            password: Patient's password (hashed)
            date_of_birth: Patient's date of birth (YYYY-MM-DD) - REQUIRED
            diabetes_type: Type 1 or Type 2 (optional)
            
        Returns:
            tuple: (success, patient_id, error_message)
        """
        # Validation
        if not name or len(name) < 2:
            return False, None, "Patient name must be at least 2 characters"
        
        if not email and not phone:
            return False, None, "Email or phone is required"
        
        if not password or len(password) < 6:
            return False, None, "Password must be at least 6 characters"
        
        # Validate date of birth
        if not date_of_birth:
            return False, None, "Date of birth is required"
        
        try:
            dob = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
        except:
            return False, None, "Invalid date format. Use YYYY-MM-DD"
        
        # Calculate age from DOB
        calculated_age = calculate_age(dob)
        if calculated_age is None or calculated_age < 5 or calculated_age > 120:
            return False, None, "Invalid date of birth. Age must be between 5 and 120 years"
        
        # Check email uniqueness if provided
        if email:
            conn = PatientManager.get_connection()
            if not conn:
                return False, None, "Database connection error"
            
            c = conn.cursor()
            c.execute("SELECT id FROM patients WHERE email = %s", (email,))
            if c.fetchone():
                c.close()
                conn.close()
                return False, None, "Email already registered"
            c.close()
            conn.close()
        
        try:
            patient_id = PatientManager.generate_patient_id()
            hashed_password = PatientManager.hash_password(password)
            
            conn = PatientManager.get_connection()
            if not conn:
                return False, None, "Database connection error"
            
            c = conn.cursor()
            
            c.execute('''
                INSERT INTO patients 
                (id, name, email, phone, password, age, date_of_birth, diabetes_type, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (patient_id, name, email, phone, hashed_password, calculated_age, dob, diabetes_type, datetime.now()))
            
            conn.commit()
            c.close()
            conn.close()
            
            return True, patient_id, "Registration successful! (Age auto-calculated from DOB)"
        
        except Error as e:
            return False, None, f"Registration error: {str(e)}"
    
    @staticmethod
    def login_patient(email=None, phone=None, password=None):
        """
        Login patient with email/phone and password
        
        Args:
            email: Patient's email
            phone: Patient's phone
            password: Patient's password
            
        Returns:
            tuple: (success, patient_id, patient_name, error_message)
        """
        if not email and not phone:
            return False, None, None, "Email or phone required"
        
        if not password:
            return False, None, None, "Password required"
        
        try:
            hashed_password = PatientManager.hash_password(password)
            
            conn = PatientManager.get_connection()
            if not conn:
                return False, None, None, "Database connection error"
            
            c = conn.cursor()
            
            if email:
                c.execute("SELECT id, name, password FROM patients WHERE email = %s", (email,))
            else:
                c.execute("SELECT id, name, password FROM patients WHERE phone = %s", (phone,))
            
            result = c.fetchone()
            
            if not result:
                c.close()
                conn.close()
                return False, None, None, "Patient not found"
            
            patient_id, patient_name, stored_password = result
            
            if stored_password != hashed_password:
                c.close()
                conn.close()
                return False, None, None, "Invalid password"
            
            # Update last login
            c.execute("UPDATE patients SET last_login = %s WHERE id = %s", (datetime.now(), patient_id))
            conn.commit()
            c.close()
            conn.close()
            
            return True, patient_id, patient_name, "Login successful!"
        
        except Error as e:
            return False, None, None, f"Login error: {str(e)}"
    
    @staticmethod
    def get_patient_info(patient_id):
        """Get patient information"""
        try:
            conn = PatientManager.get_connection()
            if not conn:
                return None
            
            c = conn.cursor()
            
            c.execute('''
                SELECT id, name, email, phone, age, date_of_birth, diabetes_type, created_at, last_login 
                FROM patients WHERE id = %s
            ''', (patient_id,))
            
            result = c.fetchone()
            c.close()
            conn.close()
            
            if result:
                return {
                    'id': result[0],
                    'name': result[1],
                    'email': result[2],
                    'phone': result[3],
                    'age': result[4],
                    'date_of_birth': result[5],
                    'diabetes_type': result[6],
                    'created_at': result[7],
                    'last_login': result[8]
                }
            return None
        
        except Error as e:
            print(f"Error fetching patient info: {e}")
            return None
    
    @staticmethod
    def save_patient_prediction(patient_id, age, bmi, insulin_intake, blood_pressure, 
                               diabetes_status, predicted_glucose, clinical_status, risk_level):
        """Save health record associated with a patient"""
        try:
            conn = PatientManager.get_connection()
            if not conn:
                print("❌ Failed to connect to database")
                return False
            
            c = conn.cursor()
            
            # Verify patient exists
            c.execute("SELECT id FROM patients WHERE id = %s", (patient_id,))
            if not c.fetchone():
                print(f"❌ Patient {patient_id} not found in database")
                c.close()
                conn.close()
                return False
            
            # Convert to proper types
            age = int(float(age))
            bmi = float(bmi)
            insulin_intake = float(insulin_intake)
            blood_pressure = int(float(blood_pressure))
            diabetes_status = int(diabetes_status)
            predicted_glucose = float(predicted_glucose)
            
            print(f"🔍 Saving: patient_id={patient_id}, age={age}, bmi={bmi}, insulin={insulin_intake}, bp={blood_pressure}, glucose={predicted_glucose}, status={clinical_status}, risk={risk_level}")
            
            c.execute('''
                INSERT INTO health_records 
                (patient_id, timestamp, age, bmi, insulin_intake, blood_pressure, diabetes_status, 
                 predicted_glucose, status, risk_level)
                VALUES (%s, NOW(), %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (patient_id, age, bmi, insulin_intake, blood_pressure, diabetes_status,
                  predicted_glucose, clinical_status, risk_level))
            
            conn.commit()
            c.close()
            conn.close()
            print(f"✅ Health record saved successfully for patient {patient_id}")
            return True
        
        except Error as e:
            print(f"❌ MYSQL Error saving health record: {e}")
            print(f"   Patient ID: {patient_id}")
            print(f"   Values: age={age}, bmi={bmi}, insulin={insulin_intake}, bp={blood_pressure}, glucose={predicted_glucose}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error saving health record: {e}")
            return False
            return False
    
    @staticmethod
    def get_patient_predictions(patient_id, days=30):
        """Get patient's health record history (last N days)"""
        try:
            conn = PatientManager.get_connection()
            if not conn:
                return []
            
            c = conn.cursor()
            
            c.execute('''
                SELECT timestamp, predicted_glucose, status, risk_level, age, bmi, 
                       insulin_intake, blood_pressure
                FROM health_records 
                WHERE patient_id = %s
                ORDER BY timestamp DESC
                LIMIT %s
            ''', (patient_id, days))
            
            results = c.fetchall()
            c.close()
            conn.close()
            
            return results
        
        except Error as e:
            print(f"Error fetching health records: {e}")
            return []
    
    @staticmethod
    def get_patient_statistics(patient_id, days=30):
        """Get glucose statistics for a patient from health records"""
        try:
            conn = PatientManager.get_connection()
            if not conn:
                return None
            
            c = conn.cursor()
            
            c.execute('''
                SELECT 
                    AVG(predicted_glucose) as avg_glucose,
                    MIN(predicted_glucose) as min_glucose,
                    MAX(predicted_glucose) as max_glucose,
                    COUNT(*) as total_readings
                FROM health_records 
                WHERE patient_id = %s 
                AND timestamp >= DATE_SUB(NOW(), INTERVAL %s DAY)
            ''', (patient_id, days))
            
            result = c.fetchone()
            c.close()
            conn.close()
            
            if result:
                return {
                    'avg_glucose': round(float(result[0]), 1) if result[0] else 0,
                    'min_glucose': round(float(result[1]), 1) if result[1] else 0,
                    'max_glucose': round(float(result[2]), 1) if result[2] else 0,
                    'total_readings': result[3]
                }
            
            return {'avg_glucose': 0, 'min_glucose': 0, 'max_glucose': 0, 'total_readings': 0}
        
        except Error as e:
            print(f"Error calculating statistics: {e}")
            return None

# Initialize database on module load
PatientManager.init_db()
patient_manager = PatientManager()
