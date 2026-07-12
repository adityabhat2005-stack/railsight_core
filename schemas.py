from pydantic import BaseModel
from datetime import time

class CommuterTransitWindow(BaseModel):
    train_no: str
    train_name: str
    category_name: str
    scheduled_departure: time
    delay_minutes: int
    actual_departure: str
    advisory_alert: str
    alert_color: str
    # --- NEW FIELDS FOR LIVE TRACKING & CROWD PREDICTION ---
    current_location: str
    predicted_crowd: str
    crowd_color: str

    class Config:
        from_attributes = True
