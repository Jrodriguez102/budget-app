"""
The allocation engine — turns Income + FixedExpense + Goal + Category records
into a Plan, following the business rules in docs/API_CONTRACT.md.

ASSUMPTIONS MADE HERE (flag to Julian/Jacob if any of these don't match intent):

1. Monthly amount conversion: weekly = amount * 52/12, biweekly = amount * 26/12,
   monthly = amount as-is. Every Income/FixedExpense is normalized to a
   monthly figure before anything else happens.

2. fund_first goal contribution amount:
   - If target_date is set: amortize evenly across the remaining months
     until target_date (minimum 1 month), capped by what's actually
     available.
   - If target_date is NOT set but monthly_contribution_cap is: contribute
     that flat capped amount (still capped further by what's available).
   - If neither target_date nor monthly_contribution_cap is set: contributes
     $0. There's no defined pace, so it's skipped rather than either
     guessing or letting it silently absorb all remaining money and starve
     other fund_first goals.
   - If target_amount is null (open-ended fund_first goal): contributes $0,
     same reasoning as above — nothing to aim for or pace against.

3. fixed_amount goals take their flat fixed_monthly_amount, capped by what's
   left after fund_first goals — processed in the order they're passed in.

4. proportional_weight goals split whatever's left after fund_first AND
   fixed_amount goals — but NOT 100% of it. They target a "savings slice" of
   30% of what's left after fund_first/fixed goals, split by relative weight,
   leaving the other 70% for remaining_after_goals / variable spending. This
   30% is a placeholder assumption, not derived from the contract doc — it
   exists so proportional goals don't eat 100% of leftover and zero out the
   variable budget on every plan. Tune this if it doesn't fit.

5. "tight" threshold: remaining_after_goals > 0 but < 5% of total_income
   (per Julian's call).

6. Category split baseline weights — inferred from plan_normal.json's
   category_suggestions (180/120/90/60/60/30/30/30 on $600 = 30/20/15/10/10/5/5/5%).
   Applied as: baseline_weight * favor_multiplier, renormalized to sum to 1,
   multiplied by remaining_after_goals.

7. "tight" status restricts spending to groceries + gas_transportation only
   (inferred from plan_tight.json, where only those two categories got
   nonzero suggestions) — split between just those two, by their relative
   baseline weights, everything else $0.
"""

from datetime import date
from math import ceil

from app.models import Goal, GoalStrategy, Frequency, CategoryKey
from app.schemas import Plan, PlanStatus, GoalContribution, CategorySuggestion


BASELINE_CATEGORY_WEIGHTS = {
    CategoryKey.groceries: 0.30,
    CategoryKey.dining_out: 0.20,
    CategoryKey.gas_transportation: 0.15,
    CategoryKey.entertainment: 0.10,
    CategoryKey.shopping: 0.10,
    CategoryKey.personal_care: 0.05,
    CategoryKey.travel: 0.05,
    CategoryKey.other: 0.05,
}

ESSENTIAL_CATEGORIES_FOR_TIGHT = [CategoryKey.groceries, CategoryKey.gas_transportation]

TIGHT_THRESHOLD_PCT_OF_INCOME = 0.05
PROPORTIONAL_GOAL_SAVINGS_SLICE = 0.30  # see assumption #4 above


def _monthly_amount(amount: float, frequency: Frequency) -> float:
    if frequency == Frequency.weekly:
        return amount * 52 / 12
    if frequency == Frequency.biweekly:
        return amount * 26 / 12
    return amount  # monthly


def _add_months(start: date, months: int) -> date:
    total_month_index = start.month - 1 + months
    year = start.year + total_month_index // 12
    month = total_month_index % 12 + 1
    return date(year, month, 1)


def _months_until(target_date_str: str, today: date) -> int:
    y, m, _ = (int(p) for p in target_date_str.split("-"))
    months = (y - today.year) * 12 + (m - today.month)
    return max(months, 1)


