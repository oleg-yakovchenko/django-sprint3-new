# Blogicum

Проект рассчитан на Python 3.14 и Django 5.2.16.

Перед началом работы перенесите каталог `blogicum/` из выполненного задания
первого спринта, затем скопируйте шаблоны из `templates/` в
`blogicum/templates/`.

## Локальный запуск

```bash
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
pytest
flake8 blogicum
cd blogicum
python manage.py check
python manage.py makemigrations --check --dry-run
```

Файл `requirements.txt` содержит только прямые зависимости задания и не
должен перезаписываться командой `pip freeze`.
