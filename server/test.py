import cv2 as cv
import json
import base64

from deserialize.src.Python.ObjectDetection.SmartCamera import ObjectDetectionTop
from deserialize.src.Python.ObjectDetection.SmartCamera import BoundingBox
from deserialize.src.Python.ObjectDetection.SmartCamera import BoundingBox2d

with open("a.txt") as f:
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
with open("a.json", "w") as f:
    json.dump(buf, f)
print(buf)


# size = (92, 112)
# model = cv.CascadeClassifier("haarcascade_frontalface_default.xml")
# img = cv.imread("face.png", cv.IMREAD_GRAYSCALE)

# faces = model.detectMultiScale(img)
# print(len(faces))
# for x, y, w, h in faces:
#     img = cv.rectangle(img, (x, y), (x + w, y + h), 255, 4)
#     cv.imshow("image", img)
#     cv.waitKey(0)
