import torch
import timm
import cv2
import numpy as np

from torchvision import transforms
from PIL import Image


class SpatialPredictor:

    def __init__(self, model_path, device):

        self.device = device

        self.model = timm.create_model(
            "efficientnet_b0",
            pretrained=False,
            num_classes=1
        )

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

    def predict(self, image_path):

        image = cv2.imread(image_path)

        image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )

        image = Image.fromarray(image)

        image = self.transform(image)

        image = image.unsqueeze(0)

        image = image.to(self.device)

        with torch.no_grad():

            output = self.model(image)

            probability = torch.sigmoid(output).item()

        return probability