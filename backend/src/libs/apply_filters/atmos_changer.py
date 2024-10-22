import cv2
from retinaface import RetinaFace

class AtmosChanger:
    def __init__(self, img, applied_filters):
        self.img = img
        self.applied_filters = applied_filters

    def get_face_position(self):
        faces = RetinaFace.detect_faces(self.img, threshold=0.7)
        return faces

    def mosaic_filter(self, img, scale=0.05): # scal : 画像をscale倍に縮小する
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

    def run_atmos_change(self):
        processed_img = self.img.copy()

        # フィルター処理の要求を全て適用した画像を作成
        for applied_filters in self.applied_filters:
            if applied_filters == "face_mosaic":
                processed_img = self.face_mosaic(processed_img)

        return processed_img

if __name__ == "__main__":
    img = cv2.imread("3.jpg")
    applied_filters = ["face_mosaic"]
    atmos_changer = AtmosChanger(img, applied_filters)
    processed_img = atmos_changer.run_atmos_change()

    cv2.imshow("img", processed_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()