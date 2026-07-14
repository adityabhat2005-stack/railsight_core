# TARGET LOCATION: /main.py
# Purpose: Final Stable Asynchronous API Gateway running on Psycopg3

import os
import datetime
from fastapi import FastAPI, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import psycopg
from psycopg.rows import dict_row
import joblib
import numpy as np
import traceback

app = FastAPI(
    title="RailSight Ultimate Gateway",
    description="Production Router Core matching Python 3.14.3 constraints",
    version="1.1.0"
)

# Cross-Origin Isolation configuration for frontend mounting maps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.environ.get("DATABASE_URL", "")
MODEL_PATH = "crowd_model.pkl"

if not os.path.exists(MODEL_PATH):
    from ml_engine import train_and_export_model
    train_and_export_model(export_path=MODEL_PATH)

loaded_classifier = joblib.load(MODEL_PATH)

def fetch_db_pool_connection():
    if not DATABASE_URL:
        raise ValueError("CRITICAL INITIALIZATION CRASH: The DATABASE_URL secret parameter is empty on Render settings.")
    # Append required SSL flag to authorize handshake safely across Neon nodes
    cleaned_url = DATABASE_URL
    if "sslmode" not in cleaned_url:
        cleaned_url += "&sslmode=require" if "?" in cleaned_url else "?sslmode=require"
    return psycopg.connect(cleaned_url, row_factory=dict_row)

@app.get("/api/transit-window")
async def get_transit_window(time_now: str = Query(None, description="ISO input window index profile")):
    try:
        if not time_now:
            now_dt = datetime.datetime.now()
            time_str = now_dt.strftime("%H:%M:%S")
            current_date = now_dt.date()
        else:
            if len(time_now.split(':')) == 2:
                time_now = f"{time_now}:00"
            parsed_t = datetime.time.fromisoformat(time_now)
            time_str = parsed_t.strftime("%H:%M:%S")
            current_date = datetime.date.today()

        day_of_week = current_date.weekday()
        is_holiday = 1 if day_of_week == 6 else 0

        # Boot db session context safely
        conn = fetch_db_pool_connection()
        cursor = conn.cursor()

        # Target Query Layout: Clean positional parameters matching psycopg v3 spec layout
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

        cursor.execute(query, [time_str, time_str])
        active_records = cursor.fetchall()
        
        compiled_results = []

        for row in active_records:
            # Safe string casting conversions to protect against datetime data parsing bugs
            act_dep_val = row['actual_departure']
            if hasattr(act_dep_val, 'hour'):
                h, m = act_dep_val.hour, act_dep_val.minute
                act_str = act_dep_val.strftime("%H:%M")
            else:
                # Fallback string isolation layer splitter
                time_parts = str(act_dep_val).split(':')
                h, m = int(time_parts[0]), int(time_parts[1])
                act_str = f"{h:02d}:{m:02d}"

            sched_dep_val = row['scheduled_departure']
            sched_str = sched_dep_val.strftime("%H:%M") if hasattr(sched_dep_val, 'hour') else str(sched_dep_val)[:5]

            # Trigger lightweight AI predictive classification row array mappings
            features = np.array([[h, m, day_of_week, is_holiday]], dtype=np.int32)
            pred_id = int(loaded_classifier.predict(features)[0])
            crowd_mapping = {0: "Low Density Available", 1: "Medium Commuter Volume", 2: "Heavy Rush"}

            calculated_fare = float(row['distance_km']) * float(row['base_fare_per_km'])
            category = str(row['category_name'])

            if row['is_specialty_unreserved']:
                fine_text = "FINE PROTECTION SECURED: Fully Unreserved Train Configuration. Step directly inside with common General Ticket."
                alert_color = "GREEN"
            elif category == "Ordinary":
                fine_text = "COMPLIANCE NOTICE: Valid for basic Ordinary Counter ticket. Express/Superfast ticket holdings not requested."
                alert_color = "AMBER"
            elif category == "Express":
                fine_text = "TTE PENALTY NOTICE: Express Ticket Mandatory. Holding an Ordinary category ticket will trigger standard penalty fees."
                alert_color = "ORANGE"
            elif category == "Superfast":
                fine_text = "CRITICAL LEGAL ADVISORY: Superfast Supplementary Surcharge Required. Boarding with un-upgraded tiers results in an automatic fine."
                alert_color = "RED"
            else:
                fine_text = "Standard documentation tracking requirements applicable."
                alert_color = "GRAY"

            compiled_results.append({
                "train_no": int(row['train_no']),
                "train_name": str(row['train_name']),
                "category": category,
                "is_specialty": bool(row['is_specialty_unreserved']),
                "distance": float(row['distance_km']),
                "scheduled": sched_str,
                "delay": int(row['delay_minutes']),
                "actual": act_str,
                "fare": round(calculated_fare, 2),
                "crowd_level": crowd_mapping.get(pred_id, "Normal Rush Indicators"),
                "crowd_id": pred_id,
                "fine_advisory": fine_text,
                "color_state": alert_color
            })

        cursor.close()
        conn.close()
        return {"meta": {"query_time": time_str, "route": "MAJN -> CLT"}, "trains": compiled_results}

    except Exception as raw_error:
        # Emergency Safe Catch: Output the precise trace back to the UI grid instead of printing blank 500 blocks
        error_traceback = traceback.format_exc()
        return {
            "meta": {"query_time": "00:00:00", "route": "ERROR CAPTURED BLOCK"},
            "trains": [],
            "error_diagnostics": {
                "message": str(raw_error),
                "trace": error_traceback
            }
        }

# Mount static frontend components cleanly below API logic layout
app.mount("/", StaticFiles(directory="static", html=True), name="static")
