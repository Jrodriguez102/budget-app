"""
SQLite database setup for v1.

Everything lives in a single local file: budget.db, created next to wherever
uvicorn is run from. No external service, no credentials — just a file.
"""

from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./budget.db"

# check_same_thread=False is needed because FastAPI can use SQLite across
# multiple threads in dev mode. Safe for our use case (single local user).
engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})


def create_db_and_tables():
    """Creates budget.db and all tables if they don't already exist."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """FastAPI dependency — yields a DB session per request."""
    with Session(engine) as session:
        yield session
