# This file resizes the downloaded or captured images and save them to the
# archive folder for model training

import cv2 as cv
import os


def detectAndCrop(img):
    (x, y, w, h) = face_cascade.detectMultiScale(img)[0]
    return img[y : y + h, x : x + w]


face_cascade = cv.CascadeClassifier("haarcascade_frontalface_default.xml")
size = (92, 112)

if __name__ == "__main__":
    path = "man"
    dst_path = "archive/john"
    dirname, dirnames, filenames = list(os.walk(path))[0]
    for filename in filenames:
        image_path = os.path.join(path, filename)
        img = cv.imread(image_path, 0)
        img = detectAndCrop(img)
        img = cv.resize(img, size)
        cv.imwrite(os.path.join(dst_path, filename), img)
        print(os.path.join(dst_path, filename))
