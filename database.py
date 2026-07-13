# database.py
import os
import psycopg2
from psycopg2.extras import RealDictCursor

# Pulled securely from Render's Environment Variables dashboard
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    """Generates an operational database engine thread directly to your Neon Console."""
    if not DATABASE_URL:
        raise RuntimeError("Neon Cluster Authentication Fail: DATABASE_URL variable missing.")
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def init_neon_tables():
    """Run this function once inside main.py to create the table structure in Neon."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Generate the table mapping our specialized train types
    cur.execute("""
        CREATE TABLE IF NOT EXISTS unreserved_trains (
            train_number VARCHAR(20) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            departure VARCHAR(20) NOT NULL,
            arrival VARCHAR(20) NOT NULL,
            duration VARCHAR(20) NOT NULL,
            tier VARCHAR(50) NOT NULL,
            base_fare INT NOT NULL,
            live_density VARCHAR(50) NOT NULL,
            density_color VARCHAR(100) NOT NULL,
            justification_text TEXT NOT NULL
        );
    """)
    
    # Check if data already exists to avoid duplication
    cur.execute("SELECT COUNT(*) FROM unreserved_trains;")
    if cur.fetchone()['count'] == 0:
        trains = [
            ("12621", "Mangaluru Express", "08:00", "17:30", "9h 30m", "AMRIT BHARAT (GS)", 450, "HIGH", "text-red-700 bg-red-50 border-red-200", "High volume unreserved availability on Konkan Railway"),
            ("16590", "Antyodaya Coastal", "10:30", "19:45", "9h 15m", "ANTYODAYA EXPRESS", 380, "MEDIUM", "text-amber-700 bg-amber-50 border-amber-200", "Social welfare unreserved express service"),
            ("17339", "Coastal Suryanagari", "14:15", "23:30", "9h 15m", "AMRIT BHARAT (GS)", 425, "HIGH", "text-red-700 bg-red-50 border-red-200", "Regional unreserved express on coastal line"),
            ("18633", "KK Express", "16:45", "02:15", "9h 30m", "DE-RESERVED SLEEPER", 520, "LOW", "text-green-700 bg-green-50 border-green-200", "De-reserved sleeper compartment availability"),
            ("11040", "Amrit Bharat Fast", "06:00", "15:30", "9h 30m", "AMRIT BHARAT (GS)", 435, "MEDIUM", "text-amber-700 bg-amber-50 border-amber-200", "Fast unreserved service with multiple stops"),
            ("12589", "Express Rajya", "20:30", "06:00", "9h 30m", "EXPRESS TIER", 400, "HIGH", "text-red-700 bg-red-50 border-red-200", "Evening unreserved express on MAJN-CLT route")
        ]
        cur.executemany("""
            INSERT INTO unreserved_trains (train_number, name, departure, arrival, duration, tier, base_fare, live_density, density_color, justification_text)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, trains)
    
    # Create train_master table for tracking
    cur.execute("""
        CREATE TABLE IF NOT EXISTS train_master (
            train_no VARCHAR(20) PRIMARY KEY,
            train_name VARCHAR(100) NOT NULL,
            category_id INT
        );
    """)
    
    # Create train_tracking table for live tracking
    cur.execute("""
        CREATE TABLE IF NOT EXISTS train_tracking (
            id SERIAL PRIMARY KEY,
            train_no VARCHAR(20) NOT NULL,
            current_station VARCHAR(100) NOT NULL,
            current_latitude DECIMAL(10, 6) NOT NULL,
            current_longitude DECIMAL(10, 6) NOT NULL,
            distance_covered_km DECIMAL(8, 2) NOT NULL,
            distance_remaining_km DECIMAL(8, 2) NOT NULL,
            current_speed_kmph DECIMAL(6, 1) NOT NULL,
            delay_minutes INT NOT NULL,
            timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR(20) NOT NULL,
            FOREIGN KEY(train_no) REFERENCES train_master(train_no)
        );
    """)
    
    # Populate train_master if empty
    cur.execute("SELECT COUNT(*) FROM train_master;")
    if cur.fetchone()['count'] == 0:
        trains_master = [
            ("12621", "Mangaluru Express"),
            ("16590", "Antyodaya Coastal"),
            ("17339", "Coastal Suryanagari"),
            ("18633", "KK Express"),
            ("11040", "Amrit Bharat Fast"),
            ("12589", "Express Rajya")
        ]
        cur.executemany("""
            INSERT INTO train_master (train_no, train_name) VALUES (%s, %s);
        """, trains_master)
    
    # Populate train_tracking if empty
    cur.execute("SELECT COUNT(*) FROM train_tracking;")
    if cur.fetchone()['count'] == 0:
        from datetime import datetime, timedelta
        now = datetime.utcnow()
        
        tracking_data = [
            # Train 12621
            ("12621", "Udupi Junction", 13.3500, 74.7421, 150.00, 230.00, 62.5, 5, now - timedelta(minutes=180), "RUNNING"),
            ("12621", "Kundapura", 13.5224, 74.6787, 170.00, 210.00, 65.0, 3, now - timedelta(minutes=150), "RUNNING"),
            ("12621", "Byndoor", 13.6854, 74.6432, 200.00, 180.00, 68.0, 4, now - timedelta(minutes=120), "RUNNING"),
            ("12621", "Honnavar", 13.8765, 74.4321, 240.00, 140.00, 70.5, 5, now - timedelta(minutes=90), "RUNNING"),
            ("12621", "Kumta", 14.0123, 74.3012, 280.00, 100.00, 72.0, 8, now - timedelta(minutes=45), "RUNNING"),
            ("12621", "Karwar", 14.8091, 74.3107, 320.00, 60.00, 75.0, 5, now, "RUNNING"),
            # Train 16590
            ("16590", "Perdur", 13.1234, 74.9876, 80.00, 300.00, 58.0, 0, now - timedelta(minutes=180), "RUNNING"),
            ("16590", "Kundapura", 13.5224, 74.6787, 130.00, 250.00, 62.0, 0, now - timedelta(minutes=150), "RUNNING"),
            ("16590", "Byndoor", 13.6854, 74.6432, 160.00, 220.00, 64.5, 2, now - timedelta(minutes=120), "RUNNING"),
            ("16590", "Honnavar", 13.8765, 74.4321, 200.00, 180.00, 66.0, 0, now - timedelta(minutes=90), "RUNNING"),
            ("16590", "Kumta", 14.0123, 74.3012, 240.00, 140.00, 68.5, 1, now - timedelta(minutes=45), "RUNNING"),
            ("16590", "Karwar", 14.8091, 74.3107, 280.00, 100.00, 70.0, 0, now, "RUNNING"),
            # Train 17339
            ("17339", "Kundapura", 13.5224, 74.6787, 80.00, 300.00, 55.0, 15, now - timedelta(minutes=180), "DELAYED"),
            ("17339", "Byndoor", 13.6854, 74.6432, 110.00, 270.00, 57.5, 18, now - timedelta(minutes=150), "DELAYED"),
            ("17339", "Honnavar", 13.8765, 74.4321, 140.00, 240.00, 59.0, 20, now - timedelta(minutes=120), "DELAYED"),
            ("17339", "Kumta", 14.0123, 74.3012, 165.00, 215.00, 61.0, 15, now - timedelta(minutes=90), "RUNNING"),
            ("17339", "Karwar", 14.8091, 74.3107, 200.00, 180.00, 62.5, 12, now - timedelta(minutes=45), "RUNNING"),
            ("17339", "Sirsi Road", 14.6234, 75.1890, 230.00, 150.00, 64.0, 10, now, "RUNNING"),
            # Train 18633
            ("18633", "Perdur", 13.1234, 74.9876, 130.00, 250.00, 70.0, 8, now - timedelta(minutes=180), "RUNNING"),
            ("18633", "Udupi Junction", 13.3500, 74.7421, 160.00, 220.00, 72.0, 6, now - timedelta(minutes=150), "RUNNING"),
            ("18633", "Kundapura", 13.5224, 74.6787, 190.00, 190.00, 74.0, 8, now - timedelta(minutes=120), "RUNNING"),
            ("18633", "Honnavar", 13.8765, 74.4321, 240.00, 140.00, 75.5, 10, now - timedelta(minutes=90), "RUNNING"),
            ("18633", "Kumta", 14.0123, 74.3012, 280.00, 100.00, 76.0, 8, now - timedelta(minutes=45), "RUNNING"),
            ("18633", "Karwar", 14.8091, 74.3107, 320.00, 60.00, 78.0, 8, now, "RUNNING"),
            # Train 11040
            ("11040", "Mangaluru Central", 12.8675, 74.8568, 40.00, 340.00, 50.0, 0, now - timedelta(minutes=180), "RUNNING"),
            ("11040", "Perdur", 13.1234, 74.9876, 60.00, 320.00, 52.0, 0, now - timedelta(minutes=150), "RUNNING"),
            ("11040", "Udupi Junction", 13.3500, 74.7421, 95.00, 285.00, 54.0, 0, now - timedelta(minutes=120), "RUNNING"),
            ("11040", "Kundapura", 13.5224, 74.6787, 115.00, 265.00, 56.0, 0, now - timedelta(minutes=90), "RUNNING"),
            ("11040", "Byndoor", 13.6854, 74.6432, 140.00, 240.00, 58.0, 0, now - timedelta(minutes=45), "RUNNING"),
            ("11040", "Honnavar", 13.8765, 74.4321, 165.00, 215.00, 60.0, 0, now, "RUNNING"),
            # Train 12589
            ("12589", "Udupi Junction", 13.3500, 74.7421, 190.00, 190.00, 65.0, 12, now - timedelta(minutes=180), "RUNNING"),
            ("12589", "Kundapura", 13.5224, 74.6787, 220.00, 160.00, 67.0, 10, now - timedelta(minutes=150), "RUNNING"),
            ("12589", "Byndoor", 13.6854, 74.6432, 250.00, 130.00, 69.0, 11, now - timedelta(minutes=120), "RUNNING"),
            ("12589", "Honnavar", 13.8765, 74.4321, 290.00, 90.00, 71.0, 12, now - timedelta(minutes=90), "RUNNING"),
            ("12589", "Kumta", 14.0123, 74.3012, 330.00, 50.00, 73.0, 12, now - timedelta(minutes=45), "RUNNING"),
            ("12589", "Kozhikode Main", 11.8745, 75.3704, 380.00, 0.00, 0.0, 12, now, "ARRIVED")
        ]
        cur.executemany("""
            INSERT INTO train_tracking (train_no, current_station, current_latitude, current_longitude, distance_covered_km, distance_remaining_km, current_speed_kmph, delay_minutes, timestamp, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, tracking_data)
        
    conn.commit()
    cur.close()
    conn.close()
