from fastapi import FastAPI, Request, status
import os.path
import traceback
import logging

import cv2 as cv

from fastapi.responses import FileResponse

import json
import base64

from deserialize.src.Python.ObjectDetection.SmartCamera import ObjectDetectionTop
from deserialize.src.Python.ObjectDetection.SmartCamera import BoundingBox
from deserialize.src.Python.ObjectDetection.SmartCamera import BoundingBox2d

SAVE_PATH_IMG = "./image"
SAVE_PATH_META = "./meta"

app_ins = FastAPI()
# Log format
log_format = "%(asctime)s - %(message)s"
# Set log level to INFO
logging.basicConfig(format=log_format, level=logging.INFO)


def save_file(file_type, content, filename):
    file_path = os.path.join(file_type, filename)
    with open(file_path, "wb") as w_fp:
        w_fp.write(content)


@app_ins.put("/meta/{filename}")
async def update_items(filename, request: Request):
    try:
        content = await request.body()
        os.makedirs(SAVE_PATH_META, exist_ok=True)
        save_file(SAVE_PATH_META, content, filename)
        logging.info("Meta File Saved: %s", filename)
        with open(f"{SAVE_PATH_META}/{filename}") as f:
            buf = json.load(f)
            buf_decode = base64.b64decode(buf["Inferences"][0]["O"])
            ppl_out = ObjectDetectionTop.ObjectDetectionTop.GetRootAsObjectDetectionTop(
                buf_decode, 0
            )
            obj_data = ppl_out.Perception()
            res_num = obj_data.ObjectDetectionListLength()
            print("NumOfDetections:" + str(res_num))
            buf["Inferences"][0].pop("O")
            for i in range(res_num):
                obj_list = obj_data.ObjectDetectionList(i)
                buf["Inferences"][0][str(i + 1)] = {}
                buf["Inferences"][0][str(i + 1)]["class_id"] = obj_list.ClassId()
                buf["Inferences"][0][str(i + 1)]["score"] = round(obj_list.Score(), 6)
                logging.info(
                    f"Class ID = {buf["Inferences"][0][str(i + 1)]["class_id"]}"
                )
        with open(f"json/{filename}", "w") as f:
            json.dump(buf, f, ensure_ascii=False, indent=4)
        return {"status": status.HTTP_200_OK}
    except Exception:
        traceback.print_exc()


@app_ins.put("/image/{filename}")
async def update_items(filename, request: Request):
    try:
        content = await request.body()
        os.makedirs(SAVE_PATH_IMG, exist_ok=True)
        save_file(SAVE_PATH_IMG, content, filename)
        logging.info("Image File Saved: %s", filename)
        return {"status": status.HTTP_200_OK}
    except Exception:
        traceback.print_exc()


@app_ins.get("/")
async def app():
    filenames = os.listdir("image")
    return FileResponse(f"image/{max(filenames)}")


@app_ins.get("/meta")
async def get_meta():
    filenames = os.listdir("json")
    return FileResponse(f"json/{max(filenames)}")
