# schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TrainQueryRequest(BaseModel):
    from_station: str
    to_station: str
    tier_filter: Optional[str] = "ALL"

class TrainResponseModel(BaseModel):
    trainNumber: str
    name: str
    departure: str
    arrival: str
    duration: str
    tier: str
    baseFare: int
    liveDensity: str
    densityColor: str
    justificationText: str

class CorridorSearchResponse(BaseModel):
    status: str
    source: str
    destination: str
    results: List[TrainResponseModel]

class TrainTrackingRequest(BaseModel):
    train_no: str

class LiveTrainStatus(BaseModel):
    train_no: str
    train_name: str
    current_station: str
    current_latitude: float
    current_longitude: float
    distance_covered_km: float
    distance_remaining_km: float
    current_speed_kmph: float
    delay_minutes: int
    status: str
    timestamp: datetime
    percent_progress: float

class TrackingHistory(BaseModel):
    train_no: str
    train_name: str
    current_status: LiveTrainStatus
    three_hour_history: List[LiveTrainStatus]
