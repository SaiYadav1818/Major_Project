#!/usr/bin/env python
"""Test script to diagnose health_records insertion issues"""

from models.patient import patient_manager
import mysql.connector
from mysql.connector import Error

def test_connection():
    """Test database connection"""
    print("\n📌 Testing MySQL Connection...")
    conn = patient_manager.get_connection()
    if conn:
        print("✅ Connection successful")
        conn.close()
        return True
    else:
        print("❌ Connection failed")
        return False

def list_patients():
    """List all patients"""
    print("\n📌 Listing all patients...")
    try:
        conn = patient_manager.get_connection()
        if not conn:
            print("❌ Cannot connect to database")
            return False
        
        c = conn.cursor()
        c.execute("SELECT id, name, email FROM patients")
        patients = c.fetchall()
        c.close()
        conn.close()
        
        if patients:
            print(f"✅ Found {len(patients)} patients:")
            for patient in patients:
                print(f"   - {patient[0]}: {patient[1]} ({patient[2]})")
        else:
            print("⚠️  No patients found")
        return True
    except Error as e:
        print(f"❌ Error: {e}")
        return False

def list_health_records():
    """List all health records"""
    print("\n📌 Listing all health records...")
    try:
        conn = patient_manager.get_connection()
        if not conn:
            print("❌ Cannot connect to database")
            return False
        
        c = conn.cursor()
        c.execute("SELECT * FROM health_records ORDER BY timestamp DESC LIMIT 10")
        records = c.fetchall()
        c.close()
        conn.close()
        
        if records:
            print(f"✅ Found {len(records)} health records:")
            for record in records:
                print(f"   - ID: {record[0]}, Patient: {record[1]}, Glucose: {record[8]}, Status: {record[9]}")
        else:
            print("⚠️  No health records found")
        return True
    except Error as e:
        print(f"❌ Error: {e}")
        return False

def check_table_structure():
    """Check health_records table structure"""
    print("\n📌 Checking health_records table structure...")
    try:
        conn = patient_manager.get_connection()
        if not conn:
            print("❌ Cannot connect to database")
            return False
        
        c = conn.cursor()
        c.execute("DESCRIBE health_records")
        columns = c.fetchall()
        c.close()
        conn.close()
        
        print("✅ Table structure:")
        for col in columns:
            print(f"   - {col[0]}: {col[1]}")
        return True
    except Error as e:
        print(f"❌ Error: {e}")
        return False

def test_insert():
    """Test inserting a sample health record"""
    print("\n📌 Testing health record insertion...")
    try:
        # Get first patient
        conn = patient_manager.get_connection()
        if not conn:
            print("❌ Cannot connect to database")
            return False
        
        c = conn.cursor()
        c.execute("SELECT id FROM patients LIMIT 1")
        result = c.fetchone()
        c.close()
        conn.close()
        
        if not result:
            print("❌ No patients found - please register a patient first")
            return False
        
        patient_id = result[0]
        print(f"   Using patient: {patient_id}")
        
        # Try to insert a test record
        success = patient_manager.save_patient_prediction(
            patient_id=patient_id,
            age=45,
            bmi=28.5,
            insulin_intake=40.0,
            blood_pressure=130,
            diabetes_status=1,
            predicted_glucose=145.2,
            clinical_status="Hyperglycemic",
            risk_level="MODERATE"
        )
        
        if success:
            print("✅ Test record inserted successfully!")
            # Verify the record was saved
            conn = patient_manager.get_connection()
            c = conn.cursor()
            c.execute("SELECT * FROM health_records WHERE patient_id = %s ORDER BY timestamp DESC LIMIT 1", (patient_id,))
            record = c.fetchone()
            c.close()
            conn.close()
            if record:
                print(f"   Verified: ID={record[0]}, Glucose={record[8]}, Status={record[9]}")
        else:
            print("❌ Test insertion failed")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("   HEALTH_RECORDS DIAGNOSTIC TEST")
    print("=" * 60)
    
    test_connection()
    list_patients()
    check_table_structure()
    list_health_records()
    test_insert()
    
    print("\n" + "=" * 60)
    print("   TEST COMPLETE")
    print("=" * 60)
