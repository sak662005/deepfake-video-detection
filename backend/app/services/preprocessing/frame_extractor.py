import logging
from pathlib import Path

import cv2
from tqdm import tqdm

logger = logging.getLogger(__name__)


class FrameExtractor:
    """
    Extract frames from videos.

    Folder structure:

    datasets/
        raw/
            real/
            fake/

        frames/
            real/
            fake/
    """

    def __init__(
        self,
        raw_dataset_path: str = "datasets/raw",
        output_path: str = "datasets/frames",
        frame_interval: int = 5,
    ):

        self.raw_dataset_path = Path(raw_dataset_path)
        self.output_path = Path(output_path)
        self.frame_interval = frame_interval

        self.real_input = self.raw_dataset_path / "real"
        self.fake_input = self.raw_dataset_path / "fake"

        self.real_output = self.output_path / "real"
        self.fake_output = self.output_path / "fake"

        self.real_output.mkdir(parents=True, exist_ok=True)
        self.fake_output.mkdir(parents=True, exist_ok=True)

    # ====================================================
    # Dataset Preprocessing
    # ====================================================

    def extract_video(self, video_path: Path, save_root: Path):

        video_name = video_path.stem

        save_dir = save_root / video_name
        save_dir.mkdir(parents=True, exist_ok=True)

        cap = cv2.VideoCapture(str(video_path))

        if not cap.isOpened():
            logger.error(f"Cannot open {video_path}")
            return

        frame_count = 0
        saved_count = 0

        while True:

            success, frame = cap.read()

            if not success:
                break

            if frame_count % self.frame_interval == 0:

                filename = save_dir / f"frame_{saved_count:04d}.jpg"

                cv2.imwrite(str(filename), frame)

                saved_count += 1

            frame_count += 1

        cap.release()

        logger.info(
            f"{video_name} -> {saved_count} frames extracted"
        )

    # ====================================================
    # Inference (Single Video)
    # ====================================================

    def extract_frames(self, video_path: str):

        video_path = Path(video_path)

        save_dir = Path("uploads/frames") / video_path.stem
        save_dir.mkdir(parents=True, exist_ok=True)

        cap = cv2.VideoCapture(str(video_path))

        if not cap.isOpened():
            raise Exception(f"Cannot open {video_path}")

        frame_paths = []

        frame_count = 0
        saved_count = 0

        while True:

            success, frame = cap.read()

            if not success:
                break

            if frame_count % self.frame_interval == 0:

                filename = save_dir / f"frame_{saved_count:04d}.jpg"

                cv2.imwrite(str(filename), frame)

                frame_paths.append(str(filename))

                saved_count += 1

            frame_count += 1

        cap.release()

        return frame_paths

    # ====================================================
    # Dataset Processing
    # ====================================================

    def process_directory(self, input_dir: Path, output_dir: Path):

        videos = []

        for ext in ("*.mp4", "*.avi", "*.mov", "*.mkv"):
            videos.extend(input_dir.glob(ext))

        logger.info(f"Found {len(videos)} videos in {input_dir}")

        for video in tqdm(videos):

            self.extract_video(video, output_dir)

    def run(self):

        logger.info("Starting Frame Extraction")

        self.process_directory(
            self.real_input,
            self.real_output,
        )

        self.process_directory(
            self.fake_input,
            self.fake_output,
        )

        logger.info("Frame Extraction Completed")


if __name__ == "__main__":

    extractor = FrameExtractor()

    extractor.run()