"""Download BLS reference files that aren't in the API:
  - current + revised seasonal factors (Excel) from the seasonal-adjustment page
  - relative importance tables (Excel/HTML) from the relative-importance pages
  - cu.item / cu.series metadata flat files

BLS servers require a browser-like User-Agent. Files land in data/bls_files/.
"""
import os, re
import requests

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "bls_files")
UA = {"User-Agent": "Mozilla/5.0 (cpi-research; contact: repo owner)"}

PAGES = [
    "https://www.bls.gov/cpi/seasonal-adjustment/",
    "https://www.bls.gov/cpi/tables/relative-importance/home.htm",
]
FLAT = [
    "https://download.bls.gov/pub/time.series/cu/cu.item",
    "https://download.bls.gov/pub/time.series/cu/cu.series",
]

def pull():
    os.makedirs(OUT, exist_ok=True)
    for page in PAGES:
        try:
            html = requests.get(page, headers=UA, timeout=60).text
        except Exception as e:
            print(f"WARN: could not fetch {page}: {e}")
            continue
        links = set(re.findall(r'href="([^"]+\.xlsx?)"', html, flags=re.I))
        for link in links:
            url = link if link.startswith("http") else "https://www.bls.gov" + link
            name = url.rsplit("/", 1)[-1]
            try:
                b = requests.get(url, headers=UA, timeout=120).content
                with open(os.path.join(OUT, name), "wb") as f:
                    f.write(b)
                print(f"BLS file: {name} ({len(b)} bytes)")
            except Exception as e:
                print(f"WARN: {url}: {e}")
    for url in FLAT:
        name = url.rsplit("/", 1)[-1]
        try:
            b = requests.get(url, headers=UA, timeout=120).content
            with open(os.path.join(OUT, name), "wb") as f:
                f.write(b)
            print(f"BLS flat file: {name} ({len(b)} bytes)")
        except Exception as e:
            print(f"WARN: {url}: {e}")

if __name__ == "__main__":
    pull()
