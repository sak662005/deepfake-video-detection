from pathlib import Path

import timm
import torch
import torch.nn as nn
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms

# -----------------------
# Config
# -----------------------

DATASET_PATH = Path("datasets/faces")

IMAGE_SIZE = 224
BATCH_SIZE = 16

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# -----------------------
# Transform
# -----------------------

transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485,0.456,0.406],
        std=[0.229,0.224,0.225]
    )
])

# -----------------------
# Dataset
# -----------------------

class FaceDataset(Dataset):

    def __init__(self, root_dir, transform=None):

        self.transform = transform
        self.images = []

        fake_dir = Path(root_dir) / "fake"
        real_dir = Path(root_dir) / "real"

        for video in fake_dir.iterdir():
            if video.is_dir():
                for img in video.glob("*.jpg"):
                    self.images.append((img,1))

        for video in real_dir.iterdir():
            if video.is_dir():
                for img in video.glob("*.jpg"):
                    self.images.append((img,0))

        print(f"Total Images : {len(self.images)}")

    def __len__(self):
        return len(self.images)

    def __getitem__(self,index):

        path,label=self.images[index]

        image=Image.open(path).convert("RGB")

        if self.transform:
            image=self.transform(image)

        return image, torch.tensor(label,dtype=torch.float32)

# -----------------------
# Loader
# -----------------------

dataset = FaceDataset(DATASET_PATH, transform)

loader = DataLoader(
    dataset,
    batch_size=BATCH_SIZE,
    shuffle=True
)



from torch.utils.data import random_split
import torch.optim as optim

# -----------------------------
# Train / Validation Split
# -----------------------------

train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size

train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE)

# -----------------------------
# Model
# -----------------------------

model = timm.create_model(
    "efficientnet_b0",
    pretrained=True,
    num_classes=1
)

model = model.to(DEVICE)

criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr=0.0001)

EPOCHS = 10

best_acc = 0

for epoch in range(EPOCHS):

    model.train()

    running_loss = 0
    correct = 0
    total = 0

    for images, labels in train_loader:

        images = images.to(DEVICE)
        labels = labels.to(DEVICE).unsqueeze(1)

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(outputs, labels)

        loss.backward()

        optimizer.step()

        running_loss += loss.item()

        predictions = (torch.sigmoid(outputs) > 0.5).float()

        correct += (predictions == labels).sum().item()

        total += labels.size(0)

    train_acc = 100 * correct / total

    # ---------------- Validation ----------------

    model.eval()

    correct = 0
    total = 0

    with torch.no_grad():

        for images, labels in val_loader:

            images = images.to(DEVICE)
            labels = labels.to(DEVICE).unsqueeze(1)

            outputs = model(images)

            predictions = (torch.sigmoid(outputs) > 0.5).float()

            correct += (predictions == labels).sum().item()

            total += labels.size(0)

    val_acc = 100 * correct / total

    print(
        f"Epoch {epoch+1}/{EPOCHS} | "
        f"Loss={running_loss:.4f} | "
        f"Train={train_acc:.2f}% | "
        f"Val={val_acc:.2f}%"
    )

    if val_acc > best_acc:

        best_acc = val_acc

        torch.save(
            model.state_dict(),
            "saved_models/spatial_model.pth"
        )

print("\nTraining Finished")
print(f"Best Validation Accuracy : {best_acc:.2f}%")






# -----------------------
# Model
# -----------------------

model = timm.create_model(
    "efficientnet_b0",
    pretrained=True,
    num_classes=1
)

model = model.to(DEVICE)

print(model)

print("\nModel Loaded Successfully")

sample_images, sample_labels = next(iter(loader))

sample_images = sample_images.to(DEVICE)

output = model(sample_images)

print("Output Shape :", output.shape)