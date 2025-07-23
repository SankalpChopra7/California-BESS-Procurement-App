# California-BESS-Procurement-App

This repo contains a minimal demo for visualizing BESS suppliers and projects on a map.

## Running

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the FastAPI server:
   ```bash
   uvicorn backend.main:app --reload
   ```
3. Open `http://localhost:8000/` in your browser. Click *Switch to 3D* to see the Cesium view.

The app loads project data from the backend, displays markers using Leaflet, and
fetches current weather for each site from the `/weather` endpoint.
