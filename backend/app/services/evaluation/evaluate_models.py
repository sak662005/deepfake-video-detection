import json
from pathlib import Path

import torch
import timm
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix

from app.services.inference.spatial_predictor import SpatialPredictor
from app.services.inference.temporal_predictor import TemporalPredictor


ROOT = Path(__file__).resolve().parents[2]
DATASET_ROOT = ROOT / "datasets"
OUTPUT_PATH = ROOT / "outputs" / "performance_metrics.json"
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)


def _load_image_paths(label_dir: Path):
    paths = []
    for image_path in sorted(label_dir.glob("*.jpg")):
        paths.append(image_path)
    return paths


def evaluate_models():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    real_dir = DATASET_ROOT / "faces" / "real"
    fake_dir = DATASET_ROOT / "faces" / "fake"

    real_paths = _load_image_paths(real_dir)
    fake_paths = _load_image_paths(fake_dir)

    if not real_paths or not fake_paths:
        return {
            "evaluated": False,
            "message": "No labelled dataset images found",
            "metrics": {},
            "comparison": {},
        }

    sample_paths = real_paths[: min(20, len(real_paths))] + fake_paths[: min(20, len(fake_paths))]
    labels = [0] * len(real_paths[: min(20, len(real_paths))]) + [1] * len(fake_paths[: min(20, len(fake_paths))])

    spatial_predictor = SpatialPredictor(str(ROOT / "saved_models" / "spatial_model.pth"), device)
    temporal_predictor = TemporalPredictor(str(ROOT / "saved_models" / "temporal_model.pth"), device)

    spatial_scores = []
    temporal_scores = []

    for image_path in sample_paths:
        spatial_scores.append(spatial_predictor.predict(str(image_path)))

    for image_path in sample_paths:
        temporal_scores.append(temporal_predictor.predict([str(image_path)]))

    spatial_preds = [1 if score >= 0.5 else 0 for score in spatial_scores]
    temporal_preds = [1 if score >= 0.5 else 0 for score in temporal_scores]
    fusion_preds = [1 if (0.6 * s + 0.4 * t) >= 0.5 else 0 for s, t in zip(spatial_scores, temporal_scores)]

    def compute_metrics(preds, scores):
        return {
            "accuracy": round(accuracy_score(labels, preds), 4),
            "precision": round(precision_score(labels, preds, zero_division=0), 4),
            "recall": round(recall_score(labels, preds, zero_division=0), 4),
            "f1_score": round(f1_score(labels, preds, zero_division=0), 4),
            "roc_auc": round(roc_auc_score(labels, scores), 4),
            "confusion_matrix": confusion_matrix(labels, preds).tolist(),
        }

    metrics = {
        "spatial": compute_metrics(spatial_preds, spatial_scores),
        "temporal": compute_metrics(temporal_preds, temporal_scores),
        "fusion": compute_metrics(fusion_preds, [(0.6 * s + 0.4 * t) for s, t in zip(spatial_scores, temporal_scores)]),
    }

    payload = {
        "evaluated": True,
        "message": "Evaluation completed",
        "metrics": metrics,
        "comparison": {
            "spatial": {"name": "Spatial CNN"},
            "temporal": {"name": "Temporal CNN + LSTM"},
            "fusion": {"name": "CNN + LSTM Fusion"},
        },
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)

    return payload


if __name__ == "__main__":
    print(evaluate_models())
