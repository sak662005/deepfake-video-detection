from pathlib import Path
import json

from fastapi import APIRouter

router = APIRouter()

METRICS_PATH = Path("outputs/performance_metrics.json")


@router.get("/performance", summary="Get model performance metrics")
async def get_performance_metrics():
    if not METRICS_PATH.exists():
        return {
            "evaluated": False,
            "message": "Not evaluated yet",
            "metrics": None,
            "comparison": None,
        }

    try:
        with open(METRICS_PATH, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except Exception as exc:  # pragma: no cover - defensive fallback
        return {
            "evaluated": False,
            "message": f"Unable to read metrics: {exc}",
            "metrics": None,
            "comparison": None,
        }

    return {
        "evaluated": data.get("evaluated", False),
        "message": data.get("message", "Metrics loaded"),
        "metrics": data.get("metrics", {}),
        "comparison": data.get("comparison", {}),
    }
