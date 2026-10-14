import torch
from torchvision import transforms
from PIL import Image

from app.ml_models.temporal.model import TemporalModel


class TemporalPredictor:

    def __init__(self, model_path, device):

        self.device = device

        self.model = TemporalModel()

        self.model.load_state_dict(
            torch.load(
                model_path,
                map_location=device
            )
        )

        self.model.eval()
        self.model.to(device)

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    def predict(self, image_paths):

        frames = []

        for image_path in image_paths:

            image = Image.open(image_path).convert("RGB")
            image = self.transform(image)
            frames.append(image)

        frames = torch.stack(frames)
        frames = frames.unsqueeze(0)
        frames = frames.to(self.device)

        with torch.no_grad():

            output = self.model(frames)
            probability = torch.sigmoid(output).item()

        return probability