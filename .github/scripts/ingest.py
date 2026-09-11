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

variants = {}
completed = 0
dropped = 0
for event in all_events:
    key = f"{event.get('pack', '')}:{event.get('variant', '')}"
    row = variants.setdefault(key, {
        "pack": event.get("pack", ""),
        "variant": event.get("variant", ""),
        "n": 0,
        "completed": 0,
        "slideMs": [],
    })
    row["n"] += 1
    if event.get("completed"):
        row["completed"] += 1
        completed += 1
    else:
        dropped += 1
    row["slideMs"].extend(event.get("slideMs") or [])

out_variants = {}
for key, row in variants.items():
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
    "events": len(all_events),
    "completed": completed,
    "dropped": dropped,
    "completeRate": (completed / len(all_events)) if all_events else 0,
    "variants": out_variants,
    "recent": [
        {
            "pack": e.get("pack"),
            "variant": e.get("variant"),
            "completed": bool(e.get("completed")),
            "slideMs": e.get("slideMs") or [],
            "endedAt": e.get("endedAt"),
        }
        for e in all_events[-20:][::-1]
    ],
}

out = root / "content" / "v1" / "metrics.json"
out.write_text(json.dumps(summary, indent=2) + "\n")
