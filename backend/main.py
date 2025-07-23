from fastapi import FastAPI
from pathlib import Path
import json
import requests
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# Setup for static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

def load_data(filename):
    path = DATA_DIR / filename
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return []

@app.get("/suppliers")
def get_suppliers():
    return load_data("suppliers.json")

@app.get("/projects")
def get_projects():
    return load_data("projects.json")

@app.get("/weather/{lat}/{lon}")
def get_weather(lat: float, lon: float):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    r = requests.get(url)
    return r.json()

# Serve index.html as default (optional but common)
@app.get("/")
def serve_index():
    return FileResponse("frontend/index.html")
