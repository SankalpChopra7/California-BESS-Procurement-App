import math
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import requests
from .parse_excel import get_suppliers, get_projects

app = FastAPI(title="BESS Procurement API")

# helper to scrub out any NaN before JSON serialization
def _clean_nan(obj):
    if isinstance(obj, float):
        return None if math.isnan(obj) else obj
    if isinstance(obj, dict):
        return {k: _clean_nan(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_clean_nan(v) for v in obj]
    return obj

# Mount frontend static directory
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Serve index.html at root
@app.get("/")
def serve_index():
    return FileResponse("frontend/index.html")

# Supplier endpoint using Excel parser with NaN cleaning
@app.get("/suppliers")
def suppliers():
    raw = get_suppliers()
    cleaned = _clean_nan(raw)
    return JSONResponse(content=cleaned)

# Project endpoint using Excel parser with NaN cleaning
@app.get("/projects")
def projects():
    raw = get_projects()
    cleaned = _clean_nan(raw)
    return JSONResponse(content=cleaned)

# Weather endpoint with error handling remains unchanged
@app.get("/weather/{lat}/{lon}")
def weather(lat: float, lon: float):
    try:
        resp = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "hourly": "temperature_2m",
                "current_weather": True
            },
            timeout=10,
        )
        resp.raise_for_status()
    except requests.RequestException as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    return resp.json()

