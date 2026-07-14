# TARGET LOCATION: /main.py
# Purpose: Real Data Static-Simulation Gateway Engine

import os
import datetime
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import joblib
import numpy as np
import traceback

app = FastAPI(title="RailSight Real-Data Simulator", version="4.0.0")

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

@app.get("/api/live-corridor")
async def get_live_corridor():
    try:
        utc_now = datetime.datetime.now(datetime.timezone.utc)
        ist_now = utc_now + datetime.timedelta(hours=5, minutes=30)
        day_of_week = ist_now.weekday()
        is_holiday = 1 if day_of_week == 6 else 0

        # REAL-WORLD FACTUAL DATA INTEGRATION MATRIX
        real_railway_dataset = [
            {
                "train_no": 12836,
                "name": "Antyodaya Express",
                "sched": "04:00",
                "actual": "04:15",
                "delay": 15,
                "base_fare": 187.85,
                "type": "Superfast",
                "location": "Kannur (CAN)",
                "msg": "Passed CAN at 06:12 AM - Running with 15m delay",
                "nodes": [
                    {"name": "MAJN (04:15)", "state": "passed"},
                    {"name": "KGQ (04:58)", "state": "passed"},
                    {"name": "CAN (06:12)", "state": "current-location"},
                    {"name": "CLT (07:22)", "state": "upcoming"}
                ]
            },
            {
                "train_no": 15102,
                "name": "Jan Sadharan Express",
                "sched": "10:45",
                "actual": "10:45",
                "delay": 0,
                "base_fare": 143.65,
                "type": "Express Run",
                "location": "Payyanur (PAY)",
                "msg": "Arrived at platform 1 - Running on schedule",
                "nodes": [
                    {"name": "MAQ (10:45)", "state": "passed"},
                    {"name": "KGQ (11:28)", "state": "passed"},
                    {"name": "KZE (11:47)", "state": "passed"},
                    {"name": "PAY (12:15)", "state": "current-location"},
                    {"name": "CAN (12:55)", "state": "upcoming"},
                    {"name": "TLY (13:18)", "state": "upcoming"},
                    {"name": "CLT (14:10)", "state": "upcoming"}
                ]
            },
            {
                "train_no": 13434,
                "name": "Amrit Bharat Express",
                "sched": "15:45",
                "actual": "16:15",
                "delay": 30,
                "base_fare": 187.85,
                "type": "Superfast",
                "location": "Kasaragod (KGQ)",
                "msg": "Approaching platform 2 - Delayed by 30 mins from yard",
                "nodes": [
                    {"name": "MAQ (16:15)", "state": "passed"},
                    {"name": "KGQ (17:05)", "state": "current-location"},
                    {"name": "PAY (17:48)", "state": "upcoming"},
                    {"name": "CAN (18:25)", "state": "upcoming"},
                    {"name": "TLY (18:48)", "state": "upcoming"},
                    {"name": "CLT (19:25)", "state": "upcoming"}
                ]
            }
        ]

        live_compiled_trains = []

        for train in real_railway_dataset:
            # Dynamically feed the real time parameters into your ML model
            act_hr, act_min = map(int, train["actual"].split(':'))
            features = np.array([[act_hr, act_min, day_of_week, is_holiday]], dtype=np.int32)
            pred_id = int(loaded_classifier.predict(features))
            crowd_mapping = {0: "Available Seating Tiers Present", 1: "Moderate Commuter Standee Load", 2: "Heavy Volume - Expect High Density"}

            live_compiled_trains.append({
                "train_no": train["train_no"],
                "train_name": train["name"],
                "category": train["type"],
                "scheduled": train["sched"],
                "delay": train["delay"],
                "actual": train["actual"],
                "fare": train["base_fare"],
                "crowd_level": crowd_mapping[pred_id],
                "crowd_id": pred_id,
                "current_location": train["location"],
                "status_message": train["msg"],
                "nodes": train["nodes"]
            })

        return {"meta": {"sync_time": ist_now.strftime("%H:%M:%S")}, "trains": live_compiled_trains}

    except Exception as raw_error:
        return {"error": str(raw_error), "trace": traceback.format_exc()}

app.mount("/", StaticFiles(directory="static", html=True), name="static")
