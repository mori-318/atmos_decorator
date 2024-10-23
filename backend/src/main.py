from fastapi import FastAPI, File, UploadFile, Query
from pydantic import BaseModel
from typing import List

from libs.classify_img_atmos.classify_atmos import ClassifyAtmos
from libs.decorate_img.atmos_decorator import AtmosDecorator
from libs.utils.utils import Utils

app = FastAPI()
utils = Utils()


@app.post("/classify_atmos")
async def classify_atmos(img_file: UploadFile = File(...)):
    img = await utils.file_to_img(img_file)
    classify_atmos = ClassifyAtmos(
        r"assets\model_weight\normal_model_weight",
        r"assets\model_weight\smile_model_weight"
    )
    result, is_face = classify_atmos.run_classify(img)
    return {"atmos": result, "isFace": is_face}


@app.post("/apply_filters")
async def apply_filters(applied_filters: List[str] = Query(...), img_file: UploadFile = File(...)):
    img = await utils.file_to_img(img_file)
    atmos_changer = AtmosDecorator(img, applied_filters)
    processed_img = atmos_changer.run_atmos_change()
    processed_img_file = utils.img_to_file(processed_img)
    return {"status": "processed", "imgFile": processed_img_file}


@app.get("/")
def read_root():
    return {"Hello": "world"}