from fastapi import FastAPI, HTTPException
from pathlib import Path
import json
import requests
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .parse_excel import get_suppliers, get_projects

app = FastAPI(title="BESS Procurement API")

# Mount frontend static directory
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Serve index.html at root
@app.get("/")
def serve_index():
    return FileResponse("frontend/index.html")

# Supplier endpoint using Excel parser
@app.get("/suppliers")
def suppliers():
    """Return supplier information from the Excel workbook."""
    return get_suppliers()

# Project endpoint using Excel parser
@app.get("/projects")
def projects():
    """Return BESS project information from the Excel workbook."""
    return get_projects()

# Weather endpoint with error handling
@app.get("/weather/{lat}/{lon}")
def weather(lat: float, lon: float):
    """Fetch simple weather forecast data from Open-Meteo."""
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

