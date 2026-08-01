# cpi-data — automated data pipeline for the CPI prediction model

This repo pulls everything the bottom-up CPI model needs, twice a day, using
GitHub Actions (which has full internet access), and commits the results as
CSVs so the modeling environment can simply `git pull`.

**Sources pulled:**

- **BLS API v2** — ~38 CPI-U components, SA + NSA, monthly since 1997
- **FRED** — headline/core SA+NSA aggregates (independent cross-check of the BLS pull) + weekly gasoline mirror
- **EIA** — weekly retail gasoline prices (the gasoline block's driver)
- **Kalshi** — snapshots of all open CPI market strips (builds our own price history)
- **BLS reference files** — seasonal factors (Excel), relative importance tables, series metadata

## One-time setup (~10 minutes)

1. Create a **new public repo** on github.com named `cpi-data`
   (public is fine — every byte of data here is public-domain government data;
   your API keys live in Secrets, never in the repo).
2. Upload the contents of this folder to the repo. Easiest ways:
   - **Web UI:** on the empty repo page click "uploading an existing file" and
     drag in `README.md` and the `pipeline/` folder. The `.github` folder often
     won't drag-drop — so ALSO click *Add file → Create new file*, name it
     exactly `.github/workflows/pull-data.yml`, and paste in the contents of
     that file from this folder.
   - **Or with git**, if you have it: clone, copy files in, push.
3. Add the three API keys as secrets: repo **Settings → Secrets and variables →
   Actions → New repository secret**, one at a time:
   - `BLS_KEY`
   - `FRED_KEY`
   - `EIA_KEY`
4. Trigger the first run: **Actions tab → pull-data → Run workflow**.
   (If Actions asks you to enable workflows, enable them.)
5. Wait ~2-3 minutes; the run should turn green and the `data/` folder will
   fill with CSVs. Done — it now refreshes itself twice daily.

Then tell Claude the repo URL (e.g. `github.com/<you>/cpi-data`) and the model
work continues from there.

## Layout

```
pipeline/       pullers (one per source) + series map
data/bls/       cpi_series.csv — tidy (series_id, year, period, value)
data/fred/      one CSV per cross-check series
data/eia/       weekly_gasoline.csv
data/kalshi/    snapshots_YYYYMM.csv — appended each run
data/bls_files/ seasonal factors + relative importance Excel files, cu.item/cu.series
```
