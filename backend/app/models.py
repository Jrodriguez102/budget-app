"""
Database models — these are the tables actually stored in budget.db.

These mirror the entities defined in docs/API_CONTRACT.md (Income,
FixedExpense, Goal, VariableExpenseCategory). If you change a field here,
update the contract doc and tell Jacob — the frontend is built against that
doc's shapes.

Note: Plan / GoalContribution / CategorySuggestion are NOT tables — they're
computed by the allocation engine on the fly, not stored. Those live in
schemas.py as plain Pydantic models.
"""

import uuid
from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field


def generate_id() -> str:
    return str(uuid.uuid4())


class Frequency(str, Enum):
    weekly = "weekly"
    biweekly = "biweekly"
    monthly = "monthly"


class IncomeSource(str, Enum):
    manual = "manual"
    bank_detected = "bank_detected"  # unused until v2 (SimpleFIN)


class GoalStrategy(str, Enum):
    fund_first = "fund_first"
    proportional_weight = "proportional_weight"
    fixed_amount = "fixed_amount"


class CategoryKey(str, Enum):
    groceries = "groceries"
    dining_out = "dining_out"
    gas_transportation = "gas_transportation"
    entertainment = "entertainment"
    shopping = "shopping"
    personal_care = "personal_care"
    travel = "travel"
    other = "other"


class Income(SQLModel, table=True):
    id: str = Field(default_factory=generate_id, primary_key=True)
    name: str
    amount: float
    frequency: Frequency
    source: IncomeSource = IncomeSource.manual  # always "manual" in v1


class FixedExpense(SQLModel, table=True):
    id: str = Field(default_factory=generate_id, primary_key=True)
    name: str
    amount: float
    frequency: Frequency


class Goal(SQLModel, table=True):
    id: str = Field(default_factory=generate_id, primary_key=True)
    name: str
    target_amount: Optional[float] = None
    target_date: Optional[str] = None  # ISO date string
    current_amount: float = 0
    strategy: GoalStrategy

    # Exactly one of these three should be set, matching `strategy`.
    # Enforced in the engine/validation layer, not at the DB level.
    priority_rank: Optional[int] = None          # required if fund_first
    weight: Optional[float] = None                # required if proportional_weight
    fixed_monthly_amount: Optional[float] = None   # required if fixed_amount

    # Required for fund_first goals that have no target_date — caps how much
    # gets funneled in per month so one open-ended goal can't silently
    # starve other fund_first goals of all available money. Optional for
    # every other case (ignored if target_date is set, since the date
    # already determines pace).
    monthly_contribution_cap: Optional[float] = None


class VariableExpenseCategory(SQLModel, table=True):
    # key is the primary key — one row per category, always all 8 present.
    key: CategoryKey = Field(primary_key=True)
    budgeted_amount: float = 0
    favor_multiplier: float = 1.0