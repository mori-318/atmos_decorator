import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision.transforms import transforms

class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()

        # 畳み込み層1
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1)

        # プーリング層
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

        # 畳み込み層2
        self.conv3 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=1, padding=1)
        self.conv4 = nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, stride=1, padding=1)

        # 全結合層
        self.fc1 = nn.Linear(256 * 8 * 8, 512)
        self.fc2 = nn.Linear(512, 128)
        self.fc3 = nn.Linear(128, 1)

        # ドロップアウト層
        self.dropout = nn.Dropout(0.5)
        
    def forward(self, x):
        # 畳み込み -> ReLU -> プーリングの繰り返し
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))

        x = self.pool(F.relu(self.conv3(x)))
        x = self.pool(F.relu(self.conv4(x)))

        # 特徴マップをフラットにする
        x = x.view(-1, 256 * 8 * 8)

        # 全結合層に通す
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        x = self.dropout(x)

        # 出力は1つ
        x = torch.sigmoid(self.fc3(x)) # 出力確立を0～1の範囲での確率に

        return x