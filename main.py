# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from schemas import TrainQueryRequest, CorridorSearchResponse
from database import init_neon_tables, get_db_connection

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
