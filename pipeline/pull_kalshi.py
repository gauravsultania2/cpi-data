"""Snapshot Kalshi CPI market strips (public API, no auth needed).

Appends one row per open market per run to data/kalshi/snapshots_YYYYMM.csv —
this builds the price history we'll use to study market behavior into releases.
"""
import os, csv, datetime
import requests

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "kalshi")
API = "https://api.elections.kalshi.com/trade-api/v2/markets"
SERIES = ["KXCPI", "KXCPIYOY", "KXCPICOREYOY", "KXCPICORE"]

def pull():
    os.makedirs(OUT, exist_ok=True)
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    fname = os.path.join(OUT, f"snapshots_{ts[:7].replace('-', '')}.csv")
    new = not os.path.exists(fname)
    n = 0
    with open(fname, "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["ts_utc", "series", "ticker", "yes_bid", "yes_ask",
                        "last_price", "volume", "open_interest", "close_time"])
        for s in SERIES:
            cursor = ""
            while True:
                r = requests.get(API, params={"series_ticker": s, "status": "open",
                                              "limit": 200, "cursor": cursor}, timeout=60)
                r.raise_for_status()
                d = r.json()
                for m in d.get("markets", []):
                    w.writerow([ts, s, m.get("ticker"), m.get("yes_bid"),
                                m.get("yes_ask"), m.get("last_price"),
                                m.get("volume"), m.get("open_interest"),
                                m.get("close_time")])
                    n += 1
                cursor = d.get("cursor") or ""
                if not cursor:
                    break
    print(f"Kalshi: appended {n} market rows to {os.path.basename(fname)}")

if __name__ == "__main__":
    pull()
