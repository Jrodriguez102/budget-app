# Budget App

A personal budgeting app that takes income + fixed expenses, lets you set financial
goals (emergency fund, house down payment, investing, anything else), and generates
a savings plan plus suggested variable-expense budgets (groceries, gas, dining, etc.)
from whatever's left over.

## How it works (high level)

```
income - fixed expenses - goal contributions = remaining
remaining -> suggested split across variable expense categories
```

Goals always take priority over discretionary spending. If goal contributions leave
little or nothing for variable spending, the app says so plainly instead of hiding it.

See `docs/API_CONTRACT.md` for the full data shapes and business rules.

## Repo structure

```
backend/    Python/FastAPI engine + API (owned by Julian)
frontend/   Next.js + Tailwind dashboard (owned by [friend])
docs/       Shared spec: API contract, data model, business rules
fixtures/   Example engine output JSON, for frontend dev without a live backend
```

## Roles

- **Backend / engine** (Julian): income & expense tracking, goal allocation logic,
  variable expense suggestion logic, API endpoints, (later) bank integration.
- **Frontend** (friend): dashboard UI, forms for income/expenses/goals, rendering
  the plan output (goal progress, suggested budgets, gap warnings) from the API
  contract below. Build against `fixtures/` first — no need to wait on a live backend.

## Getting started

1. Read `docs/API_CONTRACT.md` — this is the source of truth both of you build against.
2. Backend: see `backend/README.md`
3. Frontend: see `frontend/README.md` — start with the JSON files in `fixtures/`
4. Copy `.env.example` to `.env` and fill in your own values. Never commit `.env`.

## Status

Early scaffold. Bank integration (SimpleFIN) is deliberately deferred — v1 is
fully manual-entry and works end to end without it.
