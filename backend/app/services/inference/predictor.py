from fastapi import APIRouter, UploadFile, File

router = APIRouter()

@router.post("/")
async def predict_video(video: UploadFile = File(...)):
    return {
        "filename": video.filename,
        "prediction": "REAL",
        "confidence": 99.9,
        "spatial_score": 0.62,
        "temporal_score": 0.24,
        "final_score": 0.47,
    }