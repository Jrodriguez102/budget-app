# Backend

Python/FastAPI service. Owns:

- Income & fixed expense storage
- Goal management
- The allocation engine (hybrid strategy — see `docs/API_CONTRACT.md`)
- Variable expense category suggestions (favor-weighted)
- API endpoints returning `Plan` objects matching the shared contract
- (Later, v2) SimpleFIN bank integration

## Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API docs (interactive): http://127.0.0.1:8000/docs

Database is a single local file, `backend/budget.db` — created automatically
on first run. It's gitignored; nobody needs to share or commit it.

## Structure

```
app/
  main.py       FastAPI app + all routes
  database.py   SQLite engine/session setup
  models.py     DB tables (Income, FixedExpense, Goal, VariableExpenseCategory)
  schemas.py    Request/response shapes, incl. the Plan output type
  engine.py     The allocation engine — NOT YET IMPLEMENTED (next task)
```

## Status

- ✅ Project skeleton, SQLite models, CRUD endpoints for all four entities
- ✅ Categories auto-seed with all 8 keys on first run
- ⬜ Allocation engine (`/plan` currently returns 501)

## API surface so far

| Method | Path                    | Notes                          |
|--------|-------------------------|---------------------------------|
| GET    | `/income`               | list                            |
| POST   | `/income`                | create                           |
| DELETE | `/income/{id}`          | delete                          |
| GET    | `/fixed-expenses`       | list                             |
| POST   | `/fixed-expenses`       | create                           |
| DELETE | `/fixed-expenses/{id}`  | delete                          |
| GET    | `/goals`                | list                             |
| POST   | `/goals`                | create                            |
| DELETE | `/goals/{id}`           | delete                          |
| GET    | `/categories`           | list all 8, with current amounts |
| PATCH  | `/categories/{key}`     | update budgeted_amount / favor_multiplier |
| GET    | `/plan`                 | **501 until engine is built**   |