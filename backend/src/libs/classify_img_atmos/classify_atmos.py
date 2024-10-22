import torch
from torchvision.transforms import transforms
import os
import numpy as np
from PIL import Image
import cv2
from retinaface import RetinaFace
from .model import SimpleCNN

class ClassifyAtmos:
    def __init__(self, normal_weight_path, smile_weight_path):
        # モデルのインスタンスをそれぞれ作成
        self.normal_model = SimpleCNN()
        self.smile_model = SimpleCNN()

        # 重みの読み込み
        self._load_model_weights(normal_weight_path, smile_weight_path)

        # 画像変換の設定
        self.transform = transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])

    def _load_model_weights(self, normal_weight, smile_weight):
        self.normal_model.load_state_dict(torch.load(normal_weight, map_location='cpu'), strict=False)
        self.smile_model.load_state_dict(torch.load(smile_weight, map_location='cpu'), strict=False)

    def img_preprocessing(self, img):
        if isinstance(img, str):
            img = Image.open(img).convert('RGB')
        elif isinstance(img, np.ndarray):
            img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        return self.transform(img)

    def detect_face(self, img_path):
        faces = RetinaFace.detect_faces(img_path, threshold=0.7)
        if faces:
            return True, faces
        else:
            return False, None

    def classify_face_smiles(self, img, faces):
        smile_count = 0
        for face in faces.values():
            x1, y1, x2, y2 = face["facial_area"]
            face_roi = img[y1:y2, x1:x2]
            face_roi = self.img_preprocessing(face_roi)

            with torch.no_grad():
                output = self.smile_model(face_roi).squeeze()
                predicted_label = (output > 0.5).float()

            if predicted_label == 1.0:
                smile_count += 1

        smile_ratio = smile_count / len(faces)
        if smile_ratio >= 0.6:
            return "positive", smile_ratio
        else:
            return "negative", smile_ratio

    def classify_by_model(self, img):
        img = self.img_preprocessing(img)
        with torch.no_grad():
            output = self.normal_model(img).squeeze()
            predicted_label = (output > 0.5).float()

        if predicted_label == 1.0:
            return "positive", output
        else:
            return "negative", output

    def run_classify(self, img):
        # モデルによる雰囲気分類
        label_by_model, ratio_by_model = self.classify_by_model(img)

        # 顔検出の結果を確認
        is_face, faces = self.detect_face(img)

        # 顔が検出された場合
        if is_face:
            label_by_smile, ratio_by_smile = self.classify_face_smiles(img, faces)

            # 笑顔が多い場合
            if label_by_smile == "positive":
                if ratio_by_model + ratio_by_smile >= 1.5:
                    classify_result = "positive"
                else:
                    classify_result = "negative"

            # 笑顔が少ない場合
            else:
                if ratio_by_model + ratio_by_smile >= 0.8:
                    classify_result = "positive"
                else:
                    classify_result = "negative"

        # 顔が検出されなかった場合
        else:
            classify_result = label_by_model

        return classify_result, is_face