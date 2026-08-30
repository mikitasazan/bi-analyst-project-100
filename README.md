# Дашборд конверсий


[![hexlet-check](https://github.com/mikitasazan/bi-analyst-project-100/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/mikitasazan/bi-analyst-project-100/actions)

Создайте скрипт, который работает с апи и базой данных

Учебный проект Хекслета: https://ru.hexlet.io/programs/bi-analyst


## Стек

- Python — загрузка данных и расчёт конверсии
- Jupyter Notebook — исследование данных
- pandas, requests — работа с API и датафреймами

## Установка

```bash
git clone https://github.com/mikitasazan/bi-analyst-project-100.git
cd bi-analyst-project-100
pip install -r requirements.txt
```

## Использование

Откройте `analysis.ipynb` и выполните ячейки по порядку. Ноутбук получает
данные API за период 2023-03-01 — 2023-09-01, исключает ботов, оставляет
последний визит пользователя и сохраняет результат в `conversion.json`.

Для быстрой проверки без Jupyter:

```bash
python3 build_conversion.py
```

---

<details>
<summary>Автоматические тесты Хекслета</summary>

Тесты запускаются на каждый коммит. За запуск отвечает файл `.github/workflows/hexlet-check.yml` — не удаляйте и не переименовывайте ни его, ни репозиторий.

</details>

## О Хекслете

[Хекслет](https://ru.hexlet.io/) — школа программирования: авторские программы обучения с практикой, поддержкой наставников и реальными проектами, которые остаются в резюме. Этот репозиторий — один из таких проектов.
