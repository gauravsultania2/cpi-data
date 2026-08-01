"""CPI-U component tree for the bottom-up model.

Item codes are BLS CU-survey item codes. Series IDs:
  SA  (seasonally adjusted):    CUSR0000 + item_code
  NSA (not seasonally adjusted): CUUR0000 + item_code
Not every item has an SA series (e.g. motor vehicle insurance is NSA-only);
the puller tolerates missing series and records what it actually got.
"""

# item_code -> (name, block)
ITEMS = {
    # --- aggregates (validation & targets) ---
    "SA0":    ("All items (headline)", "aggregate"),
    "SA0L1E": ("All items less food & energy (core)", "aggregate"),
    "SA0E":   ("Energy", "aggregate"),
    "SAF1":   ("Food", "aggregate"),
    "SAH1":   ("Shelter", "aggregate"),
    "SAS4":   ("Transportation services", "aggregate"),
    "SASLE":  ("Services less energy services", "aggregate"),
    "SACL1E": ("Commodities less food & energy commodities", "aggregate"),
    "SAM":    ("Medical care", "aggregate"),
    # --- energy ---
    "SETB01": ("Gasoline (all types)", "energy"),
    "SEHF01": ("Electricity", "energy"),
    "SEHF02": ("Utility (piped) gas service", "energy"),
    "SEHE01": ("Fuel oil", "energy"),
    # --- food ---
    "SAF11":  ("Food at home", "food"),
    "SEFV":   ("Food away from home", "food"),
    # --- shelter ---
    "SEHC":   ("Owners' equivalent rent", "shelter"),
    "SEHA":   ("Rent of primary residence", "shelter"),
    "SEHB":   ("Lodging away from home", "shelter"),
    # --- core goods ---
    "SETA01": ("New vehicles", "core_goods"),
    "SETA02": ("Used cars and trucks", "core_goods"),
    "SETC":   ("Motor vehicle parts & equipment", "core_goods"),
    "SAA":    ("Apparel", "core_goods"),
    "SAM1":   ("Medical care commodities", "core_goods"),
    "SAH3":   ("Household furnishings & operations", "core_goods"),
    "SERA":   ("Video and audio", "core_goods"),
    "SEEE":   ("Information technology commodities", "core_goods"),
    "SAF116": ("Alcoholic beverages", "core_goods"),
    "SEGA":   ("Tobacco & smoking products", "core_goods"),
    # --- core services ---
    "SAM2":   ("Medical care services", "core_services"),
    "SEME":   ("Health insurance", "core_services"),
    "SETD":   ("Motor vehicle maintenance & repair", "core_services"),
    "SETE":   ("Motor vehicle insurance", "core_services"),
    "SETG01": ("Airline fares", "core_services"),
    "SEHG":   ("Water, sewer, trash collection", "core_services"),
    "SAR":    ("Recreation", "core_services"),
    "SAE":    ("Education & communication", "core_services"),
    "SAG":    ("Other goods and services", "core_services"),
    "SAG1":   ("Personal care", "core_services"),
}

def series_ids():
    """All candidate series IDs (SA + NSA) for the US city average."""
    out = []
    for code in ITEMS:
        out.append("CUSR0000" + code)   # SA
        out.append("CUUR0000" + code)   # NSA
    return out
