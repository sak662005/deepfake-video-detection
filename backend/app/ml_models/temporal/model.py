import torch
import torch.nn as nn
import timm


class TemporalModel(nn.Module):

    def __init__(self):

        super().__init__()

        # CNN Backbone (EfficientNet-B0)
        self.cnn = timm.create_model(
            "efficientnet_b0",
            pretrained=True,
            num_classes=0
        )

        feature_size = self.cnn.num_features

        # LSTM
        self.lstm = nn.LSTM(
            input_size=feature_size,
            hidden_size=256,
            num_layers=2,
            batch_first=True,
            dropout=0.3
        )

        # Final Classifier
        self.classifier = nn.Sequential(
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 1)
        )

    def forward(self, x):
        """
        x shape:
        (batch_size, sequence_length, 3, 224, 224)
        """

        batch_size, seq_len, c, h, w = x.size()

        # Merge batch and sequence dimensions
        x = x.view(batch_size * seq_len, c, h, w)

        # Extract spatial features
        features = self.cnn(x)

        # Restore sequence dimension
        features = features.view(batch_size, seq_len, -1)

        # LSTM
        lstm_out, _ = self.lstm(features)

        # Last frame output
        last_output = lstm_out[:, -1, :]

        # Classification
        output = self.classifier(last_output)

        return output