"""
Pydantic schemas — request/response shapes for the API.

The Plan / GoalContribution / CategorySuggestion types here are the exact
computed-output shapes defined in docs/API_CONTRACT.md. They match the
fixtures in /fixtures byte-for-byte in structure, so the frontend can swap a
fixture for a real API response with zero changes on Jacob's end.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel

from app.models import Frequency, IncomeSource, GoalStrategy, CategoryKey


# ---- Create/update payloads (what the frontend sends in) ----

class IncomeCreate(BaseModel):
    name: str
    amount: float
    frequency: Frequency
    source: IncomeSource = IncomeSource.manual


class FixedExpenseCreate(BaseModel):
    name: str
    amount: float
    frequency: Frequency


class GoalCreate(BaseModel):
    name: str
    target_amount: Optional[float] = None
    target_date: Optional[str] = None
    current_amount: float = 0
    strategy: GoalStrategy
    priority_rank: Optional[int] = None
    weight: Optional[float] = None
    fixed_monthly_amount: Optional[float] = None


class CategoryUpdate(BaseModel):
    budgeted_amount: Optional[float] = None
    favor_multiplier: Optional[float] = None


# ---- Plan output (computed by the allocation engine, never stored) ----

class PlanStatus(str, Enum):
    normal = "normal"
    goals_paused_negative_income = "goals_paused_negative_income"
    tight = "tight"
    no_variable_budget = "no_variable_budget"


class GoalContribution(BaseModel):
    goal_id: str
    monthly_contribution: float
    projected_completion_date: Optional[str] = None


class CategorySuggestion(BaseModel):
    key: CategoryKey
    suggested_amount: float
    favor_multiplier: float


class Plan(BaseModel):
    status: PlanStatus
    message: Optional[str] = None

    total_income: float
    total_fixed_expenses: float
    remaining_after_fixed: float

    goal_contributions: list[GoalContribution]
    remaining_after_goals: float

    category_suggestions: list[CategorySuggestion]
