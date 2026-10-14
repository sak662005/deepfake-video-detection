import torch
from pathlib import Path

from app.services.preprocessing.frame_extractor import FrameExtractor
from app.services.preprocessing.face_detector import FaceDetector

from app.services.inference.spatial_predictor import SpatialPredictor
from app.services.inference.temporal_predictor import TemporalPredictor


class VideoPredictor:

    def __init__(self):

        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        self.frame_extractor = FrameExtractor()
        self.face_detector = FaceDetector()

        self.spatial_predictor = SpatialPredictor(
            "saved_models/spatial_model.pth",
            self.device
        )

        self.temporal_predictor = TemporalPredictor(
            "saved_models/temporal_model.pth",
            self.device
        )

    def predict(self, video_path: str):

        print("\n========== STARTING PREDICTION ==========\n")

        # -----------------------------
        # Step 1 - Extract Frames
        # -----------------------------
        frame_paths = self.frame_extractor.extract_frames(video_path)

        if len(frame_paths) == 0:
            raise Exception("No frames extracted.")

        print(f"Frames Extracted : {len(frame_paths)}")

        # -----------------------------
        # Step 2 - Extract Faces
        # -----------------------------
        face_paths = self.face_detector.extract_faces(frame_paths)

        if len(face_paths) == 0:
            raise Exception("No faces detected.")

        print(f"Faces Extracted : {len(face_paths)}")

        # -----------------------------
        # Step 3 - Spatial Prediction
        # -----------------------------
        spatial_results = []
        frame_score_map = {}

        for face in face_paths:
            score = self.spatial_predictor.predict(face)
            spatial_results.append({
                "face": len(spatial_results) + 1,
                "score": round(score, 4),
                "prediction": "FAKE" if score >= 0.5 else "REAL"
            })

            face_name = Path(face).stem
            frame_label = face_name.split("_face")[0]
            frame_index = int(frame_label.rsplit("_", 1)[-1]) if frame_label.rsplit("_", 1)[-1].isdigit() else 0
            frame_score_map.setdefault(frame_index, []).append(score)

        spatial_score = sum(item["score"] for item in spatial_results) / len(spatial_results) if spatial_results else 0.0

        print(f"Spatial Score : {spatial_score:.4f}")

        # -----------------------------
        # Step 4 - Temporal Prediction
        # -----------------------------
        sequence = face_paths[:10]

        if len(sequence) < 10:
            sequence.extend([sequence[-1]] * (10 - len(sequence)))

        temporal_score = self.temporal_predictor.predict(sequence)

        print(f"Temporal Score : {temporal_score:.4f}")

        # -----------------------------
        # Step 5 - Weighted Fusion
        # -----------------------------
        final_score = (
            0.6 * spatial_score +
            0.4 * temporal_score
        )

        print(f"Final Score : {final_score:.4f}")

        prediction = "FAKE" if final_score >= 0.5 else "REAL"

        confidence = (
            final_score if prediction == "FAKE"
            else (1 - final_score)
        )

        frame_results = []
        for index, frame_path in enumerate(frame_paths, start=1):
            frame_index = int(Path(frame_path).stem.rsplit("_", 1)[-1]) if Path(frame_path).stem.rsplit("_", 1)[-1].isdigit() else index
            scores = frame_score_map.get(frame_index, [])
            frame_score = sum(scores) / len(scores) if scores else 0.5
            frame_results.append({
                "frame": index,
                "score": round(frame_score, 4),
                "prediction": "FAKE" if frame_score >= 0.5 else "REAL"
            })

        return {
            "prediction": prediction,
            "confidence": round(confidence * 100, 2),
            "spatial_score": round(spatial_score, 4),
            "temporal_score": round(temporal_score, 4),
            "final_score": round(final_score, 4),
            "frame_results": frame_results,
            "processing_info": {
                "frames_extracted": len(frame_paths),
                "faces_detected": len(face_paths),
                "status": "completed"
            },
            "faces_detected": len(face_paths),
            "frames_extracted": len(frame_paths),
            "spatial_details": spatial_results,
        }