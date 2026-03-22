#!/usr/bin/env python3
"""
generate_ai_index_json.py - Combine all data sources into a single ai-index.json
Runs as part of the daily GitHub Action workflow.
"""
import json
import os
from pathlib import Path
from datetime import datetime, timezone

def load_json_files(directory):
    """Load all JSON files from a directory."""
    items = []
    dir_path = Path(directory)
    if not dir_path.exists():
        return items
    for f in sorted(dir_path.glob("*.json")):
        try:
            with open(f, "r", encoding="utf-8") as fh:
                data = json.load(fh)
                if isinstance(data, list):
                    items.extend(data)
                elif isinstance(data, dict):
                    items.append(data)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: skipping {f}: {e}")
    return items

def load_vendor_files(directory):
    """Load all vendor JSON files from nested directory."""
    items = []
    dir_path = Path(directory)
    if not dir_path.exists():
        return items
    for f in sorted(dir_path.glob("**/*.json")):
        if f.name == "dataset-metadata.json":
            continue
        try:
            with open(f, "r", encoding="utf-8") as fh:
                data = json.load(fh)
                if isinstance(data, list):
                    items.extend(data)
                elif isinstance(data, dict):
                    items.append(data)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: skipping {f}: {e}")
    return items

def main():
    index = {
        "name": "awesome-ai-index",
        "description": "The definitive Awesome AI Index",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "version": "2026.03",
        "sections": {}
    }

    # Load models
    models = load_json_files("data/models")
    if models:
        index["sections"]["models"] = models

    # Load vendors
    vendors = load_vendor_files("data/vendors")
    if vendors:
        index["sections"]["vendors"] = vendors

    # Load benchmarks
    benchmarks = load_json_files("data/benchmarks")
    if benchmarks:
        index["sections"]["benchmarks"] = benchmarks

    # Load frameworks
    frameworks = load_json_files("data/frameworks")
    if frameworks:
        index["sections"]["frameworks"] = frameworks

    # Load papers if they exist
    papers = load_json_files("data/papers")
    if papers:
        index["sections"]["papers"] = papers

    # Load trending models from HuggingFace if they exist
    trending = load_json_files("data/trending")
    if trending:
        index["sections"]["trending"] = trending

    # Write output
    output_path = Path("ai-index.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    total = sum(len(v) for v in index["sections"].values())
    print(f"Generated ai-index.json with {len(index['sections'])} sections, {total} total entries")

if __name__ == "__main__":
    main()
