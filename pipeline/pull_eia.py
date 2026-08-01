"""Pull EIA weekly retail gasoline prices (US average) — the gasoline block's
primary input. Requires env var EIA_KEY.

Writes data/eia/weekly_gasoline.csv (period, series, value)
"""
import os, csv
import requests

KEY = os.environ["EIA_KEY"]
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "eia")
API = "https://api.eia.gov/v2/petroleum/pri/gnd/data/"

# EMM_EPMR_PTE_NUS_DPG = regular, all formulations, US
# EMM_EPM0_PTE_NUS_DPG = all grades, all formulations, US
FACETS = ["EMM_EPMR_PTE_NUS_DPG", "EMM_EPM0_PTE_NUS_DPG"]

def pull():
    os.makedirs(OUT, exist_ok=True)
    rows = []
    for facet in FACETS:
        offset, total = 0, None
        while total is None or offset < total:
            r = requests.get(API, params={
                "api_key": KEY, "frequency": "weekly", "data[0]": "value",
                "facets[series][]": facet,
                "sort[0][column]": "period", "sort[0][direction]": "asc",
                "offset": offset, "length": 5000}, timeout=60)
            r.raise_for_status()
            resp = r.json()["response"]
            total = int(resp["total"])
            for x in resp["data"]:
                rows.append([x["period"], x["series"], x["value"]])
            offset += 5000
    rows.sort()
    with open(os.path.join(OUT, "weekly_gasoline.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["week_ending", "series", "dollars_per_gallon"])
        w.writerows(rows)
    print(f"EIA: wrote {len(rows)} weekly observations")

if __name__ == "__main__":
    pull()
