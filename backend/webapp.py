from fastapi import FastAPI, Request, status
import os.path
import traceback
import logging

import cv2 as cv

from fastapi.responses import FileResponse

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
    if len(filenames) > 0:
        return FileResponse(f"image/{max(filenames)}")
    else:
        return {"status": status.HTTP_200_OK}
