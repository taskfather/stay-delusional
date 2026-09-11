#!/usr/bin/env python3
import json
import os
from datetime import datetime, timezone
from pathlib import Path

root = Path(__file__).resolve().parents[2]
raw = os.environ.get("PAYLOAD") or "{}"
try:
    payload = json.loads(raw)
except json.JSONDecodeError:
    payload = {}
events = payload.get("events") if isinstance(payload, dict) else payload
if events is None:
    events = []
if isinstance(events, dict):
    events = [events]
if not isinstance(events, list):
    events = []

log = root / "metrics" / "events.jsonl"
log.parent.mkdir(parents=True, exist_ok=True)
with log.open("a") as f:
    for event in events:
        if not isinstance(event, dict):
            continue
        f.write(json.dumps(event, separators=(",", ":")) + "\n")

lines = [ln for ln in log.read_text().splitlines() if ln.strip()][-4000:]
log.write_text("\n".join(lines) + ("\n" if lines else ""))

all_events = []
for ln in lines:
    try:
        all_events.append(json.loads(ln))
    except json.JSONDecodeError:
        pass


def name_of(event):
    if event.get("name"):
        return event["name"]
    if "completed" in event or event.get("pack"):
        return "guide_done" if event.get("completed") else "guide_drop"
    return ""


variants = {}
completed = 0
dropped = 0
named = 0
for event in all_events:
    n = name_of(event)
    if n:
        named += 1
    pack = event.get("pack") or ""
    variant = event.get("variant") or ""
    key = f"{pack}:{variant}"
    row = variants.setdefault(key, {
        "pack": pack,
        "variant": variant,
        "n": 0,
        "completed": 0,
        "slideMs": [],
    })
    if n in ("guide_start", "guide_done", "guide_drop") or (not event.get("name") and pack):
        row["n"] += 1
        if n == "guide_done" or event.get("completed"):
            row["completed"] += 1
            completed += 1
        if n == "guide_drop" or (event.get("completed") is False):
            dropped += 1
        row["slideMs"].extend(event.get("slide_ms") or event.get("slideMs") or [])

out_variants = {}
for key, row in variants.items():
    if not row["pack"]:
        continue
    slides = row["slideMs"]
    out_variants[key] = {
        "pack": row["pack"],
        "variant": row["variant"],
        "n": row["n"],
        "completed": row["completed"],
        "avgSlideMs": (sum(slides) / len(slides)) if slides else 0,
    }

summary = {
    "updatedAt": datetime.now(timezone.utc).isoformat(),
    "events": named or len(all_events),
    "completed": completed,
    "dropped": dropped,
    "completeRate": (completed / (completed + dropped)) if (completed + dropped) else 0,
    "variants": out_variants,
    "recent": [
        {
            "name": name_of(e),
            "pack": e.get("pack"),
            "variant": e.get("variant"),
            "completed": bool(e.get("completed")),
            "slideMs": e.get("slide_ms") or e.get("slideMs") or [],
            "endedAt": e.get("created_at") or e.get("endedAt"),
            "droppedAt": e.get("dropped_at") if e.get("dropped_at") is not None else e.get("droppedAt"),
        }
        for e in all_events[-20:][::-1]
    ],
}

out = root / "content" / "v1" / "metrics.json"
out.write_text(json.dumps(summary, indent=2) + "\n")
