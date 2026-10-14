import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import torch

from app.services.inference.fusion_predictor import FusionPredictor


DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

predictor = FusionPredictor(
    device=DEVICE
)

spatial_score = 1.0000
temporal_score = 0.9272

score = predictor.predict(
    spatial_score,
    temporal_score
)

print(f"Fusion Score : {score:.4f}")

if score >= 0.5:
    print("Prediction : FAKE")
else:
    print("Prediction : REAL")