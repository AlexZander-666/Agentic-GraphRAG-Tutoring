# Repository Guidelines

## Project Structure & Module Organization
This repository is split into two apps and support docs:
- `backend/`: FastAPI service (`app/main.py`), API routes in `app/api/`, extraction logic in `app/core/`, scenario definitions in `app/scenarios/`, and utilities in `app/utils/`.
- `frontend/`: Vite + React + TypeScript UI. Main entry is `src/main.tsx`, app shell is `src/App.tsx`, reusable components are in `src/components/`, and API calls are in `src/services/`.
- `docs/`: project documentation and scenario demos.
- Root scripts: `setup.sh`, `start.sh`, `start.bat`, and `docker-compose.yml`.

## Build, Test, and Development Commands
- Backend setup:
  - `cd backend && python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt`
- Backend run:
  - `cd backend && uvicorn app.main:app --reload --port 8000`
- Frontend setup/run:
  - `cd frontend && npm install && npm run dev`
- Frontend build:
  - `cd frontend && npm run build`
- Full stack helpers:
  - `./setup.sh` then `./start.sh` (Linux/macOS)
  - `start.bat` (Windows)
  - `docker compose up --build` (containerized run)

## Coding Style & Naming Conventions
- Python: PEP 8, 4-space indentation, `snake_case` for functions/modules, `PascalCase` for classes.
- TypeScript/React: 2-space indentation, functional components, `PascalCase` for component files (for example, `KnowledgeGraph.tsx`), `camelCase` for variables/functions.
- Keep API schemas centralized in `backend/app/models/schemas.py`; keep UI state in React context/providers where shared.

## Testing Guidelines
- Backend test tooling is `pytest` (`backend/requirements.txt`).
- Place tests under `backend/tests/` and name files `test_*.py`.
- Run tests with: `cd backend && pytest -q`.
- Current frontend package does not define a test script; add one when introducing frontend tests (recommended: Vitest + React Testing Library).

## Commit & Pull Request Guidelines
- This workspace snapshot does not include `.git` history, so no project-specific commit pattern is discoverable here.
- Use Conventional Commits going forward (for example, `feat(api): add scenario sample endpoint`).
- PRs should include: concise summary, linked issue/ticket, test evidence (command + result), and screenshots/GIFs for UI changes.

## Security & Configuration Tips
- Do not commit secrets. Keep API keys in `backend/.env` (for example, `DEEPSEEK_API_KEY`).
- Validate changes via `http://localhost:8000/docs` and confirm frontend-backend connectivity before opening a PR.
