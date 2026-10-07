import json
from pathlib import Path

DATA = Path(__file__).parent / "data"
QUESTIONS = json.loads((DATA / "questions.json").read_text(encoding="utf-8"))
CAREERS = json.loads((DATA / "careers.json").read_text(encoding="utf-8"))
UI = json.loads((DATA / "ui_text.json").read_text(encoding="utf-8"))
CLUSTER_ORDER = ["HEALTH", "TECH", "BIZ", "ARTS", "SERVE", "SKILL"]
ROUTES = ["SHORT", "MEDIUM", "LONG"]
OTHER = -1  # answer index meaning "typed their own answer"


def tr(texts, lang):
    return texts.get(lang) or texts["en"]


def score(answers, custom=None):
    """answers: {"q1": option_index or OTHER}; custom: {"q3": {"points": {...}} or {"route": ...}}
    for typed answers (from the AI classifier; missing when offline → 0 points)."""
    custom = custom or {}
    totals = {c: 0 for c in CLUSTER_ORDER}
    route = "MEDIUM"
    for q in QUESTIONS:
        idx = answers[q["id"]]
        option = custom.get(q["id"], {}) if idx == OTHER else q["options"][idx]
        route = option.get("route", route)
        for cluster, pts in option.get("points", {}).items():
            totals[cluster] += pts
    # sorted() is stable, so ties keep CLUSTER_ORDER and results are repeatable
    ranked = sorted(CLUSTER_ORDER, key=lambda c: -totals[c])
    earned = sum(totals.values()) or 1
    top = [{"cluster": c, "match": round(totals[c] * 100 / earned)} for c in ranked[:2]]
    return {"totals": totals, "top": top, "route": route}
