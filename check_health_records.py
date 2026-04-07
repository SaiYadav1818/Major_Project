#!/usr/bin/env python3
"""Query health_records to show prediction dates stored in database"""
from models.patient import patient_manager

conn = patient_manager.get_connection()
if conn:
    c = conn.cursor()
    
    print("📊 ALL HEALTH RECORDS IN DATABASE")
    print("="*100)
    
    # Query 1: All records with timestamps
    c.execute('''
        SELECT id, patient_id, timestamp, age, bmi, predicted_glucose, status, risk_level 
        FROM health_records 
        ORDER BY timestamp ASC
    ''')
    
    records = c.fetchall()
    print(f"\nTotal records: {len(records)}\n")
    
    for record in records:
        print(f"ID: {record[0]}")
        print(f"  Patient: {record[1]}")
        print(f"  Timestamp: {record[2]}")
        print(f"  Age: {record[3]}, BMI: {record[4]}")
        print(f"  Glucose: {record[5]}, Status: {record[6]}, Risk: {record[7]}")
        print()
    
    # Query 2: Summary by patient
    print("="*100)
    print("\n📈 PREDICTIONS BY PATIENT")
    print("="*100)
    
    c.execute('''
        SELECT patient_id, COUNT(*) as total_predictions, 
               MIN(timestamp) as first_date, MAX(timestamp) as latest_date
        FROM health_records 
        GROUP BY patient_id
        ORDER BY patient_id
    ''')
    
    summaries = c.fetchall()
    for summary in summaries:
        print(f"\nPatient: {summary[0]}")
        print(f"  Total records: {summary[1]}")
        print(f"  First prediction: {summary[2]}")
        print(f"  Latest prediction: {summary[3]}")
    
    # Query 3: SQL to get dates for chart
    print("\n" + "="*100)
    print("\n🔍 SQL QUERY FOR CHART DATA")
    print("="*100)
    print("""
SELECT timestamp, predicted_glucose, status, risk_level, age, bmi, insulin_intake, blood_pressure
FROM health_records 
WHERE patient_id = 'YOUR_PATIENT_ID' 
ORDER BY timestamp ASC
LIMIT 30;
    """)
    
    c.close()
    conn.close()
else:
    print('Connection failed')
