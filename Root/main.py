# TARGET LOCATION: /main.py
# Purpose: Dynamic Day-of-Week Calendar Filtering Engine

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

app = FastAPI(title="RailSight Day-Aware Engine", version="1.5.0")

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
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)

@app.get("/api/transit-window")
async def get_transit_window(time_now: str = Query(None)):
    try:
        if not time_now:
            utc_now = datetime.datetime.now(datetime.timezone.utc)
            ist_offset = datetime.timedelta(hours=5, minutes=30)
            ist_now = utc_now + ist_offset
            parsed_time_obj = ist_now.time()
            time_str = ist_now.strftime("%H:%M:%S")
            current_date = ist_now.date()
        else:
            if len(time_now.split(':')) == 2:
                time_now = f"{time_now}:00"
            parsed_time_obj = datetime.time.fromisoformat(time_now)
            time_str = time_now
            current_date = datetime.date.today()

        # Extract current day integer (0=Monday, 6=Sunday)
        day_of_week = current_date.weekday()
        day_str = str(day_of_week)
        is_holiday = 1 if day_of_week == 6 else 0

        dummy_date = datetime.date.today()
        combined_dt = datetime.datetime.combine(dummy_date, parsed_time_obj)
        upper_bound_dt = combined_dt + datetime.timedelta(hours=3)
        upper_bound_time_obj = upper_bound_dt.time()

        conn = fetch_db_pool_connection()
        cursor = conn.cursor()

        # SMART QUERY LAYER: Explicitly forces the database to check if today's day number sits inside the running_days string!
        if upper_bound_time_obj < parsed_time_obj:
            query = """
                SELECT s.*, m.train_name, c.category_name, c.base_fare_per_km, m.is_specialty_unreserved
                FROM Live_Schedules s
                JOIN Train_Master m ON s.train_no = m.train_no
                JOIN Train_Category c ON m.category_id = c.category_id
                WHERE c.is_premium = FALSE
                  AND (m.running_days LIKE '%%' || %s || '%%')
                  AND (s.actual_departure >= %s OR s.actual_departure <= %s)
                ORDER BY s.actual_departure ASC;
            """
        else:
            query = """
                SELECT s.*, m.train_name, c.category_name, c.base_fare_per_km, m.is_specialty_unreserved
                FROM Live_Schedules s
                JOIN Train_Master m ON s.train_no = m.train_no
                JOIN Train_Category c ON m.category_id = c.category_id
                WHERE c.is_premium = FALSE
                  AND (m.running_days LIKE '%%' || %s || '%%')
                  AND s.actual_departure >= %s AND s.actual_departure <= %s
                ORDER BY s.actual_departure ASC;
            """

        cursor.execute(query, [day_str, parsed_time_obj, upper_bound_time_obj])
        active_records = cursor.fetchall()
        
        compiled_results = []

        for row in active_records:
            act_dep_val = row['actual_departure']
            h, m = (act_dep_val.hour, act_dep_val.minute) if hasattr(act_dep_val, 'hour') else map(int, str(act_dep_val).split(':')[:2])
            act_str = f"{h:02d}:{m:02d}"

            sched_dep_val = row['scheduled_departure']
            sched_str = sched_dep_val.strftime("%H:%M") if hasattr(sched_dep_val, 'hour') else str(sched_dep_val)[:5]

            # Let the AI predict crowd sizes based on the evaluated day parameters!
            features = np.array([[h, m, day_of_week, is_holiday]], dtype=np.int32)
            pred_id = int(loaded_classifier.predict(features))
            crowd_mapping = {0: "Low Density Available", 1: "Medium Commuter Volume", 2: "Heavy Rush - Expect Crowding"}

            calculated_fare = float(row['distance_km']) * float(row['base_fare_per_km'])
            category = str(row['category_name'])
            is_specialty_flag = bool(row['is_specialty_unreserved'])

            if is_specialty_flag:
                fine_text = "FINE PROTECTION SECURED: Fully Unreserved Train Configuration. Board cleanly with basic General class paper tickets."
                alert_color = "GREEN"
            elif category == "Ordinary":
                fine_text = "COMPLIANCE NOTICE: Valid for basic Ordinary Counter ticket."
                alert_color = "AMBER"
            elif category == "Express":
                fine_text = "TTE PENALTY NOTICE: Express Ticket Mandatory."
                alert_color = "ORANGE"
            elif category == "Superfast":
                fine_text = "CRITICAL LEGAL ADVISORY: Superfast Supplementary Surcharge Required."
                alert_color = "RED"

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
                "crowd_level": crowd_mapping.get(pred_id, "Normal Rush Indicators"),
                "crowd_id": pred_id,
                "fine_advisory": fine_text,
                "color_state": alert_color
            })

        cursor.close()
        conn.close()
        return {"meta": {"query_time": time_str, "route": "MAJN -> CLT", "day_evaluated": day_of_week}, "trains": compiled_results}

    except Exception as raw_error:
        return {"meta": {"query_time": "00:00:00", "route": "ERROR"}, "trains": [], "error_diagnostics": {"message": str(raw_error), "trace": traceback.format_exc()}}

app.mount("/", StaticFiles(directory="static", html=True), name="static")
