import sys
from pathlib import Path

# Add backend folder to Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import torch
from app.ml_models.temporal.model import TemporalModel

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = TemporalModel().to(DEVICE)

dummy = torch.randn(4, 10, 3, 224, 224).to(DEVICE)

output = model(dummy)

print("Output Shape:", output.shape)