import numpy as np
import cv2
import io
import base64

class Utils:
    async def file_to_img(self, img_file):
        """
        アップロードされたファイルをOpenCV画像形式に変換
        """
        contents = await img_file.read()
        nparray = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparray, cv2.IMREAD_COLOR)
        return img

    def img_to_file(self, img):
        """
        OpenCV画像をBase64エンコードされた文字列に変換
        """
        # 画像をJPEGフォーマットにエンコード
        _, img_encoded = cv2.imencode('.jpg', img)
        # バイト列をBase64エンコード
        img_base64 = base64.b64encode(img_encoded.tobytes())
        # Base64文字列をデータURLスキーム形式に変換
        img_data_url = f"data:image/jpeg;base64,{img_base64.decode('utf-8')}"
        return img_data_url

    def save_debug_image(self, img, filename="debug_output.jpg"):
        """
        デバッグ用：画像をファイルとして保存
        """
        cv2.imwrite(filename, img)