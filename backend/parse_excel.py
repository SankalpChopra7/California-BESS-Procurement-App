import json
import pandas as pd
from pathlib import Path
from openpyxl import load_workbook
import math

ROOT       = Path(__file__).resolve().parents[1]
EXCEL_PATH = ROOT / 'California_Arizona_Texas_Procurement_Data.xlsx'
DATA_DIR   = ROOT / 'data'
DATA_DIR.mkdir(exist_ok=True)

STATE_COORDS = {
    "California": {"lat": 36.7783, "lon": -119.4179},
    "Arizona":    {"lat": 34.0489, "lon": -111.0937},
    "Texas":      {"lat": 31.9686, "lon":  -99.9018},
}

def safe_value(val):
    # Converts pandas NaN → None
    return None if isinstance(val, float) and math.isnan(val) else val

def parse_suppliers():
    # Use openpyxl for hyperlink extraction
    wb = load_workbook(EXCEL_PATH, data_only=True)
    suppliers = []

    for sheet_name, state_key in [
        ("California County Data ", "California"),
        ("Arizona County Data ",   "Arizona"),
        ("Texas County Data",       "Texas")
    ]:
        ws     = wb[sheet_name]
        header = [c.value for c in ws[1]]
        # find columns
        contact_col = header.index("Contact") + 1
        maps_col    = header.index("Location on Google Maps") + 1

        # read into pandas (to get text fields)
        df = pd.read_excel(EXCEL_PATH, sheet_name=sheet_name, dtype=str)
        df.rename(columns=lambda c: str(c).strip(), inplace=True)

        for idx, row in df.iterrows():
            # row 2 in Excel is idx=0 here, so +2
            contact_cell = ws.cell(row=idx+2, column=contact_col)
            map_cell     = ws.cell(row=idx+2, column=maps_col)

            suppliers.append({
                "state":        state_key,
                "county":       safe_value(row.get(f"{state_key} County")),
                "service_type": safe_value(row.get("Service Type")),
                "company":      safe_value(row.get("Company Name")),
                "contact_url":  contact_cell.hyperlink.target if contact_cell.hyperlink else None,
                "map_url":      map_cell.hyperlink.target     if map_cell.hyperlink     else None,
                "lat":          STATE_COORDS[state_key]["lat"],
                "lon":          STATE_COORDS[state_key]["lon"],
            })

    return suppliers

def parse_projects():
    # (you can add hyperlink logic here if needed)
    wb    = pd.ExcelFile(EXCEL_PATH)
    sites = wb.parse("SOLV BESS Sites").rename(columns=lambda c: c.strip())
    projects = []

    for _, row in sites.iterrows():
        projects.append({
            "project":   safe_value(row.get("SOLV BESS PROJECT")),
            "location":  safe_value(row.get("Location")),
            "mw_ac":     safe_value(row.get("MW AC Capacity")),
            "mw_dc":     safe_value(row.get("MW DC Capacity")),
            "client":    safe_value(row.get("Client")),
            "lat":       STATE_COORDS["California"]["lat"],
            "lon":       STATE_COORDS["California"]["lon"],
        })

    return projects

def _load_or_cache(name, parse_fn):
    path = DATA_DIR / f"{name}.json"
    if path.exists():
        return json.loads(path.read_text())
    data = parse_fn()
    path.write_text(json.dumps(data, indent=2))
    return data

def load_data():
    return {
        "suppliers": _load_or_cache("suppliers", parse_suppliers),
        "projects":  _load_or_cache("projects",  parse_projects),
    }

DATA = load_data()

def get_suppliers():
    return DATA["suppliers"]

def get_projects():
    return DATA["projects"]


if __name__ == "__main__":
    # Regenerate cache on demand
    DATA_DIR.mkdir(exist_ok=True)
    with open(DATA_DIR / "suppliers.json", "w") as f:
        json.dump(parse_suppliers(), f, indent=2)
    with open(DATA_DIR / "projects.json", "w") as f:
        json.dump(parse_projects(), f, indent=2)

