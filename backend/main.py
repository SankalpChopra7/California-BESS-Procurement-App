from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import requests
from .parse_excel import get_suppliers, get_projects

app = FastAPI(title="BESS Procurement API")

# Serve your frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")
@app.get("/")
def serve_index():
    return FileResponse("frontend/index.html")

# Return cached & cleaned supplier data (with URLs)
@app.get("/suppliers")
def suppliers():
    data = get_suppliers()
    # ensure nan → null in JSON
    return JSONResponse(content=jsonable_encoder(data))

# Return project data
@app.get("/projects")
def projects():
    data = get_projects()
    return JSONResponse(content=jsonable_encoder(data))

# Weather endpoint (unchanged)
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
