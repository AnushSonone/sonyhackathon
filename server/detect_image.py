# This file captures faces of user

import cv2 as cv


def detectAndDisplay(img):
    # img = cv.equalizeHist(img)
    faces = face_cascade.detectMultiScale(img)
    for x, y, w, h in faces:
        # center = (x + w // 2, y + h // 2)
        # img = cv.ellipse(img, center, (w // 2, h // 2), 0, 0, 360, (255, 0, 255), 4)
        img = cv.rectangle(img, (x, y), (x + w, y + h), 255, 4)
    cv.imshow("Face detection", img)
    return faces


def crop(img, p1, p2):
    return img[p1[1] : p2[1], p1[0] : p2[0]]


face_cascade = cv.CascadeClassifier("haarcascade_frontalface_default.xml")

if __name__ == "__main__":
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Unable to open camera.")
        exit()
    print("Successfully open camera!")

    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Cannot receive frame. Exiting...")

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        faces = detectAndDisplay(gray)

        key = cv.waitKey(1)
        if key == ord("q"):
            print("Quit")
            break
        if key == ord("s"):
            print("Save")
            x, y, w, h = faces[0]
            p1 = (x, y)
            p2 = (x + w, y + h)
            img = crop(gray, p1, p2)
            cv.imwrite("img%d.png" % count, img)
            count += 1
    cap.release()
    cv.destroyAllWindows()
