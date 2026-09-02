# main.py
import os
import datetime
import traceback
import joblib
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from ml_engine import train_and_export_model  # import training function

app = FastAPI(title="RailSight Final Master Engine", version="12.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = "crowd_model.pkl"

# Auto-train if model file is missing
if not os.path.exists(MODEL_PATH):
    print("[*] No model found, training now...")
    train_and_export_model(export_path=MODEL_PATH)

# Load the ML model
crowd_model = joblib.load(MODEL_PATH)
crowd_map = {0: "Low Volume", 1: "Moderate Load", 2: "Heavy Rush"}

@app.get("/api/live-corridor")
async def get_live_corridor():
    try:
        utc_now = datetime.datetime.now(datetime.timezone.utc)
        ist_now = utc_now + datetime.timedelta(hours=5, minutes=30)
        h, m = ist_now.hour, ist_now.minute
        day_of_week = ist_now.weekday()

        # Example train dataset (still static for trains, but crowd is ML-driven)
        trains = [
            {"train_no": 12836, "train_name": "Antyodaya Express", "sched": "04:00", "actual": "04:15", "delay": 15,
             "fare": 187.85, "category": "Superfast",
             "nodes": [{"name": "MAJN"}, {"name": "KGQ"}, {"name": "CAN"}, {"name": "CLT"}]}
        ]

        for t in trains:
            # Predict crowd density dynamically
            features = [[h, m, day_of_week, 0]]  # holiday flag = 0 for now
            crowd_pred = int(crowd_model.predict(features)[0])
            t["crowd_id"] = crowd_pred
            t["crowd_level"] = crowd_map[crowd_pred]

        return {"meta": {"sync_time": ist_now.strftime("%H:%M:%S")}, "trains": trains}

    except Exception as raw_error:
        return {"meta": {"sync_time": "00:00:00"}, "trains": [], "error": str(raw_error), "trace": traceback.format_exc()}

app.mount("/", StaticFiles(directory="static", html=True), name="static")
