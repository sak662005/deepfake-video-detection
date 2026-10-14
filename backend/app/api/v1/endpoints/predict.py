from pathlib import Path
import shutil
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database.models import DetectionJob
from app.database.session import get_db
from app.services.inference.video_predictor import VideoPredictor


router = APIRouter()

predictor = VideoPredictor()


@router.post("/", summary="Predict Deepfake Video")
async def predict_video(
    video: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # ----------------------------
    # Validate File
    # ----------------------------

    if not video.filename:
        raise HTTPException(
            status_code=400,
            detail="No video file selected.",
        )

    if not video.filename.lower().endswith(
        (".mp4", ".avi", ".mov", ".mkv")
    ):
        raise HTTPException(
            status_code=400,
            detail="Unsupported video format.",
        )

    # ----------------------------
    # Save Uploaded Video
    # ----------------------------

    upload_dir = Path("uploads/videos")
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_name = f"{uuid.uuid4()}_{video.filename}"
    video_path = upload_dir / file_name

    try:
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save video: {str(e)}",
        )

    # ----------------------------
    # Run Prediction
    # ----------------------------

    try:
        result = predictor.predict(str(video_path))

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}",
        )

    # ----------------------------
    # Save Result to Database
    # ----------------------------

    try:
        db_job = DetectionJob(
            video_id=str(uuid.uuid4()),
            video_name=video.filename,
            file_path=str(video_path),
            status="completed",
            is_fake=result["prediction"] == "FAKE",
            confidence=result["confidence"],
        )

        db.add(db_job)
        db.commit()
        db.refresh(db_job)

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Prediction completed, but database save failed: {str(e)}",
        )

    # ----------------------------
    # Response
    # ----------------------------

    return {
        "filename": video.filename,
        "prediction": result["prediction"],
        "confidence": result["confidence"],
        "spatial_score": result["spatial_score"],
        "temporal_score": result["temporal_score"],
        "final_score": result["final_score"],
        "frame_results": result.get("frame_results", []),
        "processing_info": result.get("processing_info", {}),
        "faces_detected": result.get("faces_detected"),
        "frames_extracted": result.get("frames_extracted"),
        "spatial_details": result.get("spatial_details", []),
    }