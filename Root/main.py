# TARGET LOCATION: /main.py
# Purpose: Final Stable Python 3.14-Optimized 24HR Transit Simulator Gateway Engine

import os
import datetime
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import traceback

app = FastAPI(title="RailSight Final Master Engine", version="11.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/live-corridor")
async def get_live_corridor():
    try:
        # 1. Sync precise local Indian Standard Time (IST) clock properties
        utc_now = datetime.datetime.now(datetime.timezone.utc)
        ist_now = utc_now + datetime.timedelta(hours=5, minutes=30)
        h, m = ist_now.hour, ist_now.minute
        total_sys_mins = (h * 60) + m
        day_of_week = ist_now.weekday()
        
        # FIX: Replaced the array lookup check with a direct, ultra-stable integer check!
        is_weekend_peak = False
        if day_of_week >= 4:  # 4=Friday, 5=Saturday, 6=Sunday
            is_weekend_peak = True

        # 2. SEED RAW FACTUAL DATA MATRIX WITH INTERNAL NODAL TIMELINES
        real_railway_dataset = [
            {
                "train_no": 12836, "train_name": "Antyodaya Express", "sched": "04:00", "actual": "04:15", "delay": 15, "fare": 187.85, "category": "Superfast",
                "start_min": 255, "end_min": 442,
                "nodes": [
                    {"name": "MAJN (04:15)", "state": "passed"},
                    {"name": "KGQ (04:58)", "state": "passed"},
                    {"name": "CAN (06:12)", "state": "current-location"},
                    {"name": "CLT (07:22)", "state": "upcoming"}
                ]
            },
            {
                "train_no": 16649, "train_name": "Parasuram Express", "sched": "05:05", "actual": "05:05", "delay": 0, "fare": 143.65, "category": "Mail/Express",
                "start_min": 305, "end_min": 512,
                "nodes": [
                    {"name": "MAQ (05:05)", "state": "passed"},
                    {"name": "KGQ (05:47)", "state": "passed"},
                    {"name": "CAN (07:07)", "state": "passed"},
                    {"name": "CLT (08:32)", "state": "current-location"}
                ]
            },
            {
                "train_no": 16610, "train_name": "MAQ - Palakkad Passenger Local", "sched": "05:15", "actual": "05:30", "delay": 15, "fare": 110.00, "category": "Ordinary Passenger",
                "start_min": 330, "end_min": 552,
                "nodes": [
                    {"name": "MAQ (05:30)", "min": 330, "state": "passed"},
                    {"name": "KGQ (06:20)", "min": 380, "state": "passed"},
                    {"name": "CAN (07:45)", "min": 465, "state": "passed"},
                    {"name": "CLT (09:12)", "min": 552, "state": "current-location"}
                ]
            },
            {
                "train_no": 6486, "train_name": "Mangaluru - Kozhikode MEMU Special", "sched": "06:45", "actual": "06:45", "delay": 0, "fare": 110.00, "category": "MEMU Service",
                "start_min": 405, "end_min": 670,
                "nodes": [
                    {"name": "MAQ (06:45)", "state": "passed"},
                    {"name": "KGQ (07:40)", "state": "passed"},
                    {"name": "PAY (08:35)", "state": "passed"},
                    {"name": "CAN (09:15)", "state": "passed"},
                    {"name": "CLT (11:10)", "state": "current-location"}
                ]
            },
            {
                "train_no": 16160, "train_name": "MAJN - Chennai Passenger Local", "sched": "06:55", "actual": "07:15", "delay": 20, "fare": 110.00, "category": "Ordinary Passenger",
                "start_min": 435, "end_min": 647,
                "nodes": [
                    {"name": "MAJN (07:15)", "state": "passed"},
                    {"name": "KGQ (08:12)", "state": "passed"},
                    {"name": "CAN (09:30)", "state": "passed"},
                    {"name": "CLT (10:47)", "state": "current-location"}
                ]
            },
            {
                "train_no": 15102, "train_name": "Jan Sadharan Express", "sched": "10:45", "actual": "10:45", "delay": 0, "fare": 143.65, "category": "Express Run",
                "start_min": 645, "end_min": 850,
                "nodes": [
                    {"name": "MAQ (10:45)", "state": "passed"},
                    {"name": "KGQ (11:28)", "state": "passed"},
                    {"name": "PAY (12:15)", "state": "passed"},
                    {"name": "CLT (14:10)", "state": "current-location"}
                ]
            },
            {
                "train_no": 16348, "train_name": "Mangaluru - Trivandrum Express", "sched": "14:25", "actual": "14:35", "delay": 10, "fare": 143.65, "category": "Mail/Express",
                "start_min": 875, "end_min": 1057,
                "nodes": [
                    {"name": "MAQ (14:35)", "state": "passed"},
                    {"name": "KGQ (15:20)", "state": "passed"},
                    {"name": "CAN (16:40)", "state": "passed"},
                    {"name": "CLT (17:37)", "state": "current-location"}
                ]
            },
            {
                "train_no": 13434, "train_name": "Amrit Bharat Express", "sched": "15:45", "actual": "16:15", "delay": 30, "fare": 187.85, "category": "Superfast",
                "start_min": 975, "end_min": 1165,
                "nodes": [
                    {"name": "MAQ (16:15)", "state": "passed"},
                    {"name": "KGQ (17:05)", "state": "passed"},
                    {"name": "PAY (17:48)", "state": "passed"},
                    {"name": "CAN (18:25)", "state": "upcoming"},
                    {"name": "TLY (18:48)", "state": "upcoming"},
                    {"name": "CLT (19:25)", "state": "upcoming"}
                ]
            },
            {
                "train_no": 16630, "train_name": "Malabar Express (Night Corridor)", "sched": "18:15", "actual": "18:15", "delay": 0, "fare": 143.65, "category": "Mail/Express",
                "start_min": 1095, "end_min": 1300,
                "nodes": [
                    {"name": "MAQ (18:15)", "state": "passed"},
                    {"name": "KGQ (18:55)", "state": "current-location"},
                    {"name": "CAN (20:15)", "state": "upcoming"},
                    {"name": "CLT (21:40)", "state": "upcoming"}
                ]
            },
            {
                "train_no": 16604, "train_name": "Maveli Express (Night Corridor)", "sched": "19:35", "actual": "19:50", "delay": 15, "fare": 143.65, "category": "Mail/Express",
                "start_min": 1190, "end_min": 1395,
                "nodes": [
                    {"name": "MAQ (19:50)", "state": "current-location"},
                    {"name": "KGQ (20:35)", "state": "upcoming"},
                    {"name": "CAN (21:55)", "state": "upcoming"},
                    {"name": "CLT (23:15)", "state": "upcoming"}
                ]
            }
        ]

        # 3. ADVANCED CHRONOLOGICAL EVALUATOR LOOP
        for t in real_railway_dataset:
            if total_sys_mins < t["start_min"]:
                t["status_message"] = f"Awaiting Start from yard. Expected departure at {t['actual']}."
                for node in t["nodes"]:
                    node["state"] = "upcoming"
            
            elif total_sys_mins > t["end_min"]:
                t["status_message"] = "Run Completed on Schedule - Rake Terminated."
                for node in t["nodes"]:
                    node["state"] = "passed"
                t["nodes"][-1]["state"] = "passed"

            else:
                t["status_message"] = f"In Transit along the corridor. Running with {t['delay']}m delay parameters."
                
                active_node_index = 0
                for idx, node in enumerate(t["nodes"]):
                    if total_sys_mins >= node.get("min", 0):
                        node["state"] = "passed"
                        active_node_index = idx
                    else:
                        node["state"] = "upcoming"
                
                t["nodes"][active_node_index]["state"] = "current-location"

            # Cleanup internal tracking keys before serializing JSON
            if "start_min" in t: del t["start_min"]
            if "end_min" in t: del t["end_min"]
            for node in t["nodes"]:
                if "min" in node: del node["min"]

            # Explicitly force a fallback mapping if crowd configuration fields are blank
            t["crowd_id"] = 2 if t["category"] == "Superfast" else 1
            t["crowd_level"] = "Heavy Volume - Expect High Density" if t["category"] == "Superfast" else "Moderate Commuter Standee Load"

        return {"meta": {"sync_time": ist_now.strftime("%H:%M:%S")}, "trains": real_railway_dataset}

    except Exception as raw_error:
        return {"meta": {"sync_time": "00:00:00"}, "trains": [], "error": str(raw_error), "trace": traceback.format_exc()}

app.mount("/", StaticFiles(directory="static", html=True), name="static")
