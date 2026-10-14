import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.services.inference.predictor import DeepfakePredictor

predictor = DeepfakePredictor()