"""
The allocation engine — the core logic of the app.

NOT IMPLEMENTED YET. This is next up after the scaffold + models.

Will take the current Income, FixedExpense, Goal, and VariableExpenseCategory
records and produce a Plan, following the business rules in
docs/API_CONTRACT.md:

1. remaining_after_fixed = total_income - total_fixed_expenses
   - If negative -> status = "goals_paused_negative_income", all goal
     contributions are 0, category_suggestions is empty.
2. Fund fund_first goals in priority_rank order first, then split whatever's
   left across proportional_weight and fixed_amount goals.
3. remaining_after_goals = remaining_after_fixed - sum(goal contributions)
   - If <= 0 -> status = "no_variable_budget", category_suggestions is empty.
   - If less than some baseline minimum -> status = "tight".
   - Otherwise -> status = "normal".
4. Split remaining_after_goals across the 8 variable categories, weighted by
   each category's favor_multiplier. Multipliers reweight the split only —
   they never change the total pool being split.

See /fixtures for four worked examples of expected output shapes.
"""

from app.schemas import Plan


def compute_plan(*args, **kwargs) -> Plan:
    raise NotImplementedError("Allocation engine not yet built")
