# Frontend - Agent Instructions

## Stack

- React + Vite + TypeScript
- Recharts for data visualization
- react-i18next for internationalization
- Vitest + React Testing Library for tests

## Commands

Prefer root `make` targets:

```bash
make fe-dev            # Vite dev server
make fe-build          # Production build
make fe-test           # Unit tests
make fe-lint           # ESLint
make fe-format         # Prettier format
make fe-format-check   # Prettier check
```

## Conventions

- All user-facing text must be wired through i18n (`useTranslation` hook)
- Design tokens are in `src/styles/tokens.ts` (Digital Agency design system)
- Components go in `src/components/`, hooks in `src/hooks/`, types in `src/types/`
- API base URL comes from `VITE_API_URL` environment variable
