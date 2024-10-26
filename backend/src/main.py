from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Query, Form
from pydantic import BaseModel
from typing import List

from libs.classify_img_atmos.classify_atmos import ClassifyAtmos
from libs.decorate_img.atmos_decorator import AtmosDecorator
from libs.utils.utils import Utils

app = FastAPI()
utils = Utils()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/classify_atmos")
async def classify_atmos(img_file: UploadFile = File(...)):
    img = await utils.file_to_img(img_file)
    classify_atmos = ClassifyAtmos(
        r"assets\model_weight\normal_model_weight_ver2",
        r"assets\model_weight\smile_model_weight_ver2"
    )
    result, is_face = classify_atmos.run_classify(img)
    if is_face:
        if result == "positive": decorate_menu = ["目元にモザイク", "顔全体にモザイク", "ちょっとホラー風"]
        else: decorate_menu = ["目元にモザイク", "顔全体にモザイク", "画像を鮮やかに"]
    else:
        if result == "positive": decorate_menu = ["ちょっとホラー風"]
        else: decorate_menu = ["画像を鮮やかに"]

    return {"atmos": result, "decorateMenu": decorate_menu}


@app.post("/apply_filters")
async def apply_filters(
    img_file: UploadFile = File(...),
    applied_filters: str = Form(...)  # FormDataとして受け取る
):
    # 文字列をリストに変換
    filters_list = applied_filters.split(',') if applied_filters else []

    img = await utils.file_to_img(img_file)
    atmos_changer = AtmosDecorator(img, filters_list)
    processed_img = atmos_changer.run_atmos_change()
    processed_img_file = utils.img_to_file(processed_img)
    return {"status": "processed", "imgFile": processed_img_file}


@app.get("/")
def read_root():
    return {"Hello": "world"}