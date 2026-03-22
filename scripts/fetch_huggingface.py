#!/usr/bin/env python3
"""Fetch trending AI models from HuggingFace Hub API."""

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

DATA_DIR = Path("data/models")

HF_CATEGORIES = [
    "text-generation",
    "text-classification",
    "image-classification",
    "object-detection",
    "image-segmentation",
    "text-to-image",
    "image-to-text",
    "automatic-speech-recognition",
    "token-classification",
    "question-answering",
    "summarization",
    "translation",
    "fill-mask",
    "sentence-similarity",
    "zero-shot-classification",
    "reinforcement-learning",
    "tabular-classification",
    "tabular-regression",
    "text-to-speech",
    "depth-estimation",
]


def fetch_trending_models(task: str, limit: int = 10) -> list:
    """Fetch trending models for a given task from HuggingFace."""
    url = "https://huggingface.co/api/models"
    params = {
        "filter": task,
        "sort": "downloads",
        "direction": -1,
        "limit": limit,
        "cardData": True,
    }
    headers = {}
    hf_token = os.getenv("HF_TOKEN")
    if hf_token:
        headers["Authorization"] = f"Bearer {hf_token}"

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=30)
        resp.raise_for_status()
        models = resp.json()
        results = []
        for m in models:
            results.append({
                "model_id": m.get("modelId", ""),
                "task": task,
                "downloads": m.get("downloads", 0),
                "likes": m.get("likes", 0),
                "created_at": m.get("createdAt", ""),
                "last_modified": m.get("lastModified", ""),
                "tags": m.get("tags", []),
                "pipeline_tag": m.get("pipeline_tag", ""),
                "fetched_at": datetime.now(timezone.utc).isoformat(),
            })
        return results
    except Exception as e:
        print(f"Error fetching {task}: {e}")
        return []


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    models_file = DATA_DIR / "hf_models.json"

    existing = []
    if models_file.exists():
        with open(models_file) as f:
            existing = json.load(f)

    existing_ids = {m["model_id"] for m in existing}
    new_models = []

    for task in HF_CATEGORIES:
        print(f"Fetching HuggingFace: {task}")
        models = fetch_trending_models(task, limit=10)
        for m in models:
            if m["model_id"] not in existing_ids:
                new_models.append(m)
                existing_ids.add(m["model_id"])
        time.sleep(0.5)

    merged = new_models + existing
    merged = merged[:2000]  # keep max 2000

    with open(models_file, "w") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)

    print(f"Done. {len(new_models)} new models added. Total: {len(merged)}")


if __name__ == "__main__":
    main()
