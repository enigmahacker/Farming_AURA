# Crops dataset

This directory contains dataset files derived from `backend/data/knowledge/crops_water_fertilizer.json`.

- `crops.csv`: full table with one row per crop.
- `crops_train.jsonl`, `crops_val.jsonl`, `crops_test.jsonl`: newline-delimited JSON splits (default 80/10/10 split).
- `schema.json`: simple schema describing fields and units.

How to regenerate:

```bash
python3 backend/scripts/prepare_dataset.py
```

Notes:
- Values are estimated for example purposes. Validate before using in production.
