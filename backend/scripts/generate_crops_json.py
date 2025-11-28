#!/usr/bin/env python3
"""
Generate an expanded JSON dataset of crops with estimated water and fertilizer requirements.
Reads `backend/data/knowledge/crops_seed.json` and writes
`backend/data/knowledge/crops_water_fertilizer.json`.
"""
from pathlib import Path
import json
import random
import math


BASE = Path(__file__).resolve().parents[1]
KNOWLEDGE_DIR = BASE / "data" / "knowledge"
SEED_FILE = KNOWLEDGE_DIR / "crops_seed.json"
OUT_FILE = KNOWLEDGE_DIR / "crops_water_fertilizer.json"


def load_seed():
    with SEED_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


CATEGORY_RANGES = {
    "Cereal": {
        "water_mm": (300, 700),
        "irrig_days": (7, 21),
        "n": (80, 200),
        "p": (20, 60),
        "k": (20, 80),
    },
    "Pulse": {
        "water_mm": (250, 550),
        "irrig_days": (10, 21),
        "n": (10, 60),
        "p": (10, 40),
        "k": (10, 40),
    },
    "Oilseed": {
        "water_mm": (300, 600),
        "irrig_days": (10, 21),
        "n": (40, 140),
        "p": (20, 50),
        "k": (20, 80),
    },
    "Vegetable": {
        "water_mm": (300, 900),
        "irrig_days": (4, 10),
        "n": (80, 250),
        "p": (40, 120),
        "k": (40, 200),
    },
    "Leafy Vegetable": {
        "water_mm": (300, 800),
        "irrig_days": (3, 8),
        "n": (50, 200),
        "p": (20, 80),
        "k": (20, 120),
    },
    "Fruit": {
        "water_mm": (400, 1500),
        "irrig_days": (7, 21),
        "n": (100, 350),
        "p": (50, 200),
        "k": (100, 350),
    },
    "Spice": {
        "water_mm": (300, 1000),
        "irrig_days": (7, 18),
        "n": (40, 220),
        "p": (20, 120),
        "k": (20, 200),
    },
    "Plantation": {
        "water_mm": (600, 2000),
        "irrig_days": (7, 30),
        "n": (120, 400),
        "p": (50, 250),
        "k": (100, 400),
    },
    "Fodder": {
        "water_mm": (400, 900),
        "irrig_days": (5, 12),
        "n": (60, 220),
        "p": (20, 80),
        "k": (40, 160),
    },
    "Fiber": {
        "water_mm": (350, 900),
        "irrig_days": (7, 21),
        "n": (60, 220),
        "p": (20, 80),
        "k": (40, 160),
    },
    "Nut": {
        "water_mm": (400, 1400),
        "irrig_days": (7, 25),
        "n": (80, 300),
        "p": (30, 150),
        "k": (80, 300),
    },
    "Herb": {
        "water_mm": (200, 600),
        "irrig_days": (4, 12),
        "n": (20, 120),
        "p": (10, 80),
        "k": (10, 120),
    },
    "Other": {
        "water_mm": (200, 1000),
        "irrig_days": (7, 21),
        "n": (20, 200),
        "p": (10, 120),
        "k": (10, 200),
    },
}


SUFFIXES = ["", " - Local", " - Hybrid", " - Improved", " - Variety A", " - Variety B", " - High Yielding", " - Traditional", " - Short Duration", " - Long Duration"]


def pick_range(category, key):
    r = CATEGORY_RANGES.get(category) or CATEGORY_RANGES.get("Other")
    return r[key]


def generate_value(rng, round_digits=1):
    v = random.uniform(rng[0], rng[1])
    return round(v, round_digits)


def main(target_count=1000):
    random.seed(42)
    seed = load_seed()
    out = []
    i = 1
    idx = 0
    # iterate expanding seed until we have target_count entries
    while len(out) < target_count:
        entry = seed[idx % len(seed)]
        base_en = entry.get("name_en")
        base_hi = entry.get("name_hi")
        category = entry.get("category", "Other")

        suffix = SUFFIXES[(len(out) + idx) % len(SUFFIXES)]
        # ensure uniqueness if name repeats
        name_en = f"{base_en}{suffix}"
        # sometimes add an index to increase variety
        if any(x["name_en"] == name_en for x in out):
            name_en = f"{name_en} #{(len(out) % 100) + 1}"

        name_hi = base_hi

        water = generate_value(pick_range(category, "water_mm"), 1)
        irrig = random.randint(*pick_range(category, "irrig_days"))
        n = generate_value(pick_range(category, "n"), 1)
        p = generate_value(pick_range(category, "p"), 1)
        k = generate_value(pick_range(category, "k"), 1)

        item = {
            "id": i,
            "name_en": name_en,
            "name_hi": name_hi,
            "category": category,
            "water_requirement_mm_per_season": water,
            "irrigation_frequency_days": irrig,
            "fertilizer_n_kg_per_ha": n,
            "fertilizer_p_kg_per_ha": p,
            "fertilizer_k_kg_per_ha": k,
            "notes": "Estimated values — region, variety and management dependent. Validate locally before use.",
        }
        out.append(item)
        i += 1
        idx += 1

    # write output
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(out)} entries to {OUT_FILE}")


if __name__ == "__main__":
    main(1000)
