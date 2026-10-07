"""Saves survey responses to Supabase when configured, else to data/responses.csv."""
import csv
from pathlib import Path

import httpx
import pandas as pd

from config import secret
from scoring import QUESTIONS

CSV_PATH = Path(__file__).parent / "data" / "responses.csv"
COLUMNS = ["created_at", "name", "grade", "school", "lang",
           *[q["id"] for q in QUESTIONS], "typed_answers", "top1", "top2", "route", "source"]


def _supabase():
    url, key = secret("SUPABASE_URL"), secret("SUPABASE_KEY")
    if not (url and key):
        return None
    headers = {"apikey": key, "Content-Type": "application/json"}
    # Legacy JWT keys also need the Bearer header; new sb_secret_ keys go in apikey only
    if key.startswith("eyJ"):
        headers["Authorization"] = f"Bearer {key}"
    return f'{url.rstrip("/")}/rest/v1/responses', headers


def _save_csv(row):
    is_new = not CSV_PATH.exists()
    # utf-8-sig so Excel shows Marathi/Hindi names correctly
    with CSV_PATH.open("a", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        if is_new:
            w.writeheader()
        w.writerow(row)


def save_response(row):
    """Returns where the row went: "supabase", "csv", or "csv_fallback" (Supabase failed)."""
    sb = _supabase()
    if sb:
        endpoint, headers = sb
        try:
            r = httpx.post(endpoint, json=row, headers={**headers, "Prefer": "return=minimal"}, timeout=10)
            r.raise_for_status()
            return "supabase"
        except httpx.HTTPError:
            _save_csv(row)
            return "csv_fallback"
    _save_csv(row)
    return "csv"


def load_responses():
    frames = []
    sb = _supabase()
    if sb:
        endpoint, headers = sb
        r = httpx.get(endpoint, params={"select": ",".join(COLUMNS)}, headers=headers, timeout=15)
        r.raise_for_status()
        frames.append(pd.DataFrame(r.json(), columns=COLUMNS))
    if CSV_PATH.exists():
        frames.append(pd.read_csv(CSV_PATH, encoding="utf-8-sig"))
    if not frames:
        return pd.DataFrame(columns=COLUMNS)
    return pd.concat(frames, ignore_index=True)
