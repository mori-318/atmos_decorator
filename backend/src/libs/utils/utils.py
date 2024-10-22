import numpy as np
import cv2

async def file_to_img(img_file):
    # アップロードされた画像をnumpy配列に変換し、openCVで読み込む
    contents = await img_file.read()
    nparray = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparray, cv2.IMREAD_COLOR)

    return img