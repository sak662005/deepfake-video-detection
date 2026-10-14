import torch
import torch.nn as nn


class FusionModel(nn.Module):
    def __init__(self):
        super().__init__()

        self.classifier = nn.Sequential(
            nn.Linear(2, 32),
            nn.ReLU(),
            nn.Dropout(0.3),

            nn.Linear(32, 16),
            nn.ReLU(),

            nn.Linear(16, 1)
        )

    def forward(self, spatial_score, temporal_score):

        x = torch.cat(
            [spatial_score, temporal_score],
            dim=1
        )

        return self.classifier(x)