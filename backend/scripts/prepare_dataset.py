#!/usr/bin/env python3
"""
Prepare dataset files from `crops_water_fertilizer.json`:
- writes `backend/data/dataset/crops.csv`
- writes JSONL splits: `crops_train.jsonl`, `crops_val.jsonl`, `crops_test.jsonl`
- writes a `schema.json` describing fields

Usage: python3 backend/scripts/prepare_dataset.py
"""
from pathlib import Path
import json
import csv
import random

BASE = Path(__file__).resolve().parents[1]
KNOW = BASE / "data" / "knowledge"
SRC = KNOW / "crops_water_fertilizer.json"
OUT_DIR = BASE / "data" / "dataset"


def load():
    with SRC.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_csv(items, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "id",
        "name_en",
        "name_hi",
        "category",
        "water_requirement_mm_per_season",
        "irrigation_frequency_days",
        "fertilizer_n_kg_per_ha",
        "fertilizer_p_kg_per_ha",
        "fertilizer_k_kg_per_ha",
        "notes",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for it in items:
            row = {k: it.get(k, "") for k in fieldnames}
            writer.writerow(row)


def write_jsonl(items, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")


def write_schema(path):
    schema = {
        "fields": {
            "id": {"type": "integer"},
            "name_en": {"type": "string", "lang": "en"},
            "name_hi": {"type": "string", "lang": "hi"},
            "category": {"type": "string"},
            "water_requirement_mm_per_season": {"type": "number", "unit": "mm"},
            "irrigation_frequency_days": {"type": "integer", "unit": "days"},
            "fertilizer_n_kg_per_ha": {"type": "number", "unit": "kg/ha (N)"},
            "fertilizer_p_kg_per_ha": {"type": "number", "unit": "kg/ha (P)"},
            "fertilizer_k_kg_per_ha": {"type": "number", "unit": "kg/ha (K)"},
            "notes": {"type": "string"},
        },
        "description": "Estimated water and fertilizer requirements per crop. Values are approximate; validate for local conditions before using in production ML systems.",
    }
    with path.open("w", encoding="utf-8") as f:
        json.dump(schema, f, ensure_ascii=False, indent=2)


def main(train_frac=0.8, val_frac=0.1, seed=42):
    items = load()
    random.Random(seed).shuffle(items)
    n = len(items)
    n_train = int(n * train_frac)
    n_val = int(n * val_frac)
    train = items[:n_train]
    val = items[n_train:n_train + n_val]
    test = items[n_train + n_val:]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(items, OUT_DIR / "crops.csv")
    write_jsonl(train, OUT_DIR / "crops_train.jsonl")
    write_jsonl(val, OUT_DIR / "crops_val.jsonl")
    write_jsonl(test, OUT_DIR / "crops_test.jsonl")
    write_schema(OUT_DIR / "schema.json")

    print(f"Wrote CSV and JSONL splits to {OUT_DIR} (train={len(train)} val={len(val)} test={len(test)})")


if __name__ == "__main__":
    main()
