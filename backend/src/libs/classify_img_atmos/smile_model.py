import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision.transforms import transforms

class SmileCNN(nn.Module):
    def __init__(self):
            super(SmileCNN, self).__init__()

            # 畳み込み層1 + バッチノーマライゼーション
            self.conv1 = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, stride=1, padding=1)
            self.bn1 = nn.BatchNorm2d(32)
            self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1)
            self.bn2 = nn.BatchNorm2d(64)

            # プーリング層
            self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

            # 畳み込み層2 + バッチノーマライゼーション
            self.conv3 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=1, padding=1)
            self.bn3 = nn.BatchNorm2d(128)
            self.conv4 = nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, stride=1, padding=1)
            self.bn4 = nn.BatchNorm2d(256)

            # 全結合層 + バッチノーマライゼーション
            self.fc1 = nn.Linear(256 * 8 * 8, 512)
            self.bn5 = nn.BatchNorm1d(512)
            self.fc2 = nn.Linear(512, 128)
            self.bn6 = nn.BatchNorm1d(128)
            self.fc3 = nn.Linear(128, 1)

            # ドロップアウト層
            self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        # 畳み込み -> バッチノーマライゼーション -> ReLU -> プーリング
        x = self.pool(F.relu(self.bn1(self.conv1(x))))
        x = self.pool(F.relu(self.bn2(self.conv2(x))))

        x = self.pool(F.relu(self.bn3(self.conv3(x))))
        x = self.pool(F.relu(self.bn4(self.conv4(x))))

        # 特徴マップをフラットにする
        x = x.view(-1, 256 * 8 * 8)

        # 全結合層にバッチノーマライゼーションを追加
        x = F.relu(self.bn5(self.fc1(x)))
        x = self.dropout(x)
        x = F.relu(self.bn6(self.fc2(x)))
        x = self.dropout(x)

        x = torch.sigmoid(self.fc3(x))

        return x