from pathlib import Path
import cv2
import torch
from torch.utils.data import Dataset
from torchvision import transforms


class TemporalDataset(Dataset):
    def __init__(
        self,
        root_dir,
        sequence_length=10,
        transform=None
    ):
        self.root_dir = Path(root_dir)
        self.sequence_length = sequence_length

        self.transform = transform or transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                [0.485, 0.456, 0.406],
                [0.229, 0.224, 0.225]
            )
        ])

        self.samples = []

        for label_name, label in [("real", 0), ("fake", 1)]:

            label_path = self.root_dir / label_name

            if not label_path.exists():
                continue

            for video_folder in sorted(label_path.iterdir()):

                if not video_folder.is_dir():
                    continue

                frames = sorted(video_folder.glob("*.jpg"))

                if len(frames) >= sequence_length:
                    self.samples.append(
                        (
                            frames[:sequence_length],
                            label
                        )
                    )

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):

        frame_paths, label = self.samples[idx]

        sequence = []

        for frame_path in frame_paths:

            image = cv2.imread(str(frame_path))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            image = self.transform(image)

            sequence.append(image)

        sequence = torch.stack(sequence)

        return sequence, torch.tensor(label).float()