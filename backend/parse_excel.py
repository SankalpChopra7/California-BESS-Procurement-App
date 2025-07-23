import json
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCEL_PATH = ROOT / 'California_Arizona_Texas_Procurement_Data.xlsx'
DATA_DIR = ROOT / 'data'
DATA_DIR.mkdir(exist_ok=True)

STATE_COORDS = {
    "California": {"lat": 36.7783, "lon": -119.4179},
    "Arizona": {"lat": 34.0489, "lon": -111.0937},
    "Texas": {"lat": 31.9686, "lon": -99.9018},
}

def parse_suppliers():
    wb = pd.ExcelFile(EXCEL_PATH)
    suppliers = []

    ca = wb.parse("California County Data ")
    ca = ca.rename(columns=lambda c: c.strip())
    for _, row in ca.iterrows():
        suppliers.append({
            "state": "California",
            "county": row.get("California County"),
            "service_type": row.get("Service Type"),
            "company": row.get("Company Name"),
            "lat": STATE_COORDS["California"]["lat"],
            "lon": STATE_COORDS["California"]["lon"],
        })

    az = wb.parse("Arizona County Data ")
    az = az.rename(columns=lambda c: c.strip())
    for _, row in az.iterrows():
        suppliers.append({
            "state": "Arizona",
            "county": row.get("Arizona  County"),
            "service_type": row.get("Service Type"),
            "company": row.get("Company Name"),
            "lat": STATE_COORDS["Arizona"]["lat"],
            "lon": STATE_COORDS["Arizona"]["lon"],
        })

    tx = wb.parse("Texas County Data")
    tx = tx.rename(columns=lambda c: c.strip())
    for _, row in tx.iterrows():
        suppliers.append({
            "state": "Texas",
            "county": row.get("Texas County"),
            "service_type": row.get("Service Type"),
            "company": row.get("Company Name"),
            "lat": row.get("Latitude", STATE_COORDS["Texas"]["lat"]),
            "lon": row.get("Longitude", STATE_COORDS["Texas"]["lon"]),
        })

    return suppliers


def parse_projects():
    wb = pd.ExcelFile(EXCEL_PATH)
    sites = wb.parse("SOLV BESS Sites")
    sites = sites.rename(columns=lambda c: c.strip())

    projects = []
    for _, row in sites.iterrows():
        projects.append({
            "project": row.get("SOLV BESS PROJECT"),
            "location": row.get("Location"),
            "mw_ac": row.get("MW AC Capacity"),
            "mw_dc": row.get("MW DC Capacity"),
            "client": row.get("Client"),
            "lat": STATE_COORDS["California"]["lat"],
            "lon": STATE_COORDS["California"]["lon"],
        })

    return projects


def _load_or_cache(name: str, parse_func):
    path = DATA_DIR / f"{name}.json"
    if path.exists():
        return json.loads(path.read_text())
    data = parse_func()
    path.write_text(json.dumps(data, indent=2))
    return data


def load_data():
    return {
        "suppliers": _load_or_cache("suppliers", parse_suppliers),
        "projects": _load_or_cache("projects", parse_projects),
    }


DATA = load_data()

def get_suppliers():
    return DATA['suppliers']

def get_projects():
    return DATA['projects']


# Optional CLI entry point for regenerating cache
if __name__ == "__main__":
    DATA_DIR.mkdir(exist_ok=True)
    with open(DATA_DIR / "suppliers.json", "w") as f:
        json.dump(parse_suppliers(), f, indent=2)
    with open(DATA_DIR / "projects.json", "w") as f:
        json.dump(parse_projects(), f, indent=2)

