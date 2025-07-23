from fastapi import FastAPI, HTTPException
import requests
from .parse_excel import get_suppliers, get_projects

app = FastAPI(title="BESS Procurement API")


@app.get("/suppliers")
def suppliers():
    """Return supplier information from the Excel workbook."""
    return get_suppliers()


@app.get("/projects")
def projects():
    """Return BESS project information from the Excel workbook."""
    return get_projects()


@app.get("/weather/{lat}/{lon}")
def weather(lat: float, lon: float):
    """Fetch simple weather forecast data from Open-Meteo."""
    try:
        resp = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": lat, "longitude": lon, "hourly": "temperature_2m", "current_weather": True},
            timeout=10,
        )
        resp.raise_for_status()
    except requests.RequestException as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    return resp.json()
