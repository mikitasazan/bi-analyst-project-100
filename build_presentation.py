"""Build a short business presentation from the generated charts."""
from pathlib import Path
import PIL.JpegImagePlugin
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent


def font(size):
    path = "/System/Library/Fonts/Supplemental/Arial.ttf"
    return ImageFont.truetype(path, size) if Path(path).exists() else ImageFont.load_default()


def page(title, subtitle):
    image = Image.new("RGB", (1600, 900), "white")
    draw = ImageDraw.Draw(image)
    draw.text((80, 50), title, fill="#172033", font=font(46))
    draw.text((80, 120), subtitle, fill="#526070", font=font(24))
    return image, draw


pages = []
image, draw = page("Дашборд конверсий", "Анализ визитов, регистраций и рекламных расходов")
draw.text((100, 260), "Период: 1 марта — 1 сентября 2023", fill="#172033", font=font(34))
draw.text((100, 340), "Цель: понять, как меняется воронка и где реклама приводит", fill="#172033", font=font(30))
draw.text((100, 390), "качественный трафик.", fill="#172033", font=font(30))
draw.text((100, 540), "Источник: data-charts-api.hexlet.app", fill="#526070", font=font(24))
pages.append(image)

image, draw = page("Воронка по платформам", "Повторные визиты сведены к последнему визиту пользователя; боты исключены")
chart = Image.open(ROOT / "charts/visits_by_platform.png").convert("RGB")
chart.thumbnail((700, 430))
image.paste(chart, (70, 210))
chart = Image.open(ROOT / "charts/registrations_by_platform.png").convert("RGB")
chart.thumbnail((700, 430))
image.paste(chart, (820, 210))
pages.append(image)

image, draw = page("Рекомендации", "Что проверить перед перераспределением бюджета")
for index, line in enumerate((
    "1. Сравнивать платформы по конверсии, а не только по числу визитов.",
    "2. Отдельно контролировать рекламные расходы по кампаниям.",
    "3. Проверять просадки по дням и сопоставлять их с изменениями бюджета.",
    "4. Использовать фильтры даты и кампании в итоговом дашборде.",
)):
    draw.text((100, 230 + index * 80), line, fill="#172033", font=font(28))
draw.text((100, 650), "Запросы и расчёты: charts_project.ipynb, build_*.py", fill="#526070", font=font(23))
pages.append(image)

pages[0].save(ROOT / "presentation.pdf", save_all=True, append_images=pages[1:])
print(f"Created {ROOT / 'presentation.pdf'}")
