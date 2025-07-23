# California-BESS-Procurement-App

This project visualizes suppliers and BESS projects from an Excel workbook on an interactive map. The map can switch between 2D and 3D views using CesiumJS with OpenStreetMap tiles. Weather data is fetched from the free Open-Meteo API.

## Setup
1. Install Python 3.11 and Node.js (if using additional tooling).
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Parse the Excel workbook and generate JSON data:
   ```bash
   python backend/parse_excel.py
   ```
   This will create `data/suppliers.json` and `data/projects.json` along with a small geocoding cache.
4. Start the FastAPI server:
   ```bash
   uvicorn backend.main:app --reload
   ```
5. Open `frontend/index.html` in your browser. When served from the same host as the backend, the map will load supplier and project markers. Use the **Toggle 2D/3D** button to switch views.

## Files
- `backend/parse_excel.py` – parses the Excel workbook and geocodes locations using OpenStreetMap.
- `backend/main.py` – FastAPI server providing `/suppliers`, `/projects`, and `/weather/{lat}/{lon}` endpoints.
- `frontend/index.html` – simple CesiumJS viewer displaying data from the backend with a toggle between 2D and 3D modes.

Run the parsing script after updating the Excel file to regenerate the JSON used by the map.
