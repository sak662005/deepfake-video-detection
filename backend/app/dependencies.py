from collections.abc import Generator

from sqlalchemy.orm import Session

from app.database.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Provide a database session for request-scoped operations."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user() -> str:
    """Placeholder dependency for future authentication support."""
    return "anonymous"
