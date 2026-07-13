# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from schemas import TrainQueryRequest, CorridorSearchResponse, TrainTrackingRequest, LiveTrainStatus, TrackingHistory
from database import init_neon_tables, get_db_connection
from datetime import datetime, timedelta
from typing import List
import json

app = FastAPI(title="Railsight Core Telemetry Engine")

# Permit cross-origin traffic across the cloud runtime pipeline
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    # Automatically sync schemas with Neon when Render spins up the app container
    try:
        init_neon_tables()
    except Exception as e:
        print(f"Neon Database Handshake Deferred: {e}")

@app.get("/", response_class=HTMLResponse)
def read_root():
    """Serves the static index.html dashboard interface on Render directly."""
    with open("index.html", "r") as file:
        return file.read()

@app.post("/api/v1/trains/lookup")
def lookup_unreserved_trains(payload: TrainQueryRequest):
    origin = payload.from_station.strip().upper()
    destination = payload.to_station.strip().upper()
    
    if origin != "MAJN" or destination != "CLT":
        raise HTTPException(
            status_code=422, 
            detail="Scope Locked: Route parameters restricted strictly to MAJN -> CLT corridor."
        )
        
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        if payload.tier_filter == "ALL":
            cur.execute("SELECT * FROM unreserved_trains;")
        else:
            cur.execute("SELECT * FROM unreserved_trains WHERE tier = %s;", (payload.tier_filter,))
            
        records = cur.fetchall()
        cur.close()
        conn.close()
        
        # Structure dataset attributes precisely to map your frontend expectations
        results = []
        for r in records:
            results.append({
                "trainNumber": r["train_number"],
                "name": r["name"],
                "departure": r["departure"],
                "arrival": r["arrival"],
                "duration": r["duration"],
                "tier": r["tier"],
                "baseFare": r["base_fare"],
                "liveDensity": r["live_density"],
                "densityColor": r["density_color"],
                "justificationText": r["justification_text"]
            })
            
        return {
            "status": "SUCCESS",
            "source": origin,
            "destination": destination,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Neon Connection Broken: {str(e)}")


@app.get("/api/v1/trains/{train_no}/status")
def get_live_train_status(train_no: str):
    """Get real-time live status of a specific train."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Fetch train and tracking info
        cur.execute("""
            SELECT 
                tm.train_no, 
                tm.train_name,
                tt.current_station,
                tt.current_latitude,
                tt.current_longitude,
                tt.distance_covered_km,
                tt.distance_remaining_km,
                tt.current_speed_kmph,
                tt.delay_minutes,
                tt.status,
                tt.timestamp
            FROM train_tracking tt
            JOIN train_master tm ON tt.train_no = tm.train_no
            WHERE tt.train_no = %s
            ORDER BY tt.timestamp DESC LIMIT 1
        """, (train_no.upper(),))
        
        record = cur.fetchone()
        cur.close()
        conn.close()
        
        if not record:
            raise HTTPException(status_code=404, detail=f"Train {train_no} tracking data not found")
        
        total_km = float(record[5]) + float(record[6])
        percent_progress = (float(record[5]) / total_km * 100) if total_km > 0 else 0
        
        return {
            "train_no": record[0],
            "train_name": record[1],
            "current_station": record[2],
            "current_latitude": record[3],
            "current_longitude": record[4],
            "distance_covered_km": float(record[5]),
            "distance_remaining_km": float(record[6]),
            "current_speed_kmph": float(record[7]),
            "delay_minutes": record[8],
            "status": record[9],
            "timestamp": record[10].isoformat(),
            "percent_progress": round(percent_progress, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching train status: {str(e)}")


@app.get("/api/v1/trains/{train_no}/history")
def get_train_tracking_history(train_no: str, hours: int = 3):
    """Get 3-hour historical tracking data with real-time clock."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get current and historical data
        time_threshold = datetime.utcnow() - timedelta(hours=hours)
        
        cur.execute("""
            SELECT 
                tm.train_no,
                tm.train_name,
                tt.current_station,
                tt.current_latitude,
                tt.current_longitude,
                tt.distance_covered_km,
                tt.distance_remaining_km,
                tt.current_speed_kmph,
                tt.delay_minutes,
                tt.status,
                tt.timestamp,
                (tt.distance_covered_km / (tt.distance_covered_km + tt.distance_remaining_km) * 100) as progress
            FROM train_tracking tt
            JOIN train_master tm ON tt.train_no = tm.train_no
            WHERE tt.train_no = %s AND tt.timestamp >= %s
            ORDER BY tt.timestamp ASC
        """, (train_no.upper(), time_threshold))
        
        records = cur.fetchall()
        cur.close()
        conn.close()
        
        if not records:
            raise HTTPException(status_code=404, detail=f"No tracking history found for train {train_no}")
        
        history = []
        for r in records:
            total_km = float(r[5]) + float(r[6])
            percent_progress = (float(r[5]) / total_km * 100) if total_km > 0 else 0
            
            history.append({
                "train_no": r[0],
                "train_name": r[1],
                "current_station": r[2],
                "current_latitude": r[3],
                "current_longitude": r[4],
                "distance_covered_km": float(r[5]),
                "distance_remaining_km": float(r[6]),
                "current_speed_kmph": float(r[7]),
                "delay_minutes": r[8],
                "status": r[9],
                "timestamp": r[10].isoformat(),
                "percent_progress": round(percent_progress, 2)
            })
        
        return {
            "train_no": records[0][0],
            "train_name": records[0][1],
            "current_status": history[-1] if history else None,
            "three_hour_history": history,
            "history_duration_hours": hours,
            "total_records": len(history),
            "last_update": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tracking history: {str(e)}")
