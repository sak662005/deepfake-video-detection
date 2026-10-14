from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split
from tqdm import tqdm


BACKEND_ROOT = Path(__file__).resolve().parents[3]
SAVED_MODELS_DIR = BACKEND_ROOT / "saved_models"


class TemporalTrainer:

    def __init__(
        self,
        model,
        dataset,
        device,
        batch_size=4,
        epochs=10,
        lr=1e-4,
    ):

        self.device = device
        self.model = model.to(device)

        train_size = int(0.8 * len(dataset))
        val_size = len(dataset) - train_size

        train_dataset, val_dataset = random_split(
            dataset,
            [train_size, val_size]
        )

        self.train_loader = DataLoader(
            train_dataset,
            batch_size=batch_size,
            shuffle=True
        )

        self.val_loader = DataLoader(
            val_dataset,
            batch_size=batch_size
        )

        self.criterion = nn.BCEWithLogitsLoss()

        self.optimizer = torch.optim.AdamW(
            self.model.parameters(),
            lr=lr,
            weight_decay=1e-4
        )
        self.scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            self.optimizer,
            mode="max",
            factor=0.5,
            patience=1,
            min_lr=1e-6
        )

        self.epochs = epochs

        self.best_accuracy = 0

        SAVED_MODELS_DIR.mkdir(exist_ok=True)

    def train(self):

        for epoch in range(self.epochs):

            train_loss = self.train_one_epoch()

            val_acc = self.validate()

            print(
                f"\nEpoch {epoch+1}/{self.epochs}"
                f"\nTrain Loss : {train_loss:.4f}"
                f"\nValidation Accuracy : {val_acc:.2f}%"
            )

            self.scheduler.step(val_acc)

            if val_acc > self.best_accuracy:

                self.best_accuracy = val_acc

                torch.save(
                    self.model.state_dict(),
                    SAVED_MODELS_DIR / "temporal_model.pth"
                )

                print("Best model saved.")

    def train_one_epoch(self):

        self.model.train()

        running_loss = 0

        for images, labels in tqdm(self.train_loader):

            images = images.to(self.device)

            labels = labels.unsqueeze(1).to(self.device)

            self.optimizer.zero_grad()

            outputs = self.model(images)

            loss = self.criterion(outputs, labels)

            loss.backward()

            self.optimizer.step()

            running_loss += loss.item()

        return running_loss / len(self.train_loader)

    def validate(self):

        self.model.eval()

        correct = 0

        total = 0

        with torch.no_grad():

            for images, labels in self.val_loader:

                images = images.to(self.device)

                labels = labels.unsqueeze(1).to(self.device)

                outputs = self.model(images)

                predictions = (
                    torch.sigmoid(outputs) > 0.5
                ).float()

                correct += (
                    predictions == labels
                ).sum().item()

                total += labels.size(0)

        return 100 * correct / total