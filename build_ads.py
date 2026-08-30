"""Combine daily conversion metrics with campaign costs."""
import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

ROOT = Path(__file__).parent
params = {"begin": "2023-03-01", "end": "2023-09-01"}
api = "https://data-charts-api.hexlet.app"


def load(endpoint):
    with urlopen(f"{api}/{endpoint}?{urlencode(params)}", timeout=30) as response:
        return json.load(response)


visits = load("visits")
registrations = load("registrations")
latest_visits = {}
for visit in visits:
    if visit["platform"] == "bot" or "bot" in visit["user_agent"].lower():
        continue
    moment = datetime.fromisoformat(visit["datetime"].replace("Z", "+00:00"))
    previous = latest_visits.get(visit["visit_id"])
    if previous is None or moment > previous[0]:
        latest_visits[visit["visit_id"]] = (moment, visit)

visits_by_day = Counter(moment.date().isoformat() for moment, _ in latest_visits.values())
registrations_by_day = Counter(
    datetime.fromisoformat(row["datetime"].replace("Z", "+00:00")).date().isoformat()
    for row in registrations
)

rows = []
with (ROOT / "ads.csv").open(newline="") as stream:
    for ad in csv.DictReader(stream):
        day = ad["date"][:10]
        rows.append({
            "date_group": int(datetime.fromisoformat(day).replace(tzinfo=timezone.utc).timestamp() * 1000),
            "visits": visits_by_day[day],
            "registrations": registrations_by_day[day],
            "cost": int(ad["cost"]),
            "utm_campaign": ad["utm_campaign"],
        })

rows.sort(key=lambda row: (row["date_group"], row["utm_campaign"]))
columns = {key: {str(index): row[key] for index, row in enumerate(rows)} for key in rows[0]}
(ROOT / "ads.json").write_text(json.dumps(columns, ensure_ascii=False, indent=2) + "\n")
print(f"Created {ROOT / 'ads.json'} with {len(rows)} rows")
