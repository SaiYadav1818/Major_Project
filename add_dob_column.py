#!/usr/bin/env python3
"""Add date_of_birth column to patients table"""
from models.patient import patient_manager

conn = patient_manager.get_connection()
if conn:
    c = conn.cursor()
    
    # Check if date_of_birth column exists
    c.execute("SHOW COLUMNS FROM patients LIKE 'date_of_birth'")
    exists = c.fetchone()
    
    if not exists:
        print("Adding date_of_birth column to patients table...")
        c.execute('''
            ALTER TABLE patients 
            ADD COLUMN date_of_birth DATE AFTER age
        ''')
        conn.commit()
        print("✅ Column added successfully")
    else:
        print("✅ date_of_birth column already exists")
    
    # Verify the updated structure
    c.execute("DESCRIBE patients")
    columns = c.fetchall()
    print("\nUpdated patients table structure:")
    print("="*70)
    for col in columns:
        print(f"  {col[0]}: {col[1]}")
    
    c.close()
    conn.close()
else:
    print("Connection failed")
