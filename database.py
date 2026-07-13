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
            id SERIAL PRIMARY KEY,
            train_number VARCHAR(10) UNIQUE NOT NULL,
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
            ("16330", "MANGALURU JN - NAGERCOIL AMRIT BHARAT EXP", "08:00 AM", "11:07 AM", "3h 07m", "AMRIT BHARAT (GS)", 90, "HEAVY RUSH", "text-red-700 bg-red-50 border-red-200", "Rake operates purely via walk-on ticketing access. IRCTC drops zero local inventory allocations for this long-haul run."),
            ("16356", "MANGALURU JN - KOCHUVELI ANTYODAYA EXP", "08:10 PM", "11:15 PM", "3h 05m", "ANTYODAYA EXPRESS", 95, "HEAVY RUSH", "text-red-700 bg-red-50 border-red-200", "100% generic high-volume passenger rolling stock. Excluded structurally from commercial internet reservation pathways."),
            ("16603", "MAVELI EXPRESS (DE-RESERVED ZONE)", "05:30 PM", "08:45 PM", "3h 15m", "DE-RESERVED SLEEPER", 80, "MODERATE RUSH", "text-amber-700 bg-amber-50 border-amber-200", "Southern Railway de-reservation rule converts standard sleeper stock cars into unreserved platforms over this local link."),
            ("16630", "MALABAR EXPRESS", "06:15 PM", "09:35 PM", "3h 20m", "EXPRESS TIER", 80, "LOW RUSH", "text-green-700 bg-green-50 border-green-200", "Standard daily express infrastructure holding accessible unreserved generic segment sections front and back.")
        ]
        cur.executemany("""
            INSERT INTO unreserved_trains (train_number, name, departure, arrival, duration, tier, base_fare, live_density, density_color, justification_text)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, trains)
        
    conn.commit()
    cur.close()
    conn.close()
