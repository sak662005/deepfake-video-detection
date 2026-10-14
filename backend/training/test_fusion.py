import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import torch
from app.ml_models.fusion.model import FusionModel

model = FusionModel()

spatial = torch.randn(4, 1)
temporal = torch.randn(4, 1)

output = model(spatial, temporal)

print(output.shape)