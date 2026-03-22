#!/usr/bin/env python3
"""Fetch public LLM leaderboard data and write to data/leaderboard/.

Sources:
  - HuggingFace Open LLM Leaderboard (public API)
  - LMSYS Chatbot Arena (public standings)
"""
import json
import os
import sys
from datetime import datetime, timezone

import requests

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'leaderboard')
os.makedirs(DATA_DIR, exist_ok=True)


def fetch_open_llm_leaderboard(limit=20):
    """Fetch top models from HuggingFace Open LLM Leaderboard v2."""
    url = 'https://huggingface.co/api/spaces/open-llm-leaderboard/open_llm_leaderboard/api/predict'
    # Fallback: scrape the dataset directly
    dataset_url = 'https://datasets-server.huggingface.co/rows?dataset=open-llm-leaderboard%2Fresults&config=default&split=train&offset=0&length=50'
    entries = []
    try:
        resp = requests.get(dataset_url, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            rows = data.get('rows', [])
            for row in rows[:limit]:
                r = row.get('row', {})
                entries.append({
                    'model': r.get('model_name', r.get('fullname', 'Unknown')),
                    'average_score': r.get('average', r.get('Average', None)),
                    'parameters': r.get('params', r.get('#Params (B)', None)),
                    'architecture': r.get('architecture', r.get('Architecture', None)),
                    'source': 'open-llm-leaderboard',
                    'url': f"https://huggingface.co/{r.get('model_name', r.get('fullname', ''))}",
                })
            print(f'[leaderboard] Fetched {len(entries)} models from Open LLM Leaderboard dataset')
        else:
            print(f'[leaderboard] Open LLM Leaderboard dataset returned {resp.status_code}')
    except Exception as e:
        print(f'[leaderboard] Error fetching Open LLM Leaderboard: {e}')
    return entries


def fetch_lmsys_arena(limit=20):
    """Fetch top models from LMSYS Chatbot Arena leaderboard."""
    url = 'https://huggingface.co/spaces/lmsys/chatbot-arena-leaderboard'
    # Use the HF datasets API for the arena results
    dataset_url = 'https://datasets-server.huggingface.co/rows?dataset=lmsys%2Fchatbot_arena_conversations&config=default&split=train&offset=0&length=1'
    # Alternative: try the arena standings JSON
    arena_url = 'https://storage.googleapis.com/arena_external_data/elo_results_latest.json'
    entries = []
    try:
        resp = requests.get(arena_url, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            # Parse Elo rankings
            if isinstance(data, dict):
                # Could be keyed by model name
                models = []
                for model_name, stats in data.items():
                    if isinstance(stats, dict):
                        models.append({
                            'model': model_name,
                            'elo_rating': stats.get('elo', stats.get('rating', None)),
                            'votes': stats.get('num_battles', stats.get('votes', None)),
                            'source': 'lmsys-chatbot-arena',
                            'url': f'https://chat.lmsys.org/',
                        })
                # Sort by Elo descending
                models.sort(key=lambda x: x.get('elo_rating') or 0, reverse=True)
                entries = models[:limit]
            elif isinstance(data, list):
                for item in data[:limit]:
                    if isinstance(item, dict):
                        entries.append({
                            'model': item.get('model', item.get('name', 'Unknown')),
                            'elo_rating': item.get('elo', item.get('rating', None)),
                            'source': 'lmsys-chatbot-arena',
                            'url': 'https://chat.lmsys.org/',
                        })
            print(f'[leaderboard] Fetched {len(entries)} models from LMSYS Arena')
        else:
            print(f'[leaderboard] LMSYS Arena returned {resp.status_code}, skipping')
    except Exception as e:
        print(f'[leaderboard] Error fetching LMSYS Arena: {e}')
    return entries


def main():
    timestamp = datetime.now(timezone.utc).isoformat()
    all_entries = []

    # Open LLM Leaderboard
    open_llm = fetch_open_llm_leaderboard(limit=20)
    all_entries.extend(open_llm)

    # LMSYS Chatbot Arena
    arena = fetch_lmsys_arena(limit=20)
    all_entries.extend(arena)

    if not all_entries:
        print('[leaderboard] WARNING: No leaderboard data fetched from any source')
        # Write empty file so workflow doesn't fail
        output = {'fetched_at': timestamp, 'sources': [], 'entries': []}
    else:
        sources = list(set(e.get('source', '') for e in all_entries))
        output = {
            'fetched_at': timestamp,
            'sources': sources,
            'total_entries': len(all_entries),
            'entries': all_entries,
        }

    output_path = os.path.join(DATA_DIR, 'llm_leaderboard.json')
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2, default=str)
    print(f'[leaderboard] Wrote {len(all_entries)} entries to {output_path}')

    # Also write a latest summary
    summary_path = os.path.join(DATA_DIR, 'latest_summary.json')
    summary = {
        'fetched_at': timestamp,
        'open_llm_leaderboard_count': len(open_llm),
        'lmsys_arena_count': len(arena),
        'top_models': [e.get('model', '') for e in all_entries[:10]],
    }
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f'[leaderboard] Wrote summary to {summary_path}')


if __name__ == '__main__':
    main()
