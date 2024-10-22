import torch
from torchvision.transforms import transforms
import os
import numpy as np
from PIL import Image
import cv2
from retinaface import RetinaFace

from model import SimpleCNN

class ClassifyAtmos:
    def __init__(self, model, normal_model_weight_path, smile_model_weight_path):
        self.normal_model = model
        self.smile_model = model
        self.normal_model.load_state_dict(torch.load(normal_model_weight_path, map_location=torch.device('cpu'), weights_only=True))
        self.smile_model.load_state_dict(torch.load(smile_model_weight_path, map_location=torch.device('cpu'), weights_only=True))

        self.transform = transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])


    def img_preprocessing(self, img):
        # 画像がパスではなく、すでに顔領域として切り出されている場合もあるので、PIL Imageかどうかをチェック
        if isinstance(img, str):  # imgがパスの場合
            img = Image.open(img).convert('RGB')
        elif isinstance(img, np.ndarray):  # imgがnumpy.ndarrayの場合
            img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))  # numpy -> PIL に変換

        img = self.transform(img)  # 変換処理（リサイズ、テンソル化、正規化）
        return img


    def detect_face(self, img_path):
        img = cv2.imread(img_path)
        faces = RetinaFace.detect_faces(img_path, threshold=0.7)

        # 顔が存在する場合は、顔の座標を返す
        # ない場合はNoneを返す
        if faces:
            return True, faces
        else:
            return None, faces


    def classify_atmos_by_smile(self, img_path, faces):
        img = cv2.imread(img_path)

        smile_count = 0
        for key in faces:
            face = faces[key]
            x1, y1, x2, y2 = face["facial_area"]
            face_roi = img[y1:y2, x1:x2] # 顔領域を切り出し
            face_roi = self.img_preprocessing(face_roi)

            # 笑顔を検出できたら、smile_countを＋１
            self.smile_model.eval()
            with torch.no_grad():
                output = self.smile_model(face_roi).squeeze()
                predicted_label = (output > 0.5).float()

            if predicted_label == 1.0:
                smile_count += 1

        # 全顔のうち、６割以上がsmlieならpositive、６割未満ならnegativeを返す
        smlie_ratio = smile_count / len(faces)
        if smlie_ratio >= 0.6:
            classify_result = "positive"
        else:
            classify_result =  "negative"

        return classify_result, smlie_ratio


    def classify_atmos_by_model(self, img_path):
        img = self.img_preprocessing(img_path)

        self.normal_model.eval()
        with torch.no_grad():
            output = self.normal_model(img).squeeze()
            predicted_label = (output > 0.5).float()

        if predicted_label == 1.0:
            classify_result = "positive"
        else:
            classify_result = "negative" 

        return classify_result, output


    def run_classify(self, img_path):
        label_by_model, ratio_by_model = self.classify_atmos_by_model(img_path) # 機械学習モデルによる雰囲気分類の結果

        """
        顔が存在する場合は、雰囲気の分類は顔の表情と、雰囲気分類モデルの出力結果を使って算出（顔の表情の重みを大きくする）
        顔が存在しない場合は、雰囲気分類モデルの出力結果のみ
        """
        is_face, faces = self.detect_face(img_path)

        if is_face:
            label_by_smile, ratio_by_smlile = self.classify_atmos_by_smile(img_path, faces) # 笑顔検出による雰囲気分類の結果
            print(ratio_by_smlile)
            if (label_by_smile == "positive"):
                if ratio_by_model + ratio_by_smlile >= 1.5:
                    classify_result = "positive"
                else:
                    classify_result = "negative"
            else:
                if ratio_by_model + ratio_by_smlile >= 0.8:
                    classify_result = "positive"
                else:
                    classify_result = "negative"
        
        else:
            classify_result = label_by_model

        return classify_result, is_face


if __name__ == "__main__":
    model = SimpleCNN()
    normal_model_weight_path = r"model_weights\model_weight_reverse_labels"
    smile_model_weight_path = r"model_weights\smile_model_weight"

    classify_atmos = ClassifyAtmos(model=model, 
                                   normal_model_weight_path=normal_model_weight_path,
                                   smile_model_weight_path=smile_model_weight_path)

    print("==== negative ===")
    folder_path = "negative_test"
    negative_img_names = os.listdir(folder_path)
    for name in negative_img_names:
        img_path = os.path.join(folder_path, name)
        classify_result, is_face = classify_atmos.run_classify(img_path)
        print(f"{name}    分類結果：{classify_result}")
    print("finish\n")
    
    print("==== positive ===")
    folder_path = "positive_test"
    positive_img_names = os.listdir(folder_path)
    for name in positive_img_names:
        img_path = os.path.join(folder_path, name)
        classify_result, is_face = classify_atmos.run_classify(img_path)
        print(f"{name}    分類結果：{classify_result}")
    print("finish\n")