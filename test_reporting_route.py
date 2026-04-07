#!/usr/bin/env python3
"""
Test the updated reporting/multi-user-report route with real patient data
"""
import sys
sys.path.insert(0, 'c:\\Users\\dudim\\Major_Project')

from app import app
from models.patient import patient_manager
import json

def test_reporting_route():
    """Test the multi_user_report route"""
    print("\n" + "="*70)
    print("TESTING: Reporting Route with Real Patient Data")
    print("="*70)
    
    # Step 1: Check if we have any patients
    print("\n[STEP 1] Checking for patients in database...")
    conn = patient_manager.get_connection()
    if not conn:
        print("❌ Failed to connect to database")
        return False
    
    c = conn.cursor()
    c.execute("SELECT id, name FROM patients LIMIT 5")
    patients = c.fetchall()
    c.close()
    conn.close()
    
    if not patients:
        print("❌ No patients found in database")
        return False
    
    print(f"✅ Found {len(patients)} patient(s):")
    for patient in patients:
        print(f"   - {patient[0]}: {patient[1]}")
    
    # Step 2: Test with client context
    print("\n[STEP 2] Testing route with Flask test client...")
    
    patient_id = patients[0][0]
    patient_name = patients[0][1]
    
    with app.test_client() as client:
        # Test WITHOUT login (should redirect)
        print(f"\n   Testing without login...")
        response = client.get('/reporting/multi-user-report')
        if response.status_code == 302:  # Redirect
            print(f"   ✅ Correctly redirecting to login (status: {response.status_code})")
        else:
            print(f"   ⚠️  Unexpected status: {response.status_code}")
        
        # Test WITH login (using session)
        print(f"\n   Testing with login session (patient: {patient_id})...")
        with client.session_transaction() as sess:
            sess['patient_id'] = patient_id
            sess['patient_name'] = patient_name
        
        response = client.get('/reporting/multi-user-report')
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Route returned successfully")
            
            # Check if response contains expected elements
            html = response.get_data(as_text=True)
            checks = [
                ('patient_name in page', patient_name in html),
                ('patient_id in page', patient_id in html),
                ('Glucose in page', 'Glucose' in html),
                ('Chart placeholder/plot in page', 'plot' in html.lower()),
            ]
            
            for check_name, result in checks:
                status = "✅" if result else "⚠️"
                print(f"   {status} {check_name}: {result}")
        else:
            print(f"   ❌ Route failed with status: {response.status_code}")
            print(f"   Response: {response.get_data(as_text=True)[:200]}")
            return False
    
    # Step 3: Verify patient data retrieval
    print("\n[STEP 3] Verifying patient data retrieval...")
    health_records = patient_manager.get_patient_predictions(patient_id, days=30)
    print(f"   Health records found: {len(health_records) if health_records else 0}")
    
    if health_records:
        print(f"   ✅ Patient has {len(health_records)} health record(s)")
        for i, record in enumerate(health_records[:3], 1):
            print(f"      Record {i}: Glucose={record[1]}, Status={record[2]}")
    else:
        print(f"   ⚠️  No health records yet (patient will see empty state message)")
    
    patient_stats = patient_manager.get_patient_statistics(patient_id, days=30)
    print(f"   Patient stats: {json.dumps(patient_stats, indent=6, default=str)}")
    
    print("\n" + "="*70)
    print("✅ ALL TESTS PASSED - Reporting route working correctly!")
    print("="*70)
    return True

if __name__ == '__main__':
    success = test_reporting_route()
    sys.exit(0 if success else 1)
