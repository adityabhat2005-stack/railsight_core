# schemas.py
from pydantic import BaseModel
from typing import List, Optional

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
