#!/usr/bin/env python3
"""
fetch_arxiv.py - Fetch latest AI/ML papers from arXiv public API
Runs daily to keep the papers index fresh.
"""

import json
import os
import requests
from datetime import datetime, timedelta
from pathlib import Path

ARXIV_API = "http://export.arxiv.org/api/query"
DATA_DIR = Path("data/papers")

QUERIES = [
    "cat:cs.LG+AND+ti:LLM",
    "cat:cs.AI+AND+ti:agent",
    "cat:cs.CL+AND+ti:language+model",
    "cat:cs.LG+AND+ti:fine-tuning",
    "cat:cs.LG+AND+ti:RAG",
]

def fetch_papers(query, max_results=5):
    """Fetch papers from arXiv API."""
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    try:
        resp = requests.get(ARXIV_API, params=params, timeout=30)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException as e:
        print(f"Error fetching arXiv papers: {e}")
        return None

def parse_arxiv_xml(xml_text):
    """Parse arXiv API XML response to extract paper metadata."""
    import xml.etree.ElementTree as ET
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "arxiv": "http://arxiv.org/schemas/atom",
    }
    papers = []
    try:
        root = ET.fromstring(xml_text)
        for entry in root.findall("atom:entry", ns):
            paper = {
                "title": entry.findtext("atom:title", "", ns).strip().replace("\n", " "),
                "authors": [a.findtext("atom:name", "", ns) for a in entry.findall("atom:author", ns)],
                "summary": entry.findtext("atom:summary", "", ns).strip()[:300],
                "arxiv_id": entry.findtext("atom:id", "", ns).split("/abs/")[-1],
                "published": entry.findtext("atom:published", "", ns)[:10],
                "updated": entry.findtext("atom:updated", "", ns)[:10],
                "url": entry.findtext("atom:id", "", ns),
                "fetched_at": datetime.utcnow().isoformat(),
            }
            papers.append(paper)
    except ET.ParseError as e:
        print(f"XML parse error: {e}")
    return papers

def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.utcnow().strftime("%Y-%m-%d")
    all_papers = []

    for query in QUERIES:
        print(f"Fetching arXiv: {query}")
        xml = fetch_papers(query)
        if xml:
            papers = parse_arxiv_xml(xml)
            all_papers.extend(papers)
            print(f"  Found {len(papers)} papers")

    # Deduplicate by arxiv_id
    seen = set()
    unique_papers = []
    for p in all_papers:
        if p["arxiv_id"] not in seen:
            seen.add(p["arxiv_id"])
            unique_papers.append(p)

    # Load existing papers
    papers_file = DATA_DIR / "papers.json"
    existing = []
    if papers_file.exists():
        with open(papers_file) as f:
            existing = json.load(f)

    # Merge: add new papers not already in existing
    existing_ids = {p["arxiv_id"] for p in existing}
    new_papers = [p for p in unique_papers if p["arxiv_id"] not in existing_ids]
    merged = new_papers + existing  # newest first
    merged = merged[:500]  # keep max 500

    with open(papers_file, "w") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)

    print(f"Done. {len(new_papers)} new papers added. Total: {len(merged)}")

if __name__ == "__main__":
    main()
