#!/usr/bin/env python3
"""
Fix NULL timestamps in health_records table by backfilling with staggered dates
"""
from models.patient import patient_manager
from datetime import datetime, timedelta

conn = patient_manager.get_connection()
if conn:
    c = conn.cursor()
    
    # Update NULL timestamps with staggered times for realistic trend data
    c.execute('SELECT id FROM health_records WHERE timestamp IS NULL ORDER BY id')
    null_records = c.fetchall()
    
    if null_records:
        print(f'Found {len(null_records)} records with NULL timestamp')
        
        # Assign timestamps staggered over the last 30 days
        base_date = datetime.now() - timedelta(days=30)
        
        for idx, (record_id,) in enumerate(null_records):
            # Stagger timestamps evenly across 30 days
            timestamp = base_date + timedelta(days=idx * (30 // len(null_records)))
            c.execute('UPDATE health_records SET timestamp = %s WHERE id = %s', (timestamp, record_id))
            ts_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            print(f'  Updated record {record_id} -> {ts_str}')
        
        conn.commit()
        print(f'✅ Updated {len(null_records)} records with timestamps')
    else:
        print('✅ No NULL timestamps found')
    
    # Verify the update
    c.execute('SELECT id, timestamp, predicted_glucose FROM health_records ORDER BY id')
    records = c.fetchall()
    print('\nVerification - Updated records:')
    print('='*70)
    for record in records:
        ts_str = record[1].strftime("%Y-%m-%d %H:%M:%S") if record[1] else "NULL"
        print(f'ID: {record[0]}, Timestamp: {ts_str}, Glucose: {record[2]}')
    
    c.close()
    conn.close()
else:
    print('Connection failed')
