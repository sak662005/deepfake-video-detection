from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.models import DetectionJob
from app.database.session import get_db

router = APIRouter()


@router.get("/", summary="List prior detections")
async def list_history(limit: int = Query(default=10, ge=1, le=100), db: Session = Depends(get_db)) -> dict[str, object]:
    jobs = db.query(DetectionJob).order_by(DetectionJob.created_at.desc()).limit(limit).all()
    items = []
    for job in jobs:
        items.append({
            "id": job.id,
            "filename": job.video_name,
            "prediction": "FAKE" if job.is_fake else "REAL",
            "confidence": job.confidence,
            "spatial_score": None,
            "temporal_score": None,
            "final_score": None,
            "timestamp": job.created_at.isoformat() if job.created_at else None,
        })
    return {"items": items, "limit": limit}


@router.delete("/{job_id}", summary="Delete a detection history item")
async def delete_history_item(job_id: int, db: Session = Depends(get_db)):
    job = db.query(DetectionJob).filter(DetectionJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="History item not found")
    db.delete(job)
    db.commit()
    return {"message": "History item deleted", "id": job_id}
