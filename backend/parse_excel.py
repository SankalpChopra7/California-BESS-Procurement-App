import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
EXCEL_PATH = ROOT / 'California_Arizona_Texas_Procurement_Data.xlsx'
DATA_DIR = Path(__file__).resolve().parent / 'data'
DATA_DIR.mkdir(exist_ok=True)


def _load_sheet(sheet: str, **kwargs) -> pd.DataFrame:
    return pd.read_excel(EXCEL_PATH, sheet_name=sheet, **kwargs)


def _load_or_cache(sheet: str, json_name: str, **kwargs):
    json_path = DATA_DIR / json_name
    if json_path.exists():
        return json.loads(json_path.read_text())
    df = _load_sheet(sheet, **kwargs)
    df = df.rename(columns=lambda c: str(c).strip())
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
    data = df.fillna('').to_dict(orient='records')
    json_path.write_text(json.dumps(data, indent=2))
    return data


def load_data():
    return {
        'suppliers': _load_or_cache('BESS Equipment', 'suppliers.json', header=1),
        'projects': _load_or_cache('SOLV BESS Sites', 'projects.json'),
    }


DATA = load_data()


def get_suppliers():
    return DATA['suppliers']


def get_projects():
    return DATA['projects']
