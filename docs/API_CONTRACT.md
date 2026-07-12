# API contract & data model

This is the shared source of truth between backend and frontend. If you need to
change a shape here, tell the other person before changing code.

## Core entities

### Income
```ts
type Income = {
  id: string;
  name: string;         // "Paycheck - Acme Corp"
  amount: number;        // per pay period
  frequency: "weekly" | "biweekly" | "monthly";
  source: "manual" | "bank_detected"; // always "manual" in v1
};
```

### FixedExpense
```ts
type FixedExpense = {
  id: string;
  name: string;          // "Rent", "Car payment", "Netflix"
  amount: number;
  frequency: "weekly" | "biweekly" | "monthly";
};
```

### Goal
```ts
type GoalStrategy = "fund_first" | "proportional_weight" | "fixed_amount";

type Goal = {
  id: string;
  name: string;
  target_amount: number | null;
  target_date: string | null;
  current_amount: number;
  strategy: GoalStrategy;
  priority_rank: number | null;
  weight: number | null;
  fixed_monthly_amount: number | null;
  monthly_contribution_cap: number | null; // NEW — see note below
};
```

### VariableExpenseCategory
```ts
type CategoryKey =
  | "groceries" | "dining_out" | "gas_transportation" | "entertainment"
  | "shopping" | "personal_care" | "travel" | "other";

type VariableExpenseCategory = {
  key: CategoryKey;
  budgeted_amount: number;   // user's actual budget once set
  favor_multiplier: number;  // default 1.0, user-adjustable, boosts suggested share
};
```

## Engine output: the "Plan"

This is what the backend computes and the frontend renders. Everything below is
what a dashboard screen needs.

```ts
type PlanStatus = "normal" | "goals_paused_negative_income" | "tight" | "no_variable_budget";

type GoalContribution = {
  goal_id: string;
  monthly_contribution: number;
  projected_completion_date: string | null; // null if no target_amount/date
};

type CategorySuggestion = {
  key: CategoryKey;
  suggested_amount: number;
  favor_multiplier: number;
};

type Plan = {
  status: PlanStatus;
  message: string | null;      // human-readable explanation, shown when status != "normal"

  total_income: number;
  total_fixed_expenses: number;
  remaining_after_fixed: number;      // income - fixed expenses

  goal_contributions: GoalContribution[];
  remaining_after_goals: number;      // remaining_after_fixed - sum(goal contributions)

  category_suggestions: CategorySuggestion[]; // empty array if remaining_after_goals <= 0
};
```

## Business rules the frontend must reflect

1. **Negative leftover** (`total_income < total_fixed_expenses`): `status =
   "goals_paused_negative_income"`. All goal contributions are 0. Show the
   `message` prominently — do not silently show negative numbers.
2. **Goals always take priority over variable spending.** `fund_first` goals
   are funded in `priority_rank` order before anything is left for
   `category_suggestions`.
3. **Tight budget** (`remaining_after_goals` is less than a baseline minimum,
   e.g. groceries + gas only): `status = "tight"`. Still show suggested
   amounts, but surface the `message` explaining the squeeze.
4. **No variable budget** (`remaining_after_goals <= 0`): `status =
   "no_variable_budget"`, `category_suggestions` is an empty array. Show the
   `message` stating goal contributions exceed leftover income. Do NOT show a
   grid of $0s — show the one message instead.
5. **Favor multipliers** re-weight suggested category splits but never change
   `remaining_after_goals` — the pool being split stays fixed; only the
   distribution across categories shifts.
6. Suggested amounts are defaults only — every category's `budgeted_amount`
   is user-editable at any time, independent of the suggestion.

## Fixtures

See `/fixtures` for example `Plan` JSON objects covering: normal, tight, and
no_variable_budget states. Build the dashboard against these before the real
API exists.
