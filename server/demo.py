import requests
import shutil
import time
import cv2 as cv
import json

url = "http://192.168.8.140:8080"
url_meta = "http://192.168.8.140:8080/meta"
face_cascade = cv.CascadeClassifier("haarcascade_frontalface_default.xml")

size = (92, 112)
# model = cv.face.EigenFaceRecognizer.create()
# model.read("eigen_face_recognizer_model_0328.xml")


def detect_faces(img):
    faces = face_cascade.detectMultiScale(img)
    img_faces = []
    coords = []
    for x, y, w, h in faces:
        coords.append(((x, y), (x + w, y + h)))
        img_faces.append(img[y : y + h, x : x + w])
    return img_faces, coords


while True:
    res = requests.get(url, stream=True)
    with open("tmp.jpg", "wb") as w_fp:
        res.raw.decode_content = True
        shutil.copyfileobj(res.raw, w_fp)
    res = requests.get(url_meta)
    with open("tmp.json", "wb") as f:
        f.write(res.content)
    with open("tmp.json") as f:
        buf = json.load(f)
    img = cv.imread("tmp.jpg")
    for key, val in buf["Inferences"][0].items():
        if not key == "T" and val["class_id"] == 0 and val["score"] >= 0.7:
            cv.putText(
                img,
                "Local",
                (50, 50),
                cv.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
                cv.LINE_AA,
            )
            # print("Human detected!")
    # faces = model.detectMultiScale(img)
    # if len(faces) > 0:
    #     print("Face detected!")
    # for x, y, w, h in faces:
    #     img = cv.rectangle(img, (x, y), (x + w, y + h), 255, 4)
    cv.imshow("image", img)
    cv.waitKey(1)
    time.sleep(1)
