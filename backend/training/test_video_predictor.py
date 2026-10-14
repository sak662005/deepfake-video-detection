import sys
from pathlib import Path

# Add backend directory to Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.services.inference.video_predictor import VideoPredictor


def main():

    predictor = VideoPredictor()

    video_path = "datasets/raw/fake/vs1.mp4"

    result = predictor.predict(video_path)

    print("\n========================================")
    print("DEEPFAKE DETECTION RESULT")
    print("========================================")
    print(f"Prediction      : {result['prediction']}")
    print(f"Confidence      : {result['confidence']}%")
    print(f"Spatial Score   : {result['spatial_score']}")
    print(f"Temporal Score  : {result['temporal_score']}")
    print(f"Final Score     : {result['final_score']}")
    print("========================================")


if __name__ == "__main__":
    main()
