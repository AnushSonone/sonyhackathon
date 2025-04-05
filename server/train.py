# This file trains the face recognition model

import cv2 as cv
import numpy as np


def read_csv(filename, separator=";"):
    f = open(filename, "r")
    arr_images = []
    arr_labels = []
    lines = f.readlines()
    for line in lines:
        image_path, label = line.strip().split(separator)
        arr_images.append(cv.imread(image_path, cv.IMREAD_GRAYSCALE))
        arr_labels.append(int(label))
    return arr_images, arr_labels


if __name__ == "__main__":
    filename_csv = "archive.txt"
    images, labels = read_csv(filename_csv)

    # Separate training data and testing data
    # test_sample1 = images.pop(0)
    # test_label1 = labels.pop(0)
    # test_sample2 = images.pop(-1)
    # test_label2 = labels.pop(-1)

    # Create an Eigenfaces model
    model = cv.face.EigenFaceRecognizer.create()
    model.setLabelInfo(0, "Bugart Lan")
    model.setLabelInfo(32, "John Doe")
    # model = cv.face.FisherFaceRecognizer.create()
    # model = cv.face.LBPHFaceRecognizer.create()
    print("Model training ...")
    model.train(np.array(images), np.array(labels))
    model.write("eigen_face_recognizer_model_0328.xml")
    print("Model trained successfully.")

    # Predict label of a test image
    # predicted_label, confidence = model.predict(test_sample1)
    # print("Test 1")
    # print("Confidence =", confidence)
    # print("Predicted class = %d; Actual class = %d" % (predicted_label, test_label1))
    #
    # predicted_label, confidence = model.predict(test_sample2)
    # print("Test 2")
    # print("Confidence =", confidence)
    # print("Predicted class = %d; Actual class = %d" % (predicted_label, test_label2))
