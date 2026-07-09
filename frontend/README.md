# Frontend

Next.js + Tailwind dashboard. Renders income/expense/goal input forms and the
`Plan` output (goal progress, suggested variable budgets, gap warnings).

## Start here

You don't need the backend running to start. Use the example `Plan` objects in
`/fixtures` at the repo root — load them directly in place of an API call while
building the UI.

1. Read `docs/API_CONTRACT.md` at the repo root first — it defines every shape
   you'll render.
2. Look at all four fixtures, not just the happy path:
   - `plan_normal.json` — everything working fine
   - `plan_tight.json` — goals are eating most of the budget
   - `plan_no_variable_budget.json` — zero left for variable spending
   - `plan_negative_income.json` — expenses exceed income, goals paused
3. Each `status` value needs a distinct visual treatment. Don't just render
   `category_suggestions` as a grid and ignore `status`/`message` — the message
   is the point for three of the four fixtures.

## Setup (planned)

```
npx create-next-app@latest .
npm install
npm run dev
```

## Key screens (planned)

- Income & fixed expense input forms
- Goal creation/editing (strategy picker, priority drag-order for fund_first goals)
- Dashboard: goal progress bars, remaining balances, category suggestions with
  favor-multiplier sliders, status banner for tight/negative/no-budget states

Not yet implemented — this is the next step.
