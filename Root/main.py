# TARGET LOCATION: /main.py
# Purpose: FastAPI Async Core Database Query Operations Routing Engine

import os
import datetime
from fastapi import FastAPI, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import psycopg
from psycopg.rows import dict_row
import joblib
import numpy as np

app = FastAPI(
    title="RailSight Engine Gateway",
    description="Production Endpoint Matrix serving the MAJN-CLT Unreserved Commuter Space",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/railsight")
MODEL_PATH = "crowd_model.pkl"

if not os.path.exists(MODEL_PATH):
    from ml_engine import train_and_export_model
    train_and_export_model(export_path=MODEL_PATH)

loaded_classifier = joblib.load(MODEL_PATH)

def fetch_db_pool_connection():
    try:
        # Connects smoothly to Neon Console using the modern psycopg v3 driver format
        return psycopg.connect(DATABASE_URL, row_factory=dict_row)
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Neon database gateway offline: {str(err)}")

@app.get("/api/transit-window")
async def get_transit_window(time_now: str = Query(None, description="ISO HH:MM:SS format constraint")):
    if not time_now:
        now_dt = datetime.datetime.now()
        time_str = now_dt.strftime("%H:%M:%S")
        current_date = now_dt.date()
    else:
        try:
            parsed_t = datetime.time.fromisoformat(time_now)
            time_str = parsed_t.strftime("%H:%M:%S")
            current_date = datetime.date.today()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid time payload. Use exact HH:MM:SS format.")

    day_of_week = current_date.weekday()
    is_holiday = 1 if day_of_week == 6 else 0 # Sunday validation mock flag logic
    
    conn = fetch_db_pool_connection()
    cursor = conn.cursor()
    
    # Real-time UTS-style rolling 3-hour constraint
    # Automatically filters out completely restricted premium services server-side
    query = """
        SELECT 
            s.schedule_id, s.train_no, m.train_name, c.category_name, 
            c.base_fare_per_km, m.is_specialty_unreserved, s.distance_km, 
            s.scheduled_departure, s.delay_minutes, s.actual_departure
        FROM Live_Schedules s
        JOIN Train_Master m ON s.train_no = m.train_no
        JOIN Train_Category c ON m.category_id = c.category_id
        WHERE c.is_premium = FALSE
          AND s.actual_departure >= %s::TIME
          AND s.actual_departure <= (%s::TIME + INTERVAL '3 hours')::TIME
        ORDER BY s.actual_departure ASC;
    """
    
    try:
        cursor.execute(query, (time_str, time_str))
        active_records = cursor.fetchall()
    except Exception as query_err:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=500, detail=f"Database compilation crash: {str(query_err)}")
        
    compiled_results = []
    
    for row in active_records:
        act_dep_obj = row['actual_departure']
        h, m = act_dep_obj.hour, act_dep_obj.minute
        
        # Feed parameters directly into loaded Random Forest model
        features = np.array([[h, m, day_of_week, is_holiday]])
        pred_id = int(loaded_classifier.predict(features)[0])
        crowd_mapping = {0: "Low Density Available", 1: "Medium Commuter Volume", 2: "Heavy Rush"}
        
        # Automated Fare Mapping Script Calculation Engine
        calculated_fare = float(row['distance_km'] * row['base_fare_per_km'])
        
        # Proactive Fine Protection Legal Mapping Logic Block
        category = row['category_name']
        if row['is_specialty_unreserved']:
            fine_text = "FINE PROTECTION SECURED: Fully Unreserved Train Configuration. Board cleanly with basic General class paper tickets."
            alert_color = "GREEN"
        elif category == "Ordinary":
            fine_text = "COMPLIANCE NOTICE: Valid exclusively for basic Ordinary Counter ticket. Express/Superfast ticket categories not required."
            alert_color = "AMBER"
        elif category == "Express":
            fine_text = "TTE PENALTY NOTICE: Express Ticket Mandatory. Holding an Ordinary ticket will result in static penalty rules."
            alert_color = "ORANGE"
        elif category == "Superfast":
            fine_text = "CRITICAL LEGAL ADVISORY: Superfast Supplementary Surcharge Required. Boarding with lower tier ticket categories results in an automatic fine."
            alert_color = "RED"
        else:
            fine_text = "Standard documentation compliance required."
            alert_color = "GRAY"
            
        compiled_results.append({
            "train_no": row['train_no'],
            "train_name": row['train_name'],
            "category": category,
            "is_specialty": row['is_specialty_unreserved'],
            "distance": float(row['distance_km']),
            "scheduled": row['scheduled_departure'].strftime("%H:%M"),
            "delay": row['delay_minutes'],
            "actual": act_dep_obj.strftime("%H:%M"),
            "fare": round(calculated_fare, 2),
            "crowd_level": crowd_mapping[pred_id],
            "crowd_id": pred_id,
            "fine_advisory": fine_text,
            "color_state": alert_color
        })
        
    cursor.close()
    conn.close()
    return {"meta": {"query_time": time_str, "route": "MAJN -> CLT"}, "trains": compiled_results}

# Mount lightweight web UI directory natively to deliver fast page views
app.mount("/", StaticFiles(directory="static", html=True), name="static")
