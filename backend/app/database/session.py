from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.logger import setup_logging
from app.database.base import Base

logger = setup_logging()


# --------------------------------------------------
# DATABASE ENGINE
# --------------------------------------------------

if settings.USE_SQLITE:

    engine = create_engine(
        settings.database_url,
        echo=False,
        future=True,
        connect_args={
            "check_same_thread": False
        }
    )

else:

    engine = create_engine(
        settings.database_url,
        echo=False,
        future=True
    )


# --------------------------------------------------
# SESSION
# --------------------------------------------------

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# --------------------------------------------------
# DATABASE DEPENDENCY
# --------------------------------------------------

def get_db():
    """
    Provides a database session to FastAPI endpoints.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# --------------------------------------------------
# INITIALIZE DATABASE
# --------------------------------------------------

def init_db() -> None:
    """
    Create all database tables.
    """

    try:

        Base.metadata.create_all(bind=engine)

        logger.info(
            "Database tables initialized successfully."
        )

    except Exception as e:

        logger.warning(
            f"Database initialization warning: {e}"
        )