#!/usr/bin/env python3
"""Generate CSV exports and markdown tables from JSON datasets."""
import csv
import json
import io
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def json_to_csv(json_path: Path, csv_path: Path, list_key: str):
    with open(json_path) as f:
        data = json.load(f)
    items = data.get(list_key, [])
    if not items:
        print(f"  No items in {json_path.name}")
        return
    # Flatten nested dicts
    flat_items = []
    for item in items:
        flat = {}
        for k, v in item.items():
            if isinstance(v, dict):
                for sk, sv in v.items():
                    flat[f"{k}.{sk}"] = sv
            elif isinstance(v, list):
                flat[k] = "; ".join(str(x) for x in v)
            else:
                flat[k] = v
        flat_items.append(flat)
    fieldnames = list(flat_items[0].keys())
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(flat_items)
    print(f"  {csv_path.name}: {len(flat_items)} rows")


def main():
    print("Generating CSV exports...\n")
    exports = [
        ("models/models.json", "models/models.csv", "models"),
        ("vendors/vendors.json", "vendors/vendors.csv", "vendors"),
        ("benchmarks/benchmarks.json", "benchmarks/benchmarks.csv", "benchmarks"),
        ("compliance/frameworks.json", "compliance/frameworks.csv", "frameworks"),
    ]
    for json_rel, csv_rel, key in exports:
        jp = DATA / json_rel
        cp = DATA / csv_rel
        if jp.exists():
            json_to_csv(jp, cp, key)
    print("\nDone.")


if __name__ == "__main__":
    main()