# Repository Guidelines

## Project Structure & Module Organization
This folder is the Python backend for Agentic-GraphRAG. Core code lives in `app/`:
- `app/main.py`: FastAPI app entrypoint and middleware setup.
- `app/api/`: HTTP route handlers (`routes.py`, `rag_routes.py`).
- `app/core/`: extraction orchestration logic.
- `app/services/`: integrations (vector stores, parser, QA agent).
- `app/scenarios/`: domain-specific extraction scenarios.
- `app/models/`: Pydantic request/response schemas.
- `app/utils/`: sanitization and cache helpers.

Configuration is defined in `app/config.py`; environment defaults are in `.env.example`; Python dependencies are pinned in `requirements.txt`.

## Build, Test, and Development Commands
- `python -m venv .venv` then `.\.venv\Scripts\Activate.ps1`: create/activate local virtualenv (Windows).
- `pip install -r requirements.txt`: install backend dependencies.
- `uvicorn app.main:app --reload --port 8001`: run API locally with auto-reload.
- `pytest -q`: run tests (add tests first if none exist yet).
- From repository root: `docker compose up --build`: start backend + frontend containers.

## Coding Style & Naming Conventions
Use 4-space indentation and follow PEP 8 conventions. Prefer type hints for public functions and service interfaces.
- Modules/functions/variables: `snake_case`
- Classes/Pydantic models: `PascalCase`
- Environment variables: `UPPER_SNAKE_CASE`

Keep route handlers thin; move business logic into `app/core/` or `app/services/`. Add brief docstrings for non-obvious behavior.

## Testing Guidelines
Use `pytest` (and `httpx` for API-level tests). Store tests under a top-level `tests/` directory mirroring `app/` package structure.
- File names: `test_<module>.py`
- Test names: `test_<behavior>`

For changes in routes, scenarios, or extraction logic, include both happy-path and failure-path coverage.

## Commit & Pull Request Guidelines
Git history is not available in this checkout, so follow Conventional Commit style:
- `feat(api): add scenario filter endpoint`
- `fix(cache): handle empty key safely`

PRs should include: concise summary, linked issue (if any), test evidence (`pytest` output), and sample request/response for API changes.

## Security & Configuration Tips
Never commit secrets or `.env`. Start from `.env.example` and set keys locally (for example `DEEPSEEK_API_KEY`). Validate new config keys in `app/config.py` and document defaults.
