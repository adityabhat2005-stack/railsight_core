# TARGET LOCATION: /main.py
# Purpose: Chronologically Accurate 24HR Transit Simulator Gateway Engine (Fixed Comments Syntax)

import os
import datetime
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import traceback

app = FastAPI(title="RailSight Dynamic Time-Tracking Engine", version="9.1.0")

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
        
        is_weekend_peak = day_of_week in [4, 5, 6]

        # 2. SEED RAW FACTUAL DATA MATRIX WITH INTERNAL NODAL TIMELINES (Mins From Midnight)
        real_railway_dataset = [
            {
                "train_no": 12836, "train_name": "Antyodaya Express", "sched": "04:00", "actual": "04:15", "delay": 15, "fare": 187.85, "category": "Superfast",
                "start_min": 255, "end_min": 442,  # 04:15 AM to 07:22 AM
                "nodes": [
                    {"name": "MAJN (04:15)", "min": 255},
                    {"name": "KGQ (04:58)", "min": 298},
                    {"name": "CAN (06:12)", "min": 372},
                    {"name": "CLT (07:22)", "min": 442}
                ]
            },
            {
                "train_no": 16649, "train_name": "Parasuram Express", "sched": "05:05", "actual": "05:05", "delay": 0, "fare": 143.65, "category": "Mail/Express",
                "start_min": 305, "end_min": 512,  # 05:05 AM to 08:32 AM
                "nodes": [
                    {"name": "MAQ (05:05)", "min": 305},
                    {"name": "KGQ (05:47)", "min": 347},
                    {"name": "CAN (07:07)", "min": 427},
                    {"name": "CLT (08:32)", "min": 512}
                ]
            },
            {
                "train_no": 16610, "train_name": "MAQ - Palakkad Passenger Local", "sched": "05:15", "actual": "05:30", "delay": 15, "fare": 110.00, "category": "Ordinary Passenger",
                "start_min": 330, "end_min": 552,  # 05:30 AM to 09:12 AM
                "nodes": [
                    {"name": "MAQ (05:30)", "min": 330},
                    {"name": "KGQ (06:20)", "min": 380},
                    {"name": "CAN (07:45)", "min": 465},
                    {"name": "CLT (09:12)", "min": 552}
                ]
            },
            {
                "train_no": 6486, "train_name": "Mangaluru - Kozhikode MEMU Special", "sched": "06:45", "actual": "06:45", "delay": 0, "fare": 110.00, "category": "MEMU Service",
                "start_min": 405, "end_min": 670,  # 06:45 AM to 11:10 AM
                "nodes": [
                    {"name": "MAQ (06:45)", "min": 405},
                    {"name": "KGQ (07:40)", "min": 460},
                    {"name": "PAY (08:35)", "min": 515},
                    {"name": "CAN (09:15)", "min": 555},
                    {"name": "CLT (11:10)", "min": 670}
                ]
            },
            {
                "train_no": 16160, "train_name": "MAJN - Chennai Passenger Local", "sched": "06:55", "actual": "07:15", "delay": 20, "fare": 110.00, "category": "Ordinary Passenger",
                "start_min": 435, "end_min": 647,  # 07:15 AM to 10:47 AM
                "nodes": [
                    {"name": "MAJN (07:15)", "min": 435},
                    {"name": "KGQ (08:12)", "min": 492},
                    {"name": "CAN (09:30)", "min": 570},
                    {"name": "CLT (10:47)", "min": 647}
                ]
            },
            {
                "train_no": 15102, "train_name": "Jan Sadharan Express", "sched": "10:45", "actual": "10:45", "delay": 0, "fare": 143.65, "category": "Express Run",
                "start_min": 645, "end_min": 850,  # 10:45 AM to 02:10 PM
                "nodes": [
                    {"name": "MAQ (10:45)", "min": 645},
                    {"name": "KGQ (11:28)", "min": 688},
                    {"name": "PAY (12:15)", "min": 735},
                    {"name": "CLT (14:10)", "min": 850}
                ]
            },
            {
                "train_no": 16348, "train_name": "Mangaluru - Trivandrum Express", "sched": "14:25", "actual": "14:35", "delay": 10, "fare": 143.65, "category": "Mail/Express",
                "start_min": 875, "end_min": 1057,  # 02:35 PM to 05:37 PM
                "nodes": [
                    {"name": "MAQ (14:35)", "min": 875},
                    {"name": "KGQ (15:20)", "min": 920},
                    {"name": "CAN (16:40)", "min": 1000},
                    {"name": "CLT (17:37)", "min": 1057}
                ]
            },
            {
                "train_no": 13434, "train_name": "Amrit Bharat Express", "sched": "15:45", "actual": "16:15", "delay": 30, "fare": 187.85, "category": "Superfast",
                "start_min": 975, "end_min": 1165,  # 04:15 PM to 07:25 PM
                "nodes": [
                    {"name": "MAQ (16:15)", "min": 975},
                    {"name": "KGQ (17:05)", "min": 1025},
                    {"name": "PAY (17:48)", "min": 1068},
                    {"name": "CAN (18:25)", "min": 1105},
                    {"name": "TLY (18:48)", "min": 1128},
                    {"name": "CLT (19:25)", "min": 1165}
                ]
            },
            {
                "train_no": 16630, "train_name": "Malabar Express (Night Corridor)", "sched": "18:15", "actual": "18:15", "delay": 0, "fare": 143.65, "category": "Mail/Express",
                "start_min": 1095, "end_min": 1300,  # 06:15 PM to 09:40 PM
                "nodes": [
                    {"name": "MAQ (18:15)", "min": 1095},
                    {"name": "KGQ (18:55)", "min": 1135},
                    {"name": "CAN (20:15)", "min": 1215},
                    {"name": "CLT (21:40)", "min": 1300}
                ]
            },
            {
                "train_no": 16604, "train_name": "Maveli Express (Night Corridor)", "sched": "19:35", "actual": "19:50", "delay": 15, "fare": 143.65, "category": "Mail/Express",
                "start_min": 1190, "end_min": 1395,  # 07:50 PM to 11:15 PM
                "nodes": [
                    {"name": "MAQ (19:50)", "min": 1190},
                    {"name": "KGQ (20:35)", "min": 1235},
                    {"name": "CAN (21:55)", "min": 1315},
                    {"name": "CLT (23:15)", "min": 1395}
                ]
            }
        ]

        # 3. ADVANCED CHRONOLOGICAL EVALUATOR LOOP
        for t in real_railway_dataset:
            # Case A: Train has not started its journey yet
            if total_sys_mins < t["start_min"]:
                t["status_message"] = f"Awaiting Start from yard. Expected departure at {t['actual']}."
                for node in t["nodes"]:
                    node["state"] = "upcoming"
            
            # Case B: Train has completely finished its run past destination terminal
            elif total_sys_mins > t["end_min"]:
                t["status_message"] = "Run Completed on Schedule - Rake Terminated."
                for node in t["nodes"]:
                    node["state"] = "passed"
                t["nodes"][-1]["state"] = "passed"

            # Case C: Train is actively on the tracks running right now!
            else:
                t["status_message"] = f"In Transit along the corridor. Running with {t['delay']}m delay parameters."
                
                active_node_index = 0
                for idx, node in enumerate(t["nodes"]):
                    if total_sys_mins >= node["min"]:
                        node["state"] = "passed"
                        active_node_index = idx
                    else:
                        node["state"] = "upcoming"
                
                t["nodes"][active_node_index]["state"] = "current-location"

            # Cleanup internal mathematical tracking metrics before serializing JSON
            del t["start_min"]
            del t["end_min"]
            for node in t["nodes"]:
                del node["min"]

        return {"meta": {"sync_time": ist_now.strftime("%H:%M:%S")}, "trains": real_railway_dataset}

    except Exception as raw_error:
        return {"meta": {"sync_time": "00:00:00"}, "trains": [], "error": str(raw_error), "trace": traceback.format_exc()}

app.mount("/", StaticFiles(directory="static", html=True), name="static")
