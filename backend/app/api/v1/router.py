from fastapi import APIRouter

from app.api.v1.endpoints import history, metrics, predict, upload

api_router = APIRouter()

api_router.include_router(upload.router, prefix="/upload", tags=["upload"])
api_router.include_router(predict.router, prefix="/predict", tags=["predict"])
api_router.include_router(history.router, prefix="/history", tags=["history"])
api_router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
