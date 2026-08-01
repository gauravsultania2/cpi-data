"""Pull all CPI component series (SA + NSA) from the BLS API v2.

Writes data/bls/cpi_series.csv  (tidy: series_id, year, period, value, footnotes)
and    data/bls/missing_series.txt (requested but not returned).
Requires env var BLS_KEY.
"""
import os, sys, time, json, csv
import requests
sys.path.insert(0, os.path.dirname(__file__))
from series_map import series_ids

API = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
KEY = os.environ["BLS_KEY"]
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "bls")

# 20-year window cap per request; 50 series per request.
WINDOWS = [(1997, 2016), (2017, 2026)]

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def pull():
    ids = series_ids()
    rows, seen = [], set()
    missing = set(ids)
    for (y0, y1) in WINDOWS:
        for chunk in chunks(ids, 50):
            payload = {"seriesid": chunk, "startyear": str(y0), "endyear": str(y1),
                       "registrationkey": KEY}
            for attempt in range(3):
                try:
                    r = requests.post(API, json=payload,
                                      headers={"Content-Type": "application/json"}, timeout=60)
                    d = r.json()
                    break
                except Exception as e:
                    if attempt == 2:
                        raise
                    time.sleep(10)
            if d.get("status") != "REQUEST_SUCCEEDED":
                print("BLS API message:", d.get("message"), file=sys.stderr)
            for s in d.get("Results", {}).get("series", []):
                sid = s["seriesID"]
                if s.get("data"):
                    missing.discard(sid)
                for obs in s.get("data", []):
                    if obs["period"].startswith("M") and obs["period"] != "M13":
                        key = (sid, obs["year"], obs["period"])
                        if key in seen:
                            continue
                        seen.add(key)
                        fn = ";".join(f.get("text", "") for f in obs.get("footnotes", []) if f)
                        rows.append([sid, obs["year"], obs["period"], obs["value"], fn])
            time.sleep(1)

    rows.sort(key=lambda r: (r[0], r[1], r[2]))
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "cpi_series.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["series_id", "year", "period", "value", "footnotes"])
        w.writerows(rows)
    with open(os.path.join(OUT, "missing_series.txt"), "w") as f:
        f.write("\n".join(sorted(missing)) + "\n")
    print(f"BLS: wrote {len(rows)} observations; {len(missing)} series missing/empty")

if __name__ == "__main__":
    pull()
