# TARGET LOCATION: /main.py
# Purpose: No-Time-Filter Gateway Engine for Immediate Data Delivery

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

app = FastAPI(title="RailSight Unfiltered Gateway", version="1.7.0")

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
        raise ValueError("DATABASE_URL variable is missing in Render environment.")
    cleaned_url = DATABASE_URL
    if "sslmode" not in cleaned_url:
        cleaned_url += "&sslmode=require" if "?" in cleaned_url else "?sslmode=require"
    return psycopg.connect(cleaned_url, row_factory=dict_row)

@app.get("/api/transit-window")
async def get_transit_window(time_now: str = Query(None)):
    try:
        # Track the input time purely for logging and dashboard display meta properties
        if not time_now:
            time_str = "Live Clock Sync"
        else:
            time_str = time_now

        current_date = datetime.date.today()
        day_of_week = current_date.weekday()
        day_str = str(day_of_week)
        is_holiday = 1 if day_of_week == 6 else 0

        conn = fetch_db_pool_connection()
        cursor = conn.cursor()

        # REMOVED FILTER LAYER: The 3-hour time check is completely gone! 
        # This scans your entire 24-hour table setup matching the day.
        query = """
            SELECT s.*, m.train_name, c.category_name, c.base_fare_per_km, m.is_specialty_unreserved
            FROM Live_Schedules s
            JOIN Train_Master m ON s.train_no = m.train_no
            JOIN Train_Category c ON m.category_id = c.category_id
            WHERE c.is_premium = FALSE
              AND (m.running_days LIKE '%%' || %s || '%%')
            ORDER BY s.actual_departure ASC;
        """

        cursor.execute(query, [day_str])
        active_records = cursor.fetchall()
        
        compiled_results = []

        for row in active_records:
            act_dep_val = row['actual_departure']
            if hasattr(act_dep_val, 'hour'):
                h, m = act_dep_val.hour, act_dep_val.minute
                act_str = act_dep_val.strftime("%H:%M")
            else:
                time_parts = str(act_dep_val).split(':')
                h, m = int(time_parts[0]), int(time_parts[1])
                act_str = f"{h:02d}:{m:02d}"

            sched_dep_val = row['scheduled_departure']
            sched_str = sched_dep_val.strftime("%H:%M") if hasattr(sched_dep_val, 'hour') else str(sched_dep_val)[:5]

            # Custom Machine Learning inference prediction using the evaluated departure parameters
            features = np.array([[h, m, day_of_week, is_holiday]], dtype=np.int32)
            pred_id = int(loaded_classifier.predict(features))
            crowd_mapping = {0: "Low Density Available", 1: "Medium Commuter Volume", 2: "Heavy Rush - Expect Crowding"}

            calculated_fare = float(row['distance_km']) * float(row['base_fare_per_km'])
            category = str(row['category_name'])
            is_specialty_flag = str(row['is_specialty_unreserved']).lower() in ['true', '1', 't', 'yes']

            if is_specialty_flag:
                fine_text = "FINE PROTECTION SECURED: Fully Unreserved Train configuration. Step inside with a General Ticket."
                alert_color = "GREEN"
            elif category == "Ordinary":
                fine_text = "COMPLIANCE NOTICE: Valid for basic Ordinary Counter ticket."
                alert_color = "AMBER"
            elif category == "Express":
                fine_text = "TTE PENALTY NOTICE: Express Ticket Mandatory. Basic ticket will face fines."
                alert_color = "ORANGE"
            elif category == "Superfast":
                fine_text = "CRITICAL LEGAL ADVISORY: Superfast Supplementary Surcharge Required."
                alert_color = "RED"
            else:
                fine_text = "Standard documentation tracking requirements applicable."
                alert_color = "GRAY"

            compiled_results.append({
                "train_no": int(row['train_no']),
                "train_name": str(row['train_name']),
                "category": category,
                "is_specialty": is_specialty_flag,
                "distance": float(row['distance_km']),
                "scheduled": sched_str,
                "delay": int(row['delay_minutes']),
                "actual": act_str,
                "fare": round(calculated_fare, 2),
                "crowd_level": crowd_mapping.get(pred_id, "Normal volume"),
                "crowd_id": pred_id,
                "fine_advisory": fine_text,
                "color_state": alert_color
            })

        cursor.close()
        conn.close()
        return {"meta": {"query_time": time_str, "route": "MAJN -> CLT (Time Filter Disabled)"}, "trains": compiled_results}

    except Exception as raw_error:
        return {"meta": {"query_time": "00:00:00", "route": "ERROR"}, "trains": [], "error_diagnostics": {"message": str(raw_error), "trace": traceback.format_exc()}}

app.mount("/", StaticFiles(directory="static", html=True), name="static")