def _fund_goal_contributions(goals: list[Goal], available: float, today: date):
    """
    Returns (contributions: list[GoalContribution], remaining_available: float).
    Follows the priority order described in the module docstring (assumptions #2-#4).
    """
    contributions: list[GoalContribution] = []

    fund_first = sorted(
        [g for g in goals if g.strategy == GoalStrategy.fund_first],
        key=lambda g: (g.priority_rank if g.priority_rank is not None else 999999),
    )
    fixed_amount_goals = [g for g in goals if g.strategy == GoalStrategy.fixed_amount]
    proportional_goals = [g for g in goals if g.strategy == GoalStrategy.proportional_weight]

    # 1. fund_first goals, in priority order
    for goal in fund_first:
        if available <= 0 or goal.target_amount is None:
            contributions.append(GoalContribution(
                goal_id=goal.id, monthly_contribution=0, projected_completion_date=None,
            ))
            continue

        remaining_need = max(goal.target_amount - goal.current_amount, 0)

        if goal.target_date:
            months_left = _months_until(goal.target_date, today)
            desired = remaining_need / months_left
        elif goal.monthly_contribution_cap is not None:
            desired = goal.monthly_contribution_cap
        else:
            # No date and no cap set — can't determine a safe pace, so this
            # goal contributes $0 rather than risk starving other goals.
            contributions.append(GoalContribution(
                goal_id=goal.id, monthly_contribution=0, projected_completion_date=None,
            ))
            continue

        contribution = min(desired, available, remaining_need)
        available -= contribution

        completion_date = None
        if contribution > 0:
            months_needed = ceil(remaining_need / contribution)
            completion_date = _add_months(today, months_needed).isoformat()

        contributions.append(GoalContribution(
            goal_id=goal.id, monthly_contribution=round(contribution, 2),
            projected_completion_date=completion_date,
        ))

    # 2. fixed_amount goals, in list order
    for goal in fixed_amount_goals:
        contribution = min(goal.fixed_monthly_amount or 0, max(available, 0))
        available -= contribution

        completion_date = None
        if goal.target_amount is not None and contribution > 0:
            remaining_need = max(goal.target_amount - goal.current_amount, 0)
            months_needed = ceil(remaining_need / contribution) if remaining_need > 0 else 0
            completion_date = _add_months(today, months_needed).isoformat() if months_needed else today.isoformat()

        contributions.append(GoalContribution(
            goal_id=goal.id, monthly_contribution=round(contribution, 2),
            projected_completion_date=completion_date,
        ))

    # 3. proportional_weight goals split a slice of what's left (assumption #4)
    if proportional_goals and available > 0:
        savings_pool = available * PROPORTIONAL_GOAL_SAVINGS_SLICE
        total_weight = sum(g.weight or 0 for g in proportional_goals)
        for goal in proportional_goals:
            share = (goal.weight or 0) / total_weight if total_weight > 0 else 0
            contribution = savings_pool * share
            available -= contribution

            completion_date = None
            if goal.target_amount is not None and contribution > 0:
                remaining_need = max(goal.target_amount - goal.current_amount, 0)
                months_needed = ceil(remaining_need / contribution) if remaining_need > 0 else 0
                completion_date = _add_months(today, months_needed).isoformat() if months_needed else today.isoformat()

            contributions.append(GoalContribution(
                goal_id=goal.id, monthly_contribution=round(contribution, 2),
                projected_completion_date=completion_date,
            ))
    else:
        for goal in proportional_goals:
            contributions.append(GoalContribution(
                goal_id=goal.id, monthly_contribution=0, projected_completion_date=None,
            ))

    return contributions, max(available, 0)


def _split_categories(remaining_after_goals: float, categories, status: PlanStatus) -> list[CategorySuggestion]:
    if remaining_after_goals <= 0:
        return []

    if status == PlanStatus.tight:
        keys = ESSENTIAL_CATEGORIES_FOR_TIGHT
    else:
        keys = list(BASELINE_CATEGORY_WEIGHTS.keys())

    by_key = {c.key: c for c in categories}
    weighted = {
        key: BASELINE_CATEGORY_WEIGHTS[key] * by_key[key].favor_multiplier
        for key in keys if key in by_key
    }
    total_weight = sum(weighted.values())

    suggestions = []
    for key in BASELINE_CATEGORY_WEIGHTS.keys():
        if key in weighted and total_weight > 0:
            amount = remaining_after_goals * (weighted[key] / total_weight)
        else:
            amount = 0
        favor = by_key[key].favor_multiplier if key in by_key else 1.0
        suggestions.append(CategorySuggestion(
            key=key, suggested_amount=round(amount, 2), favor_multiplier=favor,
        ))
    return suggestions


def compute_plan(incomes, fixed_expenses, goals, categories, today: date | None = None) -> Plan:
    today = today or date.today()

    total_income = round(sum(_monthly_amount(i.amount, i.frequency) for i in incomes), 2)
    total_fixed_expenses = round(sum(_monthly_amount(e.amount, e.frequency) for e in fixed_expenses), 2)
    remaining_after_fixed = round(total_income - total_fixed_expenses, 2)

    if remaining_after_fixed < 0:
        return Plan(
            status=PlanStatus.goals_paused_negative_income,
            message="Your fixed expenses exceed your income this month. Goal contributions are paused until income or expenses change.",
            total_income=total_income,
            total_fixed_expenses=total_fixed_expenses,
            remaining_after_fixed=remaining_after_fixed,
            goal_contributions=[],
            remaining_after_goals=remaining_after_fixed,
            category_suggestions=[],
        )

    goal_contributions, remaining_after_goals = _fund_goal_contributions(
        goals, remaining_after_fixed, today,
    )
    remaining_after_goals = round(remaining_after_goals, 2)

    if remaining_after_goals <= 0:
        status = PlanStatus.no_variable_budget
        message = "Your goal contributions exceed your leftover income. Any discretionary spending would come from reducing goal contributions or fixed expenses."
        category_suggestions = []
    elif total_income > 0 and remaining_after_goals < total_income * TIGHT_THRESHOLD_PCT_OF_INCOME:
        status = PlanStatus.tight
        message = "This covers only groceries and gas — there's little left for dining, entertainment, or other discretionary spending this month."
        category_suggestions = _split_categories(remaining_after_goals, categories, status)
    else:
        status = PlanStatus.normal
        message = None
        category_suggestions = _split_categories(remaining_after_goals, categories, status)

    return Plan(
        status=status,
        message=message,
        total_income=total_income,
        total_fixed_expenses=total_fixed_expenses,
        remaining_after_fixed=remaining_after_fixed,
        goal_contributions=goal_contributions,
        remaining_after_goals=remaining_after_goals,
        category_suggestions=category_suggestions,
    )