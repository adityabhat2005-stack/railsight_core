from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from database import get_db, engine, Base
import models
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="RailSight Core Engine")

# This allows your web browser to access the API safely from anywhere
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/transit-matrix", response_model=List[schemas.CommuterTransitWindow])
def get_transit_matrix(db: Session = Depends(get_db)):
    schedules = db.query(models.LiveSchedules).all()
    matrix = []

    for item in schedules:
        train = db.query(models.TrainMaster).filter(models.TrainMaster.train_no == item.train_no).first()
        category = db.query(models.TrainCategory).filter(models.TrainCategory.category_id == train.category_id).first()
        
        if category.category_name == "Superfast":
            color, alert = "RED", "BANNED: Ordinary/Express tickets will cause severe penalties!"
        elif category.category_name == "Express":
            color, alert = "YELLOW", "WARNING: Ensure you hold an Express tier category ticket."
        else:
            color, alert = "GREEN", "VALID: Standard general unreserved paper tickets accepted."

        matrix.append({
            "train_no": item.train_no,
            "train_name": train.train_name,
            "category_name": category.category_name,
            "scheduled_departure": item.scheduled_departure,
            "delay_minutes": item.delay_minutes,
            "actual_departure": f"Delayed by {item.delay_minutes} mins" if item.delay_minutes > 0 else "On Time",
            "advisory_alert": alert,
            "alert_color": color
        })
    return matrix
