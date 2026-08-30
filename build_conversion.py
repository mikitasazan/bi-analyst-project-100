"""Build conversion.json from the API exports used in the notebook."""
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

ROOT = Path(__file__).parent
params = {"begin": "2023-03-01", "end": "2023-09-01"}
api = "https://data-charts-api.hexlet.app"


def load(endpoint):
    url = f"{api}/{endpoint}?{urlencode(params)}"
    with urlopen(url, timeout=30) as response:
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

visits_by_day = defaultdict(int)
for moment, visit in latest_visits.values():
    visits_by_day[(moment.date().isoformat(), visit["platform"])] += 1

registrations_by_day = defaultdict(int)
for registration in registrations:
    moment = datetime.fromisoformat(registration["datetime"].replace("Z", "+00:00"))
    registrations_by_day[(moment.date().isoformat(), registration["platform"])] += 1

keys = sorted(set(visits_by_day) | set(registrations_by_day))
columns = {"date_group": {}, "platform": {}, "visits": {}, "registrations": {}, "conversion": {}}
for index, (day, platform) in enumerate(keys):
    visits_count = visits_by_day[(day, platform)]
    registrations_count = registrations_by_day[(day, platform)]
    timestamp = int(datetime.fromisoformat(day).replace(tzinfo=timezone.utc).timestamp() * 1000)
    columns["date_group"][str(index)] = timestamp
    columns["platform"][str(index)] = platform
    columns["visits"][str(index)] = visits_count
    columns["registrations"][str(index)] = registrations_count
    columns["conversion"][str(index)] = registrations_count / visits_count * 100 if visits_count else 0

(ROOT / "conversion.json").write_text(json.dumps(columns, ensure_ascii=False, indent=2) + "\n")
print(f"Created {ROOT / 'conversion.json'} with {len(keys)} rows")
