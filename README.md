# Django Bootcamp

A hands-on Django learning project. Built step by step to cover the full Django cycle — models, views, templates, forms, auth, signals, atomic transactions, and more.

## Project: Todo List App

A personal task manager with user authentication.

**Features:**
- Add / edit / delete tasks
- Mark tasks as done
- Personal tasks per user (login required)

## Stack
- Python 3.x
- Django 6.x
- PostgreSQL (planned)
- pytest for testing
- GitHub Actions for CI

## Setup
```bash
git clone https://github.com/Arsha-shf/Django-Bootcamp
cd Django-Bootcamp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Branch Strategy
- `main` — stable, production-ready code only
- `feat/*` — new features
- `fix/*` — bug fixes