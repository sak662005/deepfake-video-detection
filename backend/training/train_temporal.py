import sys
from pathlib import Path

# Add backend root to Python path
BACKEND_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(BACKEND_ROOT))

import torch

from app.ml_models.temporal.dataset import TemporalDataset
from app.ml_models.temporal.model import TemporalModel
from app.ml_models.temporal.trainer import TemporalTrainer

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
DATASET_DIR = BACKEND_ROOT / "datasets" / "faces"
SAVED_MODELS_DIR = BACKEND_ROOT / "saved_models"

SAVED_MODELS_DIR.mkdir(exist_ok=True)

print(f"Device : {DEVICE}")

# -----------------------
# Dataset
# -----------------------

dataset = TemporalDataset(
    root_dir=str(DATASET_DIR),
    sequence_length=10
)

print(f"Total Videos : {len(dataset)}")

# -----------------------
# Model
# -----------------------

model = TemporalModel()

# -----------------------
# Trainer
# -----------------------

trainer = TemporalTrainer(
    model=model,
    dataset=dataset,
    device=DEVICE,
    batch_size=4,
    epochs=15,
    lr=5e-5
)

trainer.train()

print("\nTraining Finished Successfully!")