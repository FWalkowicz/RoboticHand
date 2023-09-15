import os
import cv2
import time
import mediapipe as mp
import numpy as np

# Menu setting
header_folder = 'header'
header_folder_path = os.path.join(os.getcwd(), header_folder)
header_image = cv2.imread(os.path.join(header_folder_path, 'menu.png'))
header_image = cv2.resize(header_image, (1280, header_image.shape[0]))

# camera settings
camera = cv2.VideoCapture(0)
camera.set(3, 1280)
camera.set(4, 720)

# Hand detection module
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=2,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils


while True:
    # read frame from camera
    ret, frame = camera.read()

    # set menu into frame from camera
    frame[0:125] = cv2.addWeighted(frame[0:125], 0.5, header_image, 0.7, 0)

    # detect hand from frame
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    # draw hand landmarks
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate( handLms.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

            mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break
