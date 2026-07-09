# Backend

Python/FastAPI service that owns:

- Income & fixed expense storage
- Goal management + the allocation engine (hybrid strategy — see `docs/API_CONTRACT.md`)
- Variable expense category suggestions (favor-weighted)
- API endpoints returning `Plan` objects matching the shared contract
- (Later) SimpleFIN bank integration

## Setup (planned)

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Structure (planned)

```
app/
  main.py          FastAPI app + routes
  models.py         DB models (income, expenses, goals, categories)
  engine.py         Allocation engine — the core logic
  schemas.py        Pydantic schemas matching docs/API_CONTRACT.md
```

Not yet implemented — this is the next step.
