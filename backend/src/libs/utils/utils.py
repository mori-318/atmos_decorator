import numpy as np
import cv2
import base64

class Utils:
    async def file_to_img(self, img_file):
        # アップロードされた画像をnumpy配列に変換し、openCVで読み込む
        contents = await img_file.read()
        nparray = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparray, cv2.IMREAD_COLOR)
        return img

    def img_to_file(self, img):
        cv2.imshow('img', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        # 画像をBase64エンコード
        _, img_encoded = cv2.imencode('.jpg', img)
        img_file = base64.b64encode(img_encoded).decode('utf-8')
        return img_file