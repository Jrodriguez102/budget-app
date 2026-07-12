"""
FastAPI app entrypoint.

Run with:  uvicorn app.main:app --reload
Docs at:   http://127.0.0.1:8000/docs  (auto-generated, interactive)
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from app.database import create_db_and_tables, engine
from app.models import Income, FixedExpense, Goal, VariableExpenseCategory, CategoryKey
from app.schemas import IncomeCreate, FixedExpenseCreate, GoalCreate, CategoryUpdate, Plan as PlanSchema
from app.engine import compute_plan


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    _seed_categories()
    yield


app = FastAPI(title="Budget App API", lifespan=lifespan)

# Allows the Next.js dev server (localhost:3000) to call this API during
# local development. Tighten this before any real deployment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _seed_categories():
    """Ensures all 8 variable expense categories exist as rows on first run."""
    with Session(engine) as session:
        existing = session.exec(select(VariableExpenseCategory)).all()
        existing_keys = {c.key for c in existing}
        for key in CategoryKey:
            if key not in existing_keys:
                session.add(VariableExpenseCategory(key=key))
        session.commit()


@app.get("/")
def root():
    return {"status": "ok", "service": "budget-app-api"}


# ---- Income ----

@app.get("/income", response_model=list[Income])
def list_income():
    with Session(engine) as session:
        return session.exec(select(Income)).all()


@app.post("/income", response_model=Income)
def create_income(payload: IncomeCreate):
    with Session(engine) as session:
        income = Income.model_validate(payload.model_dump())
        session.add(income)
        session.commit()
        session.refresh(income)
        return income


@app.delete("/income/{income_id}")
def delete_income(income_id: str):
    with Session(engine) as session:
        income = session.get(Income, income_id)
        if not income:
            raise HTTPException(status_code=404, detail="Income not found")
        session.delete(income)
        session.commit()
        return {"deleted": income_id}


# ---- Fixed expenses ----

@app.get("/fixed-expenses", response_model=list[FixedExpense])
def list_fixed_expenses():
    with Session(engine) as session:
        return session.exec(select(FixedExpense)).all()


@app.post("/fixed-expenses", response_model=FixedExpense)
def create_fixed_expense(payload: FixedExpenseCreate):
    with Session(engine) as session:
        expense = FixedExpense.model_validate(payload.model_dump())
        session.add(expense)
        session.commit()
        session.refresh(expense)
        return expense


@app.delete("/fixed-expenses/{expense_id}")
def delete_fixed_expense(expense_id: str):
    with Session(engine) as session:
        expense = session.get(FixedExpense, expense_id)
        if not expense:
            raise HTTPException(status_code=404, detail="Fixed expense not found")
        session.delete(expense)
        session.commit()
        return {"deleted": expense_id}


# ---- Goals ----

@app.get("/goals", response_model=list[Goal])
def list_goals():
    with Session(engine) as session:
        return session.exec(select(Goal)).all()


@app.post("/goals", response_model=Goal)
def create_goal(payload: GoalCreate):
    with Session(engine) as session:
        goal = Goal.model_validate(payload.model_dump())
        session.add(goal)
        session.commit()
        session.refresh(goal)
        return goal


@app.delete("/goals/{goal_id}")
def delete_goal(goal_id: str):
    with Session(engine) as session:
        goal = session.get(Goal, goal_id)
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")
        session.delete(goal)
        session.commit()
        return {"deleted": goal_id}


# ---- Variable expense categories ----

@app.get("/categories", response_model=list[VariableExpenseCategory])
def list_categories():
    with Session(engine) as session:
        return session.exec(select(VariableExpenseCategory)).all()


@app.patch("/categories/{key}", response_model=VariableExpenseCategory)
def update_category(key: CategoryKey, payload: CategoryUpdate):
    with Session(engine) as session:
        category = session.get(VariableExpenseCategory, key)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        if payload.budgeted_amount is not None:
            category.budgeted_amount = payload.budgeted_amount
        if payload.favor_multiplier is not None:
            category.favor_multiplier = payload.favor_multiplier
        session.add(category)
        session.commit()
        session.refresh(category)
        return category


# ---- Plan (the actual point of the app) ----

@app.get("/plan", response_model=PlanSchema)
def get_plan():
    with Session(engine) as session:
        incomes = session.exec(select(Income)).all()
        fixed_expenses = session.exec(select(FixedExpense)).all()
        goals = session.exec(select(Goal)).all()
        categories = session.exec(select(VariableExpenseCategory)).all()

    return compute_plan(incomes, fixed_expenses, goals, categories)