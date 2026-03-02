# Repository Guidelines

## Project Structure & Module Organization
This frontend is a Vite + React (TSX) app rooted in `frontend/`.
- `src/main.tsx` bootstraps the app, and `src/App.tsx` controls top-level flow.
- `src/components/` holds feature components; `src/components/ui/` contains reusable Radix-style primitives.
- `src/context/` stores providers, `src/services/` contains API clients, and `src/data/` keeps mock/demo data.
- `src/styles/globals.css` defines design tokens and utility layers.
- `public/` contains static demo pages (`demo-*.html`, `graph*.html`).
- Build output is generated to `build/` by Vite.

## Build, Test, and Development Commands
- `npm install`: install dependencies.
- `npm run dev`: start local dev server on port `13001` (configured in `vite.config.ts`).
- `npm run build`: create production bundle in `build/`.
- `npx vite preview --port 4173`: preview the production build locally.

## Coding Style & Naming Conventions
- Use TypeScript React function components and keep indentation at 2 spaces.
- Component files use `PascalCase` (for example, `KnowledgeGraph.tsx`); hooks/util helpers use `camelCase`.
- In `src/components/ui/`, keep existing kebab-case naming (for example, `dropdown-menu.tsx`).
- Prefer explicit, typed props/interfaces for component and service boundaries.
- Keep shared styles/tokens in `src/styles/globals.css`; avoid accidental large edits to generated-heavy `src/index.css`.

## Testing Guidelines
No automated test script is currently configured in `package.json`.
- Treat `npm run build` as the minimum CI safety check.
- For UI/logic changes, perform manual smoke tests: landing flow, step navigation, and API-backed extraction path.
- When adding test infrastructure, place tests near features (for example, `src/components/steps/__tests__/QuestionAnswer.test.tsx`) and prioritize user-visible behavior.

## Commit & Pull Request Guidelines
This workspace snapshot does not include `.git` history, so follow Conventional Commit style:
- `feat: add evidence highlight for extracted entities`
- `fix: handle missing VITE_API_BASE_URL fallback`

PRs should include:
- a concise summary and scope,
- linked issue/task ID,
- screenshots or short recordings for UI changes,
- commands run (at minimum `npm run build`) and results.

## Security & Configuration Tips
- API base URL resolves from `VITE_API_BASE_URL`, otherwise defaults to `http://<hostname>:8001/api`.
- Never commit secrets or environment-specific endpoints in source files.
