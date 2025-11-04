# Repository Guidelines

## Project Structure & Module Organization
The Django project root lives in `Neetechs/` (settings, ASGI/WSGI entry points, websocket routing, logging). Business domains sit in sibling apps such as `Category/`, `Checkout/`, `Profile/`, `Service/`, `home/`, and `chat/`; each app exposes `models.py`, DRF `serializers.py`, viewsets, and `tests.py`. Static assets aggregate in `static/`, while deployable diagrams and reports sit under `report/` and `diagram*.png` for quick reference. Environment templates reside in `env.example`—copy this into `.env` before running management commands. Treat app-level `migrations/` directories as source; do not hand-edit generated files.

## Build, Test, and Development Commands
- `python -m venv .venv && source .venv/bin/activate` — create an isolated runtime that matches production dependencies.
- `pip install -r requirements.txt` (use the OS-specific file if needed) — installs Django 5, DRF, Channels, Firebase tooling, and other integrations expected by `Neetechs/settings.py`.
- `python manage.py migrate` — brings the relational schema in line with the latest app migrations.
- `python manage.py runserver 0.0.0.0:8000` — boots the local API and websocket stack using settings exposed via `.env`.
- `pytest` or `pytest Category/tests.py -q` — executes tests using `pytest.ini`, which wires `DJANGO_SETTINGS_MODULE=Neetechs.settings` and enables DRF test helpers.

## Coding Style & Naming Conventions
Follow standard Django/DRF patterns: 4-space indentation, `snake_case` for modules/functions, and `PascalCase` for models, serializers, and API views (e.g., `ServiceRequestSerializer`). Keep serializers thin and push business rules into model methods or dedicated services under `Service/`. Group settings overrides within `Neetechs/settings/` and avoid duplicating secrets across modules—import from the base settings file instead. Prefer class-based views and DRF viewsets, and co-locate URL patterns in each app’s `urls.py`. When adding logging, route configuration through `Neetechs/logging_config.py` so deployment targets can override handlers centrally.

## Testing Guidelines
Pytest discovers files named `tests.py`, `test_*.py`, or `*_tests.py` (see `pytest.ini`). Mirror the app layout: `Category/tests/test_filters.py` should exercise `Category/serializers.py` and `Category/views.py`. Use `pytest.mark.django_db` for ORM-heavy cases and `pytest.mark.parametrize` to cover edge cases without duplicating fixtures. Target meaningful coverage for serializers and permissions—most regressions stem from DRF permission classes or Firebase hooks—so add regression tests before refactoring. Run `pytest --reuse-db` locally to speed up iterative work, and keep factories or fixtures alongside the tests they serve.

## Commit & Pull Request Guidelines
Write imperative, scope-first commit subjects (`Category: add filtering options`) and keep the body focused on rationale or migration notes. Squash noisy WIP commits before opening a PR. Every PR should include: a summary of changes, reproduction or verification steps (commands you ran), linked GitHub issues or ticket IDs, schema or API contract updates, and screenshots for any admin or template tweaks (e.g., updates under `chat/templates/`). Highlight required env variables or credentials whenever touching code that reads from `.env` or `firebase.py`.
