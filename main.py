import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, time
import httpx  # Added for making live API calls

from database import get_db, engine, Base
import models
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="RailSight Core Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper function for Crowd Prediction Logic (Simulating your ML rules)
def predict_crowd_density(scheduled_time: time, category_name: str) -> tuple:
    hour = scheduled_time.hour
    
    # Peak hours: Morning (8-10 AM) and Evening (5-7 PM)
    is_peak_hour = (8 <= hour <= 10) or (17 <= hour <= 19)
    
    if category_name == "Ordinary" and is_peak_hour:
        return "HEAVY CROWD", "RED"
    elif is_peak_hour or category_name == "Ordinary":
        return "MODERATE CROWD", "YELLOW"
    else:
        return "LOW CROWD", "GREEN"

@app.get("/")
def home():
    return {"status": "RailSight API is Live"}

@app.get("/api/transit-matrix", response_model=List[schemas.CommuterTransitWindow])
async def get_transit_matrix(db: Session = Depends(get_db)):
    schedules = db.query(models.LiveSchedules).all()
    matrix = []

    # Setup RapidAPI configuration for Live Train Status
    RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
    RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "://rapidapi.com")

    async with httpx.AsyncClient() as client:
        for item in schedules:
            train = db.query(models.TrainMaster).filter(models.TrainMaster.train_no == item.train_no).first()
            category = db.query(models.TrainCategory).filter(models.TrainCategory.category_id == train.category_id).first()
            
            # --- FEATURE 1: FETCH LIVE DATA IF API CREDENTIALS EXIST ---
            live_location = "Station Platform"
            current_delay = item.delay_minutes  # Default fallback to DB value
            
            if RAPIDAPI_KEY:
                try:
                    # Querying an external Indian Railways live tracker engine
                    url = f"https://{RAPIDAPI_HOST}/api/v1/liveTrainStatus"
                    headers = {"X-RapidAPI-Key": RAPIDAPI_KEY, "X-RapidAPI-Host": RAPIDAPI_HOST}
                    response = await client.get(url, headers=headers, params={"trainNo": item.train_no}, timeout=3.0)
                    
                    if response.status_code == 200:
                        live_data = response.json()
                        live_location = live_data.get("current_station_name", "In Transit")
                        current_delay = int(live_data.get("delay", item.delay_minutes))
                        
                        # Update database instantly so the cloud data stays synchronized
                        item.delay_minutes = current_delay
                        db.commit()
                except Exception:
                    # If the external API fails or times out, safely fallback to the database values
                    pass

            # --- ORIGINAL TIERED FARE RULES ---
            if category.category_name == "Superfast":
                color, alert = "RED", "BANNED: Ordinary/Express tickets will cause severe penalties!"
            elif category.category_name == "Express":
                color, alert = "YELLOW", "WARNING: Ensure you hold an Express tier category ticket."
            else:
                color, alert = "GREEN", "VALID: Standard general unreserved paper tickets accepted."

            # --- FEATURE 2: CALL CROWD PREDICTION RULES ---
            crowd_status, crowd_color = predict_crowd_density(item.scheduled_departure, category.category_name)

            matrix.append({
                "train_no": item.train_no,
                "train_name": train.train_name,
                "category_name": category.category_name,
                "scheduled_departure": item.scheduled_departure,
                "delay_minutes": current_delay,
                "actual_departure": f"Delayed by {current_delay} mins" if current_delay > 0 else "On Time",
                "advisory_alert": alert,
                "alert_color": color,
                # New values map directly into frontend components
                "current_location": live_location,
                "predicted_crowd": crowd_status,
                "crowd_color": crowd_color
            })
            
    return matrix
