import sys
from pathlib import Path

# Add backend folder to Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import torch
from app.services.inference.spatial_predictor import SpatialPredictor


def main():

    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    predictor = SpatialPredictor(
        model_path="saved_models/spatial_model.pth",
        device=device
    )

    image_path = "datasets/faces/fake/vs1/frame_0000.jpg"

    probability = predictor.predict(image_path)

    print("\n==============================")
    print("Spatial Prediction Result")
    print("==============================")
    print(f"Image       : {image_path}")
    print(f"Probability : {probability:.4f}")

    if probability >= 0.5:
        print("Prediction  : FAKE")
    else:
        print("Prediction  : REAL")


if __name__ == "__main__":
    main()