import cv2
from retinaface import RetinaFace

class AtmosChanger:
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


    def face_mosaic(self, img):
        faces = self.get_face_position()

        # 写真に写っている全顔に対してモザイク処理を行う
        for face in faces.values():
            x1, y1, x2, y2 = face["facial_area"]
            face_img = img[y1:y2, x1:x2]
            result_face_img = self.mosaic_filter(face_img, scale=0.05)
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


    def run_atmos_change(self):
        processed_img = self.img.copy()
        # フィルター処理の要求を全て適用した画像を作成
        for applied_filters in self.applied_filters:
            if applied_filters == "eye_mosaic":
                processed_img = self.eye_mosaic(processed_img)

            elif applied_filters == "face_mosaic":
                processed_img = self.face_mosaic(processed_img)

        return processed_img