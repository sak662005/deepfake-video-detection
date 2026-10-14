import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import torch
from app.services.inference.temporal_predictor import TemporalPredictor


DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

predictor = TemporalPredictor(
    model_path="saved_models/temporal_model.pth",
    device=DEVICE
)

image_paths = [
    "datasets/faces/fake/vs1/frame_0000.jpg",
    "datasets/faces/fake/vs1/frame_0001.jpg",
    "datasets/faces/fake/vs1/frame_0002.jpg",
    "datasets/faces/fake/vs1/frame_0003.jpg",
    "datasets/faces/fake/vs1/frame_0004.jpg",
    "datasets/faces/fake/vs1/frame_0005.jpg",
    "datasets/faces/fake/vs1/frame_0006.jpg",
    "datasets/faces/fake/vs1/frame_0007.jpg",
    "datasets/faces/fake/vs1/frame_0008.jpg",
    "datasets/faces/fake/vs1/frame_0009.jpg"
]

score = predictor.predict(image_paths)

print(f"Prediction Score : {score:.4f}")

if score >= 0.5:
    print("Prediction : FAKE")
else:
    print("Prediction : REAL")