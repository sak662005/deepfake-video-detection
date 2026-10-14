import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

from app.ml_models.fusion.model import FusionModel


# ---------------------------------------------------
# Dummy Dataset (Temporary)
# ---------------------------------------------------

class FusionDataset(Dataset):

    def __init__(self):

        self.spatial_scores = torch.rand(1000, 1)
        self.temporal_scores = torch.rand(1000, 1)

        self.labels = (
            (self.spatial_scores + self.temporal_scores) > 1
        ).float()

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):

        return (
            self.spatial_scores[idx],
            self.temporal_scores[idx],
            self.labels[idx]
        )


# ---------------------------------------------------
# Device
# ---------------------------------------------------

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print(f"Device : {DEVICE}")


# ---------------------------------------------------
# Dataset
# ---------------------------------------------------

dataset = FusionDataset()

loader = DataLoader(
    dataset,
    batch_size=32,
    shuffle=True
)


# ---------------------------------------------------
# Model
# ---------------------------------------------------

model = FusionModel().to(DEVICE)

criterion = nn.BCEWithLogitsLoss()

optimizer = optim.Adam(
    model.parameters(),
    lr=0.001
)

EPOCHS = 20


# ---------------------------------------------------
# Training
# ---------------------------------------------------

for epoch in range(EPOCHS):

    model.train()

    running_loss = 0

    correct = 0

    total = 0

    for spatial, temporal, labels in loader:

        spatial = spatial.to(DEVICE)

        temporal = temporal.to(DEVICE)

        labels = labels.to(DEVICE)

        optimizer.zero_grad()

        outputs = model(
            spatial,
            temporal
        )

        loss = criterion(
            outputs,
            labels
        )

        loss.backward()

        optimizer.step()

        running_loss += loss.item()

        predictions = (
            torch.sigmoid(outputs) > 0.5
        ).float()

        correct += (
            predictions == labels
        ).sum().item()

        total += labels.size(0)

    accuracy = 100 * correct / total

    print(
        f"Epoch {epoch+1}/{EPOCHS} "
        f"Loss={running_loss:.4f} "
        f"Accuracy={accuracy:.2f}%"
    )


# ---------------------------------------------------
# Save Model
# ---------------------------------------------------

torch.save(
    model.state_dict(),
    "saved_models/fusion_model.pth"
)

print("\nFusion Model Saved Successfully!")