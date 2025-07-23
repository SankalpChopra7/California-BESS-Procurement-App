from fastapi import FastAPI
from pathlib import Path
import json
import requests

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

app = FastAPI()


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
