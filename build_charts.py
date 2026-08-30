"""Create the PNG charts required by the project using Pillow."""
import json
from collections import defaultdict
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
CHARTS = ROOT / "charts"
CHARTS.mkdir(exist_ok=True)


def font(size):
    path = "/System/Library/Fonts/Supplemental/Arial.ttf"
    return ImageFont.truetype(path, size) if Path(path).exists() else ImageFont.load_default()


def make_chart(title, labels, values, filename, color="#3973d6", suffix=""):
    image = Image.new("RGB", (1400, 800), "white")
    draw = ImageDraw.Draw(image)
    draw.text((70, 45), title, fill="#172033", font=font(38))
    left, top, right, bottom = 120, 140, 1320, 700
    max_value = max(values or [1])
    bar_width = max(20, (right - left) // max(1, len(values) * 2))
    gap = bar_width
    for index, (label, value) in enumerate(zip(labels, values)):
        x = left + index * (bar_width + gap)
        height = int((bottom - top - 50) * value / max_value)
        draw.rectangle((x, bottom - height, x + bar_width, bottom), fill=color)
        draw.text((x, bottom + 15), str(label)[:16], fill="#172033", font=font(18))
        draw.text((x, bottom - height - 32), f"{value:,.1f}{suffix}".replace(",.0", ""), fill="#172033", font=font(17))
    draw.line((left, bottom, right, bottom), fill="#526070", width=2)
    image.save(CHARTS / filename)


data = json.loads((ROOT / "conversion.json").read_text())
rows = [{key: data[key][str(i)] for key in data} for i in range(len(data["platform"]))]
platforms = sorted({row["platform"] for row in rows})
make_chart("Визиты по платформам", platforms, [sum(r["visits"] for r in rows if r["platform"] == p) for p in platforms], "visits_by_platform.png")
make_chart("Регистрации по платформам", platforms, [sum(r["registrations"] for r in rows if r["platform"] == p) for p in platforms], "registrations_by_platform.png", "#54a875")
make_chart("Средняя конверсия по платформам", platforms, [sum(r["conversion"] for r in rows if r["platform"] == p) / max(1, sum(r["visits"] for r in rows if r["platform"] == p)) for p in platforms], "conversion_by_platform.png", "#e28b3e", "%")
daily = defaultdict(lambda: {"visits": 0, "registrations": 0})
for row in rows:
    daily[row["date_group"]]["visits"] += row["visits"]
    daily[row["date_group"]]["registrations"] += row["registrations"]
days = sorted(daily)
labels = [str(day)[:10] for day in days]
make_chart("Итоговые визиты по дням", labels, [daily[day]["visits"] for day in days], "total_visits.png")
make_chart("Итоговые регистрации по дням", labels, [daily[day]["registrations"] for day in days], "total_registrations.png", "#54a875")
make_chart("Средняя конверсия по дням", labels, [daily[day]["registrations"] / max(1, daily[day]["visits"]) * 100 for day in days], "average_conversion.png", "#e28b3e", "%")

ads = json.loads((ROOT / "ads.json").read_text())
ad_rows = [{key: ads[key][str(i)] for key in ads} for i in range(len(ads["cost"]))]
campaigns = defaultdict(int)
for row in ad_rows:
    campaigns[row["utm_campaign"]] += row["cost"]
top_campaigns = sorted(campaigns.items(), key=lambda item: item[1], reverse=True)[:10]
make_chart("Расходы по рекламным кампаниям", [x[0] for x in top_campaigns], [x[1] for x in top_campaigns], "ad_costs_by_campaign.png", "#c45656")
print(f"Created charts in {CHARTS}")
