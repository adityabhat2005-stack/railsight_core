# TARGET LOCATION: /main.py
# Purpose: Self-Contained Live GPS Telemetry Simulation Gateway Engine

import os
import datetime
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import joblib
import numpy as np
import traceback

app = FastAPI(title="RailSight Live Radar Engine", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = "crowd_model.pkl"
if not os.path.exists(MODEL_PATH):
    from ml_engine import train_and_export_model
    train_and_export_model(export_path=MODEL_PATH)

loaded_classifier = joblib.load(MODEL_PATH)

def calculate_live_gps_spot(train_no: int, current_hour: int, current_minute: int):
    """
    Simulates real-time physical track positions along the MAJN-CLT line
    based on the actual current time parameters.
    """
    total_minutes = (current_hour * 60) + current_minute
    
    # 1. ANTYODAYA EXPRESS POSITION ENGINE
    if train_no == 12836:
        # Scheduled 13:10, Actual 13:30. Runs 13:30 to 16:30
        start = (13 * 60) + 30
        if total_minutes < start:
            return {"delay": 20, "location": "Mangaluru Yard", "msg": "Rake Stable at Platform"}
        elif total_minutes > start + 180:
            return {"delay": 15, "location": "Kozhikode Main (CLT)", "msg": "Terminated at Destination"}
        else:
            pct = (total_minutes - start) / 180
            if pct < 0.25: return {"delay": 20, "location": "Kasaragod (KGQ)", "msg": "Departed Platform 2"}
            elif pct < 0.60: return {"delay": 15, "location": "Approaching Kannur (CAN)", "msg": "Signals Clear"}
            else: return {"delay": 10, "location": "Thalassery (TLY)", "msg": "In Transit"}

    # 2. JAN SADHARAN EXPRESS POSITION ENGINE
    elif train_no == 15102:
        # Scheduled 14:45, On Time. Runs 14:45 to 17:50
        start = (14 * 60) + 45
        if total_minutes < start:
            return {"delay": 0, "location": "Mangaluru Central (MAJN)", "msg": "Boarding Active at PF 3"}
        elif total_minutes > start + 185:
            return {"delay": 0, "location": "Kozhikode Main (CLT)", "msg": "Terminated"}
        else:
            pct = (total_minutes - start) / 185
            if pct < 0.30: return {"delay": 0, "location": "Payyanur (PAY)", "msg": "In Transit"}
            elif pct < 0.70: return {"delay": 5, "location": "Kannur (CAN)", "msg": "Arriving on PF 1"}
            else: return {"delay": 0, "location": "Badagara (BDY)", "msg": "Signals Green"}

    # 3. AMRIT BHARAT EXPRESS POSITION ENGINE
    else:
        # Scheduled 15:10, Delayed 15:50. Runs 15:50 to 19:10
        start = (15 * 60) + 50
        if total_minutes < start:
            return {"delay": 40, "location": "Mangaluru Main Yard", "msg": "Delayed Start - Awaiting Loco"}
        elif total_minutes > start + 200:
            return {"delay": 30, "location": "Kozhikode Main (CLT)", "msg": "Arrived"}
        else:
            pct = (total_minutes - start) / 200
            if pct < 0.40: return {"delay": 40, "location": "Kasaragod (KGQ)", "msg": "Regulating Speed"}
            else: return {"delay": 35, "location": "Payyanur (PAY)", "msg": "Running Late"}

# TARGET LOCATION: /main.py -> Replace the /api/live-corridor function block
import pandas as pd # Make sure this import is added to the top of your file!

@app.get("/api/live-corridor")
async def get_live_corridor():
    try:
        # Capture current local Indian Standard Time (IST) variables
        utc_now = datetime.datetime.now(datetime.timezone.utc)
        ist_now = utc_now + datetime.timedelta(hours=5, minutes=30)
        h, m = ist_now.hour, ist_now.minute
        day_of_week = ist_now.weekday()
        is_holiday = 1 if day_of_week == 6 else 0

        master_fleet = [
            {"train_no": 12836, "name": "Antyodaya Express", "sched": "13:10", "base_fare": 187.85, "type": "Superfast"},
            {"train_no": 15102, "name": "Jan Sadharan Express", "sched": "14:45", "base_fare": 143.65, "type": "Express Run"},
            {"train_no": 13434, "name": "Amrit Bharat Express", "sched": "15:10", "base_fare": 187.85, "type": "Superfast"}
        ]

        live_compiled_trains = []

        for train in master_fleet:
            # Run local tracking calculations matching the exact current minute
            telemetry = calculate_live_gps_spot(train["train_no"], h, m)
            
            # Compute dynamic arrival time strings
            sched_hr, sched_min = map(int, train["sched"].split(':'))
            actual_time = datetime.datetime.combine(datetime.date.today(), datetime.time(sched_hr, sched_min))
            actual_time += datetime.timedelta(minutes=telemetry["delay"])
            actual_str = actual_time.strftime("%H:%M")

            # FIX: Format parameters into a proper Pandas DataFrame with matching structural text headers
            # This completely stops the scikit-learn validation warnings in your deployment log stream
            features_df = pd.DataFrame([{
                'departure_hour': int(actual_time.hour),
                'departure_minute': int(actual_time.minute),
                'day_of_the_week': int(day_of_week),
                'is_holiday': int(is_holiday)
            }])
            
            pred_id = int(loaded_classifier.predict(features_df)[0])
            crowd_mapping = {0: "Available Seating Tiers Present", 1: "Moderate Commuter Standee Load", 2: "Heavy Volume - Expect High Density"}

            live_compiled_trains.append({
                "train_no": train["train_no"],
                "train_name": train["name"],
                "category": train["type"],
                "scheduled": train["sched"],
                "delay": telemetry["delay"],
                "actual": actual_str,
                "fare": train["base_fare"],
                "crowd_level": crowd_mapping[pred_id],
                "crowd_id": pred_id,
                "current_location": telemetry["location"],
                "status_message": telemetry["msg"]
            })

        return {"meta": {"sync_time": ist_now.strftime("%H:%M:%S")}, "trains": live_compiled_trains}

    except Exception as raw_error:
        return {"error": str(raw_error), "trace": traceback.format_exc()}


app.mount("/", StaticFiles(directory="static", html=True), name="static")
