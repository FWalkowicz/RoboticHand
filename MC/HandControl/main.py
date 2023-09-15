import os
import cv2
import time
import mediapipe
import numpy as np

header_folder = 'header'
header_folder_path = os.path.join(os.getcwd(), header_folder)
header_image = cv2.imread(os.path.join(header_folder_path, 'menu.png'))
header_image = cv2.resize(header_image, (1280, header_image.shape[0]))

camera = cv2.VideoCapture(0)
camera.set(3, 1280)
camera.set(4, 720)

while True:
    ret, frame = camera.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break
