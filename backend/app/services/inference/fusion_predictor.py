import torch

from app.ml_models.fusion.model import FusionModel


class FusionPredictor:

    def __init__(self, device):

        self.device = device

        self.model = FusionModel()

        self.model.eval()
        self.model.to(device)

    def predict(self, spatial_score, temporal_score):

        spatial_score = torch.tensor(
            [[spatial_score]],
            dtype=torch.float32,
            device=self.device
        )

        temporal_score = torch.tensor(
            [[temporal_score]],
            dtype=torch.float32,
            device=self.device
        )

        with torch.no_grad():

            output = self.model(
                spatial_score,
                temporal_score
            )

            probability = torch.sigmoid(output).item()

        return probability