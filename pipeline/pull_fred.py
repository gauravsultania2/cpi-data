"""Pull cross-check aggregates from FRED (independent transcription of the same
BLS data — used to validate the BLS API pull) plus the FRED mirror of EIA
weekly gasoline. Requires env var FRED_KEY.

Writes data/fred/<series>.csv
"""
import os, csv
import requests

KEY = os.environ["FRED_KEY"]
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "fred")
API = "https://api.stlouisfed.org/fred/series/observations"

SERIES = [
    "CPIAUCSL",        # headline SA
    "CPIAUCNS",        # headline NSA  (YoY settlement path)
    "CPILFESL",        # core SA
    "CPILFENS",        # core NSA
    "CUSR0000SETA02",  # used cars SA (component cross-check)
    "CUSR0000SEHC",    # OER SA (component cross-check)
    "GASREGW",         # EIA weekly retail regular gasoline (cross-check for EIA pull)
]

def pull():
    os.makedirs(OUT, exist_ok=True)
    for sid in SERIES:
        r = requests.get(API, params={
            "series_id": sid, "api_key": KEY, "file_type": "json",
            "observation_start": "1997-01-01"}, timeout=60)
        r.raise_for_status()
        obs = r.json()["observations"]
        with open(os.path.join(OUT, f"{sid}.csv"), "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["date", "value"])
            for o in obs:
                w.writerow([o["date"], o["value"]])
        print(f"FRED: {sid} {len(obs)} obs")

if __name__ == "__main__":
    pull()
