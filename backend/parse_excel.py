import pandas as pd
import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / "California_Arizona_Texas_Procurement_Data.xlsx"
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "data"

STATE_COORDS = {
    "California": {"lat": 36.7783, "lon": -119.4179},
    "Arizona": {"lat": 34.0489, "lon": -111.0937},
    "Texas": {"lat": 31.9686, "lon": -99.9018},
}


def parse_suppliers():
    wb = pd.ExcelFile(DATA_FILE)
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
    wb = pd.ExcelFile(DATA_FILE)
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


def main():
    suppliers = parse_suppliers()
    projects = parse_projects()
    OUTPUT_DIR.mkdir(exist_ok=True)
    with open(OUTPUT_DIR / "suppliers.json", "w") as f:
        json.dump(suppliers, f, indent=2)
    with open(OUTPUT_DIR / "projects.json", "w") as f:
        json.dump(projects, f, indent=2)


if __name__ == "__main__":
    main()
