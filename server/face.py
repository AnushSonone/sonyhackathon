import cv2 as cv
import face_recognition

model = cv.CascadeClassifier("haarcascade_frontalface_default.xml")

img = cv.imread("a.jpg", cv.IMREAD_GRAYSCALE)
image = face_recognition.load_image_file("a.jpg")
face_locations = face_recognition.face_locations(image)
faces = model.detectMultiScale(img)
print(len(face_locations))
print(len(faces))
