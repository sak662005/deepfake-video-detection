from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logger import setup_logging
from app.database.session import init_db

logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI) -> Any:
    logger.info("Application startup initiated")

    try:
        init_db()
    except Exception as e:
        logger.warning(f"Database initialization warning: {e}")

    yield

    logger.info("Application shutdown initiated")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.APP_VERSION,
    description="Deepfake Video Detection using Spatiotemporal Analysis",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Routes
# --------------------------------------------------

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Deepfake Video Detection API",
        "version": settings.APP_VERSION,
    }


@app.get("/health", tags=["Health"])
async def health():
    return {
        "status": "healthy"
    }


app.include_router(
    api_router,
    prefix=settings.API_V1_STR
)