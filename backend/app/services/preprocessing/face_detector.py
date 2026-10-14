from pathlib import Path

import cv2
from tqdm import tqdm


class FaceDetector:

    def __init__(self):

        self.frames_root = Path("datasets/frames")
        self.faces_root = Path("datasets/faces")

        self.faces_root.mkdir(parents=True, exist_ok=True)

        self.face_detector = cv2.CascadeClassifier(
            cv2.data.haarcascades +
            "haarcascade_frontalface_default.xml"
        )

    # =====================================================
    # Dataset Processing
    # =====================================================

    def process_label(self, label):

        input_root = self.frames_root / label
        output_root = self.faces_root / label

        output_root.mkdir(parents=True, exist_ok=True)

        video_folders = sorted(input_root.iterdir())

        for video_folder in tqdm(video_folders, desc=label):

            save_folder = output_root / video_folder.name
            save_folder.mkdir(parents=True, exist_ok=True)

            frame_files = sorted(video_folder.glob("*.jpg"))

            for frame_path in frame_files:

                image = cv2.imread(str(frame_path))

                if image is None:
                    continue

                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                faces = self.face_detector.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(60, 60)
                )

                if len(faces) == 0:
                    continue

                x, y, w, h = max(
                    faces,
                    key=lambda f: f[2] * f[3]
                )

                face = image[y:y+h, x:x+w]
                face = cv2.resize(face, (224, 224))

                save_path = save_folder / frame_path.name

                cv2.imwrite(str(save_path), face)

    # =====================================================
    # Single Video Prediction
    # =====================================================

    def extract_faces(self, frame_paths):

        output_dir = Path("uploads/faces")
        output_dir.mkdir(parents=True, exist_ok=True)

        face_paths = []

        for frame_path in frame_paths:

            image = cv2.imread(frame_path)

            if image is None:
                continue

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            faces = self.face_detector.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(60, 60)
            )

            if len(faces) == 0:
                continue

            for index, (x, y, w, h) in enumerate(faces):
                face = image[y:y+h, x:x+w]
                face = cv2.resize(face, (224, 224))

                frame_stem = Path(frame_path).stem
                save_path = output_dir / f"{frame_stem}_face{index}.jpg"

                cv2.imwrite(str(save_path), face)

                face_paths.append(str(save_path))

        return face_paths

    # =====================================================
    # Dataset
    # =====================================================

    def run(self):

        print("\nExtracting REAL faces...\n")
        self.process_label("real")

        print("\nExtracting FAKE faces...\n")
        self.process_label("fake")

        print("\nFace Extraction Completed Successfully!")


if __name__ == "__main__":

    detector = FaceDetector()
    detector.run()