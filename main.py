# main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from schemas import TrainQueryRequest, CorridorSearchResponse
from database import CRYO_STATION_DATABASE

app = FastAPI(title="Railsight Core Telemetry Engine")

# Permit browser cross-origin asset lookups
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/v1/trains/lookup", response_model=CorridorSearchResponse)
def lookup_unreserved_trains(payload: TrainQueryRequest):
    origin = payload.from_station.strip().upper()
    destination = payload.to_station.strip().upper()
    
    # Boundary Scope Freeze Evaluation Rule
    allowed = CRYO_STATION_DATABASE["supported_corridor"]
    if origin != allowed["from"] or destination != allowed["to"]:
        raise HTTPException(
            status_code=422, 
            detail=f"Scope Locked: Route parameters restricted strictly to {allowed['from']} -> {allowed['to']} corridor for evaluation check."
        )
        
    compiled_results = []
    for train in CRYO_STATION_DATABASE["trains"]:
        if payload.tier_filter == "ALL" or train["tier"] == payload.tier_filter:
            compiled_results.append(train)
            
    return {
        "status": "SUCCESS",
        "source": origin,
        "destination": destination,
        "results": compiled_results
    }
