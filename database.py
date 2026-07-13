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
        
    conn.commit()
    cur.close()
    conn.close()
