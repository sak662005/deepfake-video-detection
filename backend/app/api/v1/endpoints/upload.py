from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/", summary="Upload a video for analysis")
async def upload_video(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file selected")

    if not file.filename.lower().endswith((".mp4", ".avi", ".mov", ".mkv")):
        raise HTTPException(status_code=400, detail="Unsupported video format")

    video_id = str(uuid4())

    extension = Path(file.filename).suffix
    save_path = UPLOAD_DIR / f"{video_id}{extension}"

    with open(save_path, "wb") as buffer:
        buffer.write(await file.read())

    return {
        "message": "Video uploaded successfully",
        "video_id": video_id,
        "filename": file.filename,
        "file_path": str(save_path)
    }