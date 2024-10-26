import cv2
import numpy as np
import random
from retinaface import RetinaFace

class AtmosDecorator:
    def __init__(self, img, applied_filters):
        self.img = img
        self.applied_filters = applied_filters


    def get_face_position(self):
        faces = RetinaFace.detect_faces(self.img, threshold=0.7)
        return faces


    def mosaic_filter(self, img, scale): # scal : 画像をscale倍に縮小する
        img_h, img_w = img.shape[:2]
        small_img = cv2.resize(img, dsize=None, fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)
        result_img = cv2.resize(small_img, dsize=(img_w, img_h), interpolation=cv2.INTER_NEAREST)
        return result_img


    def face_mosaic(self, img, scale=0.05):
        faces = self.get_face_position()

        # 写真に写っている全顔に対してモザイク処理を行う
        for face in faces.values():
            x1, y1, x2, y2 = face["facial_area"]
            face_img = img[y1:y2, x1:x2]
            result_face_img = self.mosaic_filter(face_img, scale)
            img[y1:y2, x1:x2] = result_face_img

        return img

    def eye_mosaic(self, img):
        faces = self.get_face_position()

        # 写真に写っている全顔の目元部分を黒で塗りつぶす
        for face in faces.values():
            try:
                landmarks = face['landmarks']
                left_eye = landmarks['left_eye']
                right_eye = landmarks['right_eye']

                # 目元部分を覆う矩形の座標を決定
                top_x = int(min(left_eye[0], right_eye[0]))
                bottom_x = int(max(left_eye[0], right_eye[0]))
                top_y = int(min(left_eye[1], right_eye[1]))
                bottom_y = int(max(left_eye[1], right_eye[1]))
                width = bottom_x - top_x

                # 矩形を描画して目元を黒で塗りつぶす
                cv2.rectangle(img, (int(top_x-width/2.2), int(top_y-width/5)), (int(bottom_x+width/2.2), int(bottom_y+width/5)), (0,0,0), thickness=-1)

            except Exception as e:
                print(f"目元部分を取得できませんでした: {e}")

        return img

    def create_horror_noise(self, img):
        # 顔がある場合はモザイク処理をかける
        faces = self.get_face_position()
        if faces:
            img = self.eye_mosaic(img)
        processed_img = img.copy()
        img_height, img_width, _ = img.shape

        for count in range(100):
            nois_size = random.randint(1, int(img_width/20))
            noise_x1 = random.randint(0, img_width-nois_size)
            noise_y1= random.randint(0, img_height-nois_size)
            noise_x2 = noise_x1 + random.randint(0, nois_size)
            noise_y2 = noise_y1 + random.randint(0, nois_size)
            color = (0,0,0)
            cv2.rectangle(processed_img, (noise_x1, noise_y1), (noise_x2, noise_y2), color, thickness=-1)

        return processed_img


    def horror_filter(self, img):
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)
        hsvf = hsv_img.astype(np.float32)
        hsvf[:,:,0] = np.clip(hsvf[:,:,0] - 30, 0, 180)  # 色相を赤方向にシフト
        hsvf[:,:,1] = np.clip(hsvf[:,:,1] * 0.5 - 30, 0, 255)
        hsv8 = hsvf.astype(np.uint8)
        processed_img = cv2.cvtColor(hsv8, cv2.COLOR_HSV2BGR_FULL)
        processed_img = self.create_horror_noise(processed_img)
        return processed_img


    def vivid_filter(self, img):
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)
        hsvf = hsv_img.astype(np.float32)
        hsvf[:,:,1] = np.clip(hsvf[:,:,1] * 2.0 - 20, 0, 255)
        hsv8 = hsvf.astype(np.uint8)
        processed_img = cv2.cvtColor(hsv8, cv2.COLOR_HSV2BGR_FULL)
        return processed_img



    def run_atmos_change(self):
        processed_img = self.img.copy()
        print(f"適用処理：{self.applied_filters}")
        # フィルター処理の要求を全て適用した画像を作成
        for applied_filters in self.applied_filters:
            if applied_filters == "目元にモザイク":
                processed_img = self.eye_mosaic(processed_img)

            elif applied_filters == "顔全体にモザイク":
                processed_img = self.face_mosaic(processed_img)

            elif applied_filters == "ちょっとホラー風":
                processed_img = self.horror_filter(processed_img)

            elif applied_filters == "画像を鮮やかに":
                processed_img = self.vivid_filter(processed_img)

        return processed_img

if __name__ == "__main__":
    img = cv2.imread(r"test_imgs\3.jpg")
    applied_filters = ["vivid_filter"]
    atmos_decorator = AtmosDecorator(img, applied_filters)

    processed_img = atmos_decorator.run_atmos_change()

    cv2.imshow('img', processed_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()