import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision.transforms import transforms
import os
from PIL import Image
from .model import SimpleCNN

class ClassifyAtmos:
    def __init__(self, model, model_weight_path):
        self.model = model
        self.model.load_state_dict(torch.load(model_weight_path, map_location=torch.device('cpu'), weights_only=True))

        self.transform = transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])

    def img_preprocessing(self, img_path):
        img = Image.open(img_path).convert('RGB')
        img = self.transform(img)

        return img

    def classify_atmos(self, img_path):
        img = self.img_preprocessing(img_path)

        self.model.eval()
        with torch.no_grad():
            output = self.model(img).squeeze()
            predicted_label = (output > 0.5).float()
        
        if predicted_label == 1.0:
            return predicted_label, "ネガティブ"
        
        else:
            return predicted_label, "ポジティブ" 



if __name__ == "__main__":
    model = SimpleCNN()
    model_weight_path = "model_weight_ver2"

    classify_atmos = ClassifyAtmos(model=model, model_weight_path=model_weight_path)

    print("==== negative ===")
    folder_path = "negative_test"
    negative_img_names = os.listdir(folder_path)
    for name in negative_img_names:
        img_path = os.path.join(folder_path, name)
        predicted_label, classify_result = classify_atmos.classify_atmos(img_path)
        print(f"{name}   分類結果：{classify_result}")
    print("finish\n")
    
    print("==== positive ===")
    folder_path = "positive_test"
    positive_img_names = os.listdir(folder_path)
    for name in positive_img_names:
        img_path = os.path.join(folder_path, name)
        predicted_label, classify_result = classify_atmos.classify_atmos(img_path)
        print(f"{name}   分類結果：{classify_result}")
    print("finish\n")




