from pathlib import Path
import json
import httpx
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

DATA_FILE = Path(__file__).parent / 'data' / 'projects.json'
with DATA_FILE.open() as f:
    projects = json.load(f)

@app.get('/projects')
async def get_projects():
    return projects

@app.get('/weather')
async def get_weather(lat: float, lon: float):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
    return resp.json().get('current_weather', {})

FRONTEND_DIR = Path(__file__).resolve().parent.parent / 'frontend'

@app.get('/')
async def serve_index():
    return FileResponse(FRONTEND_DIR / 'index.html')

app.mount('/static', StaticFiles(directory=FRONTEND_DIR), name='static')
