from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import numpy as np
import cv2

from libs.classify_img_atmos.classify_atmos import ClassifyAtmos
from libs.utils.utils import *


app = FastAPI()


@app.post("/classify_atmos")
async def classify_atmos(img_file: UploadFile = File(...)):
    img = await file_to_img(img_file)

    classify_atmos = ClassifyAtmos(
        r"assets\model_weight\normal_model_weight",
        r"assets\model_weight\smile_model_weight"
    )

    result, is_face = classify_atmos.run_classify(img)

    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return {"atmos": result, "isFace": is_face}

@app.get("/")
def read_root():
    return {"Hello": "world"}