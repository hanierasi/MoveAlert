import cv2
import time
import glob
import threading
from email_sender import send_email
import os

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
count = 1
status_list = []

def clean_folder():
    images = glob.glob('./image/*.png')
    for image in images:
        os.remove(image)

while True:
    status = 0
    check, frame = video.read()

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    thresh_frame = cv2.threshold(delta_frame, 70, 255, cv2.THRESH_BINARY)[1]
    dilate_frame = cv2.dilate(thresh_frame, None, iterations=5)
    cv2.imshow("my video", dilate_frame)

    contours, check = cv2.findContours(dilate_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        if rectangle.any():
            status = 1
            cv2.imwrite(f"./image/{count}.png", frame)
            count += 1
            all_image = glob.glob(f"./image/*.png")
            index = int(len(all_image) / 2)
            image_with_object = all_image[index]

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0 :
        email_thread = threading.Thread(target=send_email, args=(image_with_object,))
        email_thread.daemon = True
        clean_thread = threading.Thread(target=clean_folder)
        email_thread.daemon = True

        email_thread.start()

    cv2.imshow('video', frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
video.release()
clean_thread.start()